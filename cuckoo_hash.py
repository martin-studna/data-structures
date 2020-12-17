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

        self.n += 1
        self.insert_with_timeout(key, math.ceil(math.log(self.n) + 1))


    def insert_with_timeout(self, key, timeout):

        if timeout == 0:
            self.rehash_and_insert(key)
            return

        b0 = self.hashes[0].hash(key)
        b1 = self.hashes[1].hash(key)

        if self.table[b0] is None:
            self.table[b0] = key
            return
        if self.table[b1] is None:
            self.table[b1] = key
            return

        new_key = self.table[b0]
        self.table[b0] = key
        self.insert_with_timeout(new_key, timeout - 1)

    def rehash_and_insert(self, key):

        old_table = self.table
        self.table = self.table = [None] * self.num_buckets
        self.n = 0
        self.hashes = [TabulationHash(self.num_buckets), TabulationHash(self.num_buckets)]

        self.insert(key)
        for value in old_table:
            if value is not None:
                self.insert(value)
