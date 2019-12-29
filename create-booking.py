import json
import redis

from code_generator import app as code

redis_host="localhost"
redis_port=6379
redis_db=2

try:
    cache = redis.Redis(
        host=redis_host,
        port=redis_port,
        db=redis_db
    )
    print("Successfully connected to Redis ({})...".format(redis_host))
except:
    print("Error connecting to Redis ({})...".format(redis_host))

def handler(event, context):
    print("[book.py] New booking received. Inputs on next log:")
    print("{}".format(event))

    booking_id = code.generate()
    # Booking Key Notes:
    # - Formula: muggley:<source>:<booking id>
    # - Example: muggley:slack:abc123
    key = "muggley:slack:" + booking_id
    value = { "a": "b" }
    output = cache.set(key, json.dumps(value))
    print("Caching booking info of {}... Result: {}".format(booking_id, output))

    body = {
        "code": "OK",
        "result": {
            "booking_id": booking_id
        }
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response
