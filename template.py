#!/usr/bin/env python3

import os, sys
from pathlib import Path

# Script to generate the default python file for these problems

def main(problemNumber):
    """
    Takes in the problem number and generates a python file with the following structure

    Imports

    def main():
        pass

    if __name__ == "__main__":
        main()
    
    File is named prob_problemNumber.py
    """
    fileName = f"prob_{problemNumber:04d}.py"
    
    path = Path('.')
    dirs = [d for d in path.iterdir() if d.is_dir() and len(list(d.glob('*.py'))) > 0]

    imports = '\n'.join([f"import {d}.{d} as {d}" for d in dirs])

    template = '\n'.join([imports, 
                '\n',
                '@wrappers.printTimeTaken',
                'def main():',
                '    pass',
                '\n',
                'if __name__ == "__main__":',
                '    main()'
                ])

    with open(fileName, "w") as file:
        print(template)
        file.write(template)

if __name__ == "__main__":
    args = sys.argv
    
    if len(args) == 1:
        raise Exception("Need a problem number")
    else:
        main(int(args[1]))

