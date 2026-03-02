s = 's = %r\nwith open("Grace_kid.py", "w") as f:\n    f.write(s %% s)\n'
with open("Grace_kid.py", "w") as f:
    f.write(s % s)
