import discord
import requests
from pygicord import Paginator
from bs4 import BeautifulSoup as bs

from io import BytesIO
from discord.ext import commands
from discord_slash import cog_ext, context


class extra(commands.Cog):
    def __init__(self, client):
        self.client = client

    async def split_string(self, ctx, string_to_be_split, n=None):
        if n == None:
            print('\n\n\n\nNo amount of pages indicated moment\n\n\n\n')
            return
        else:
            # for i in range(0, len(string_to_be_split), n - 10):
            #     IRanOutOfVarNames = [string_to_be_split[i:i + n]]
            # return IRanOutOfVarNames
            a = []
            embed_list = []

            # abcde = [string_to_be_split[i:i+n] for i in range(0, len(string_to_be_split), n)]
            for i in range(0, len(string_to_be_split), n):
                a.append(string_to_be_split[i:i+n])

            print(a)
            # embed = (discord.Embed(description = f'This is page {x}').add_field(name = 'lel', value = f'```html\n{abcde[x]}```'))

    @cog_ext.cog_slash(name='topgg', description='Sends the top.gg vote link', guild_ids=[802202917737463829])
    async def topgg(self, ctx: context):
        print(ctx)
        await ctx.send('[Here it is](https://top.gg/servers/802202917737463829/vote)', hidden=False)

    # @cog_ext.cog_slash(name = 'InvalidName', guild_ids = [802202917737463829])
    # async def __bro(self, ctx : context):
    #     await ctx.send('whoever reads this is epic', hidden = True)

    @commands.command()
    async def web(self, ctx, *, url):
        await ctx.message.add_reaction('✅')
        if not url.startswith('https://'):
            url = 'https://' + url
        sdasd = requests.get(url)
        asdfsdf = bs(str(sdasd.content), features='html.parser')
        xd = BytesIO(asdfsdf.prettify().encode())
        await ctx.send(file=discord.File(xd, f'{url}.html'))

    @commands.command()
    @commands.is_owner()
    async def moment(self, ctx):
        msg = await ctx.send(embed=discord.Embed())
        await msg.edit(suppress=True)
        await msg.add_reaction('🗿')

#    @commands.Cog.listener()
#    async def on_message(self, message):
#        """
#            Playing with wait_for
#        """
#        if message.content.startswith('.moment'):
#            channel = message.channel
#            await channel.send('Send me that 👍 reaction, mate')
#            try:
#                reaction, user = await self.client.wait_for('reaction_add', timeout=60.0, check=lambda reaction, user: reaction.emoji == '👍')
#            except asyncio.TimeoutError:
#                await channel.send('👎')
#            else:
#                await channel.send('👍')
#                print(reaction)
#                print(user)


def setup(client):
    client.add_cog(extra(client))
