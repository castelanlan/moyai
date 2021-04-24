import asyncio
import discord
from discord.ext import commands


class boosters(commands.Cog):
    def __init__(self, client):
        self.client = client

#                                                           afearns
#                                                           afearns
#                                                           afearns
#                                                           afearns

    @commands.Cog.listener()
    async def on_message(self, message):
        """
            Checks if 'cum' is in the message
            content and if the message
            author is afearns
        """
        apple = self.client.get_user(562315807099584533)
        # olerius = self.client.get_user(518228495235547148)
        #afearns = self.client.get_user(632838862145585153)
        if 'cum' in message.content.lower() and message.author.id == 632838862145585153:
            await message.channel.send('Make me wet daddy🥵')
        if apple in message.mentions:
            await message.channel.send('Apple is watching hardcore hentai right now...')
        # elif afearns in message.mentions:
        #    await message.channel.send('Afearns is masturbating right now')
        # if 'sex' in message.content.lower() and message.author.id == 518228495235547148: # olerius
        #     await message.channel.send('Harder daddy')
        # if olerius in message.mentions:
        #     await message.channel.send('Olerius says: fuck off')

#                                                           olerius
#                                                           olerius
#                                                           olerius
#                                                           olerius

#                                                    pretty empty here eh

#                                                           tbjosh
#                                                           tbjosh
#                                                           tbjosh
#                                                           tbjosh

    @commands.command()
    async def josh(self, ctx, *, c: commands.clean_content = None):
        await ctx.send(f'<@290191358516527104>, {c}', allowed_mentions=discord.AllowedMentions(users=True))
        await asyncio.sleep(0.5)
        await ctx.send(f'<@290191358516527104>, {c}', allowed_mentions=discord.AllowedMentions(users=True))
        await asyncio.sleep(0.5)
        await ctx.send(f'<@290191358516527104>, {c}', allowed_mentions=discord.AllowedMentions(users=True))
        await asyncio.sleep(0.5)
        await ctx.send(f'<@290191358516527104>, {c}', allowed_mentions=discord.AllowedMentions(users=True))
        await asyncio.sleep(0.5)
        await ctx.send(f'<@290191358516527104>, {c}', allowed_mentions=discord.AllowedMentions(users=True))

    @commands.command()
    async def cimm(self, ctx):
        await ctx.message.delete()
        if ctx.author.id != 608727414725410816:
            return
        else:
            embed = discord.Embed(
                description=f'{ctx.author.mention} has cummed on oxi\'s mouth!\nThank you Josh!', color=0xe66e8a)
            embed.set_thumbnail(url=f'{ctx.author.avatar_url}')
            await ctx.send(embed=embed)


def setup(client):
    client.add_cog(boosters(client))
