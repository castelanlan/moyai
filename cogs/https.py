import aiohttp
import json
import discord
import random
from discord.ext import commands

class reddit(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases = ['reddit', 'subreddit'])
    @commands.cooldown(1, 7, commands.BucketType.user)
    async def sub(self, ctx, *, subreddit):
        new_sub = subreddit.replace(' ', '_')
        #try:
        async with aiohttp.ClientSession() as cs:
            async with cs.get(f'https://www.reddit.com/r/{new_sub}/new.json?sort=hot') as r:
                try:
                    res    =   await r.json()
                    nmr    =   random.randint(0, 25)
                    image  =   res['data']['children'][nmr]['data']['url']
                    author =   res['data']['children'][nmr]['data']['author']
                    sub    =   res['data']['children'][nmr]['data']['subreddit_name_prefixed']
                    text   =   res['data']['children'][nmr]['data']['title']
                    link   =   res['data']['children'][nmr]['data']['permalink']

                    embed  =   discord.Embed(title = text,
               description =   f'From {sub} - [Here\'s the link](https://reddit.com{link})\nRequested by **{ctx.author.name}**', 
                    color  =   0xf874fc
                        )
                    embed.set_image(url = image)
                    embed.set_footer(text = f'This post was made by u/{author}')
                    msg = await ctx.send(embed = embed)
                    await msg.add_reaction('🔼')
                    await msg.add_reaction('↕️')
                    await msg.add_reaction('🔽')
                    print(f'reddit {subreddit}')
                except Exception as e:
                    await ctx.send(embed = discord.Embed(description = 'Something went wrong, check if the subreddit name is correct!', color = 0x2F3136))
                    print(f'reddit {subreddit} FAILED')
                    print(e)

    @commands.command(name = 'randomperson', aliases = ['rp', 'randomp', 'rperson'])
    async def random_person(self, ctx):
        async with aiohttp.ClientSession() as cd:
            async with cd.get(f'https://randomapi.com/api/6de6abfedb24f889e0b5f675edc50deb?fmt=raw&sole') as r:
                try:
                    res = await r.read()
                    ablabl = json.loads(res)
                    #print(ablabl)
                    first_name = ablabl[0]['first']
                    last_name = ablabl[0]['last']
                    email = ablabl[0]['email']
                    address = ablabl[0]['address']
                    created_at = ablabl[0]['created']
                    balance = ablabl[0]['balance']
                    embed = discord.Embed(title = 'Random Person', 
                    description = f'Name: **{first_name} {last_name}**\nEmail: **{email}**\nAddress: **{address}**\nCreated at: **{created_at}**\nBalance: **{balance}**',
                    color = discord.Color.random()
                    )
                    await ctx.send(embed = embed)
                except Exception as e:
                    await ctx.send(f'An error eccourred...\n```py\n{e.__class__.__name__}: {e}\n```')

    @commands.command(aliases = ['search', 'wiki', 'wikiof', 'wikipedia'])
    async def wikisearch(self, ctx, search):
        new_search = search.replace(' ', '_')
        await ctx.channel.trigger_typing()
        async with aiohttp.ClientSession() as cs:
            async with cs.get(f'https://en.wikipedia.org/w/api.php?action=opensearch&format=json&search={new_search}') as r:
                try:
                    res = await r.json()
                    first_result = res[1]
                    if first_result != []:
                        embed = discord.Embed(title = 'Wikipedia', description = f'Here are the wikipedia results for **{new_search}**:', color = 0xacff26)
                        for results in first_result:
                                results_links = results.replace(' ', '_')
                                embed.add_field(name = results, value = f'[Link here](https://en.wikipedia.org/wiki/{results_links})', inline = False)
                    else:
                        embed = discord.Embed(description = 'There are no articles to be found :pensive:', color = 0x2F3136)
                    await ctx.send(embed = embed)
                except:
                    await ctx.send(embed = discord.Embed(description = 'There are no articles to be found :pensive:', color = 0x2F3136))

    @commands.command()
    async def ip(self, ctx, number):
        await ctx.trigger_typing()
        async with aiohttp.ClientSession as cs:
            async with cs.get(f'https://api.ipgeolocation.io/ipgeo?apiKey=905ce85034b94477b63f6a345f6bc04f&ip={number}') as r:
                try:
                    res = await r.json()
                    print(res)
                except Exception as e:
                    await ctx.send(f'```py\n{e.__class__.__name__}: {e}```')


    @commands.command()
    async def test(self, ctx):
        await ctx.trigger_typing()
        async with aiohttp.ClientSession as cs:
            async with cs.get('https://oasis.sh/api/users') as r:
                await ctx.send(f'Status: \n```py\n{r.status}```')
                print(r)
                try:
                    res = await r.json()
                    print(res)
                except Exception as e:
                    await ctx.send(f'```py\n{e.__class__.__name__}: {e}```')


    @sub.error
    async def sub_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(embed = discord.Embed(description = f'You\'re on cooldown! Try again in {round(error.retry_after, 2)} seconds.', color = 0x2F3136))
            print('cooldown')
        else:
            await ctx.send(embed = discord.Embed(description = f'Something unexpected happened...\n\n {error}'))

def setup(client):
    client.add_cog(reddit(client))