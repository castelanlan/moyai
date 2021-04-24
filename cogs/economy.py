import random
import discord
import aiosqlite

from discord.ext import commands

db = aiosqlite.connect('economy.sql')
cursor = db.cursor()


class economy(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.START_BAL = 200

    async def get_stones(self, ctx, user) -> int:
        """
            Gets the specified user's amount of stones

            -------

            Only meant to be used when a connection is present.
        """
        cursor = await db.execute(f"SELECT user_id FROM main WHERE user_id={user.id}")
        user_stones = await cursor.fetchone()
        return user_stones

    async def get_win_chance(self, ctx, amount):
        Ellipsis

    async def get_user_name_from_id(self, ctx, user_id) -> str:
        user = await self.client.get_user(user_id)
        return user.name

    @commands.command(aliases=['ldb'])
    @commands.is_owner()
    async def load_db(self, ctx):
        try:
            await db
            await cursor
            await ctx.send('Connected to database')
        except Exception as error:
            await ctx.send(f'Error:\n```py\n{error.__class__.__name__}: {error}```')
            raise error

    @commands.command(aliases=['cdb'])
    @commands.is_owner()
    async def close_db(self, ctx):
        try:
            cursor.close()
            db.close()
            print(db)
            print(cursor)
            await ctx.send('Closed database')
            print('Closed database')
        except Exception as error:
            await ctx.send(f'Error:\n```py\n{error.__class__.__name__}: {error}```')
            raise error

    @commands.command(
        aliases=['bal'],
        brief='Shows how many Moyai Stones you have.',
        description="Will show you how many Moyai Stones you have, if you want to see someone else's stones, you can do .balof <person>"
    )
    async def Balance(self, ctx):
        USER_ID = ctx.message.author.id
        USER_NAME = str(ctx.message.author)

        cursor = await db.execute(f"SELECT user_id FROM main WHERE user_id={USER_ID}")
        result_ID = await cursor.fetchone()

        if result_ID == None:
            await cursor.execute('INSERT INTO main(user_name, balance, user_id) values(?, ?, ?)', (USER_NAME, self.START_BAL, USER_ID))
            await db.commit()
            await ctx.send("""**Hi, I see you're new...** :thinking: \n Welcome to Moyai Bot:moyai:, here your objective is to get as much Moyai stones as possible, you can do so by sending `.pray`, `.daily`, or `.scout`!""")
        else:
            await cursor.execute(f'SELECT balance FROM main WHERE user_id={USER_ID}')
            result_userBal = await cursor.fetchone()
            embed = discord.Embed(
                description=f'{USER_NAME} has **{result_userBal[0]}** moyai stones :moyai::sunglasses:', color=0xf8c40c)
            embed.set_author(name=ctx.author.name,
                             icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)

    @commands.command(
        aliases=['balof', 'ballsof'],
        brief='Shows how many Moyai Stones a user has.',
        description='Will show how many Moyai Stones a user has, if you want to see your stones, you can do .bal'
    )
    async def Balanceof(self, ctx, member: discord.Member = None):
        try:
            await d
        except:
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
        aliases=['p'],
        brief='Pray🙏 to Moyai🗿',
        description='The pray command, has a one hour cooldown, and gives you 50-130 Moyai Stones🗿'
    )
    @commands.cooldown(1, 3600, commands.BucketType.user)
    async def Pray(self, ctx):
        USER_ID = ctx.message.author.id
        USER_NAME = str(ctx.message.author)

        cursor = await db.execute(f"SELECT user_id FROM main WHERE user_id={USER_ID}")
        result_userID = await cursor.fetchone()

        if result_userID is None:
            await cursor.execute('INSERT INTO main(user_name, balance, user_id) values(?, ?, ?)', (USER_NAME, self.START_BAL, USER_ID))
            await db.commit()
            await ctx.send("""**Hi, I see you're new...** :thinking: \nWelcome to Moyai Bot:moyai:, here your objective is to get as much Moyai stones as possible, you can do so by sending `.pray` and/or `.daily`! \n⚠️Warning: You can only pray every 1 hour, but, considering you're new, I gave you 200 Moyai Stones :wink:""")
        else:
            addup = random.randint(50, 130)
            await cursor.execute('UPDATE main SET balance = balance + ? WHERE user_id=?', (addup, USER_ID))
            await db.commit()
            embed = discord.Embed(
                description=f'You prayed and found **{addup}**:moyai::pray:', color=0xf8c40c)
            embed.set_author(name=ctx.author.name,
                             icon_url=ctx.author.avatar_url)
            # await ctx.send(f'You prayed and found **{addup}**:moyai::pray:')
            await ctx.send(embed=embed)

    @commands.command(
        aliases=['d'],
        brief='The daily prayers command🗿🙏',
        description='The daily command, you can do it every 24 hours, and gives you 200-500 Moyai Stones🗿'
    )
    @commands.cooldown(1, 86400, commands.BucketType.user)
    async def Daily(self, ctx):
        USER_ID = ctx.message.author.id
        USER_NAME = str(ctx.message.author)

        cursor = await db.execute(f"SELECT user_id FROM main WHERE user_id={USER_ID}")
        result_user_id = await cursor.fetchone()

        if result_user_id is None:
            await cursor.execute('INSERT INTO main(user_name, balance, user_id) values(?, ?, ?)', (USER_NAME, self.START_BAL, USER_ID))
            await db.commit()
            await ctx.send("""**Hi, I see you're new...** :thinking: \nWelcome to Moyai Bot:moyai:, here your objective is to get as much Moyai stones as possible, you can do so by sending `.pray` and/or `.daily`! \n⚠️Warning: You can only do `.daily` every 24 hours, but, considering you're new, I gave you 200 Moyai Stones :wink:""")
        else:
            addup = random.randint(200, 500)
            await cursor.execute('UPDATE main SET balance = balance + ? WHERE user_id=?', (addup, USER_ID))
            await db.commit()
            embed = discord.Embed(
                description=f'You went to the Moyai Church and found **{addup}** Moyai stones:moyai::pray:', color=0xf8c40c)
            embed.set_author(name=ctx.author.name,
                             icon_url=ctx.author.avatar_url)
            # await ctx.send(f'You went to the Moyai Church and found **{addup}** Moyai stones:moyai::pray:')
            await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 100, commands.BucketType.user)
    async def bet(self, ctx, amount: int):
        cursor = await db.execute(f'SELECT balance FROM main where user_id = {ctx.author.id}')
        user_money = await cursor.fetchone()

        if user_money is None:
            await ctx.send("You can't do this command! You haven't started your journey!")
        if amount >= int(user_money[0]):
            await ctx.send(embed=discord.Embed(description='You don\'t have all that money <:MoyPensive:806407627721932810>', color=0x2F3136))
            return
        else:
            number = random.randint(0, 100)
            if number > 55:
                await cursor.execute(f'UPDATE main SET balance = balance + {round(amount * 2)} WHERE user_id = {ctx.author.id}')
                await db.commit()
                await ctx.send(embed=discord.Embed(description=f'You bet {amount} stones, and got back {round(amount * 2)}. Now you have {user_money[0] + round(amount * 1.5)} stones <:MoyPepeAndMoyai:808347852513476619> ', color=discord.Color.green()))
            else:
                await cursor.execute(f'UPDATE main SET balance = balance - {round(amount)} WHERE user_id = {ctx.author.id}')
                await db.commit()
                await ctx.send(embed=discord.Embed(description=f'You bet {amount} stones, and lost all of them <:MoyPensive:806407627721932810> Now you have {user_money[0] - amount}', color=discord.Color.red()))

    @commands.command(
        aliases=['s'],
        brief='Scout command🏃‍♂️',
        description='The scout command, you can do it every 10 seconds, and gives you 2-10 Moyai Stones🗿'
    )
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def Scout(self, ctx):
        USER_ID = ctx.message.author.id
        USER_NAME = str(ctx.message.author)

        cursor = await db.execute(f"SELECT user_id FROM main WHERE user_id={USER_ID}")
        result_userID = await cursor.fetchone()

        if result_userID is None:
            await cursor.execute('INSERT INTO main(user_name, balance, user_id) values(?, ?, ?)', (USER_NAME, self.START_BAL, USER_ID))
            await db.commit()
            await ctx.send("""**Hi, I see you're new...** :thinking: \nWelcome to Moyai Bot:moyai:, here your objective is to get as much Moyai stones as possible, you can do so by sending `.pray` and/or `.daily`! \n⚠️Warning: You can only do `.daily` every 24 hours, but, considering you're new, I gave you 200 Moyai Stones :wink:""")
        else:
            amount_get_after = random.randint(2, 10)
            await cursor.execute('UPDATE main SET balance = balance + ? WHERE user_id = ?', (amount_get_after, USER_ID))
            await db.commit()
            embed = discord.Embed(
                description=f'You scouted around, and found **{amount_get_after}** Moyai stones!', color=0xf8c40c)
            embed.set_author(name=ctx.author.name,
                             icon_url=ctx.author.avatar_url)
            # await ctx.send(f'You scouted around, and found **{amount_get_after}** Moyai stones!')
            await ctx.send(embed=embed)

    @commands.command(
        aliases=['g'],
        name='give',
        brief='A command to give other people Stones',
        description='Anyone that has started their Moyai journey is eligible to receiving Moyai Stones'
    )
    async def give(self, ctx, user: discord.Member = None, amount: int = None):
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

    @commands.command(aliases=['lb', 'rank', 'top'], name='Leaderboard', brief='People with the most Moyai Stones 🗿', description='Shows the top 10 users with the most Moyai Stones 🗿')
    async def leaderboard(self, ctx):
        cursor = await db.execute(f'SELECT balance FROM main ORDER BY balance DESC')
        balances = await cursor.fetchall()
        cursor = await db.execute(f'SELECT user_id FROM main ORDER BY balance DESC')
        names = await cursor.fetchall()
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

    @commands.command(aliases=['antilb', 'alb', 'antileaderboard'], name='Anti-leaderboard', brief='Leaderboard command but inverse! 😭🗿', description='Shows the top 10 users with the LESS Moyai Stones 🗿')
    async def antileaderboard(self, ctx):
        cursor = await db.execute(f'SELECT balance FROM main ORDER BY balance ASC')
        balances = await cursor.fetchall()
        cursor = await db.execute(f'SELECT user_id FROM main ORDER BY balance ASC')
        names = await cursor.fetchall()
        embed = discord.Embed(
            title='Anti Leaderboard 🗿🙏',
            description='\n',
            color=0x29cc54
        )
        for x in range(0, 10):
            try:
                bruh = ctx.guild.get_member(names[x][0]).display_name
            except:
                bruh = '`This user left 😔`'
            print(bruh)
            embed.add_field(
                name=f'#{x + 1} {bruh}', value=f'{balances[x][0]} stones 🗿', inline=False)
        await ctx.send(embed=embed)

    @commands.command(aliases=['agive'], hidden=True)
    @commands.is_owner()
    async def admin_give(self, ctx, user: discord.Member, amount: int):
        cursor = await db.execute(f'UPDATE main SET balance = balance + {amount} WHERE user_id={user.id}')
        await db.commit()
        await ctx.send(f"Added {amount} stones to {user.display_name}'s name.")

    @commands.command(hidden=True)
    @commands.is_owner()
    async def update(self, ctx, user: discord.Member = None):
        if user is None:
            return
        else:
            await cursor.execute(f'UPDATE main SET user_name = {user.name} WHERE user_id = {user.id}')

    @bet.error
    async def bet_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f'You can\'t bet now, you may do so in {round(error.retry_after)} seconds')
        else:
            await ctx.send('<@762084217185763369>', allowed_mentions=discord.AllowedMentions.all())

    @Scout.error
    async def scout_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f"You're on cooldown, you may scout again in {round(error.retry_after)} seconds.")

    @Pray.error
    async def pray_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            cd = round(error.retry_after / 60)
            embed = discord.Embed(
                description=f"A good moyai is patient, you can pray again in {cd} minutes.", color=0x2F3136)
            if cd == 1:
                embed = discord.Embed(
                    description=f"A good moyai is patient, you can pray again in {cd} minute.", color=0x2F3136)
            await ctx.send(embed=embed)
        else:
            raise error

    @Daily.error
    async def daily_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            cd = round(error.retry_after / 3600, 1)
            embed = discord.Embed(
                description=f"The church is closed! It should be open for you in **{cd}** hours", color=0x2F3136)
            if cd == 1:
                embed = discord.Embed(
                    description=f"The church is closed! It should be open for you in **{cd}** hour", color=0x2F3136)
            await ctx.send(embed=embed)
        else:
            raise error


def setup(client):
    client.add_cog(economy(client))
