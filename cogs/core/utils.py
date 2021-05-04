from discord import Embed
from discord.ext import commands

# class helper:
# 
#     # def __init__(self, a):
#     #     self.a = a
class bruh:
    async def pogo_embed_maker(ctx, name, description = None):
        """
            Makes a embed with the specified name
            Takes:
                `ctx`: Standard context object from discord.
                `name`: String, name of the pokemon raid
                `description`: Optional, string, extra info the user may or may not add.
        """
        embed = Embed(title = f'{name} raid', description = f'A new {name} raid appeared! React with an 🗿 to join')
        embed.set_footer(text = 'Bot made exclusively for the Moyai Cult server 🗿😎')
        embed.set_author(ctx.author.display_name, icon_url = ctx.author.avatar_url)
        if description is None:
            embed.add_field(name = 'Extra info:', value = description)
        return embed
    
    async def delete_channel(ctx):
        """
            Deletes a channel.
            Takes: 
                `ctx`: standard context object from discord.
        """
        await ctx.send(embed = discord.Embed(description = '️️⚠️ This channel will be deleted in 5 seconds ⚠️', color = EMBED_BODY_COLOR))
        await asyncio.sleep(5)
        await ctx.channel.delete(reason = 'RAID SYSTEM - DELETE')

# class memba(commands.MemberConverter):
#    async def convert(self, ctx, arg):

