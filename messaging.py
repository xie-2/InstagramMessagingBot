import time
import random
import os
from instagrapi import Client
from dotenv import load_dotenv
import pandas as pd

# Load environment variables from .env
load_dotenv()
IG_USERNAME = os.getenv("IG_USERNAME")
IG_PASSWORD = os.getenv("IG_PASSWORD")

# Load leads from Excel (Name + Instagram)
def load_leads_from_excel(filepath):
    df = pd.read_excel(filepath)

    # Keep only needed columns and drop empty ones
    df = df[["Name", "Instagram"]].dropna()

    # Clean Instagram usernames (remove @, trim spaces)
    df["Instagram"] = df["Instagram"].astype(str).str.replace("@", "").str.strip()
    df["Name"] = df["Name"].astype(str).str.strip()

    return list(zip(df["Instagram"], df["Name"]))

# Log into Instagram
cl = Client()
cl.login(IG_USERNAME, IG_PASSWORD)

# Load recipients from Excel file
leads = load_leads_from_excel("Path")  # Update path if needed

# Message loop
for username, name in leads:
    try:
        # Attempt fast lookup first
        try:
            user_id = cl.user_id_from_username(username)
        except:
            print(f"⚠️ Fallback for {username}")
            user_info = cl.user_info_by_username(username)
            user_id = user_info.pk

        # Format display name (fallback to username if empty)
        display_name = name if name else username

        # Create personalized message
        messages = [
            f"message1",
             "message2",
            "message3"
        ]

        for msg in messages:
            cl.direct_send(msg, [user_id])
            print(f"✅ Sent message: {msg}")
            time.sleep(random.uniform(2, 4))  # brief pause between messages to mimic human behavior
        # Wait between 12–25 seconds to avoid spam
        delay = random.uniform(12, 25)
        print(f"🕒 Waiting {round(delay, 2)} seconds...")
        time.sleep(delay)

    except Exception as e:
        print(f"❌ Could not message {username}: {e}")
        time.sleep(10)
