import redis

# 创建连接池，将连接保存在连接池中
pool = redis.ConnectionPool(host="127.0.0.1", port=6379, db=0, password="foxActive110", max_connections=10)

# 创建一个redis实例，并使用连接池"pool"
redis_client = redis.Redis(connection_pool=pool)

if __name__ == '__main__':
    redis_client.set("hello2", "world", ex=60)
    for key in redis_client.keys():
        redis_client.delete(key)
