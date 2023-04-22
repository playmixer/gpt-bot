import discord
from classes import chat_gpt
from classes.logger import logger

log = logger(prefix='discord_')
chat: chat_gpt.ChatGPT = None

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
bot = discord.Client(intents=intents)


@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))


@bot.event
async def on_message(ctx):
    try:
        if ctx.author != bot.user and (
                (ctx.guild is not None and ctx.content.startswith(f"<@{bot.user.id}>")) or ctx.guild is None):
            answer = await ctx.reply("Думаю ...")
            log.info(f"{ctx.channel.id} Q: {ctx.content}")
            log.info(ctx)
            response = chat.input(ctx.channel.id, ctx.content)

            log.info(f"{ctx.channel.id} A: {response}")

            await answer.edit(content=response)
    except Exception as err:
        print(err)
        log.error(err)


def run(discord_api_key='', openai_api_key=''):
    global chat
    global bot
    chat = chat_gpt.ChatGPT(openai_api_key)
    config = {
        'token': discord_api_key,
        'prefix': 'prefix',
    }
    bot.run(config['token'])
