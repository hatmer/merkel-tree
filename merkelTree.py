from random import randint
import math
import sys
import logging
logging.basicConfig(filename='output.log', level=logging.DEBUG, format='%(asctime)s %(message)s')

class Node:
    """
    Inner nodes that form merkel tree
    """
    def __init__(self, left_child, right_child):
        self.hash = None
        self.left = left_child
        self.right = right_child

    def recompute(self):
        """
        recursively recompute tree hash values
        """
        l = self.left.recompute()
        r = self.right.recompute()
        self.hash = str(abs(hash(l + r)))
        #self.hash = str(abs(hash(self.left.recompute() + self.right.recompute())))
        return self.hash

class Leaf():
    """
    Leaf Nodes on merkel Tree that contain data
    """
    def __init__(self, x):
        self.data = x
        self.recompute()

    def write(self, new_data):
        self.data = new_data

    def recompute(self):
        self.hash = str(abs(hash(self.data)))
        return self.hash

class Tree:
    def __init__(self, num_leaves):
        self.tree = []
        self.total_nodes = 0 # total number of nodes in tree (including leaves since leaves contain both data and hash)

        # add leaves
        self.actual_num_leaves = int(math.pow(2, math.ceil(math.log(num_leaves,2)))) # round up to the nearest power of 2
        logging.info("creating tree with {} data blocks".format(self.actual_num_leaves))
        for x in range(0, self.actual_num_leaves):
            self.tree.append(Leaf(None))
            self.total_nodes += 1
        
        # add inner Nodes
        total_nodes = self.actual_num_leaves
        start = 0
        nodes_this_level = self.actual_num_leaves
        while nodes_this_level > 1:
            for i in range(start, start + nodes_this_level, 2):
                self.tree = [Node(self.tree[-1 * (i + 2)], self.tree[-1 * (i + 1)])] + self.tree
                self.total_nodes += 1
            start = start + nodes_this_level
            nodes_this_level = int(nodes_this_level / 2)

        # compute nodes
        self.levels = int(math.log(self.actual_num_leaves, 2)) # number of levels of the tree
        self.root = self.tree[0]
        self.root.recompute()
        logging.info("tree initialization complete")


    def traversal(self, n):
        """
        traverse up through the tree from data block, return all nodes and siblings on path to root
        """
        nodes = []
        level = self.levels
        while True:
            # n is root node
            if n == 0:
                nodes.append((level, self.tree[n].hash, ""))
                return nodes
            # calculate parent node number
            if n % 2 == 1: # odd(left) case
                parent = int((n - 1) / 2)
                nodes.append((level, self.tree[n].hash, self.tree[parent].right.hash))
            else: # even(right) case
                parent = int((n - 2) / 2)
                nodes.append((level, self.tree[parent].left.hash, self.tree[n].hash))
            # move up one level
            n = parent
            level -= 1

    def read(self, block_id):
        """
        read block from Tree, return block data and all required nodes
        """
        nodes = []  # block's hash and sibling, parent, parent's sibling, ... root Node and its other child
        n = -1 * (block_id + 1)
    
        block = len(self.tree) + n # actual node number
        level_hashes = self.traversal(block) # hashes for each level of the tree
        #hashes = list(map(lambda node : node.hash, nodes))
        return (self.tree[block].data, level_hashes)
        
    def write(self, block_id, new_data):
        """
        write a block to Tree
        """
        self.tree[-1 * (block_id + 1)].write(new_data)
        self.root.recompute() # can optimize by calling once after multiple writes
        logging.info("data block {} <- value {}".format(block_id, new_data))
        return 0

class Client:
    def __init__(self, tree):
        self.t = tree
        logging.info("client initialization complete")

    def read(self, block_id):
        logging.info("reading block #{}".format(block_id))
        (data, hashes) = self.t.read(block_id) # hashes are in [(level, left_hash, right_hash),...] format
        logging.info("read {} <- block #{}".format(data, block_id))
        
        # verify hashes and output verification msg
        hash_below = ""
        invalid = False
        for (level, left, right) in hashes:
            if level < self.t.levels: # not the bottom(data) level
                if ((hash_below != left) and (hash_below != right)):
                    invalid = True

            hash_below = str(abs(hash(left + right)))

        if invalid:
            logging.info("invalid!")
        else:
            logging.info("valid!")
            

    def write(self, block_id, new_data):
        logging.info("writing {} -> block #{}".format(new_data, block_id))
        self.t.write(block_id, new_data)

def demo(leaves):

    logging.info("Welcome to the Merkel Tree demo!")

    # create Tree
    logging.info("Initializing tree...")

    t = Tree(float(leaves))
    
    # create client
    c = Client(t)

    # read/write demo
    for i in range(0, 3):
        b = randint(0, t.actual_num_leaves)
        new_data = randint(0, 99999999)
        c.read(b)
        c.write(b, new_data)
        c.read(b)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: python3 merkelTree.py <number_of_data_blocks>")
        
    else:
        logging.info('Initializing...')
        demo(sys.argv[1])
