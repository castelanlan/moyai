import ast
import discord
import inspect
import time
from dis import dis
from inspect import getsource
from discord.ext import commands
from pygicord import Paginator


class Admin(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.game = discord.Activity(
            type=discord.ActivityType.watching, name="my cute lil moyai's")


    async def insert_returns(self, body):
        """ 
            insert return statement if
            the last expression is an 
            expression statement
        """
        if isinstance(body[-1], ast.Expr):
            body[-1] = ast.Return(body[-1].value)
            ast.fix_missing_locations(body[-1])

        """
            Same thing as above, but for if statements,
            we insert returns into the body and the orelse.
        """
        if isinstance(body[-1], ast.If):
            self.insert_returns(body[-1].body)
            self.insert_returns(body[-1].orelse)

        """
            Inserting returns if we use `with ...`.
        """
        if isinstance(body[-1], ast.With):
            self.insert_returns(body[-1].body)

    async def get_pages(self, inputt, result : str, time) -> list or str:
        pages = []
        NUMERO = 1200
        l = len(str(result))
        base = discord.Embed(description = f'Ran in {round(time, 2)} seconds', color = 0x000000).add_field(name = 'Input', value = f'```py\n{inputt}\n```', inline = False)

        try:
            if l > NUMERO:

                res = []

                for i in range(0, l, NUMERO):
                    res.append(result[i : i + NUMERO])

                x = 0
                for i in range(len(res)):

                    if x != 0:
                        page_embed = base.copy()
                        page_embed.add_field(name = 'Return', value = f'```py\n{res[i]}\n```', inline = False)
                        print(f'bruh: {len(page_embed._fields)}')
                        pages.append(page_embed)
                        del page_embed

                    x += 1

                print(f'A: {len(pages)}')    
                return pages

            else:
                return [(base.add_field(name = 'Return', value = f'```py\n{result}\n```', inline = False))]
        except Exception as e:
            raise e

    async def cu(self, ctx, cmd):
        """
            Eval command, really good
            and useful for testing, 
            You got to be really careful tho.
        """
        await ctx.trigger_typing()
        before = time.time()

        try:
            cmd_1 = cmd
            fn_name = "_eval_expr"
            cmd = cmd.strip("```' ")
            cmd = "\n".join(f"    {i}" for i in cmd.splitlines())
            body = f"async def {fn_name}():\n{cmd}"
            parsed = ast.parse(body)
            body = parsed.body[0].body
            await self.insert_returns(body)

            env = {
                'cmd': cmd,
                'dis': dis,
                'ctx': ctx,
                'sex': 'sex',
                'body': body,
                'src': getsource,
                'discord': discord,
                'commands': commands,
                'client': self.client,
                '__import__': __import__
            }

            exec(compile(parsed, filename="<ast>", mode="exec"), env)

            result = await eval(f"{fn_name}()", env)

            # if len(str(result)) > 1980:
            #     file = BytesIO(str(result).encode())
            #     await ctx.send(file=discord.File(file, 'result.py'))
            #     return

            after = time.time()
            delta = after - before
            pages = await self.get_pages(cmd_1, result, delta)
            pag = Paginator(pages = pages)
            await pag.start(ctx)
            print('sucesso')

        except Exception as e:
            # if str(e) == '400 Bad Request (error code: 50006): Cannot send an empty message':
            #     raise e
            # 
            # else:
            await ctx.send(f'\n```py\n{e.__class__.__name__}: {e}\n```')

    @commands.command(hidden=True, name = 'eval', aliases=['e'])
    @commands.is_owner()
    async def _eval(self, ctx, *, cmd):
        await self.cu(ctx, cmd)

    @commands.group(invoke_without_command=True, hidden = True)
    @commands.is_owner()
    async def status(self, ctx):
        await ctx.send('I have to set my status to something dum dum :rage:')

    @status.command(hidden = True)
    @commands.is_owner()
    async def idle(self, ctx):
        await self.client.change_presence(status=discord.Status.Idle, activity=self.game)
        await ctx.send("Changed status to idle", delete_after=5)

    @status.command(hidden = True)
    @commands.is_owner()
    async def dnd(self, ctx):
        await self.client.change_presence(status=discord.Status.dnd, activity=self.game)
        await ctx.send("Changed status to do not disturb", delete_after=5)

    @status.command(hidden = True)
    @commands.is_owner()
    async def online(self, ctx):
        await self.client.change_presence(status=discord.Status.online, activity=self.game)
        await ctx.send("Changed status to online", delete_after=5)

    @status.command(hidden = True)
    @commands.is_owner()
    async def offline(self, ctx):
        await self.client.change_presence(status=discord.Status.invisible)
        await ctx.send("Changed status to invisible", delete_after=5)

    @commands.command(hidden = True)
    @commands.is_owner()
    async def close(self, ctx):
        await ctx.send('Are you sure :moyai:')
        message = await self.client.wait_for('message', check=lambda m: m.author == ctx.author, timeout=10)
        if message.content == 'y':
            await self.client.close()
        else:
            await ctx.send('Aborted', delete_after=5)


def setup(client):
    client.add_cog(Admin(client))
