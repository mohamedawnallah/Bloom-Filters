import math
import mmh3

class BloomFilter:
    def __init__(self, capacity, error_rate=0.001):
        """
        Initialize a Bloom filter.
        
        Args:
            capacity: Expected number of elements to be added
            error_rate: Desired false positive probability
        """
        self.capacity = capacity
        self.error_rate = error_rate
        
        # Calculate optimal filter size and number of hash functions.
        self.size = self._calculate_size(capacity, error_rate)
        self.hash_count = self._calculate_hash_count(self.size, capacity)
        
        # Initialize bit array.
        self.bit_array = [0] * self.size
    
    def _calculate_size(self, capacity, error_rate):
        """Calculate optimal bit array size."""
        # The natural logarithm gives more weightss to smaller false positives rate.
        # The inverse relationship the higher the false positives rate
        # the lesser the bit array size and vice versa.
	# It is originally derived from this formula to minimize the bit array size:
	# error_rate = (1 - e^(-k * n / m))^k
	# (k: number of hash functions, n: number of elements expected to be stored in the bloom filter,
	# m: size of the bit array).
        size = -capacity * math.log(error_rate) / (math.log(2) ** 2)
        return int(size)
    
    def _calculate_hash_count(self, size, capacity):
        """Calculate optimal number of hash functions."""
	# Taking the derivative of f(k) with respect to k, setting it to zero, and solving for k
        # in the original bloomfilter error rate formula. This gives us the smallest number of hash
        # functions to do.
        hash_count = (size / capacity) * math.log(2)
        return int(hash_count)
    
    def add(self, item):
        """Add an item to the Bloom filter."""
        # The same initialization vectors range need to be same when querying
        # to avoid cases where false negatives arise and that would defeat the
        # specification of bloom filter algorithm.
        for i in range(self.hash_count):
            # Use initialization vectors (i) to get different hash values.
            index = mmh3.hash(str(item), i) % self.size
            self.bit_array[index] = 1
    
    def might_contain(self, item):
        """
        Check if an item might be in the set.
        
        Returns:
            True: Item might be in the set
            False: Item is definitely not in the set
        """
	# The number of hash computations is constant no matter the size of data to lookup.
        # The ideal time complexity for it is O(1).
        for i in range(self.hash_count):
            index = mmh3.hash(str(item), i) % self.size
            if self.bit_array[index] == 0:
                return False
        return True
    
    def __contains__(self, item):
        """Support for 'in' operator."""
        return self.might_contain(item)


if __name__ == "__main__":
    # Create a Bloom filter expecting 1000 items with 0.1% false positive rate.
    bloom = BloomFilter(capacity=1000, error_rate=0.001)
    
    # Add some items.
    words = ["apple", "banana", "cherry", "date", "elderberry"]
    for word in words:
        bloom.add(word)
    
    # Test membership.
    print("Test contains:")
    for word in ["apple", "blueberry", "cherry", "dragonfruit"]:
        result = word in bloom
        actually_in = word in words
        print(f"'{word}' in filter: {result} (Actually in set: {actually_in})")
