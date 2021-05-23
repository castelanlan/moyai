import re
import discord
import aiohttp
from io import BytesIO
from pygicord import Paginator
from fuzzywuzzy import fuzz
from discord.ext import commands
from bs4 import BeautifulSoup as bs
from discord_slash import cog_ext, context
from discord_slash.utils.manage_commands import create_option

class memba(commands.MemberConverter):
    async def convert(self, ctx, count):
        if count:
            try:
                super().convert(ctx, argument)
                if count:
                    msgs = []
                    async for m in ctx.channel.history(limit = count, oldest_first = False):
                        msgs.append(m.author.display_name)
                    return msgs[count - 1]
                else:
                    return ctx.author
            except:
                ...
        else:
            return ctx.author


class extra(commands.Cog):
    def __init__(self, client):
        self.client = client

    async def do_string_sort(self, a : str) -> str:
        list(a)
        helpa = ''

        for i in a:
            helpa += i

        helpa = list(helpa)
        helpa.sort()

        helpa2 = ''

        for i in helpa:
            helpa2 += i

        return helpa2

    async def search_from_sphinx(self, keyword, docs = 'dpy', fuzzSort=True) -> list:
        """
        :param url: url of sphinx docs
        Searches sphinx for a pages matching keyword
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
        await ctx.message.add_reaction('✅')
        text = text.split('|')
        base_url = 'https://discordpy.readthedocs.io/en/stable/'
        docs = 'dpy'
        try:
            if text[1]:
                if 'slash' in text[1]:
                    base_url = 'https://discord-py-slash-command.readthedocs.io/en/latest/'
                    docs = 'slash'
                elif 'py' in text[1]:
                    docs = 'py'
                    base_url = 'https://docs.python.org/3/'
        except IndexError:
           pass # gaming

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
                page_embed.add_field(name=f"""‎‎ """, value=f"[`{x.split('#')[1]}`]({link}) Confidence: **{keys[idx]}**%", inline=False)
                
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

    @commands.command(name = 'sort')
    async def _sort(self, ctx, *, words):
        try:
            a = await self.do_string_sort(words)
            await ctx.send(a)
        except Exception as e:
            await ctx.send(e)

    @cog_ext.cog_slash(name = 'sort', description = 'sorts every letter in your message alphabetically', options = [create_option('message', 'The message to be sorted', 3, True)], guild_ids = [802202917737463829])
    async def sortt(self, ctx : context, message):
        try:
            a = await self.do_string_sort(message)
            await ctx.send(a)
        except Exception as e:
            await ctx.send(e)

    @cog_ext.cog_slash(name='topgg', description='Sends this server\'s top.gg link', guild_ids=[802202917737463829])
    async def topgg(self, ctx: context):
        await ctx.send('[Here it is](https://top.gg/servers/802202917737463829/vote)')

def setup(client):
    client.add_cog(extra(client))