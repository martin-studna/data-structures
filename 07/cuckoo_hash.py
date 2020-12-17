import random
import math

class TabulationHash:
    """Hash function for hashing by tabulation.

    The 32-bit key is split to four 8-bit parts. Each part indexes
    a separate table of 256 randomly generated values. Obtained values
    are XORed together.
    """

    def __init__(self, num_buckets):
        self.tables = [None] * 4
        for i in range(4):
            self.tables[i] = [random.randint(0, 0xffffffff) for _ in range(256)]
        self.num_buckets = num_buckets

    def hash(self, key):
        h0 = key & 0xff
        h1 = (key >> 8) & 0xff
        h2 = (key >> 16) & 0xff
        h3 = (key >> 24) & 0xff
        t = self.tables
        return (t[0][h0] ^ t[1][h1] ^ t[2][h2] ^ t[3][h3]) % self.num_buckets

class CuckooTable:
    """Hash table with Cuckoo hashing.

    We have two hash functions, which map 32-bit keys to buckets of a common
    hash table. Unused buckets contain None.
    """

    def __init__(self, num_buckets):
        """Initialize the table with the given number of buckets.
        The number of buckets is expected to stay constant."""

        self.n = 0

        # The array of buckets
        self.num_buckets = num_buckets
        self.table = [None] * num_buckets

        # Create two fresh hash functions
        self.hashes = [TabulationHash(num_buckets), TabulationHash(num_buckets)]

    def lookup(self, key):
        """Check if the table contains the given key. Returns True or False."""

        b0 = self.hashes[0].hash(key)
        b1 = self.hashes[1].hash(key)
        # print("## Lookup key={} b0={} b1={}".format(key, b0, b1))
        return self.table[b0] == key or self.table[b1] == key

    def insert(self, key):
        """Insert a new key to the table. Assumes that the key is not present yet."""
        # If the key is already present in the hashtable, stop insertion method.
        if self.lookup(key):
          return

        # Increment count of current elements present in the table.
        self.n += 1

        # Timeout variable represents limit for maximum number of insertions and swaps between two tables.  
        timeout = 5 * int(math.log(self.n) + 1)
        b0, b1 = 0, 0
        for _ in range(timeout):
          # Calculate hash index with first hash function.
          b0 = self.hashes[0].hash(key)

          # If the hash index is the same as the previously calculated hash index of the second hash function,
          # calculate again the hash index with the second function.
          if b0 == b1:
            b0 = self.hashes[1].hash(key)

          # If the slot is empty, insert the element and stop insertion method.  
          if self.table[b0] is None:
            self.table[b0] = key
            return
          
          # Swap elements
          temp = self.table[b0]
          self.table[b0] = key
          key = temp

          b1 = b0
          
        # If the insertion of the element has failed, rehash the table and try insert it again.
        self.rehash_table()
        self.insert(key)

    def rehash_table(self):
        # Reset counter.
        self.n = 0
        # Create new hash functions.
        self.hashes = [TabulationHash(self.num_buckets), TabulationHash(self.num_buckets)]
        # Store old table.
        temp_table = self.table

        # Init new table.
        self.table = [None] * self.num_buckets
        for x in temp_table:
          if x is not None:
            self.insert(x)