import datetime
import config
import logging
from handlers.database import Database

DB_URL = config.DB_URL
DB_NAME = config.DB_NAME
LOG_CHANNEL = config.LOG_CHANNEL

db = Database(DB_URL, DB_NAME)

async def handle_user_status(bot, cmd):
    chat_id = cmd.from_user.id
    if not await db.is_user_exist(chat_id):
        data = await bot.get_me()
        BOT_USERNAME = data.username
        await db.add_user(chat_id)
        if LOG_CHANNEL:
            await bot.send_message(
                LOG_CHANNEL,
                f"""
#NEW_USERS
┏━━━━━━━━━━━━┓
┣★ 𝙉𝙚𝙬 𝙐𝙨𝙚𝙧: [{cmd.from_user.first_name}](tg://user?id={cmd.from_user.id})
┣★ 𝘽𝙤𝙩 𝙐𝙨𝙚𝙧𝙉𝙖𝙢𝙚 : @{BOT_USERNAME}
┣★ 𝗕𝗼𝘁 𝗢𝘄𝗻𝗲𝗿 : @AM_YTBOTT""",
            )
        else:
            logging.info(f"#NewUser\nNew User : {cmd.from_user.first_name} \nUser Id : {cmd.from_user.id}")

    ban_status = await db.get_ban_status(chat_id)
    if ban_status["is_banned"]:
        if (
            datetime.date.today() - datetime.date.fromisoformat(ban_status["banned_on"])
        ).days > ban_status["ban_duration"]:
            await db.remove_ban(chat_id)
        else:
            await cmd.reply_text("You are Banned from using this Bot", quote=True)
            return
    await cmd.continue_propagation()
