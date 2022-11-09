import os
from dotenv import load_dotenv
import discord
import openai

load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
OPENAI_TOKEN = os.getenv('OPENAI_TOKEN')
client = discord.Client(intents=discord.Intents.all())
openai.api_key = OPENAI_TOKEN

@client.event
async def on_ready():
    string = f'{client.user} has connected to: '
    print("#" * len(string))
    print(string)
    print(', '.join(map(str, client.guilds)))
    print("#" * len(string))
    await client.user.edit(username="Dr. Jekyll and Mr. Hyde")

@client.event
async def on_error(event, *args, **kwargs):
    with open('error.log', 'a', encoding='utf-8') as f:
        if event == 'on_message':
            f.write(f'Unhandled message: {args[0]}\n')
        else:
            raise

@client.event
async def on_message(message):
    if message.author == client.user: # if the bot sends a message, ignore it
        return
    if "!openai" in message.content[0:7]:
        await ask_openai(message)

async def ask_openai(message):
    prompt = message.content[message.content.index("!openai") + 8:]
    completion = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0)
    func = await message.channel.send(completion["choices"][0]["text"].lstrip())
    await run_as_jekyll(func)

async def run_as_jekyll(func):
    await client.user.edit(username="Dr. Jekyll")
    await func
    await client.user.edit(username="Dr. Jekyll and Mr. Hyde")
async def run_as_hyde(func):
    await client.user.edit(username="Mr. Hyde")
    await func
    await client.user.edit(username="Dr. Jekyll and Mr. Hyde")

client.run(DISCORD_TOKEN)