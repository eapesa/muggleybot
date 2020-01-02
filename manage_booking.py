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

  if intent == "FlightBookingIntent":
    return new_booking(event.get("currentIntent"))
  elif intent == "CheckBookingIntent":
    return check_booking(event.get("currentIntent"))
  elif intent == "CancelBookingIntent":
    return cancel_booking(event.get("currentIntent"))
  else:
    return default_handler()
  
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

def generate_response(reply):
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

def generate_cache_key(booking_id):
  # Booking Key Notes:
  # - Formula: muggley:<source>:<booking id>
  # - Example: muggley:slack:abc123
  key = "muggley:slack:" + booking_id
  return key

def default_handler():
  reply = "Sorry. I am not sure how to handle that. Please call our customer service hotline number 810-1234 or you may email us at helpdesk@muggleybooking.com"
  return generate_response(reply)

def new_booking(intent):
  booking_id = code.generate()
  key = generate_cache_key(booking_id)
  booking_deets = intent.get("slots")

  output = cache.set(key, json.dumps(booking_deets))
  print("Caching booking info of {}... Result: {}".format(booking_id, output))

  reply = "Done booking your flight. Your booking reference is {}. Kindly check your email for more details.".format(booking_id)
  return generate_response(reply)

def check_booking(intent):
  booking_id = intent.get("slots").get("BookingReference")
  key = generate_cache_key(booking_id)

  output = cache.get(key)
  if not output:
    reply = "I'm sorry but I can't find that flight reservation. If this is a mistake, kindly consult with out customer service. You may call us in hotline number 810-1234 or email us at helpdesk@muggleybooking.com."
    return generate_response(reply)
  else:
    booking_deets = json.loads(output)

    destination = booking_deets.get("Country")
    flight_date = booking_deets.get("FlightDate")
    return_date = booking_deets.get("ReturnDate")
    airline = booking_deets.get("Airline")
    reply = "Your flight details are as follows:\n\nDestination: {}\nFlight Date: {}\nReturn Date: {}\nAirline: {}".format(destination, flight_date, return_date, airline)

    return generate_response(reply)

def cancel_booking(intent):
  booking_id = intent.get("slots").get("BookingReference")
  key = generate_cache_key(booking_id)

  output = cache.delete(key)
  if not output:
    reply = "We encountered error cancelling your reservation {}. For urgent cancellation, kindly call our customer service hotline 810-1234 or email us at helpdesk@muggleybooking.com".format(booking_id)
    return generate_response(reply)
  else:
    reply = "Your booking reference {} has been cancelled. Kindly check your email for the cancellation details.".format(booking_id)
    return generate_response(reply)