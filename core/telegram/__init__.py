import telegram
from telegram.ext import Application, Updater, CommandHandler, MessageHandler, filters
from classes.chat_gpt import ChatGPT
from classes.logger import logger
from classes.replicate import Replicate
from classes.translater import translate as translate_text

chat_gpt: ChatGPT = None
rep: Replicate = None
log = logger(prefix="telegram_")


async def start(update, context):
    try:
        addcommand = await context.bot.set_my_commands([
            telegram.bot.BotCommand("start", "eqweq")
        ])
        log.info(addcommand)
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text="Привет! Я виртуальный ассистент. Что я могу для вас сделать?")
    except Exception as err:
        log.error(err)


async def translate(update, context):
    try:
        text = update.message.text.split(" ")[1:]
        text = ' '.join(text)

        t = translate_text(text)

        answer = await context.bot.send_message(chat_id=update.effective_chat.id, text=t,
                                                reply_to_message_id=update.effective_message.id)
    except Exception as err:
        log.error(err)


async def paint(update, context):
    try:
        text = update.message.text.split(" ")[1:]
        text = ' '.join(text)
        log.info(f"{id} Q Prompt: {text}")

        answer = await context.bot.send_message(chat_id=update.effective_chat.id, text="Готовлю рисунок...",
                                                reply_to_message_id=update.effective_message.id)

        if len(text) > 0:
            trans = translate_text(text)
            url = rep.paint(trans)
        else:
            url = "short prompt"

        log.info(f"{id} R Prompt: {url}")

        await context.bot.edit_message_text(chat_id=update.effective_chat.id, text=url,
                                            message_id=answer.id)
    except Exception as err:
        await context.bot.edit_message_text(chat_id=update.effective_chat.id,
                                            text="Извините, возникла проблема при формировании ответа",
                                            message_id=answer.id)
        log.error(err)


async def echo(update, context):
    try:
        text = update.message.text
        id = update.effective_chat.id
        log.info(f"{id} Q: {text}")

        answer = await context.bot.send_message(chat_id=update.effective_chat.id, text="Готовлю ответ...",
                                                reply_to_message_id=update.effective_message.id)
        await context.bot.send_chat_action(chat_id=update.effective_chat.id,
                                           action=telegram.constants.ChatAction.TYPING, pool_timeout=100)

        response = chat_gpt.chat(id=id, text=text)
        log.info(f"{id} A: {response}")

        await context.bot.edit_message_text(chat_id=update.effective_chat.id, text=response,
                                            message_id=answer.id)
    except Exception as err:
        chat_gpt.reset_history(update.effective_chat.id)
        await context.bot.edit_message_text(chat_id=update.effective_chat.id,
                                            text="Извините, возникла проблема при формировании ответа",
                                            message_id=answer.id)
        log.error(err)


async def reset(update, context):
    try:
        chat_gpt.reset_history(update.effective_chat.id)
        answer = await context.bot.send_message(chat_id=update.effective_chat.id, text="История сброшена",
                                                reply_to_message_id=update.effective_message.id)
    except Exception as err:
        await context.bot.edit_message_text(chat_id=update.effective_chat.id,
                                            text="Извините, возникла проблема при формировании ответа",
                                            message_id=answer.id)
        log.error(err)


class TelegramBot:
    def __init__(self, telegram_api_key=None, openai_api_key=None, replicate_api_key=None):
        global chat_gpt
        global rep
        try:
            chat_gpt = ChatGPT(openai_api_key, log)
            self.application = Application.builder().token(telegram_api_key).build()

            rep = Replicate(api_token=replicate_api_key)

            self.application.add_handler(CommandHandler("start", start))
            self.application.add_handler(CommandHandler("translate", translate))
            self.application.add_handler(CommandHandler("paint", paint))
            self.application.add_handler(CommandHandler("reset", reset))
            self.application.add_handler(MessageHandler(filters.TEXT, echo))
        except Exception as err:
            log.error(err)

    def run(self):
        self.application.run_polling()
