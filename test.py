import argparse

MIN_SIZE = 200

parser = argparse.ArgumentParser(description='Some description.')
parser.add_argument('-s', type=int, help="The size.")
args = parser.parse_args()
print(args)

# Check argument
if args.s < MIN_SIZE:
    raise ValueError("The size (-s argument) must be greater or equal to %d." % MIN_SIZE)