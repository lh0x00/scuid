import pytest
from scuid import Scuid, pad, base36_encode, scuid, slug, fingerprint, create_fingerprint

# Test Suite 1: Utility functions
class TestUtilities:
    def test_pad(self):
        # Test Case 1: Padding shorter strings
        assert pad("123", "0", 5) == "00123"
        # Test Case 2: Padding with different character
        assert pad("hello", "*", 8) == "***hello"
        # Test Case 3: Truncating longer strings
        assert pad("world", "-", 3) == "rld"

    def test_base36_encode(self):
        # Test Case 1: Encoding 0
        assert base36_encode(0) == "0"
        # Test Case 2: Encoding a small number
        assert base36_encode(35) == "z"
        # Test Case 3: Encoding a number requiring multiple digits
        assert base36_encode(36) == "10"
        # Test Case 4: Encoding a larger number
        assert base36_encode(123456) == "2n9c"


# Test Suite 2: Static methods in Scuid class
class TestScuidStaticMethods:
    def test_host_id(self):
        hostname = "test-host"
        result = Scuid.host_id(hostname)
        # Test Case 1: Host ID length
        assert len(result) == 2
        # Test Case 2: Host ID format
        assert result.isalnum()

    def test_fingerprint(self):
        pid = 12345
        hostname = "test-host"
        result = Scuid.fingerprint(pid=pid, hostname=hostname)
        # Test Case 1: Fingerprint length
        assert len(result) == 4
        # Test Case 2: Fingerprint format
        assert result.isalnum()


# Test Suite 3: Instance methods in Scuid class
class TestScuidInstanceMethods:
    @pytest.fixture
    def scuid_instance(self):
        return Scuid()

    def test_count(self, scuid_instance):
        # Test Case 1: Initial count
        initial_count = scuid_instance.count()
        assert initial_count == 0
        # Test Case 2: Increment count
        next_count = scuid_instance.count()
        assert next_count == 1

    def test_counter_block(self, scuid_instance):
        result = scuid_instance.counter_block()
        # Test Case 1: Counter block length
        assert len(result) == scuid_instance.blockSize
        # Test Case 2: Counter block format
        assert result.isalnum()

    def test_random_block(self, scuid_instance):
        result = scuid_instance.random_block()
        # Test Case 1: Random block length
        assert len(result) == scuid_instance.blockSize
        # Test Case 2: Random block format
        assert result.isalnum()

    def test_timestamp(self, scuid_instance):
        result = scuid_instance.timestamp()
        # Test Case 1: Timestamp length
        assert len(result) == 8
        # Test Case 2: Timestamp format
        assert result.isalnum()

    def test_id(self, scuid_instance):
        result = scuid_instance.id()
        # Test Case 1: ID starts with prefix
        assert result.startswith(scuid_instance.prefix)
        # Test Case 2: ID length
        assert len(result) > 20

    def test_slug(self, scuid_instance):
        result = scuid_instance.slug()
        # Test Case 1: Slug length
        assert len(result) == 7
        # Test Case 2: Slug format
        assert result.isalnum()


# Test Suite 4: Singleton functions
class TestSingletonFunctions:
    def test_scuid_function(self):
        result = scuid()
        # Test Case 1: Scuid starts with default prefix
        assert result.startswith("c")
        # Test Case 2: Scuid length
        assert len(result) > 20

    def test_slug_function(self):
        result = slug()
        # Test Case 1: Slug length
        assert len(result) == 7
        # Test Case 2: Slug format
        assert result.isalnum()

    def test_fingerprint_function(self):
        result = fingerprint()
        # Test Case 1: Fingerprint length
        assert len(result) == 4
        # Test Case 2: Fingerprint format
        assert result.isalnum()

    def test_create_fingerprint(self):
        pid = 12345
        hostname = "custom-host"
        result = create_fingerprint(pid, hostname)
        # Test Case 1: Fingerprint length
        assert len(result) == 4
        # Test Case 2: Fingerprint format
        assert result.isalnum()


# Test Suite 5: Edge cases
class TestEdgeCases:
    def test_discrete_values(self):
        scuid_instance = Scuid()
        # Test Case: Discrete values calculation
        assert scuid_instance.discreteValues == 36 ** scuid_instance.blockSize

    def test_counter_wrap(self):
        scuid_instance = Scuid()
        scuid_instance._counter = scuid_instance.discreteValues - 1
        # Test Case 1: Counter at max value
        assert scuid_instance.count() == scuid_instance.discreteValues - 1
        # Test Case 2: Counter wraps to 0
        assert scuid_instance.count() == 0


# Test Suite 6: Collision Resistance
class TestCollisionResistance:
    @staticmethod
    def check_collision(fn, iterations):
        """
        Helper function to test collision resistance of a given ID generator function.
        """
        ids = set()  # Use a set for fast lookups
        for _ in range(iterations):
            id_value = fn()
            if id_value in ids:
                return False  # Collision detected
            ids.add(id_value)
        return True  # No collisions detected

    def test_scuid_collision(self):
        # Test Case 1: No collisions for scuid() with 2 million iterations
        assert self.check_collision(scuid, 2000000), "scuid() IDs should not collide within 2 million iterations"

    def test_slug_collision(self):
        # Test Case 2: No collisions for slug() with 1 million iterations
        assert self.check_collision(slug, 1000000), "slug() IDs should not collide within 1 million iterations"
