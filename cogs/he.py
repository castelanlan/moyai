from discord.ext import commands
from pygicord import Paginator
from bot import get_prefix
import discord

class Help(commands.Cog):
    def __init__(self, client):
        self.client = client

    #async def bed(self, ctx, stuff):
    #    base = (Embed(description = stuff, color = ctx.me.color)
    #            .set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
    #            .set_footer(text = 'Thank you for using Moyai Bot! 😎🙏', icon_url = 'https://cdn.discordapp.com/app-icons/815562681267650589/7a0867519705776b1f874f1a05e76f0a.webp?size=1024')
    #    )
    #    return base

    @commands.command(name = 'help')
    @commands.is_owner()
    async def _help(self, ctx):
        _embed = (discord.Embed(description=f"My prefix is `{get_prefix(self.client, ctx.message)[0]}` 😎🙏", color = ctx.me.color)
                    .set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
                    .set_footer(text = 'Thank you for using Moyai Bot! 😎🙏', icon_url = 'https://cdn.discordapp.com/app-icons/815562681267650589/7a0867519705776b1f874f1a05e76f0a.webp?size=1024')
        )

        for cog_name, cog in self.client.cogs.items():
            if len(cog.get_commands()):
                _embed.add_field(
                    name=cog_name.capitalize(),
                    value='  •  '.join(sorted(f'{c.name}' for c in cog.get_commands() if not c.hidden)),
                    inline=False
                )

        await ctx.send(embed=_embed)



def setup(client):
    client.add_cog(Help(client))
