"""
    MoyaiBot

    --------------

    Made by oxi, aka oxi#0309 on discord.

    --------------

    I don't really have much to say, this is 
    a pretty nice one-server bot, moderation
    tools, fun stuff, custom made commands,
    and a lot of fun stuff, overall pretty
    nice bot 😎
"""

import os
import sys
import json
import random
import logging

import _monke_patch
from _private import token, asc

import discord
from discord.ext import commands
from discord_slash import SlashCommand

def get_prefix(client, message):
    with open('user_prefixes.json', 'r') as f:
        prefixes = json.load(f)
        f.close()
    try:
        return prefixes[str(message.author.id)]
    except:
        return ['.', '. ', '<@!815562681267650589> ', '<@!815562681267650589>', '<@815562681267650589> ', '<@815562681267650589>']


client = commands.AutoShardedBot(command_prefix=get_prefix, help_command=None, intents=discord.Intents.all(),
                                 case_insensitive=True, allowed_mentions=discord.AllowedMentions.none())
slash = SlashCommand(client, sync_commands = False, sync_on_cog_reload=False)
logging.basicConfig(format = '%(name)s::%(asctime)s::%(levelname)s::%(message)s', level = logging.INFO)
client.logger = logging.getLogger('discord')

@client.event
async def on_message(message):
    if message.guild is None:
        return
    else:
        await client.process_commands(message)

@client.command(aliases=['prefix'])
async def userprefix(ctx, *, prefix = ''):
    if prefix == '':

        await ctx.send('You can\'t set your prefix to nothing young man :sunglasses:')
        return

    else:

        with open('user_prefixes.json', 'r') as f:
            prefixes = json.load(f)
            f.close()

        prefixes[str(ctx.author.id)] = f'{prefix} ', prefix, '<@!815562681267650589> ', '<@!815562681267650589>', '<@815562681267650589> ', '<@815562681267650589>'

        try:

            with open('user_prefixes.json', 'w') as f:
                json.dump(prefixes, f, indent=4)
                f.close()

            await ctx.send(f'User prefix succesfully changed to `{prefix}`')
            
        except:
            await ctx.send("You can't change your prefix to that.")


@client.command(aliases=['l'])
@commands.is_owner()
async def load(ctx, extension='all'):
    """
        Command for loading a
        specific cog/extension.
    """
    await ctx.trigger_typing()
    if extension == 'all':

        msg = await ctx.send('Loading all extensions...')
        try:

            for filename in os.listdir('./cogs'):

                if filename.endswith('.py'):

                    client.load_extension(f'cogs.{filename[:-3]}')

            await msg.edit(content='All extensions loaded successfully.')

        except commands.ExtensionError as e:

            await msg.edit(content=f'An error happened...\n```py\n{e.__class__.__name__}: {e}\n```')

    else:

        msg = await ctx.send(f'Loading {extension}...')
        try:

            client.load_extension(f'cogs.{extension}')
            await msg.edit(content=f'{extension} loaded successfully.')

        except commands.ExtensionError as e:
            await msg.edit(content=f'An error happened...\n```py\n{e.__class__.__name__}: {e}\n```')


@client.command(aliases=['u'])
@commands.is_owner()
async def unload(ctx, extension='all'):
    """
        Command for unloading a
        specific cog/extension
    """
    await ctx.trigger_typing()
    if extension == 'all':

        msg = await ctx.send('Unloading all extensions...')
        try:

            for filename in os.listdir('./cogs'):

                if filename.endswith('.py'):

                    client.unload_extension(f'cogs.{filename[:-3]}')

            await msg.edit(content='All extensions unloaded succesfully.')

        except commands.ExtensionError as e:

            await msg.edit(content=f'An error happened...\n```py\n{e.__class__.__name__}: {e}\n```')

    else:

        msg = await ctx.send(f'Unloading {extension}...')
        try:

            client.unload_extension(f'cogs.{extension}')
            await msg.edit(content=f'{extension} unloaded successfully.')

        except commands.ExtensionError as e:
            await msg.edit(content=f'An error happened...\n```py\n{e.__class__.__name__}: {e}\n```')


@client.command(name='reload', aliases=['r'])
@commands.is_owner()
async def _reload(ctx, extension='all'):
    """
        Command for reloading a
        specific cog/extension
    """
    if extension == 'all':

        msg = await ctx.send('Reloading all extensions...')

        try:

            await ctx.trigger_typing()

            for filename_cogs in os.listdir('./cogs'):

                if filename_cogs.endswith('.py'):

                    client.reload_extension(f'cogs.{filename_cogs[:-3]}')

            await msg.edit(content='All extensions reloaded successfully.')

        except commands.ExtensionError as e:

            await msg.edit(content=f'An error happened...\n```py\n{e.__class__.__name__}: {e}\n```')

    else:

        msg = await ctx.send(f'Reloading {extension}...')
        try:

            client.reload_extension(f'cogs.{extension}')
            await msg.edit(content=f'Cog "{extension}" reloaded successfully.')

        except commands.ExtensionError as e:
            await msg.edit(content=f'An error happened...```py\n{e.__class__.__name__}: {e}\n```')


if __name__ == '__main__':
    from termcolor import colored
    import random
    print(colored(random.choice(asc), 'yellow', 'on_grey', ['blink']), end = '\n\n')

    for filename in os.listdir('./cogs'):
        if filename.endswith('.py') and not filename.startswith('_'):
            client.load_extension(f'cogs.{filename[:-3]}')
            client.logger.info(f'Loaded {filename}')

    client.run(token)
