import os, json

from datetime import datetime
from redis import Redis
from dotenv import load_dotenv

load_dotenv()

REDIS_HOST=os.getenv("REDIS_HOST")
REDIS_PORT=os.getenv("REDIS_PORT")
REDIS_DB_ID=os.getenv("REDIS_DB_ID")

CONTRACTOR_QUEUE_KEY=os.getenv("CONTRACTOR_QUEUE_KEY")
CONTRACTOR_SUBPAGES_SUBKEY=os.getenv("CONTRACTOR_SUBPAGES_SUBKEY")

SUBPAGE_QUEUE_KEY=os.getenv("SUBPAGE_QUEUE_KEY")

redis = Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB_ID, decode_responses=True)

def set_contractor_info(contractor_id: str, info: dict):
    redis.hmset(contractor_id, {k: json.dumps(v) for k, v in info.items()})

def get_contractor_info(contractor_id: str):
    return {k: json.loads(v) for k, v in redis.hgetall(contractor_id).items()}

def add_contractor_subpage(contractor_id: str, url: str):
    redis.sadd(f"{contractor_id}:{CONTRACTOR_SUBPAGES_SUBKEY}", url)

def get_contractor_subpages(contractor_id: str):
    return redis.smembers(f"{contractor_id}:{CONTRACTOR_SUBPAGES_SUBKEY}")

def set_subpage_info(url: str, info: dict):
    redis.hmset(url, {k: json.dumps(v) for k, v in info.items()})

def get_subpage_info(url: str):
    return {k: json.loads(v) for k, v in redis.hgetall(url).items()}

def push_subpage_queue(contractor_id: str, url: str):
    redis.sadd(SUBPAGE_QUEUE_KEY, f"{contractor_id}:{url}")

def pop_subpage_queue():
    res = redis.spop(SUBPAGE_QUEUE_KEY)

    if res is None:
        return None
    else:
        return res.split(':', 1)

def get_subpage_queue():
    return redis.smembers(SUBPAGE_QUEUE_KEY)