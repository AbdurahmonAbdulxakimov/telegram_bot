from dotenv import load_dotenv
import os
import requests
import json


load_dotenv()

TOKEN = os.environ.get("TOKEN")
BASE_URL = f"https://api.telegram.org/bot{TOKEN}/"


def make_request(method: str, params: dict = None):
    res = requests.get(f"{BASE_URL}{method}", params=params)
    return res.json()


def get_updates(offset: int = 0):
    return make_request("getUpdates", {"offset": offset})["result"]


def main():
    offset = 0
    make_request(
        "setMyCommands",
        {
            "commands": json.dumps(
                [
                    {
                        "command": "start",
                        "description": "Start the bot.",
                    },
                    {
                        "command": "help",
                        "description": "List of available commands.",
                    },
                    {
                        "command": "me",
                        "description": "Get information about yourself.",
                    },
                ]
            )
        },
    )

    while True:
        updates = get_updates(offset)
        for update in updates:
            offset: int = update["update_id"] + 1
            print(update["message"])

            if update["message"]:
                chat_id: int = update["message"]["chat"]["id"]
                message = update["message"]

                if "text" in message:
                    res = ""
                    match message["text"]:
                        case "/start":
                            res = make_request(
                                "sendMessage",
                                {
                                    "chat_id": chat_id,
                                    "text": f'Assalomu alaykum, {update["message"]["from"]["first_name"]}. Hush kelibsiz!',
                                    "reply_markup": json.dumps(
                                        {
                                            "keyboard": [
                                                [
                                                    {
                                                        "text": "My location",
                                                        "request_location": True,
                                                    }
                                                ],
                                                [
                                                    {
                                                        "text": "My phone number",
                                                        "request_contact": True,
                                                    }
                                                ],
                                            ],
                                        },
                                    ),
                                },
                            )
                        case "/help":
                            cmds: list = make_request("getMyCommands")["result"]
                            content: str = "Here is the list of commands:\n\n"
                            for cmd in cmds:
                                content += f'/{cmd["command"]} - {cmd["description"]}\n'

                            res = make_request(
                                "sendMessage",
                                {
                                    "chat_id": chat_id,
                                    "text": content,
                                },
                            )
                        case "/me":
                            user_id: int = message.get("from").get("id")
                            user_photos: dict = (
                                make_request(
                                    "getUserProfilePhotos",
                                    {
                                        "user_id": user_id,
                                    },
                                )
                                .get("result")
                                .get("photos")
                            )
                            photos = []
                            for user_photo in user_photos:
                                photos.append(
                                    {
                                        "type": "photo",
                                        "media": user_photo[1].get("file_id"),
                                    }
                                )
                            if photos:
                                photos[0].update(
                                    {
                                        "caption": message.get("from").get("first_name")
                                        + " "
                                        + message.get("from").get("last_name"),
                                    }
                                )

                            res = send_file(
                                method="sendMediaGroup",
                                body={
                                    "chat_id": chat_id,
                                    "media": json.dumps(photos),
                                },
                            )

                    print(res)
                elif "contact" in message:
                    contact = message["contact"]
                    first_name = contact.get("first_name", "")
                    last_name = contact.get("last_name", "")

                    res = make_request(
                        "sendMessage",
                        {
                            "chat_id": chat_id,
                            "text": f"{first_name} {last_name} phone number is {contact['phone_number']}",
                        },
                    )
                    print(res)
                elif "location" in message:
                    location = message["location"]

                    res = make_request(
                        "sendLocation",
                        {
                            "chat_id": chat_id,
                            "latitude": location["latitude"],
                            "longitude": location["longitude"],
                        },
                    )
                    print(res)

                    res = make_request(
                        "sendMessage",
                        {
                            "chat_id": chat_id,
                            "text": f"Your location is {location['latitude']} by latitude and {location['longitude']} by longitude.",
                            "reply_parameters": json.dumps(
                                {
                                    "message_id": res["result"].get("message_id"),
                                    "chat_id": chat_id,
                                }
                            ),
                        },
                    )
                    print(res)


if __name__ == "__main__":
    main()
