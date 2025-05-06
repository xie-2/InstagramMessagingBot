import os
import time
import random
from datetime import datetime, timedelta
from instagrapi import Client
from dotenv import load_dotenv

# Load .env credentials
load_dotenv()
IG_USERNAME = os.getenv("IG_USERNAME")
IG_PASSWORD = os.getenv("IG_PASSWORD")

# Load the follow-up history
def load_followed_users(filepath):
    if not os.path.exists(filepath):
        return set()
    with open(filepath, "r") as f:
        return set(line.strip() for line in f if line.strip())

# Save a new username after follow-up
def save_followed_user(filepath, username):
    with open(filepath, "a") as f:
        f.write(username + "\n")

# Setup
followed_up_path = "followed_up.txt"
followed_up_users = load_followed_users("Path")

# Login
cl = Client()
cl.login(IG_USERNAME, IG_PASSWORD)

#48 hours cutoff
cutoff_time = datetime.now() - timedelta(hours = 48)

# Fetch inbox threads
threads = cl.direct_threads(amount=20)

for thread in threads:
    try:
        if not thread.messages:
            continue

        last_msg = thread.messages[0]
        last_msg_time = last_msg.timestamp
        username = thread.users[0].username

        recipient_id = thread.users[0].pk  # the recipient, not you
        seen_timestamp = thread.last_seen_at.get(recipient_id, {}).get("timestamp", None)

        has_seen = seen_timestamp is not None and datetime.fromtimestamp(int(seen_timestamp) / 1e6) > last_msg_time

        # Check conditions
        print(f"🧪 Checking {thread.users[0].username}")
        print(f"    Last sender: {last_msg.user_id} (you: {cl.user_id})")
        print(f"    Last message at: {last_msg_time}, cutoff: {cutoff_time}")
        print(f"    Seen: {has_seen}")
        print(f"    Already followed up: {username in followed_up_users}")

        if (
            str(last_msg.user_id) == str(cl.user_id) and
            last_msg_time < cutoff_time and
            not has_seen and
            username not in followed_up_users
        ):
            print(f"🎯 Conditions passed — attempting to message {username}...")

            follow_up = (
                f"Hey, just checking in on the message in case you were busy."
            )

            try:
                cl.direct_send(follow_up, [recipient_id])
                print(f"✅ Follow-up sent to {username}")
                save_followed_user(followed_up_path, username)
                followed_up_users.add(username)
                time.sleep(random.uniform(10, 20))
            except Exception as e:
                print(f"❌ Failed to send message to {username}: {e}")
        else:
            print(f"⛔ Did not pass condition for {username}")

    except Exception as e:
        print(f"❌ Error processing thread: {e}")
        time.sleep(5)
