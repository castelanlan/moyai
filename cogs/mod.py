import discord
from discord.ext import commands
import asyncio

class mod(commands.Cog):
    def __init__(self, client):
        self.client = client

#     async def parse_time(self, ctx, time):
#         amount_to_sleep = time.split('|')
#     
#         if 'min' or 'm' or 'minutes' in amount_to_sleep[1]:
#             amount_to_sleep = amount_to_sleep * 60
#             return amount_to_sleep
# 
#         elif 'seconds' or 'secs' or 'sec' or 's' in amount_to_sleep[1]:
#             return amount_to_sleep
# 
#             return amount_to_sleep

    @commands.command(aliases=['purge'])
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount: int):
        await ctx.channel.purge(limit=amount + 1)
        await ctx.send(f'{amount} messages deleted <a:MoyaiPet:802208522892738632>', delete_after=7)
        # await donecommandschannel.send(f'Command clear done ({amount})')

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def mute(self, ctx, member: discord.Member, time = None):
        role = ctx.guild.get_role(804465223335411722)

        if time is None:
            await member.add_roles(role, atomic=True)
            await ctx.send(f'Member {member.mention} has been muted :pensive:')
        else:
            try:
                await member.add_roles(role, atomic = True)
                await ctx.send(f'Member {member.mention} has been muted :pensive:')
                await asyncio.sleep(int(time) * 60)
                await member.remove_roles(role, atomic = True)
                await ctx.send(f'Member {member.mention} has been unmuted :sunglasses:')

            except ValueError:
                await ctx.send('That\'s not a number chief :moyai:', delete_after = 5)                

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def unmute(self, ctx, member: discord.Member):
        role = ctx.guild.get_role(804465223335411722)
        await member.remove_roles(role, atomic=True)
        await ctx.send(f'Member {member.mention} has been unmuted :sunglasses:')

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def warn(self, ctx, member: discord.Member, *, reason=None):
        warnchannel = self.client.get_channel(804046832370974734)
        embed = discord.Embed(title=f'New warn - {member}', color=0xff0000)
        embed.add_field(
            name='testing', value=f'Member {member} has been warned for: {reason} ')
        await ctx.send(f'{member} warned :flushed:')
        await warnchannel.send(embed=embed)

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        await member.kick(reason=reason)
        await ctx.send(f'Member {member} kicked for reason: {reason}')

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        await member.ban(reason=reason)
        await ctx.send(f'User {member} has been banned for reason: {reason}')

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, *, member_id):
        try:
            member = discord.Object(id=member_id)
            await ctx.send(f'User with ID: `{member_id}` has been unbanned.')
        except Exception as error:
            await ctx.send(embed=discord.Embed(description=f'This command failed.\n\n{error}', color=0x2F3136), delete_after=10)

    @commands.command()
    async def apply(self, ctx, *, message='No text provided'):
        # channel = self.client.get_channel(818617863677411389)
        await ctx.message.delete()
        await ctx.send('Applications are closed :pensive:')
        # embed = discord.Embed(title = f'Application by {ctx.author.name}', description = message)
        # embed.set_thumbnail(url = ctx.author.avatar_url)
        # embed.set_footer(text = f'{ctx.author} || {ctx.author.id}')
        # await channel.send('New application!', embed = embed)
        # await ctx.author.send('Your application has been sent!')


def setup(client):
    client.add_cog(mod(client))
