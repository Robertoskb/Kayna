import os
import discord
from discord.ext import commands
from decouple import config
from django.core import management
from manage import init_django


init_django()
management.call_command('makemigrations')
management.call_command('migrate')

management.call_command('loaddata', 'data.json')

client = commands.Bot(command_prefix='-', intents=discord.Intents.all(),
                      application_id=1162450467452895282)


@client.event
async def on_ready():
    print('I am ready')


@client.event
async def on_disconnect():
    print('Disconnected')


def load():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            client.load_extension(f'cogs.{filename[:-3]}')


def main():
    load()
    client.run(config("TOKEN"))


main()
