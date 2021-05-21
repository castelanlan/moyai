import time
import discord
import asyncio
import datetime

from datetime import datetime
from discord.ext import commands


class Info(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.client.launch_time = datetime.utcnow()

    @commands.command()
    async def info(self, ctx):
        dsc = ctx.guild.description
        if dsc is None:
            dsc = "This server doesn't have a description"
        embed = discord.Embed(
            title=ctx.guild.name, description=dsc, color=0xff33ff)
        embed.add_field(name="Server created at",
                        value=ctx.guild.created_at, inline=False)
        embed.add_field(name="Server Owner",
                        value=ctx.guild.owner, inline=False)
        embed.add_field(name="Server Region",
                        value=ctx.guild.region, inline=False)
        embed.add_field(name="Server ID",
                        value=ctx.guild.id, inline=False)
        embed.set_thumbnail(url=ctx.guild.icon_url)
        await ctx.send(embed=embed)
        
    def parse_time(self, time : str) -> str:
        return str(time).split('.')[0]

    @commands.command()
    async def user(self, ctx, member: discord.Member = None):

        if member is None:
            member = ctx.author

        joined_at = self.parse_time(member.joined_at)
        created_at = self.parse_time(member.created_at)

        roles = []
        for r in member.roles:
            roles.append(r.mention)
        roles.reverse()

        embed = discord.Embed(
            title=f'{member}', description=f'This the info for {member.name}', color=0x2b2be5)

        embed.add_field(name = 'Roles:', value = ' '.join(roles), inline = False)
        embed.add_field(name = 'Joined at:', value = joined_at, inline = False)
        embed.add_field(name = 'Accout created at:', value = created_at, inline = False)

        embed.set_footer(text='Bot created specifically for the Moyai Cult server😎',
                         icon_url=f'{ctx.guild.icon_url}')
        await ctx.send(f'{member.id}', embed=embed)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def rules(self, ctx):
        embed = discord.Embed(title='Welcome to the **Moyai Cult**')
        embed.add_field(name='<:FatMoyai:802203172630167573> Here are the epic rules you must follow :sunglasses:',
                        value='Any questions ask a online staff :flushed:<a:MoyaiPet:802208522892738632> \n ‎‎‎‎‎‎‎‏‏‎ ‎‏‏‎ ‎‏‏‎ ‎‏‏‎ ‎‏‏‎ ‎‏‏‎ ‎‏‏‎ ‎‏‏‎ ‎‏‏‎ ‎‏‏‎ ‎‏‏‎ ‎‏‏‎ ‎‏‏‎ ‎‏‏‎ ‎‏‏‎ ‎', inline=False)
        embed.add_field(name=':one:', value='\n No spamming of links (including discord invites) allowed anywhere. <:FatMoyai:802203172630167573> \n ‎‎‎‎‎‎‎‏‏‎ ‎‏‏‎ ‎‏‏‎ ‎‏‏‎ ‎‏‏‎ ‎‏‏‎ ‎‏‏‎ ‎‏‏‎ ‎‏‏‎ ‎‏‏‎ ‎‏‏‎ ‎‏‏‎ ‎‏‏‎ ‎‏‏‎ ‎‏‏‎ ', inline=False)
        embed.add_field(name=':two:', value="Please don't spam moyai :moyai: or similar emojis unless you are in <#802203364963516467>. <:FatMoyai:802203172630167573> \n ‎‎‎‎‎‎‎‏‏‎ ‎‏‏‎ ‎‏‏‎ ‎‏‏‎ ‎‏‏‎ ‎‏‏‎ ‎‏‏‎ ‎‏‏‎ ‎‏‏‎ ‎‏‏‎ ‎‏‏‎ ‎‏‏‎ ‎‏‏‎ ‎‏‏‎ ‎‏‏‎ ", inline=False)
        embed.add_field(name=':three:', value="Make sure you're posting in the correct channel, <#802202918316671048>, <#804026610578882570>, etc... <:FatMoyai:802203172630167573> \n ‎‎‎‎‎‎‎‏‏‎ ‎‏‏‎ ‎‏‏‎ ‎‏‏‎ ‎‏‏‎ ‎‏‏‎ ‎‏‏‎ ‎‏‏‎ ‎‏‏‎ ‎‏‏‎ ‎‏‏‎ ‎‏‏‎ ‎‏‏‎ ‎‏‏‎ ‎‏‏‎ ", inline=False)
        embed.add_field(name=':four:', value="No gore, sexual/NSFW or scary content. <:MoyDespair:802215202703671336> \n ‎‎‎‎‎‎‎‏‏‎ ‎‏‏‎ ‎‏‏‎ ‎‏‏‎ ‎‏‏‎ ‎‏‏‎ ‎‏‏‎ ‎‏‏‎ ‎‏‏‎ ‎‏‏‎ ‎‏‏‎ ‎‏‏‎ ‎‏‏‎ ‎‏‏‎ ‎‏‏‎ ", inline=False)
        embed.add_field(name=':five:', value="No hating/being offensive <a:MoyBlobs:802208505775128626><a:MoyBlobs:802208505775128626>, Moyai Cult is a _chill_ place, let's keep it that way. <:MoyTooCool:802228849756078151> \n ‎‎‎‎‎‎‎‏‏‎ ‎‏‏‎ ‎‏‏‎ ‎‏‏‎ ‎‏‏‎ ‎‏‏‎ ‎‏‏‎ ‎‏‏‎ ‎‏‏‎ ‎‏‏‎ ‎‏‏‎ ‎‏‏‎ ‎‏‏‎ ‎‏‏‎ ‎‏‏‎ ", inline=False)
        embed.add_field(name=':six:', value="If you break these guidelines you'll be asked to stop, and if you become too much of a pain, you'll be kicked or banned depending on staff patience. <:MoySpy:802215953222991962> \n ‎‎‎‎‎‎‎‏‏‎ ‎‏‏‎ ‎‏‏‎ ‎‏‏‎ ‎‏‏‎ ‎‏‏‎ ‎‏‏‎ ‎‏‏‎ ‎‏‏‎ ‎‏‏‎ ‎‏‏‎ ‎‏‏‎ ‎‏‏‎ ‎‏‏‎ ‎‏‏‎ ")
        embed.set_footer(text='Made exclusively for the Moyai Cult server. 😎')
        await ctx.send(embed=embed)

    # @commands.command()
    # async def help(self, ctx):
    #    embed = discord.Embed(
    #        title='Welcome to castelan bot!',
    #        description=f'This is a help command asked by {ctx.author.name}',
    #        color=0xff4040
    #    )
    #    embed.add_field(name='bruh',
    #                    value='this command is not done yet lul, ping oxi to finish it'
    #                    )
    #    await ctx.send(embed=embed)

    @commands.command()
    async def suggest(self, ctx, *, content):
        suggestchannel = self.client.get_channel(804430796701564979)
        embed = discord.Embed(
            title=f'New suggestion from {ctx.author}', description='ㅤㅤㅤㅤㅤㅤㅤ', color=0x20ff30)
        embed.add_field(name=f'{content}', value='React with 👍 or 👎 to vote.')
        embed.set_thumbnail(url=f'{ctx.guild.icon_url}')
        embed.set_author(name=f'{ctx.author}',
                         icon_url=f'{ctx.author.avatar_url}')
        embed.set_footer(
            text='Bot made exclusively for the Moyai Cult server 😎')
        msg = await suggestchannel.send(embed=embed)
        await msg.add_reaction('👍')
        await msg.add_reaction('👎')

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def todo(self, ctx, *, content: str = None):
        try:
            if content is not None:
                with open('todo.py', 'at') as f:
                    f.write(f'"TODO: {content} - {ctx.author}"\n')
            await ctx.send('Done:sunglasses:', delete_after = 5)
        except:
            await ctx.send(':thinkinh: Hmmm, something went wrong, ping oxi')

    @commands.command(aliases=['m'])
    async def members(self, ctx):
        embed = discord.Embed(title=f'{ctx.guild.name}', color=0x3030ff)
        embed.add_field(name='Member count:',
                        value=f'This server currently has {ctx.guild.member_count} gamers :sunglasses:')
        embed.set_footer(text='Bot made exclusively for the Moyai Cult server😎',
                         icon_url=f'{ctx.guild.icon_url}')
        await ctx.send(embed=embed)

    @commands.command(aliases=['owner', 'author'], hidden = True)
    async def whomadeyou(self, ctx):
        donecommandschannel = self.client.get_channel(796218151879835658)
        await ctx.send(f"I was made by {self.client.owner.name}")

    @commands.command()
    async def ping(self, ctx):
        await ctx.trigger_typing()
        time_start = datetime.utcnow()
        msg = await ctx.send(embed=discord.Embed(description='Calculating ping...'))
        time_after = datetime.utcnow()
        result = str(time_after - time_start)
        await msg.edit(content=None, embed=discord.Embed(description=f'📡 **{round(self.client.latency * 1000)}** ms\n🖥️ **{result[8:11]}** ms', color=0x2F3136))

    @commands.command(aliases=['avatar', 'profilepicture', ])
    async def pfp(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author
        embed = discord.Embed()
        embed.set_image(url=f'{member.avatar_url}')
        await ctx.send(embed=embed)

    @commands.command()
    async def uptime(self, ctx):
        delta_uptime = datetime.utcnow() - self.client.launch_time
        hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)
        embed = discord.Embed(
            description=f'**{days}** days, **{hours}** hours, **{minutes}** minutes and **{seconds}** seconds', color=0x4ea6b8)
        await ctx.send(embed=embed)

    @todo.error
    async def todo_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send('Ayo u todo\'ing too much :moyai: ', delete_after=5)


def setup(client):
    client.add_cog(Info(client))
