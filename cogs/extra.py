import discord
import requests
import aiohttp
from pygicord import Paginator
from bs4 import BeautifulSoup as bs
import re
from io import BytesIO
from fuzzywuzzy import fuzz
from discord.ext import commands
from discord_slash import cog_ext, context
from pprint import pprint

class extra(commands.Cog):
    def __init__(self, client):
        self.client = client

    async def search_from_sphinx(self, keyword, docs = 'dpy', fuzzSort=True) -> list:
        """
        Searches sphinx for a pages matching keyword
        :param url: url of sphinx docs
        :param keyword: the keyword to search for
        :param fuzzSort: should fuzzy matching/sorting be used
        :return: list of matches
        """
        if docs == 'dpy':
            url = 'https://discordpy.readthedocs.io/en/stable/genindex.html'
        elif docs == 'slash':
            url = 'https://discord-py-slash-command.readthedocs.io/en/latest/genindex.html'
        elif docs == 'py':
            url = 'https://docs.python.org/3/genindex-all.html'
        keyword = keyword.lower()
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as res:
                text = await res.read()
        soup = bs(text, "html.parser")
        if fuzzSort:
            # utilises fuzzy string matching to determine which page is most likely to be what the user wants
            rData = {}
            for x in soup.find_all('a'):
                if len(str(x.get('href'))) > 3:
                    data = [x.get('href')]
            data = [x.get("href") for x in soup.find_all("a") if len(str(x.get("href"))) > 3]
        
            for val in data: # for str(val) in data: # gaming
                val = str(val) # 🗿
                # remove any links to github or sphinx itself
                if re.search(r'\.org*?$', val) or val.startswith("https://github.com/"):
                    continue
        
                # "topic" of each link, while preserving the link 🧠
                val = (val, re.sub(r'\.html$', '', val).split(".")[-1].replace("_", " "))
        
                # determining how likely the result is
                ratio = fuzz.ratio(val[1].lower(), keyword)
                rData[val[0]] = ratio
        
            # get top 5 values
            
            data = sorted(rData, key=rData.get, reverse=True)#[:5]
            keys = sorted(rData.values(), reverse = True)
            return data, keys
        else:
            data = [x.get("href") for x in soup.findAll("a") if keyword in str(x).lower()]
            return data

    @commands.command()
    async def docs(self, ctx, *, text):
        # if text.startswith('slash '):
        #     base_url = 'https://discord-py-slash-command.readthedocs.io/en/latest/genindex.html'
        #     text
        # elif text.startswith('py'):
        #     ...
        await ctx.message.add_reaction('✅')
        text = text.split('|')
        base_url = 'https://discordpy.readthedocs.io/en/stable/'
        docs = 'dpy'
        # fu = True
        try:
            if text[1]:
                if 'slash' in text[1]:
                    base_url = 'https://discord-py-slash-command.readthedocs.io/en/latest/'
                    docs = 'slash'
                elif 'py' in text[1]:
                    docs = 'py'
                    base_url = 'https://docs.python.org/3/'
        except IndexError:
            ...

        resp, keys = await self.search_from_sphinx(text[0].lower(), docs)
        if not resp:
            await ctx.send(embed = (discord.Embed(title = 'No results found :(', color = 0x2f3136)).set_footer(text = ctx.author, icon_url = ctx.author.avatar_url))
            return
        base_embed = discord.Embed(title="Search", color= 0x2f3136)
        base_embed.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
        count = 1
        embed_list = []
        page_embed = base_embed.copy()
        for_res = resp.copy()
        idx = 0
        for x in for_res:
            if count != 1 and count % 5 == 1:
                embed_list.append(page_embed)
                page_embed = base_embed.copy()
            link = base_url + x
            try:            
                page_embed.add_field(name=f'{count} | Confidence: {keys[idx]}', value=f"[`{x.split('#')[1]}`]({link})", inline=False)
            except IndexError:
                continue
            resp.remove(x)
            count += 1
            idx += 1
        embed_list.append(page_embed)
        if not embed_list:
            return await ctx.send("No result found.")
        pags = Paginator(pages = embed_list)
        await pags.start(ctx)
        # await ctx.send(result)


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

    async def get_member_from_chapeu(self, ctx, count):
        msgs = []
        async for m in ctx.channel.history(limit = count, oldest_first = False):
            msgs.append(m.author.display_name)

        return msgs

    @commands.command()
    @commands.is_owner()
    async def tes(self, ctx, arg):
        if arg:
            try:
                if arg.startswith('^'):
                    count = arg.count('^')
                    members = await self.get_member_from_chapeu(ctx, count)
                    print(count)
                    print(len(members))
                    print(members)
                    await ctx.send(members[count - 1])
                    #count = arg.count('^')
                    #await ctx.send(f'gamings: {count}')
            except Exception as errror:
                raise errror

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

