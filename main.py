from telegram.ext import *
import my_secrets 
from cleantext import clean
from logic import MyBot

print('Starting up bot...')


# Lets us use the /start command
def start_command(update, context):
    update.message.reply_text('Hello there! I\'m a bot. What\'s up?')


# Lets us use the /help command
def help_command(update, context):
    update.message.reply_text('Try typing anything and I will do my best to respond!')


# Lets us use the /custom command

def handle_response(text) -> str:
    response = _EXTERNAL_CHATBOT.respond(text)
    return response


def handle_message(update, context):
    # Get basic info of the incoming message
    message_type = update.message.chat.type # Can be 'private', 'group', 'supergroup' or 'channel'
    
    text = str(update.message.text).lower()
    text = clean(text)
    text = text.strip()
    

    # Print a log for debugging
    print(f'User ({update.message.chat.id}) says: "{text}" in: {message_type}')


    response = handle_response(text)

    # Reply normal if the message is in private
    update.message.reply_text(response)


# Log errors
def error(update, context):
    print(f'Update {update} caused error {context.error}')


# Run the program
if __name__ == '__main__':
    _EXTERNAL_CHATBOT = MyBot()


    updater = Updater(my_secrets.token, use_context=True)
    dp = updater.dispatcher

    # Commands
    dp.add_handler(CommandHandler('start', start_command))
    dp.add_handler(CommandHandler('help', help_command))

    # Messages
    dp.add_handler(MessageHandler(Filters.text, handle_message))

    # Log all errors
    dp.add_error_handler(error)

    # Run the bot
    updater.start_polling(1.0) # bit listening
    updater.idle()