from discord.ext import commands
from pygicord import Paginator
from bot import get_prefix
import discord

class Help(commands.Cog):
    def __init__(self, client):
        self.client = client

    async def do_normal_help(self, ctx):
        try:
            _embed = (discord.Embed(description=f"My prefix for you is `{get_prefix(self.client, ctx.message)[0]}` 😎🙏", color = ctx.me.color)
                        .set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
                        .set_footer(text = 'Thank you for using Moyai Bot! 😎🙏', icon_url = 'https://cdn.discordapp.com/app-icons/815562681267650589/7a0867519705776b1f874f1a05e76f0a.webp?size=1024')
            )

            for cog_name, cog in self.client.cogs.items():
                if len(cog.get_commands()):

                    a = []
                    for c in cog.get_commands():
                        if not c.hidden:
                            a.append(c.name)
                        else:
                            pass

                    try:
                        if a[0]:                    
                            value = ', '.join(a)

                        _embed.add_field(
                            name=cog_name.capitalize(),
                            value= value,
                            inline=False
                        )

                    except IndexError as error:
                        continue


            await ctx.send(embed=_embed)
        except Exception as error:
            raise error

    @commands.command(name = 'help', invoke_without_command = True)
    async def _help2(self, ctx, helpme = None):
        if helpme is None:
            await self.do_normal_help(ctx)
        else:
            ...

def setup(client):
    client.add_cog(Help(client))
