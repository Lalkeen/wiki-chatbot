import random
import requests
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Enter your bot token here
TOKEN = "BOT_TOKEN"

# Initialize the bot
bot = telegram.Bot(TOKEN)

# Define the message counter
msg_counter = 0

# Define the maximum number of messages to receive before sending a message
MAX_MSGS = random.randint(10, 50)

# Define the function that will send the message
def send_message(update, context):
    message_text = update.message.text
    chat_id = update.message.chat_id

    # Generate a random Wikipedia article title in Russian
    article_title = get_random_wikipedia_article()

    # Format the article title as a link to the Wikipedia page
    article_url = f'https://ru.wikipedia.org/wiki/{article_title.replace(" ", "_")}'
    article_link = f'{article_title} ({article_url})'
    reply_text = f'нет блять, {article_link}'
    message_id = update.message.message_id

    # Send the reply message
    context.bot.send_message(chat_id=chat_id, text=reply_text, reply_to_message_id=message_id)


# Define a function to retrieve a random Wikipedia article title in Russian
def get_random_wikipedia_article():
    response = requests.get(
        'https://ru.wikipedia.org/w/api.php?action=query&list=random&rnnamespace=0&rnlimit=1&format=json')
    response_json = response.json()
    article_title = response_json['query']['random'][0]['title']
    return article_title



# Define the function that will handle messages
def handle_message(update, context):
    global msg_counter, MAX_MSGS
    msg_counter += 1
    if msg_counter >= MAX_MSGS:
        # Reset the message counter
        msg_counter = 0
        # Reset the maximum number of messages to receive before sending a message

        MAX_MSGS = random.randint(5, 10)
        # Send the message
        send_message(update, context)

# Define the function that will start the bot
def start(update, context):
    message_text = "Hi there! пашел нахер"
    context.bot.send_message(chat_id=update.effective_chat.id, text=message_text)

# Define the main function
def main():
    # Create the updater and dispatcher
    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # Add handlers for the start command and messages
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text, handle_message))

    # Start the bot
    updater.start_polling()
    updater.idle()

# Call the main function
if __name__ == '__main__':
    main()
