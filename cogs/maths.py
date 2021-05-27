import discord
from discord.ext import commands

class maths(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.command()
    async def add(self, ctx, a: int, b: int):
        try:
            await ctx.send(a + b)
        except Exception as e:
            await ctx.send(f"```py\n{e.__class__.__name__}: {e}```")
    @commands.command()
    async def subtract(self, ctx, a: int, b: int):
        try:
            await ctx.send(a - b)
        except Exception as e:
            await ctx.send(f"```py\n{e.__class__.__name__}: {e}```")

    @commands.command()
    async def multiply(self, ctx, a: int, b: int):
        try:
            await ctx.send(a * b)
        except Exception as e:
            await ctx.send(f"```py\n{e.__class__.__name__}: {e}```")
 
    @commands.command()
    async def divide(self, ctx, a: int, b: int):
        try:
            await ctx.send(a / b)
        except Exception as e:
            await ctx.send(f"```py\n{e.__class__.__name__}: {e}```")
 
def setup(client):
    client.add_cog(maths(client))