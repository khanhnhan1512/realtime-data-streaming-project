import json
import requests
from kafka import KafkaProducer
import time

def get_data():
    req = requests.get("https://randomuser.me/api")
    req = req.json()['results'][0]
    return req

def format_data(req):
    data = {}
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
        # Get and format data first
        response = get_data()
        formatted_response = format_data(response)
        print(json.dumps(formatted_response, indent=4))
        
        # Initialize Kafka producer with more robust settings
        producer = KafkaProducer(
            bootstrap_servers=['broker:29092'],  
            # bootstrap_servers=['localhost:9092'], # Use this for local testing
            max_block_ms=10000,  # Increased timeout for container environment
            request_timeout_ms=30000,  # 30 second timeout
            retry_backoff_ms=100,
            retries=3,
            acks='all',  # Wait for all replicas to acknowledge
            key_serializer=lambda x: x.encode('utf-8'),
            value_serializer=lambda x: x.encode('utf-8')
        )
        
        # Create a unique key for the message using username
        message_key = formatted_response['username']
        message_value = json.dumps(formatted_response)
        
        # Send message with key and get future object
        future = producer.send(
            'users_created', 
            key=message_key,
            value=message_value
        )
        
        # Block and wait for message to be sent with longer timeout
        record_metadata = future.get(timeout=30)
        
        print(f"Message sent successfully!")
        print(f"Topic: {record_metadata.topic}")
        print(f"Partition: {record_metadata.partition}")
        print(f"Offset: {record_metadata.offset}")
        print(f"Key: {message_key}")
        
        return f"Successfully processed user: {message_key}"
        
    except Exception as e:
        error_msg = f"Failed to process data or send message: {str(e)}"
        print(error_msg)
        # Re-raise the exception so Airflow can detect the failure
        raise Exception(error_msg)
        
    finally:
        if producer is not None:
            try:
                # Ensure all messages are sent before closing
                producer.flush()
                producer.close()
            except Exception as e:
                print(f"Error closing producer: {str(e)}")
                # Don't re-raise here as it might mask the original error
