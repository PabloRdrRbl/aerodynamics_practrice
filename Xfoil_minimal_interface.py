import subprocess
import sys, os

commands = ['naca 0018',
            'oper',
            'iter 300',
            're 3e7']

for aoa in [0, 7, 14, 21]:
    path = os.path.join(os.path.dirname(__file__),
                        'data/naca0018-cpx-aoa{0}.txt'.format(aoa))
    commands.extend(['pcwr',
                     'path',
                     'alfa {0}'.format(aoa),
                     'aseq -10 25 0.5'])

p = subprocess.Popen(["/Applications/Xfoil.app/Contents/MacOS/Xfoil",],
                     stdin=subprocess.PIPE,
                     stdout=subprocess.PIPE)

for command in commands:
     p.stdin.write((command + '\n').encode())

p.stdin.write("\nquit\n".encode())
p.stdin.close()
for line in p.stdout.readlines():
    print(line.decode(), end='')
