import random
import discord
import aiosqlite
import asyncio

from discord.ext import commands

db = aiosqlite.connect('ne.sql')
cursor = db.cursor()


class ne(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.START_BAL = 200

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.content.startswith(';;;') and message.author.id == 762084217185763369:
            ...

    async def errored(self, ctx, e):
        """
            laziness.png
            Takes:
                `ctx`: standart context object
                `e`: exception
        """
        await ctx.send(f'An error happened...\n```py\n{e.__class__.__name__}: {e}\n```')
        raise e

    async def load_db(self, ctx):
        """
            Tries to load the db.
            Takes:
                `ctx`: standard context object
        """
        try:
            await db
            await cursor
            await ctx.send('Connected to database')
        except Exception as e:
            await errored(ctx, e)

    async def close_db(self, ctx):
        """
            Tries to close the db.
            Takes:
                `ctx`: standard context object
        """
        try:
            cursor.close()
            db.close()
            await ctx.send('Closed database')
            print('Closed database')
        except Exception as error:
            await errored(ctx, e)

    async def check_moneys(self, ctx, user=None):
        """
            Checks if the user is in the db, and
            if the user isn't, adds them to it.
            Takes:
                `ctx`: Standard context object
                [optional]`user`: The user to be checked
        """
        try:
            cursor = await db.execute(f"SELECT user_id FROM main WHERE user_id={ctx.message.author.id}")
            result_ID = await cursor.fetchone()

        except Exception as e:
            try:
                await load_db()
            except Exception as e:
                await errored(ctx)
                return

        if result_ID == None:
            await cursor.execute(f'INSERT INTO main(user_name, balance, user_id) values({ctx.message.author.name}, 200, {str(ctx.author.id)})')
            await db.commit()
            await ctx.send("""**Hi, I see you're new...** :thinking:\nWelcome to Moyai Bot:moyai:, here your objective is to get as much Moyai stones as possible! Do `.help economy` to see all available commands""")
            return

    async def add_to_bal(self, ctx, amount: int, user=None):
        """
            Adds money to a user balance
            Takes:
                `ctx`: Standard context object
                `amount`[int]: Amount to be added to the user's account
                `user`[optional]: 
        """
        try:
            if user is None:
                user = ctx.message.author

            await cursor.execute(f'UPDATE main SET balance = balance + {amount} WHERE user_id ={user.id}')

        except Exception as e:
            try:
                await load_db()
                await add_to_bal(ctx, amount, user)
            except Exception as e:
                await errored(ctx)
                return

    # def check_connection(self, ctx):
    #     try:
    #         asyncio.run(self.load_db())
    #         return True
    #     except Exception as error:
    #         print(error)
    #         return False
    #     # return commands.check(predicate)

    def check_connection(self):
        async def predicate(ctx):
            try:
                print(bool(await load_db()))
            except Exception as error:
                raise error
        return commands.check(predicate)

    @commands.command()
    @commands.check(check_connection)
    async def abc(self, ctx, *, a):
        await ctx.send(a)

    @commands.command(aliases=['_ldb'])
    @commands.is_owner()
    async def __ldb(self, ctx):
        await load_db(ctx)

    @commands.command(aliases=['_cdb'])
    @commands.is_owner()
    async def __cdb(self, ctx):
        await close_db()

    @commands.command(
        #        aliases=['bal'],
        #        brief='Shows how many Moyai Stones you have.',
        #        description="Will show you how many Moyai Stones you have, if you want to see someone else's stones, you can do .balof <person>"
    )
    async def _balance(self, ctx):
        await check_moneys(ctx.author)
        await cursor.execute(f'SELECT balance FROM main WHERE user_id={USER_ID}')
        result_userBal = await cursor.fetchone()
        embed = discord.Embed(
            description=f'{USER_NAME} has **{result_userBal[0]}** moyai stones :moyai::sunglasses:', color=0xf8c40c)
        embed.set_author(name=ctx.author.name,
                         icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    @commands.command(
        #        aliases=['balof', 'ballsof'],
        #        brief='Shows how many Moyai Stones a user has.',
        #        description='Will show how many Moyai Stones a user has, if you want to see your stones, you can do .bal'
    )
    async def _balanceof(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author
        else:
            cursor = await db.execute(f'SELECT balance FROM main WHERE user_id={member.id}')
            balance = await cursor.fetchone()
            if balance is None:
                embed = discord.Embed(
                    description=f"This member hasn't started his journey yet!", color=0xf8c40c)
            else:
                embed = discord.Embed(
                    description=f'{member.name} has **{balance[0]}** moyai stones :moyai::sunglasses:', color=0xf8c40c)
            embed.set_author(name=member.name, icon_url=member.avatar_url)
            await ctx.send(embed=embed)

    @commands.command(
        #        aliases=['g'],
        #        name='give',
        #        brief='A command to give other people Stones',
        #        description='Anyone that has started their Moyai journey is eligible to receiving Moyai Stones'
    )
    async def _give(self, ctx, user: discord.Member = None, amount: int = None):
        cursor = await db.execute(f'SELECT balance FROM main WHERE user_id = {ctx.author.id}')
        dinheiro_doador = await cursor.fetchone()

        cursor = await db.execute(f'SELECT balance FROM main WHERE user_id = {user.id}')
        membro = await cursor.fetchone()

        if user is None:
            await ctx.send('You have to specify a user!')
            return
        elif membro is None:
            await ctx.send('This member hasn\'t started their journey yet!')
            return
        elif user is ctx.author:
            await ctx.send('Donating to yourself moment :moyai:')
            return
        elif amount is None:
            await ctx.send('You have to specify an amount!')
            return
        elif amount == 0:
            await ctx.send('Donation of 0 Stones moment :moyai:')
            return
        elif amount < 0:
            await ctx.send('Why are you even trying that 🧐')
            return
        elif int(dinheiro_doador[0]) < amount:
            await ctx.send("You don't have enough stones to donate that amount :pensive:")
            return
        elif dinheiro_doador is None:
            await ctx.send('You have\'t started your career yet!')
            return
        else:
            await cursor.execute('UPDATE main SET balance = balance + ? WHERE user_id = ?', (amount, user.id))
            await cursor.execute('UPDATE main SET balance = balance - ? WHERE user_id = ?', (amount, ctx.author.id))
            await db.commit()
            await ctx.send(embed=discord.Embed(title='Donation',
                                               description=f'{ctx.author.display_name} has donated {amount} to {user.display_name}',
                                               color=0x8c34eb
                                               ))

    @commands.command(
        #aliases=['lb', 'rank', 'top'],
        #    name='Leaderboard',
        #    brief='People with the most Moyai Stones 🗿',
        #    description='Shows the top 10 users with the most Moyai Stones 🗿'
    )
    async def _leaderboard(self, ctx):
        cursor = await db.execute(f'SELECT balance FROM main ORDER BY balance DESC')
        balances = await cursor.fetchall()
        cursor = await db.execute(f'SELECT user_id FROM main ORDER BY balance DESC')
        names = await cursor.fetchall()
        # EMBED
        embed = discord.Embed(
            title='Moyai Leaderboard 🗿🙏',
            description='\n',
            color=0x29cc54
        )
        for x in range(0, 10):
            bruh = ctx.guild.get_member(names[x][0]).display_name
            embed.add_field(
                name=f'#{x + 1} {bruh}', value=f'{balances[x][0]} stones 🗿', inline=False)
        await ctx.send(embed=embed)

    @commands.command(
        #aliases=['antilb', 'alb', 'antileaderboard'],
        # name='Anti-leaderboard',
        #brief='Leaderboard command but inverse! 😭🗿',
        #description='Shows the top 10 users with the LESS Moyai Stones 🗿'
    )
    async def _antileaderboard(self, ctx):
        cursor = await db.execute(f'SELECT balance FROM main ORDER BY balance ASC')
        balances = await cursor.fetchall()
        cursor = await db.execute(f'SELECT user_name FROM main ORDER BY balance ASC')
        names = await cursor.fetchall()
        # EMBED
        embed = discord.Embed(
            title='Anti Leaderboard 🗿🙏',
            description='\n',
            color=0x29cc54
        )
        for x in range(0, 10):
            embed.add_field(
                name=f'#{x + 1} {names[x][0]}', value=f'{balances[x][0]} stones 🗿', inline=False)
        await ctx.send(embed=embed)

    @commands.command(aliases=['_agive'], hidden=True)
    @commands.is_owner()
    async def _admin_give(self, ctx, user: discord.Member, amount: int):
        cursor = await db.execute(f'UPDATE main SET balance = balance + {amount} WHERE user_id={user.id}')
        await db.commit()
        await ctx.send(f"Added {amount} stones to {user.display_name}'s name.")

#     @_bet.error
#     async def bet_error(self, ctx, error):
#         if isinstance(error, commands.CommandOnCooldown):
#             await ctx.send(f'You can\'t bet now, you may do so in {round(error.retry_after)} seconds')
#         else:
#             await ctx.send('<@762084217185763369>', allowed_mentions=discord.AllowedMentions.all())
#
#     @_scout.error
#     async def scout_error(self, ctx, error):
#         if isinstance(error, commands.CommandOnCooldown):
#             await ctx.send(f"You're on cooldown, you may scout again in {round(error.retry_after)} seconds.")
#
#     @_pray.error
#     async def pray_error(self, ctx, error):
#         if isinstance(error, commands.CommandOnCooldown):
#             cd = round(error.retry_after / 60)
#             embed = discord.Embed(
#                 description=f"A good moyai is patient, you can pray again in {cd} minutes.", color=0x2F3136)
#             if cd == 1:
#                 embed = discord.Embed(
#                     description=f"A good moyai is patient, you can pray again in {cd} minute.", color=0x2F3136)
#             await ctx.send(embed=embed)
#         else:
#             raise error
#
#     @_daily.error
#     async def daily_error(self, ctx, error):
#         if isinstance(error, commands.CommandOnCooldown):
#             cd = round(error.retry_after / 3600, 1)
#             embed = discord.Embed(
#                 description=f"The church is closed! It should be open for you in **{cd}** hours", color=0x2F3136)
#             if cd == 1:
#                 embed = discord.Embed(
#                     description=f"The church is closed! It should be open for you in **{cd}** hour", color=0x2F3136)
#             await ctx.send(embed=embed)
#         else:
#             raise error


def setup(client):
    client.add_cog(ne(client))
