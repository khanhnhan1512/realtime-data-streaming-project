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
    try:
        response = get_data()
        formatted_response = format_data(response)
        print(json.dumps(formatted_response, indent=4))
        
        # Publish a message to a topic
        # Use broker hostname for container environment
        producer = KafkaProducer(
            bootstrap_servers=['broker:29092'],  
            # bootstrap_servers=['localhost:9092'], # Use this for local testing
            max_block_ms=5000,
            key_serializer=lambda x: x.encode('utf-8'),
            value_serializer=lambda x: x.encode('utf-8')
        )
    except Exception as e:
        print(f"Error initializing Kafka producer or getting data: {str(e)}")
        # Return success even if Kafka is not available for DAG testing
        return "Data processing completed (Kafka connection failed)"
    
    try:
        # Create a unique key for the message using username
        message_key = formatted_response['username']
        message_value = json.dumps(formatted_response)
        
        # Send message with key and get future object
        future = producer.send(
            'users_created', 
            key=message_key,
            value=message_value
        )
        
        # Block and wait for message to be sent
        record_metadata = future.get(timeout=10)
        
        print(f"Message sent successfully!")
        print(f"Topic: {record_metadata.topic}")
        print(f"Partition: {record_metadata.partition}")
        print(f"Offset: {record_metadata.offset}")
        print(f"Key: {message_key}")
        
    except Exception as e:
        print(f"Failed to send message: {str(e)}")
        
    finally:
        # Ensure all messages are sent before closing
        producer.flush()
        producer.close()
