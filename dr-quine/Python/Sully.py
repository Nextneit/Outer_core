import subprocess
s = 'import subprocess\ns = %r\ni = %d\nif i > 0:\n    fname = "Sully_" + str(i) + ".py"\n    with open(fname, "w") as f:\n        f.write(s %% (s, i - 1))\n    subprocess.run(["python3", fname])\n'
i = 5
if i > 0:
    fname = "Sully_" + str(i) + ".py"
    with open(fname, "w") as f:
        f.write(s % (s, i - 1))
    subprocess.run(["python3", fname])
