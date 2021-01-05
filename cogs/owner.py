"""
위 모듈은 개발자 뭉개구름이 제작하였으며 무단으로 사용할 경우 라이선스 위반에 해당됩니다.
"""

import discord
from discord.ext.commands import command, Cog, is_owner, CommandNotFound
import traceback
import textwrap
from contextlib import redirect_stdout
from utils.module import Module
import io
from os import listdir
from os.path import isfile, join
import neispy
from datetime import datetime, timedelta
module = Module()


class Owner(Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_result = None

    def cleanup_code(self, content):
        """Automatically removes code blocks from the code."""
        # remove ```py\n```
        if content.startswith('```') and content.endswith('```'):
            return '\n'.join(content.split('\n')[1:-1])

        # remove `foo`
        return content.strip('` \n')

    def get_syntax_error(self, e):
        if e.text is None:
            return '```py\n{0.__class__.__name__}: {0}\n```'.format(e)
        return '```py\n{0.text}{1:>{0.offset}}\n{2}: {0}```'.format(e, '^', type(e).__name__)

    @command(pass_context=True, hidden=True, name='eval', no_pm=True)
    @is_owner()
    async def _eval(self, ctx, *, body: str):
        env = {
            'self': self,
            'bot': self.bot,
            'ctx': ctx,
            'channel': ctx.channel,
            'author': ctx.author,
            'server': ctx.guild,
            'message': ctx.message,
            '_': self._last_result
        }

        env.update(globals())

        body = self.cleanup_code(body)
        stdout = io.StringIO()

        to_compile = 'async def func():\n%s' % textwrap.indent(body, '  ')

        try:
            exec(to_compile, env)
        except SyntaxError as e:
            return await ctx.send(self.get_syntax_error(e))

        func = env['func']
        try:
            with redirect_stdout(stdout):
                ret = await func()
        except Exception as e:
            value = stdout.getvalue()
            await ctx.send('```py\n{}{}\n```'.format(value, traceback.format_exc()))
        else:
            value = stdout.getvalue()
            try:
                await ctx.message.add_reaction('\u2705')
            except:
                pass

            if ret is None:
                if value:
                    await ctx.send('```py\n%s\n```' % value)
            else:
                self._last_result = ret
                await ctx.send('```py\n%s%s\n```' % (value, ret))

    @command(pass_context=True, hidden=True, name='reload')
    @is_owner()
    async def reload(self, ctx):
        coglist = ['post', 'owner']
        for i in coglist:
            self.bot.reload_extension('cogs.' + i)
        await ctx.message.add_reaction('\u2705')

    @command(pass_context=True, hidden=True, name='apikey')
    @is_owner()
    async def apikey(self, ctx, key=None):
        if key == None:
            return await ctx.send('키를 입력해주세요!')
        await ctx.message.delete()
        data = module.open('settings.json')
        if data.get('apikey') == None:
            data['apikey'] = ""
        data['apikey'] = key
        module.save('settings.json', data)
        return await ctx.send('성공적으로 업데이트 하였습니다!')

    @command(pass_context=True, hidden=True, name='dbkrtoken')
    @is_owner()
    async def dbkrtoken(self, ctx, key=None):
        if key == None:
            return await ctx.send('키를 입력해주세요!')
        await ctx.message.delete()
        data = module.open('settings.json')
        if data.get('dbkrtoken') == None:
            data['dbkrtoken'] = ""
        data['dbkrtoken'] = key
        module.save('settings.json', data)
        return await ctx.send('성공적으로 업데이트 하였습니다!')

    @command(pass_context=True, hidden=True, name='hellothisisverification')
    async def hellothisisverification(self, ctx):
        settings = module.open('settings.json')
        owner = settings['owner']
        return await ctx.send(self.bot.get_user(owner[0]))

    @Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, CommandNotFound):
            em = discord.Embed(colour=0xB200FF)
            em.add_field(name='명령어를 찾을 수 없습니다!', value=f'{ctx.prefix}help를 이용해 명령어를 알아보세요!')
            return await ctx.send(embed=em)
        await ctx.send(error)

def setup(bot):
    bot.add_cog(Owner(bot))