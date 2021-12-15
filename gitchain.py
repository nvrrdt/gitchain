import argparse
import sys
import os
import glob
import subprocess
from pathlib import Path
import json
from hashlib import sha256

def main():
    # Initialize parser
    parser = argparse.ArgumentParser()
    
    # Adding optional arguments
    parser.add_argument("-c", "--create-chain", help = "Create chained patches", action="store_true")
    parser.add_argument("-v", "--verify-chain", help = "Verify the chained patches", action="store_true")
    parser.add_argument("-o", "--compare-chains", help = "Compare two chains", action="store_true")
    
    # Read arguments from command line
    args = parser.parse_args()
    
    # Argument selection
    if args.create_chain:
        # Get this git output
        output = subprocess.getoutput('git log -p')

        #print(output)

        # Split the output between 'commit' (including)
        result = []
        for line in output.splitlines():
            if line.startswith('commit'):
                l = []
                l.append(line)  
                if l:
                    result.append(l)
            else:
                l.append(line)

        # Reverse the array
        result.reverse()

        # Create chain folder
        if not os.path.exists('./chain'):
            os.makedirs('./chain')
        
        count = 0
        for i, filepath in enumerate(sorted(glob.glob(os.path.join('./chain', '*'))), start=1):
            count = i+1

        # Create chain subfolders
        if not os.path.exists('./chain/' + str(count+1)):
            os.makedirs('./chain/' + str(count))
        

        # Create the json to store the results with the prev_hash and save thes json's
        ph = "g"
        for i, p in enumerate(result, start=1):
            j = {"patch": p, "prev_hash": ph}
    
            file_name = '{0:08d}'.format(i)
            f = open('./chain/' + str(count) + '/' + file_name, 'w+')
            f.write(json.dumps(j))
            f.close()

            ph = sha256((json.dumps(j)).encode('utf-8')).hexdigest()

    elif args.verify_chain:
        for i, filepath1 in enumerate(sorted(glob.glob(os.path.join('./chain', '*'))), start=1):
            error = False

            for j, filepath2 in enumerate(sorted(glob.glob(os.path.join('./chain/' + str(i), '*'))), start=1):
                with open(filepath2) as f:
                    j_json = json.load(f)

                if j == 1 and j_json['prev_hash'] == 'g':
                    ph = sha256((json.dumps(j_json)).encode('utf-8')).hexdigest()
                elif j_json['prev_hash'] == ph:
                    ph = sha256((json.dumps(j_json)).encode('utf-8')).hexdigest()
                else:
                    error = True
                    break

            if (error):
                print("Chain", i,"is broken in", j-1)
            else:
                print("Chain is correct")

    elif args.compare_chains:
        for i, filepath1 in enumerate(sorted(glob.glob(os.path.join('./chain', '*'))), start=1):
            error = False
            is_ended = False

            prev_hash1 = []
            prev_hash2 = []

            for j, filepath2 in enumerate(sorted(glob.glob(os.path.join('./chain/' + str(i), '*'))), start=1):
                with open(filepath2) as f:
                    j_json = json.load(f)

                prev_hash1.append(sha256((json.dumps(j_json)).encode('utf-8')).hexdigest())
            
            for k, filepath3 in enumerate(sorted(glob.glob(os.path.join('./chain/' + str(i+1), '*'))), start=1):
                with open(filepath3) as f:
                    j_json = json.load(f)

                prev_hash2.append(sha256((json.dumps(j_json)).encode('utf-8')).hexdigest())

            patch_nr = 0
            for p, ph1 in enumerate(prev_hash1):
                if prev_hash2:
                    for h, ph2 in enumerate(prev_hash2):
                        if p == h:
                            if ph1 != ph2:
                                patch_nr = p+1
                                error = True
                else:
                    is_ended = True

            if (error):
                print("Chain", i,"and chain", i+1, "are broken in patch", patch_nr)
            elif (is_ended):
                break
            else:
                print("Chain", i,"and chain", i+1, "are correct")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)