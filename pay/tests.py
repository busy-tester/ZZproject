from django.test import TestCase
import redis
import json
from utils.redis_pool import POOL
# Create your tests here.
# {
#   name1: "",
#   name2: {},
#   name3, []
#   zhoujunhao: {}
# }

conn = redis.Redis(connection_pool=POOL)
conn.set("name1", "xiaowei")
ret1 = conn.get("name1")

conn.hset("zhoujunhao", "key1", "value1")
conn.hmset("wangfan", {"key2":"value2", "key3":"value3"})
print(conn.hget("zhoujunhao", "key1"))
print(conn.hgetall("wangfan"))
print(conn.get("name1"))





