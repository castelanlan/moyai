import discord
import asyncio
import logging
from datetime import datetime
from discord.ext import commands, tasks
from bot import get_prefix
from .economy import load_db
import json

class events(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_connect(self):
        self.client.logger.info(f'Bot connected - {datetime.utcnow()}')

    @commands.Cog.listener()
    async def on_ready(self):
        """
            For knowing if the bot is actually
            live / the last time I ran this 
            script.
        """
        self.client.logger.info(f'Bot ready - {datetime.utcnow()}')

    @commands.Cog.listener()
    async def on_disconnect(self):
        self.client.logger.warning(f'Bot disconnected - {datetime.utcnow()}')

    @commands.Cog.listener()
    async def on_message(self, message):
        """
            No-branch-programming? What's that?
        """
        try:
            if message.content.startswith('hi '):
                await message.channel.send('Hello my little pogchamp 😽')
            elif message.content == '<@!815562681267650589>' or message.content == '<@!815562681267650589> ':
                await message.channel.send(f'My prefix for you is `{get_prefix(self.client, message)[0]}`, and stop pinging me :rage:')
            elif message.content.startswith('hello '):
                await message.channel.send('no')
            elif message.content.startswith('Hey bot'):
                await message.add_reaction('👋')
            elif message.content.startswith('who asked'):
                await message.channel.send('I asked')
            elif message.content.startswith('xd'):
                await message.add_reaction('<a:MoyWobble:802208434085822474>')
            elif message.content.startswith('XD'):
                await message.add_reaction('<a:MoyWobbleIntensifies:802208413555228682>')
            elif message.content.startswith('xD'):
                await message.add_reaction('<:MoyJoy:802215478755065897>')
            elif message.content.startswith('Xd'):
                await message.add_reaction('<:MoyVibeCheckWoke:802228762694647850>')
            elif message.content.startswith('lol'):
                await message.add_reaction('<a:MoyBlobs:802208505775128626>')
            elif message.content.startswith('lmao'):
                await message.add_reaction('<a:MoyaiPet:802208522892738632>')
            elif message.content.startswith('lmfao'):
                await message.add_reaction('<a:MoyRoll:802208448841777152>')
            elif message.content.startswith('fax'):
                await message.add_reaction('<:MoyWoke:802228902411894804>')
            elif message.content.startswith('factual'):
                await message.add_reaction('<:MoyWoke:802228902411894804>')
            elif message.content.startswith('true'):
                await message.add_reaction('<:MoyWoke:802228902411894804>')
            elif message.content.startswith('wdm'):
                await message.add_reaction('<:MoyThinkGray:804062890356244480>')
            elif message.content.startswith('wdym'):
                await message.add_reaction('<:MoyThinkGray:804062890356244480>')
            elif message.content.startswith('wtf'):
                await message.add_reaction('<:MoyThink:804062311299940352>')
            elif message.content.startswith('da fuq'):
                await message.add_reaction('<:MoyThink:804062311299940352>')
            elif message.content.startswith('sus'):
                await message.add_reaction('<:MoySus:814973805163446272>')
            elif message.content.startswith('/dog'):
                await message.delete()
                await message.add_reaction('<:MoyThink:804062311299940352>')
            elif message.content == '🤝':
                await message.add_reaction('🤝')
            elif message.content.startswith('/pog'):
                await message.channel.send('indeed, pog <:MoyPog:802214897710530560>')
        except Exception as error:
            await message.channel.send(f'{error.__class__.__name__}: {error}')

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        test = self.client.get_channel(805645055917424671)
        embed = discord.Embed(
            title='Deleted message:',
            color=0x000000
        )
        embed.add_field(
            name=f'Author: {message.author}',
            value=f'Content: {message.content}\nChannel: <#{message.channel.id}>'
        )
        await test.send(embed=embed)

    @commands.Cog.listener()
    async def on_raw_message_edit(self, payload):
        channel = self.client.get_channel(payload.channel_id)
        try:
            message = await channel.fetch_message(payload.message_id)
            await self.client.process_commands(message)
        except Exception as e:
            await channel.send(f'<@762084217185763369>\n```py\n{e.__class__.__name__}: {e}```', allowed_mentions=discord.AllowedMentions.all())

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        """
            Reaction logger
        """
        channel = self.client.get_channel(818260844868796457)
        embed = discord.Embed(color=0x2F3136)
        embed.add_field(name='Emoji: ', value=str(payload.emoji), inline=False)
        embed.add_field(
            name='User: ', value=f'<@{str(payload.user_id)}>', inline=False)
        embed.add_field(name='Channel: ',
                        value=f'<#{str(payload.channel_id)}>', inline=False)

        await channel.send(embed=embed)
        member = payload.member
        guild_member = self.client.get_guild(payload.guild_id)

        if payload.channel_id == 825101719474143293:
            if str(payload.emoji) == '🗿':
                nsfw_role = guild_member.get_role(817510639068643418)
                await member.add_roles(nsfw_role)
            elif str(payload.emoji) == '😎':
                pogo_role = guild_member.get_role(816992672954449921)
                await member.add_roles(pogo_role)
            elif str(payload.emoji) == '🤖':
                bott_role = guild_member.get_role(840371852588220416)
                await member.add_roles(bott_role)
            elif str(payload.emoji) == '⚒️':
                serv_role = guild_member.get_role(836312355029647450)
                await member.add_roles(serv_role)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        """
            Reaction logger
        """
        # member = payload.member
        if payload.channel_id == 825101719474143293:
            guild_member = self.client.get_guild(payload.guild_id)
            member = guild_member.get_member(payload.user_id)
            nsfw_role = guild_member.get_role(817510639068643418)
            pogo_role = guild_member.get_role(816992672954449921)
            if str(payload.emoji) == '🗿':
                await member.remove_roles(nsfw_role)
            elif str(payload.emoji) == '😎':
                await member.remove_roles(pogo_role)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        """
            Standard event, sends a message to
            a specific channel when a member 
            joins any server the bot is in.
        """
        channel = self.client.get_channel(804074100678066245)
        # Bot get guild(server) roles
        r = discord.utils.get(member.guild.roles, name='🗿 Epic')
        embed = discord.Embed(
            title='**A new member just arrived!** :sunglasses:',
            description=f"{member.mention} joined, now we're at {member.guild.member_count} gamers :sunglasses:",
            color=0xff3030
        )
        embed.set_thumbnail(url=f"{member.avatar_url}")
        await channel.send(embed=embed)
        await member.add_roles(r)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        channel = self.client.get_channel(804074100678066245)
        embed = discord.Embed(
            title='member left :pensive:',
            description=f"{member.name} left, now we're at {member.guild.member_count} gamers :pensive:",
            color=0xff3030,
        )
        embed.set_thumbnail(url=f"{member.avatar_url}")
        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        """
            Very basic on_command_error event
            usage
        """
        if isinstance(error, commands.MissingRequiredArgument):
            bruh = str(error.param).split(':')
            await ctx.send(embed=discord.Embed(description=f'Please pass in all arguments. Missing argument: {bruh[0]}', color=0x2f3136))
            return

        elif isinstance(error, commands.CommandNotFound):
            return

        elif isinstance(error, commands.BadArgument):
            await ctx.send(f'You or oxi did something wrong... ||(probably oxi tbh)||\n```py\n{error}\n```')

        elif isinstance(error, commands.CommandOnCooldown):
            self.client.logger.error(f'Cooldown - {error.retry_after}')
            return

        elif isinstance(error, commands.NotOwner):
            await ctx.send('Yo wtf u tryna do :moyai:', delete_after = 7)
            return
        
        elif str(error) == 'Command raised an exception: ValueError: no active connection':
            await ctx.send('aaa uhhhhh cum')
            try:
                await load_db(ctx)
                await self.client.process_commands(ctx.message)
            except Exception as error:
                self.client.logger.error(f'{error.__class__.__name__}: {error}')
            return

        else:
            self.client.logger.error(f'{error.__class__.__name__}: {error}')
            return

    @commands.Cog.listener()
    async def on_command_completion(self, ctx):
        if ctx.prefix == None:
            return
        self.client.logger.info(
            f'{ctx.prefix}{ctx.command} - {ctx.channel.name} / {ctx.channel.id} - {ctx.author} {ctx.author.id}')

    @commands.Cog.listener()
    async def on_slash_command(self, ctx):
        self.client.logger.info(
            f'{ctx.command} - {ctx.channel.name} / {ctx.channel.id} - {ctx.author} {ctx.author.id}')


def setup(client):
    client.add_cog(events(client))
