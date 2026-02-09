import os
import json
import time
import uuid
import threading
from datetime import datetime
import boto3
from botocore.exceptions import ClientError

# Import configuration
try:
    import config
except ImportError:
    print("Error: config.py not found. Please create it based on the template.")
    exit(1)

# --- Constants & State ---
IDENTITY_FILE = "identity.json"
POLL_INTERVAL = 5 # seconds

state = {
    "user_id": None,
    "user_name": None,
    "messages": [],
    "last_sync_time": 0,
    "running": True
}

# --- AWS S3 Setup ---
s3_client = boto3.client(
    's3',
    aws_access_key_id=config.AWS_ACCESS_KEY,
    aws_secret_access_key=config.AWS_SECRET_KEY,
    region_name=config.S3_REGION
)

def get_s3_messages():
    """Download the shared messages.json from S3."""
    try:
        response = s3_client.get_object(Bucket=config.S3_BUCKET_NAME, Key=config.MESSAGES_FILE)
        content = response['Body'].read().decode('utf-8')
        return json.loads(content)
    except ClientError as e:
        if e.response['Error']['Code'] == "NoSuchKey":
            # If the file doesn't exist yet, return an empty list
            return []
        else:
            print(f"\n[Error] Cloud storage error: {e}")
            return None
    except Exception as e:
        print(f"\n[Error] Unexpected error: {e}")
        return None

def save_s3_messages(messages):
    """Upload the updated messages list to S3."""
    try:
        s3_client.put_object(
            Bucket=config.S3_BUCKET_NAME,
            Key=config.MESSAGES_FILE,
            Body=json.dumps(messages, indent=2),
            ContentType='application/json'
        )
        return True
    except Exception as e:
        print(f"\n[Error] Failed to upload messages: {e}")
        return False

# --- Identity Management ---
def initialize_identity():
    """Load or create user identity."""
    if os.path.exists(IDENTITY_FILE):
        with open(IDENTITY_FILE, "r") as f:
            data = json.load(f)
            state["user_id"] = data.get("id")
            state["user_name"] = data.get("name")
            print(f"Welcome back, {state['user_name']}!")
    else:
        print("Welcome to Cloud Chat!")
        name = input("Enter your name to join the chat: ").strip()
        if not name:
            name = "Anonymous"
        
        user_id = str(uuid.uuid4())[:8]
        state["user_id"] = user_id
        state["user_name"] = name
        
        with open(IDENTITY_FILE, "w") as f:
            json.dump({"id": user_id, "name": name}, f)
        
        print(f"Identity saved! Your ID is {user_id}.")

# --- Background Sync ---
def sync_worker():
    """Background thread to poll for new messages."""
    while state["running"]:
        remote_messages = get_s3_messages()
        if remote_messages is not None:
            # Simple check if there are new messages
            if len(remote_messages) > len(state["messages"]):
                new_count = len(remote_messages) - len(state["messages"])
                state["messages"] = remote_messages
                # Clear line and print update if we aren't waiting for input (basic CLI)
                # Note: In a real TUI we'd use curses or similar, but keeping it simple for students.
                pass 
        time.sleep(POLL_INTERVAL)

# --- UI Methods ---
def display_messages():
    """Clear terminal and show all messages."""
    # For a simple student demo, we'll just print them in order
    os.system('cls' if os.name == 'nt' else 'clear')
    print("=== CLOUD CHAT ROOM ===")
    print(f"Logged in as: {state['user_name']} ({state['user_id']})")
    print("-" * 30)
    
    if not state["messages"]:
        print("\nNo messages yet. Be the first to say hello!")
    else:
        for msg in state["messages"]:
            timestamp = msg.get("time", "??:??")
            user = msg.get("user", "Unknown")
            uid = msg.get("uid", "xxxx")
            text = msg.get("text", "")
            
            prefix = "[YOU]" if uid == state["user_id"] else f"[{user}]"
            print(f"{timestamp} {prefix}: {text}")
    
    print("-" * 30)
    print("Commands: ':q' to quit, ':r' to refresh, or just type your message.")

def send_message(text):
    """Add a message to the shared list and upload."""
    new_msg = {
        "uid": state["user_id"],
        "user": state["user_name"],
        "text": text,
        "time": datetime.now().strftime("%H:%M")
    }
    
    # Critical section: Pull latest, append, push
    # Note: This is prone to race conditions if two people send AT THE SAME SECOND
    # but for a demo it's perfect to explain high-level cloud state.
    latest = get_s3_messages()
    if latest is None:
        latest = []
    
    latest.append(new_msg)
    if save_s3_messages(latest):
        state["messages"] = latest
        return True
    return False

# --- Main Entry ---
def main():
    initialize_identity()
    
    # Initial fetch
    print("Connecting to cloud storage...")
    state["messages"] = get_s3_messages() or []
    
    # Start background sync
    threading.Thread(target=sync_worker, daemon=True).start()
    
    # Simple Loop
    while True:
        display_messages()
        try:
            choice = input("\nMessage: ").strip()
            
            if choice.lower() == ':q':
                state["running"] = False
                print("Goodbye!")
                break
            elif choice.lower() == ':r':
                print("Refreshing...")
                state["messages"] = get_s3_messages() or []
                continue
            elif choice:
                send_message(choice)
        except KeyboardInterrupt:
            state["running"] = False
            break

if __name__ == "__main__":
    main()
