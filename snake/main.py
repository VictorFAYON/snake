def ouf():
    print("ouf !")
import argparse

def h():
    parser = argparse.ArgumentParser(description='Some description.')
    parser.add_argument('-a', help="A text explaining what is the use of the -a option and what type of value it takes.")
    args = parser.parse_args()
    print(args)