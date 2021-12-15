import argparse
import sys
import os
import subprocess
from pathlib import Path

def main():
    # Initialize parser
    parser = argparse.ArgumentParser()
    
    # Adding optional arguments
    parser.add_argument("-c", "--create-chain", help = "Create chained patches", action="store_true")
    parser.add_argument("-v", "--verify-chain", help = "Verify the chained patches", action="store_true")
    
    # Read arguments from command line
    args = parser.parse_args()
    
    # Argument selection
    if args.create_chain:
        # Get this git output
        output = subprocess.getoutput('git log -p')

        # Split the output between 'commit' (including)
        result = []
        one_commit = []
        for line in output.splitlines():
            if line.startswith('commit'):
                if not result and not one_commit:
                    one_commit.append(line)
                elif one_commit:
                    result.append(one_commit)
                    one_commit.clear()
                    one_commit.append(line)
            else:
                one_commit.append(line)
        result.append(one_commit)

        print(result)

        # Create the json to store the results with the prev_hash and save thes json's

    elif args.verify_chain:
        print("test")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)