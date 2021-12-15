## Gitchain - an example of chained git log patches

The chaining happens as follows: sorted json files consisting of one patch and a prev_hash are saved. The prev_hash is the hash of the json from the previous json file.  
It is not a blockchain because there is no p2p component, but gitchain is the execution of the chain in the name blockchain.  
Effectively if you create the json files and afterwards change something in the patch or the prev_hash of one of those created files, the following hash will then not be the same as previously anymore.  

As git probably clones a codebase based on these patches, there is no way of verifying the correctness of these patches between users of this codebase. I think gitchain enables this.

The goal was to be able to see at a glance if a committed git codebase changed sometime, whether or not maliciously.  

I don't know if this is useful or that it even exists, but I liked coding it.  

### How to use?

- ```'python3 gitchain.py -c' or 'python3 gitchain.py --create-chain'```  
Creation of the json's in the chain directory and each json comprises of a git patch and the prev_hash.
- ```'python3 gitchain.py -v' or 'python3 gitchain.py --verify-chain'```  
Each prev_hash links to the hash of the previous json and this chain is being verified for correctness.
- ```'python3 gitchain.py -o' or 'python3 gitchain.py --compare-chains'```  
Comparison of the prev_hash'es of two gitchain's.  