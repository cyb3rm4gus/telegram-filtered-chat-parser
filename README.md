
# telegram-chat-parser

Python scripts to parse a Telegram chat history backup (`JSON`) into tabular format (`CSV`).

Original script telegram-chat-parser requires no extra packages, only Python 3.x, but it won't process large JSON files.

The second script tg-user-message-parser.py requires ijson module that allows it to process JSON file of any size.

## How to use it

Create venv & install requirements:

```bash
python3 -m venv venv

source venv/bin/activate

pip install -r requirements.txt
```

Using Telegram's Desktop or Web interfaces, go to the chat you want to parse, click on the options button (three dots in the upper right corner) and them click on `Export chat history`. In the dialog window, right next to `Format`, chose `JSON`. After the backup is completed, Telegram will generate a `results.json` file.
Next you need to copy or move it to script directory and optionally rename it.

Command to run the original script that converts WHOLE JSON to CSV:

```bash
python3 telegram-chat-parser.py <jsonfile.json>
```

For each chat backup in `results.json`, a `.csv` file will be created in the same directory. The output filename is a stripped down version of the actual chat name (only letters and numbers are kept).

Command to parse JSON for specific user's messages:
```bash
python3 tg-user-message-parser.py <jsonfile.json> <user_id>
```

If there are messages from specified user in chat history you will get a CSV that contains them. The file name would be the same as jsonfile,
for example if you process file mychat.json you will get mychat.csv

## The output format

Once the script is done parsing, the result `CSV` file will have the format bellow:

 - `msg_id`: the unique identifier of the message
 - `sender`: the literal name of the sender
 - `sender_id`: the unique identifier of the sender
 - `reply_to_mesg_id`: if the message is a reply, this column will store the id of that message, or -1 otherwise
 - `date`: date time stamp of the message
 - `msg_type`:  can be one of the following: `text, sticker, file, photo, poll, location or link`
 - `msg_content`: the text content the message, already cleaned in terms of newline and spaces; if the message was not a text (sticker, media, etc) this field will store the path pointing to the media
 - `has_mention`: it will be `1` if there's a mention in the text, `0` otherwise
 - `has_email`: it will be `1` if there's a email in the text, `0` otherwise
 - `has_phone`: it will be `1` if there's a phone contact in the message, `0` otherwise
 - `has_hashtag`: it will be `1` if there's a hashtag in the text, `0` otherwise
 - `is_bot_command`: it will be `1` if the message is a bot command, `0` otherwise

## Contributing

The original script author is Artur Rodrigues Rocha Neto @ https://github.com/keizerzilla
Second script author is cyb3rm4gus @ https://github.com/cyb3rm4gus

I hope this little script helps you in your project! If you have any suggestions or ideas to improve it, please feel free to open an issue. Thank you!
