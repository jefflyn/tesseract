import redis

redis_client = redis.Redis(host='127.0.0.1', port=6379, db=0)


if __name__ == '__main__':
    redis_client.set("hello2", "world", 10)
