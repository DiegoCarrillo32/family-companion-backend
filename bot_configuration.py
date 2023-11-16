from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from queries import *
import requests
TOKEN: Final = '6801162244:AAFfKg3o-ThaHmSkwYcI7M6VNxaXaQNNoHk'
BOT_USERNAME: Final = '@ai_cozy_home_bot'


# Commands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text("Hello friend! Thank you for give a chance to user our innovative solution to "
                                    "improve the environment in your home")
    # await INSERT_ADMIN_USER('A', update.message.chat.id)
    data = {
        "family_user_chatId": update.message.chat.id,
        "user_mode": "A"
    }
    response = requests.post('http://localhost:5000/register_user?', json=data)
    print(response.content)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("I am Cozy Home bot! try to type 'configCozy' to configure our service ")


async def config_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("This is the config registration command. Please type 'user: <chat_id>' to "
                                    "register a family member")


# Responses
def handle_response(update: Update, text: str) -> str:
    lowerText: str = text.lower()

    if 'start cozy' in lowerText:
        return 'Iniciando servicios'
    if 'hello' in lowerText:
        return 'Hello friend!'
    if 'user:' in lowerText:
        family_member = lowerText[5:]
        data = {
            "family_user_chatId": str(update.message.chat.id),
            "family_member_chatId": family_member,
            "user_mode": "F"
        }
        response = requests.post('http://localhost:5000/register_family_member?', json=data)
        print(response.content)
        return 'Family user registered successfully'
    return 'I do not understand what you wrote'


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text

    print(f'User ({update.message.chat.id}) in {message_type}: "{text}"')

    if message_type == 'group':
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, '').strip()
            response: str = handle_response(update, new_text)
        else:
            return
    else:
        response: str = handle_response(update, text)

    print('Bot', response)
    await update.message.reply_text(response)


async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')



if __name__ == '__main__':
    print('Starting bot....')
    app = Application.builder().token(TOKEN).build()

    # Commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('config', config_command))


    # Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # Errors
    app.add_error_handler(error)

    # Polls the bot
    print('Polling...')
    app.run_polling(poll_interval=3)
