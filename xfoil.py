'''
Xfoil interface. Calculating data at different Reynolds numbers

Thanks to the Aeropython team for helping me with the Xfoil interface!

References
----------
1. [https://github.com/AeroPython/aeropy/tree/Xfoil_interaction/
   aeropy/Xfoil_Interaction]
2. [http://stackoverflow.com/questions/15010650/how-can-i-interact-
   with-an-application-on-mac-through-python-subprocess]
3. [https://hakantiftikci.wordpress.com/2010/12/21/using-xfoil-and-
   automating-via-python-subprocess-module/]

'''


# import libraries and modules needed
import subprocess
import sys, os
import time
import argparse

# idea taken from
# [http://stackoverflow.com/questions/28479543/run-python-script-with-some-of
# -the-argument-that-are-optional]
#
def parseArguments():
    # create argument parser
    parser = argparse.ArgumentParser()

    # optional arguments
    parser.add_argument("-re", help="Reynolds number used",
                        type=str, default='3e+5')

    # parse arguments
    args = parser.parse_args()

    return args

def add_header(file_path, re):
    # "you generally can't prepend data to an existing flat structure without
    # rewriting the entire structure"
    # [http://stackoverflow.com/questions/4454298/prepend-a-
    # line-to-an-existing-file-in-python]
    #
    with open(file_path, 'r+') as f:
        lines = f.readlines()
        f.seek(0)
        f.write('#\n')
        f.write('# Data generated using Xfoil and the scrip xfoil.py\n')
        f.write('# Re = ' + re + '\n')
        f.write('#\n')
        f.writelines(lines)

def comment_firts_lines(file_path, n_lines=12):
    with open(file_path, 'r+') as f:
        lines = f.readlines()
        f.seek(0)
        for line in lines[0:n_lines:]:
            f.write('#' + line)
        f.writelines(lines[n_lines::])

def get_airfoil_data(re='6e+5'):
    xfoil_path = '/Applications/Xfoil.app/Contents/Resources/xfoil'


    aoa = [0, 7, 14, 21]
    file_paths = []
    commands = ['naca 0018',
                'plop',
                'g',
                '',
                'oper',
                'iter 500',
                're ' + re,
                'visc']

    for i in aoa:
        path = 'data/naca0018-cpx-aoa{0}.txt'.format(i)
        file_paths.append(path)
        commands.extend(['alfa ' + str(i),
                         'cpwr ' + path])

    cla_path = 'data/cla-data/naca0018-cla-re{0}.txt'.format(re)
    if os.path.isfile(cla_path): # check if the file already exist
        os.remove(cla_path)      # when it does we remove to avoid problems
    file_paths.append(cla_path)

    commands.extend(['pacc',
                     cla_path,
                     '',
                     'aseq -5 25 1',
                     'pacc'])


    p = subprocess.Popen(xfoil_path,
                         stdin=subprocess.PIPE,
                         # we don't need to get response
                         # but otherwise Xfoil keeps opened!
                         stdout=subprocess.PIPE,
                         stderr=None)

    for command in commands:
         p.stdin.write((command + '\n').encode())

    p.stdin.write("\nquit\n".encode())
    p.communicate() # otherwise data has not been written
                    # by Xfoil when we add the header

    for file_path in file_paths[:-1]:
        add_header(file_path, re)

    comment_firts_lines(file_paths[-1])

if __name__ == "__main__":
    args = parseArguments()
    get_airfoil_data(args.re)
