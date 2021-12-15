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
        output = subprocess.getoutput('git log -p')
        print(output)
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