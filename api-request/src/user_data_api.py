import json
import requests
from kafka import KafkaProducer
import time
import logging
import uuid

def get_data():
    req = requests.get("https://randomuser.me/api")
    req = req.json()['results'][0]
    return req

def format_data(req):
    data = {}
    data['id'] = str(uuid.uuid4())
    data['first_name'] = req['name']['first']
    data['last_name'] = req['name']['last']
    data['gender'] = req['gender']
    location = req['location']
    data['address'] = f"{str(location['street']['number'])} {location['street']['name']}, {location['city']}, {location['state']}, {location['country']}"
    data["postcode"] = location["postcode"]
    data["email"] = req["email"]
    data["username"] = req["login"]["username"]
    data["dob"] = req["dob"]["date"]
    data["registered_date"] = req["registered"]["date"]
    data["phone"] = req["phone"]
    data["picture"] = req["picture"]["medium"]
    return data
    
def stream_data(): 
    producer = None
    try:
        producer = KafkaProducer(
            bootstrap_servers=['broker:29092'],  
            # bootstrap_servers=['localhost:9092'], # Use this for local testing
            max_block_ms=5000,  # Increased timeout for container environment
            request_timeout_ms=20000,  
            retry_backoff_ms=100,
            retries=3,
            acks='all',  # Wait for all replicas to acknowledge
            key_serializer=lambda x: x.encode('utf-8'),
            value_serializer=lambda x: json.dumps(x).encode('utf-8') if isinstance(x, dict) else x.encode('utf-8')
        )
        cur_time = time.time()
        
        while True:
            if time.time() > cur_time + 60:
                break
            try:
                # Get and format data first
                response = get_data()
                formatted_response = format_data(response)
                logging.info(json.dumps(formatted_response, indent=2))
                # Create a unique key for the message using id (already string)
                message_key = formatted_response['id']
                message_value = formatted_response
                # Send message with key and get future object
                future = producer.send(
                    'users_created', 
                    key=message_key,
                    value=message_value
                )
                # Block and wait for message to be sent with longer timeout
                record_metadata = future.get(timeout=30)
                logging.info(f"Message sent successfully! Key: {message_key}, Topic: {record_metadata.topic}, Partition: {record_metadata.partition}, Offset: {record_metadata.offset}")
            except Exception as e:
                logging.error(f"Error sending message: {str(e)}")
                continue   
    except Exception as e:
        logging.error(f"Error in Connection: {str(e)}")
        raise Exception(f"Error in Connection: {str(e)}")
    finally:
        if producer is not None:
            try:
                # Ensure all messages are sent before closing
                producer.flush()
                producer.close()
            except Exception as e:
                logging.error(f"Error closing producer: {str(e)}")
