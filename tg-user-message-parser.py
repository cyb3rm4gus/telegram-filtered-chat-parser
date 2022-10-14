#!/usr/bin/env python3

"""
file:         tg-user-message.py
author:       cyb3rm4gus
email:        cybersec78@gmail.com
github:       https://github.com/cyb3rm4gus
description:  Script to parse a Telegram chat history JSON file for specific users messages into a tabular format (CSV).
requirements: Python 3.x, ijson
"""

import csv
import json
import re
import sys
import os
import ijson
from datetime import datetime


columns = [
    "msg_id",
    "sender",
    "sender_id",
    "reply_to_msg_id",
    "date",
    "msg_type",
    "msg_content",
    "has_mention",
    "has_email",
    "has_phone",
    "has_hashtag",
    "is_bot_command",
]

file_types = [
    "animation",
    "video_file",
    "video_message",
    "voice_message",
    "audio_file",
]

mention_types = [
    "mention",
    "mention_name",
]

null_name_counter = 0


def parse_telegram_to_csv(jdata):

    chat_name = str(sys.argv[1])
    output_filepath = f"{chat_name}.csv"

    with open(output_filepath, "w", encoding="utf-8") as output_file:

        writer = csv.DictWriter(output_file, columns, dialect="unix", quoting=csv.QUOTE_NONNUMERIC)
        writer.writeheader()

        for message in jdata:

            msg_id = message["id"]
            sender = message["from"]
            sender_id = message["from_id"]
            reply_to_msg_id = message["reply_to_message_id"] if "reply_to_message_id" in message else -1
            date = message["date"].replace("T", " ")
            dt = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")

            msg_content = message["text"]
            msg_type = "text"

            if "media_type" in message:
                msg_type = message["media_type"]
                if message["media_type"] == "sticker":
                    if "sticker_emoji" in message:
                        msg_content = message["file"]
                    else:
                        msg_content = "?"
                elif message["media_type"] in file_types:
                    msg_content = message["file"]
            elif "file" in message:
                msg_type = "file"
                msg_content = message["file"]

            if "photo" in message:
                msg_type = "photo"
                msg_content = message["photo"]
            elif "poll" in message:
                msg_type = "poll"
                msg_content = str(message["poll"]["total_voters"])
            elif "location_information" in message:
                msg_type = "location"
                loc = message["location_information"]
                msg_content = str(loc["latitude"]) + "," + str(loc["longitude"])

            has_mention = 0
            has_email = 0
            has_phone = 0
            has_hashtag = 0
            is_bot_command = 0

            if type(msg_content) == list:
                txt_content = ""
                for part in msg_content:
                    if type(part) == str:
                        txt_content += part
                    elif type(part) == dict:
                        if part["type"] == "link":
                            msg_type = "link"
                        elif part["type"] in mention_types:
                            has_mention = 1
                        elif part["type"] == "email":
                            has_email = 1
                        elif part["type"] == "phone":
                            has_phone = 1
                        elif part["type"] == "hashtag":
                            has_hashtag = 1
                        elif part["type"] == "bot_command":
                            is_bot_command = 1

                        txt_content += part["text"]
                msg_content = txt_content

            msg_content = msg_content.replace("\n", " ")

            row = {
                "msg_id": msg_id,
                "sender": sender,
                "sender_id": sender_id,
                "reply_to_msg_id": reply_to_msg_id,
                "date": date,
                "msg_type": msg_type,
                "msg_content": msg_content,
                "has_mention": has_mention,
                "has_email": has_email,
                "has_phone": has_phone,
                "has_hashtag": has_hashtag,
                "is_bot_command": is_bot_command,
            }

            writer.writerow(row)


if __name__ == "__main__":

    if len(sys.argv) != 3:
        print("ERROR: incorrect number of arguments!")
        print("How to use it:")
        print("    python3 tg-user-message-parser.py <chat_history_json> <user_id>")
        print("Example:")
        print("    python3 tg-user-message-parser.py movies_group.json 12345678")
        sys.exit()

    filtered = []

    with open(sys.argv[1], 'r', encoding='utf-8') as f:
        print("opened file")
        objects = ijson.items(f, 'messages.item')
        for item in objects:
            try:
                if sys.argv[2] in item['from_id']:
                    filtered.append(item)
            except KeyError as e:
                # sometimes TG json item has no 'from_id' field, but that's no reason to crash
                pass

    parse_telegram_to_csv(filtered)

