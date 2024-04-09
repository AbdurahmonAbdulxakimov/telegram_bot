from typing import Dict
from telegram import Bot, BotCommand


def set_up_commands(bot_instance: Bot) -> None:
    commands: Dict[str, str] = {
        "start": "🚀 Start Authenticator bot",
    }

    bot_instance.delete_my_commands()
    bot_instance.set_my_commands(
        commands=[
            BotCommand(command, description)
            for command, description in commands.items()
        ],
    )
