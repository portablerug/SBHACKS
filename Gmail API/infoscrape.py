from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
import pickle
import os
import csv  # Import the CSV module

#trivial change
# Load credentials from the saved token.pickle file
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def get_gmail_service():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        raise Exception("Invalid or missing credentials.")
    return build('gmail', 'v1', credentials=creds)

def list_messages(service, user_id='me'):
    # List the messages in the user's mailbox
    response = service.users().messages().list(userId=user_id).execute()
    messages = response.get('messages', [])
    return messages

def get_message(service, user_id, msg_id):
    # Get the message content
    message = service.users().messages().get(userId=user_id, id=msg_id).execute()
    return message

def save_messages_to_csv(messages_data, filename='gmail_messages.csv'):
    # Save the messages data to a CSV file
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Message ID', 'Snippet'])  # Header row
        for message in messages_data:
            writer.writerow([message['id'], message['snippet']])  # Write each message's data

def main():
    service = get_gmail_service()
    messages = list_messages(service)
    if not messages:
        print('No messages found.')
    else:
        print(f'Found {len(messages)} messages.')
        messages_data = []
        for message in messages:
            msg = get_message(service, 'me', message['id'])
            print(f"Message snippet: {msg['snippet']}")
            messages_data.append({'id': message['id'], 'snippet': msg['snippet']})
        
        # Save the messages data into CSV after processing all messages
        save_messages_to_csv(messages_data)
        print("Messages saved to 'gmail_messages.csv'.")

if __name__ == '__main__':
    main()
