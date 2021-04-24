import discord

from bot import get_prefix
from discord import Embed
from pygicord import Paginator
from discord.ext import commands


def get_pages(client, message):
    user_prefix = get_prefix(client, message)[0]
    if user_prefix == '':
        user_prefix = ' '
    main_embed = (Embed(description=f'Welcome to Moyai Bot! Your prefix is `{user_prefix}`!', color=discord.Color.red())).add_field(
        name='Meta:', value=f'`{user_prefix}ping`: Shows Moyai Bot\'s ping.\n'
    )

    moderation_embed = (Embed(description='Here are all the moderation commands Moyai Bot provides you')).add_field(
        name=f'Basic moderation:', value=f'`{user_prefix}kick <person>`: kicks someone')

    pages = [main_embed, moderation_embed]
    return pages

    # Generate a list of 5 embeds
    # for i in range(1, 6):
    #     embed = discord.Embed(title = f'I\'m the embed {i}')
    #     pages.append(embed)
    # return pages


class help(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name='ahelp')
    async def _help(self, ctx):
        paginator = Paginator(pages=get_pages(self.client, ctx.message))
        await paginator.start(ctx)


def setup(client):
    client.add_cog(help(client))

#    @commands.group(aliases = ['help'],invoke_without_command=True)
#    async def ahelp(self, ctx):
#        embed = discord.Embed()
#        await ctx.send(embed = embed)
#
#    @ahelp.group(invoke_without_command=True)
#    async def reddit(self, ctx):
#        await ctx.send('help reddit')
#
#    @reddit.command()
#    async def third(self, ctx):
#        await ctx.send('third')
