import json
import logging
import os
import requests

CF_ACCESS_CLIENT_ID = os.environ.get('CF_ACCESS_CLIENT_ID')
CF_ACCESS_CLIENT_SECRET = os.environ.get('CF_ACCESS_CLIENT_SECRET')

def update_message_token_usage(user_id, message_id, message_type, llm_token_usage=0, embedding_token_usage=0) -> bool:
    logging.info(f"Updating message token usage for user {user_id} and message {message_id}")

    endpoint_url = "https://api.myreader.io/api/message"
    headers = {
        'CF-Access-Client-Id': CF_ACCESS_CLIENT_ID,
        'CF-Access-Client-Secret': CF_ACCESS_CLIENT_SECRET,
    }
    data = {
        'user': {
            "user_from": "slack",
            "user_platform_id": user_id
        },
        "message": {
            "message_platform_id": message_id,
            "message_type": message_type,
            "llm_token_usage": llm_token_usage,
            "embedding_token_usage": embedding_token_usage
        }
    }
    json_data = json.dumps(data)
    response = requests.post(endpoint_url, headers=headers, data=json_data)
    if response.status_code == 200:
        json_response = response.json()
        if 'error' in json_response:
            return False
        return True
    else:
        return False
    
def get_user(user_id):
    endpoint_url = f"https://api.myreader.io/api/user/slack/{user_id}"
    headers = {
        'CF-Access-Client-Id': CF_ACCESS_CLIENT_ID,
        'CF-Access-Client-Secret': CF_ACCESS_CLIENT_SECRET,
    }
    response = requests.get(endpoint_url, headers=headers)
    if response.status_code == 200:
        try:
            json_response = response.json()
            if 'error' in json_response:
                return None
            return json_response
        except:
            return "Error: Unable to parse JSON response"
    else:
        return f"Error: {response.status_code} - {response.reason}"
