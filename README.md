# Python Implementation of Merkel Hash Tree

A Merkel Hash Tree is a data structure with built-in verifiability. The data is stored in blocks which form the leaves of the tree. Each data block is hashed, and the level in the tree above it is formed by nodes which store the hash of the sum of the two nodes below it. Read request responses are accompanied by a list of hashes, and a client only needs to know the root hash in order to be able to verify the authenticity of data returned from the server maintaining the tree. Hash trees are used extensively in distributed systems such as P2P file sharing applications.

![Architecture](https://upload.wikimedia.org/wikipedia/commons/thumb/9/95/Hash_Tree.svg/1200px-Hash_Tree.svg.png)

Usage:
```bash
python merkelTree.py <number_of_data_blocks> && cat output.log
```

tested with python2.7 and python3.4
