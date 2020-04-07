import redis

redis_client = redis.Redis(host='127.0.0.1', port=6379, db=0, password='foxActive110')


if __name__ == '__main__':
    redis_client.set("hello2", "world", ex=60)
    for key in redis_client.keys():
        redis_client.delete(key)
