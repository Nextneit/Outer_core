[BITS 64]

global stub_start
global stub_end

stub_start:

; ============================================================
; 1. PRINT "....WOODY...."
; ============================================================
    mov     rax, 1                      ; sys_write
    mov     rdi, 1                      ; stdout
    lea     rsi, [rel woody_msg]        ; puntero al mensaje (RIP-relativo)
    mov     rdx, 14                     ; longitud "....WOODY....\n"
    syscall

; ============================================================
; 2. mprotect(seg_addr, seg_size, PROT_READ|PROT_WRITE|PROT_EXEC)
;    Necesario para poder escribir en el segmento .text
;    syscall 10 = mprotect
;    rdi = addr (page-aligned), rsi = len, rdx = prot
; ============================================================
    mov     rdi, [rel seg_addr]
    and     rdi, -4096                  ; alinear a página (addr & ~0xFFF)
    mov     rsi, [rel seg_size]
    add     rsi, 4095                   ; redondear tamaño al alza
    and     rsi, -4096
    mov     rdx, 7                      ; PROT_READ|PROT_WRITE|PROT_EXEC
    mov     rax, 10                     ; sys_mprotect
    syscall

; ============================================================
; 3. DESENCRIPTAR SEGMENTO (XOR con clave de KEY_SIZE bytes)
; ============================================================
    mov     rdi, [rel seg_addr]         ; dirección virtual del segmento cifrado
    mov     rcx, [rel seg_size]         ; tamaño en bytes del segmento
    lea     rbx, [rel key]              ; puntero a los 16 bytes de clave
    xor     r9, r9                      ; índice de clave = 0

.xor_loop:
    test    rcx, rcx
    jz      .done_xor
    movzx   r10d, byte [rdi]            ; leer byte del segmento
    movzx   r11d, byte [rbx + r9]       ; leer byte de la clave
    xor     r10b, r11b                  ; XOR
    mov     byte [rdi], r10b            ; escribir byte desencriptado
    inc     rdi
    inc     r9
    and     r9, 15                      ; r9 = r9 % 16
    dec     rcx
    jmp     .xor_loop

.done_xor:

; ============================================================
; 4. mprotect(seg_addr, seg_size, PROT_READ|PROT_EXEC)
;    Restaurar permisos originales del segmento
; ============================================================
    mov     rdi, [rel seg_addr]
    and     rdi, -4096
    mov     rsi, [rel seg_size]
    add     rsi, 4095
    and     rsi, -4096
    mov     rdx, 5                      ; PROT_READ|PROT_EXEC
    mov     rax, 10                     ; sys_mprotect
    syscall

; ============================================================
; 5. SALTAR AL ENTRY POINT ORIGINAL
; ============================================================
    mov     rax, [rel orig_entry]
    jmp     rax

; ============================================================
; DATOS — placeholders rellenados por inject_stub() en C
; ============================================================
woody_msg:  db  "....WOODY....", 0x0A   ; 14 bytes

key:        times 16 db 0               ; 16 bytes clave XOR
seg_addr:   dq  0                       ; uint64_t dirección segmento cifrado
seg_size:   dq  0                       ; uint64_t tamaño segmento cifrado
orig_entry: dq  0                       ; uint64_t entry point original

stub_end:
