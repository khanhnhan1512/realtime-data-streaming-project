import json
import requests
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
        print("User Data Generated:")
        print(json.dumps(formatted_response, indent=4))
        
        # Simulate Kafka production (without actual Kafka)
        print(f"✅ Successfully processed user data for: {formatted_response['username']}")
        print(f"📧 Email: {formatted_response['email']}")
        print(f"🏠 Address: {formatted_response['address']}")
        print("📤 Data would be sent to Kafka topic 'users_created'")
        
        return f"Data streaming completed successfully for user: {formatted_response['username']}"
        
    except Exception as e:
        print(f"Error in stream_data: {str(e)}")
        return f"Failed to stream data: {str(e)}"