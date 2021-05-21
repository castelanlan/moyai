import random
import asyncio
import discord
from owotext import OwO
from discord.ext import commands


class chatreact(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.counter = 7

    @commands.command(aliases=['uwu'])
    async def owo(self, ctx, *, message: commands.clean_content):
        await ctx.send((OwO().translate(str(message))))

    @commands.command()
    async def poll(self, ctx, *, content):
        embed = discord.Embed(
            title=f'**Poll**', colour=discord.Colour(0x219900))
        author = ctx.message.author
        poolid = random.randint(1, 10000000)
        embed.set_thumbnail(url=f'{author.avatar_url}')
        embed.add_field(
            name=f'Question: {content}', value=f'_Question asked by {ctx.author}_', inline=False)
        embed.set_footer(text=f'Poll sent to {ctx.guild} \n Poll ID: {poolid}')
        message = await ctx.send('New poll!', embed=embed)
        await message.add_reaction('👍')
        await message.add_reaction('👎')

    @commands.command()
    async def egg(self, ctx):
        await ctx.message.add_reaction('🥚')

    @commands.command(aliases=['8ball', '8b'])
    async def eightball(self, ctx, *, question):
        responses = ['Certainly :innocent:', "Probably :grinning:", "Without a doubt :thumbup:", "Yes, definitely :smile:", "You may rely on it :yum:", "As I see it, yes :slight_smile:", "Most likely.", "Outlook good :wink:", "Yes :pinching_hand::sunglasses:", "2/3 correct :woozy_face:", "Reply hazy, try again :shushing_face:",
                     "Ask again later :alarm_clock:", "Better not tell you now :grimacing:", "Can't predict now :pensive:", "Concentrate and ask again XD", "Don't count on it :zipper_mouth:", "My reply is no. :regional_indicator_n::regional_indicator_o:", "My verified sources say no :face_with_monocle:", "Outlook not so good :confused:", "Very doubtful :thinking:"]
        await ctx.send(f'Question: {question}\n Answer: {random.choice(responses)}')

    @commands.command()
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def say(self, ctx, *, text: commands.clean_content):
        message = ctx.message
        await message.delete()
        await ctx.send(f'{text}', allowed_mentions=None)

    @commands.command(hidden = True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def popgr(self, ctx):
        if ctx.author.id != 506436520455176192:
            return
        else:
            gr = random.randint(0, 100)
            await ctx.send(f"You're {gr}% gay! Nice :sunglasses:")

    @commands.command(aliases=['gr', 'grate', 'gayr'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def gayrate(self, abc):
        if abc.author.id == 506436520455176192:
            await abc.send("haha you're 100% gay lmao")
        else:
            gr = random.randint(0, 100)
        await abc.send(f"You're {gr}% gay! Nice :sunglasses:")

    @commands.command(aliases=['f'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def fuck(self, ctx, member: discord.Member):
        embed = discord.Embed(
            title='Fuck',
            description=f'{ctx.author.mention} fucked {member.mention} hard <:MoyFlushedBig:804062311001620531>',
            color=0xd60e00
        )
        embed.set_thumbnail(url=f'{ctx.author.avatar_url}')
        await ctx.send(embed=embed)

    @commands.command(aliases=['k'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def kiss(self, ctx, member: discord.Member):
        embed = discord.Embed(
            title='Kiss',
            description=f'{ctx.author.mention} kissed {member.mention} on the cheek :flushed:',
            color=0xe66e8a
        )
        embed.set_thumbnail(url=f'{ctx.author.avatar_url}')
        await ctx.send(embed=embed)

    @commands.command(aliases=['h'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def hug(self, ctx, member: discord.Member):
        embed = discord.Embed(
            title='Hug',
            description=f'{ctx.author.mention} hugged {member.mention} :people_hugging:',
            color=0x6029cf
        )
        embed.set_thumbnail(url=f'{ctx.author.avatar_url}')
        await ctx.send(embed=embed)

    @commands.command()
    async def sex(self, ctx, member: discord.Member):
        embed = discord.Embed(
            title='Sex',
            description=f'{ctx.author.mention} has sexed {member.mention} <:MoySex:817039347333333062>',
            color=0xe74c3c
        )
        embed.set_thumbnail(url=f'{ctx.author.avatar_url}')
        await ctx.send(embed=embed)

    @commands.command(aliases=['c'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def cum(self, ctx, member: discord.Member):
        embed = discord.Embed(
            title='Cum',
            description=f'{ctx.author.mention} has cummed on {member.mention} :sweat_drops:',
            color=0x6029cf
        )
        embed.set_thumbnail(url=f'{ctx.author.avatar_url}')
        await ctx.send(embed=embed)

    @commands.command()
    async def emojify(self, ctx, emoji, *, message: commands.clean_content):
        transformed_message = message.replace(' ', emoji)
        await ctx.send(str(transformed_message))

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.content.lower().startswith('catjam'):
            await message.delete()
            await message.channel.send('<a:catjam:812348579661742130>')

    @commands.command(hidden = True)
    @commands.has_permissions(administrator=True)
    async def senddm(self, ctx, member: discord.Member, *, content):
        await member.send(f'{content}')
        await ctx.message.delete()
        self.client.logger.info(f'"{content}" has been sent to {member}')

    # @commands.command()
    # @commands.has_permissions(administrator = True)
    # async def godsay(self, ctx, channel : discord.TextChannel = None, *, stuff):
    #     if channel is None:
    #         await ctx.send('Pass a channel duh')
    #     await channel.send(stuff)

    @commands.command(hidden = True)
    @commands.has_permissions(manage_messages=True)
    async def spam(self, ctx, *, message):
        """
            Spams a message
            l
            i
            k
            e
            -
            t
            h
            i
            s
        """
        async with ctx.typing():
            new_message = message.replace(' ', '-')
            for x in new_message:
                await ctx.send(x)
                await asyncio.sleep(0.5)

    @commands.command(aliases=['rb'])
    async def reactionbomb(self, ctx, message: discord.Message = None):
        """
            Reaction bombs a message
        """
        if message is None:
            message = ctx.message
        else:
            await message.add_reaction('<:MoyWoke:802228902411894804>')
            await asyncio.sleep(0.3)
            await message.add_reaction('<a:MoyWobbleIntensifies:802208413555228682>')
            await asyncio.sleep(0.3)
            await message.add_reaction('<a:MoyWobble:802208434085822474>')
            await asyncio.sleep(0.3)
            await message.add_reaction('<:MoyWide:806400142030274581>')
            await asyncio.sleep(0.3)
            await message.add_reaction('<:MoyVibeCheckWoke:802228762694647850>')
            await asyncio.sleep(0.3)
            await message.add_reaction('<:MoyVibeCheck:802228738514747452>')
            await asyncio.sleep(0.3)
            await message.add_reaction('<:MoyTooCool:802228849756078151>')
            await asyncio.sleep(0.3)
            await message.add_reaction('<:MoyThis:807087298218688522>')
            await asyncio.sleep(0.3)
            await message.add_reaction('<:MoyThinkGray:804062890356244480>')
            await asyncio.sleep(0.3)
            await message.add_reaction('<:MoyThink:804062311299940352>')
            await asyncio.sleep(0.3)
            await message.add_reaction('<:MoyStonks:807087297433567283>')
            await asyncio.sleep(0.3)
            await message.add_reaction('<:MoySpy:802215953222991962>')
            await asyncio.sleep(0.3)
            await message.add_reaction('<:MoyULTIMATE:807413869395443762>')
            await asyncio.sleep(0.3)
            await message.add_reaction('<:MoySmirk:804392711922647080>')
            await asyncio.sleep(0.3)
            await message.add_reaction('<:MoySleep:802215820230918154>')
            await asyncio.sleep(0.3)
            await message.add_reaction('<:MoySick:802215779377741825>')
            await asyncio.sleep(0.3)
            await message.add_reaction('<:MoyShy:807087298784264222>')
            await asyncio.sleep(0.3)
            await message.add_reaction('<:MoyShush:802215749346656286>')
            await asyncio.sleep(0.3)
            await message.add_reaction('<:MoySanta:802215724306792458>')
            await asyncio.sleep(0.3)
            await message.add_reaction('<a:MoyRoll:802208448841777152>')
            await asyncio.sleep(0.3)


def setup(client):
    client.add_cog(chatreact(client))
