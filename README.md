# InstagramMessagingBot
📬 Instagram DM Outreach Bot

This project is an automated outreach tool that sends personalized Instagram DMs to users listed in a spreadsheet. It uses the instagrapi library to interface with the Instagram API, and supports features like:

✨ Features
🔐 Secure login via .env file
📄 Loads names and usernames from an Excel (.xlsx) sheet
💬 Sends three separate DMs per user for natural conversation flow
📛 Skips duplicates using a follow-up tracker file
🕒 Waits between messages to avoid spam detection
✅ Fallbacks for username lookup when needed
📁 Excel Format (leads.xlsx)
| Name | Instagram | (other columns ignored) |
|------------|----------------|
| Name | Username |
| Bob | Bob123456 |

Only the Name and Instagram columns are used. Others (email, phone, etc.) are ignored.
