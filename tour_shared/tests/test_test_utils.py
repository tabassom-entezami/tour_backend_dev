from tour_shared.test_utils import StubRedis, StubRedisLock
import pytest


@pytest.fixture
def stub_redis():
    return StubRedis()


class TestStubRedis:
    def test_set_get_success(self, stub_redis: StubRedis):
        key = "some key"
        value = "some value"
        stub_redis.set(key, value)
        assert isinstance(stub_redis.get(key), bytes)
        assert stub_redis.get(key).decode() == value

    def test_get_missing(self, stub_redis: StubRedis):
        assert stub_redis.get("some missing key") is None

    def test_getitem_setitem_success(self, stub_redis: StubRedis):
        key = "some key"
        value = "some value"
        stub_redis[key] = value
        assert isinstance(stub_redis[key], bytes)
        assert stub_redis[key].decode() == value

    def test_getitem_missing(self, stub_redis: StubRedis):
        with pytest.raises(KeyError):
            _ = stub_redis["some invalid key"]

    def test_delitem_contain_success(self, stub_redis: StubRedis):
        key = "some key"
        stub_redis[key] = "blah-blah"
        assert key in stub_redis
        del stub_redis[key]
        assert key not in stub_redis

    def test_Hash(self, stub_redis: StubRedis):
        hash_name = "some name"
        another_hash_name = "some other name"
        hash_instance = stub_redis.Hash(hash_name)
        another_hash_instance = stub_redis.Hash(another_hash_name)
        hash_instance["key_1"] = "value_1"
        another_hash_instance["key_2"] = "value_3"
        assert "key_1" in stub_redis.Hash(hash_name) and "key_2" not in stub_redis.Hash(hash_name)
        assert "key_2" in stub_redis.Hash(another_hash_name) and "key_1" not in stub_redis.Hash(another_hash_name)

    def test_lock_acquire_release(self, stub_redis: StubRedis):
        lock_name = "some name"
        lock: StubRedisLock = stub_redis.lock(lock_name)
        assert lock.acquire()
        assert not stub_redis.lock(lock_name).acquire(block=False)
        assert lock.release()
        assert not stub_redis.lock(lock_name).release()

    def test_lock_context_manager(self, stub_redis: StubRedis):
        lock: StubRedisLock = stub_redis.lock("some name")
        with lock:
            assert not lock.acquire(block=False)
        assert lock.acquire(block=False)
