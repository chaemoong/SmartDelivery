"""
위 모듈은 개발자 뭉개구름이 제작하였으며 무단으로 사용할 경우 라이선스 위반에 해당됩니다.
"""

import discord
from discord.ext.commands import AutoShardedBot as Bot
from utils.module import Module
from os import listdir
from os.path import isfile, join

module = Module()
settings = module.open('settings.json')
prefix = settings['prefix']
owner = settings['owner']
token = settings['token']

bot = Bot(command_prefix=prefix, owner_ids=owner)

@bot.event
async def on_ready():
    readylist = ['='*50, f'{bot.user}에 로그인하였습니다!', '='*50]
    for i in readylist:
        print(i)
    coglist = ['post', 'owner']
    for i in coglist:
        bot.load_extension('cogs.' + i)

bot.run(token)