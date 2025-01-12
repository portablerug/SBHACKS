
# Not working


def get_gmail_service():
    # Create a Gmail API service instance
    # This is a placeholder function. You need to implement the actual logic to create and return the service instance.
    import google.auth
    from googleapiclient.discovery import build

    creds, _ = google.auth.default()
    service = build('gmail', 'v1', credentials=creds)
    return service


def get_history(service, user_id='me', start_history_id=None):
    # Get the history of changes in the mailbox
    history = service.users().history().list(userId=user_id, startHistoryId=start_history_id).execute()
    return history

def main():
    service = get_gmail_service()
    # Replace with a stored historyId from the last read email
    start_history_id = '1234567890'  # Example historyId
    
    history = get_history(service, start_history_id=start_history_id)
    if not history.get('history'):
        print('No new changes found.')
    else:
        print(f"History: {history}")

if __name__ == '__main__':
    main()