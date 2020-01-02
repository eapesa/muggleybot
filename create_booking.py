import os
import json
import redis

from code_generator import app as code

redis_host = os.environ.get("redis_host")
if not redis_host:
  redis_host = "localhost"
print("Redis host configured: {}".format(redis_host))

redis_port = os.environ.get("redis_port")
if not redis_port:
  redis_port = 6379
print("Redis port configured: {}".format(redis_port))

redis_db = os.environ.get("redis_db")
if not redis_db:
  redis_db = 0
print("Redis DB configured: {}".format(redis_db))

redis_ssl = os.environ.get("redis_ssl")
if not redis_ssl:
  redis_ssl = False
print("Redis SSL setup configured: {}".format(redis_ssl))

try:
    print("Connecting to Redis ({})...".format(redis_host))
    cache = redis.StrictRedis(
        host=redis_host,
        port=redis_port,
        db=redis_db,
        ssl=redis_ssl
    )
    print("Successfully connected to Redis ({})...".format(redis_host))
except:
    print("Error connecting to Redis ({})...".format(redis_host))

def handler(event, context):
    print("[book.py] New booking received. Inputs on next log:")
    print("{}".format(event))

    intent = event.get("currentIntent").get("name")
    print("[book.py] From intent: {}".format(intent))

    booking_id = code.generate()
    # Booking Key Notes:
    # - Formula: muggley:<source>:<booking id>
    # - Example: muggley:slack:abc123
    key = "muggley:slack:" + booking_id
    booking_deets = event.get("currentIntent").get("slots")
    output = cache.set(key, json.dumps(booking_deets))
    print("Caching booking info of {}... Result: {}".format(booking_id, output))

    reply = "Done booking your flight. Your booking reference is {}. Kindly check your email for more details.".format(booking_id)
    lex_response = {
        "sessionAttributes": {},
        "dialogAction": {
            "type": "Close",
            "fulfillmentState": "Fulfilled",
            "message": {
                "contentType": "PlainText",
                "content": reply
            }
        }
    }

    return lex_response

    # NOTE: Response for API Gateway / For testing via Serverless-Offline
    # body = {
    #     "code": "OK",
    #     "result": {
    #         "booking_id": booking_id
    #     }
    # }
    # response = {
    #     "statusCode": 200,
    #     "body": json.dumps(lex_response)
    # }