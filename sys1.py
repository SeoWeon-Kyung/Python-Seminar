import os
import sys

def li(dire):
    filenames = os.listdir(dire)
    for filename in filenames:
        path = os.path.join(dire, filename)
        print(path)
        print(os.path.abspath(path))

def main():
    li(sys.argv[1])

if __name__=='__main__':
    main()
