from discord import Embed
import aiohttp
from asyncio import TimeoutError
from utils.module import Module as json
from discord.ext.commands import command, Cog, is_owner, cooldown
json = json()

class Post(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.api = json.open('settings.json')
        self.company = json.open('company/company.json')
        self.user = json.open('userdata.json')

    @command(name='택배조회', aliases=['택배', 'post', 'ㅔㅐㄴㅅ', 'xorqo', 'xorqowhghl'], no_pm=True)
    @cooldown(1, 3)
    async def post(self, ctx, 택배회사:str=None, 송장번호:int=None):
        if 택배회사 == None and 송장번호 == None:
            data = self.user.get(str(ctx.author.id))
            if data:
                return await self.tbcheck(ctx, data)
            elif 택배회사 == None:
                return await ctx.send('택배회사를 적어주십시오!')
            elif 송장번호 == None:
                return await ctx.send('송장번호를 적어주십시오!')
        code = await self.tbcompany(ctx, 택배회사)
        em = await self.lookup(ctx, code, 송장번호)
        try:
            em.isalpha()
            await ctx.send(em)
        except:
            return await ctx.send(embed=em)

    @command(name='추가', aliases=['ㅁㅇㅇ', 'add', '송장추가', 'thdwkdcnrk'], no_pm=True)
    @cooldown(1, 3)
    async def add(self, ctx):  
        data = self.user
        msg = ['택배회사', '송장번호']
        if data.get(str(ctx.author.id)) == None:
            data[str(ctx.author.id)] = []
        for i in msg:
            msg = await ctx.send(f"추가하실 택배정보의 {i}를 적어주십시오.")
            def check(m):
                return m.channel == ctx.channel and m.author == ctx.author 
            try:
                content = await self.bot.wait_for('message', check=check, timeout=30)        
                await content.delete()    
                if i == "택배회사":
                    result = await self.tbcompany(ctx, content.content)
                    코드 = str(result)
                if i == "송장번호":
                    result = await self.lookup(ctx, result, content.content)
                    if result == "유효하지 않은 운송장 번호 혹은 택배사 코드 입력":
                        return await ctx.send('유효하지 않은 운송장 번호 혹은 택배사 입니다!')
                    try:
                        result.isalpha()
                        return await ctx.send(result)
                    except:
                        송장 = str(content.content)
            except TimeoutError:
                return await msg.edit(embed=None, content='시간 초과로 인하여 취소되었습니다!')
        jsondata = {'code': str(송장), 'name': str(코드)}
        if jsondata in data[str(ctx.author.id)]:
            return await ctx.send('이미 저장된 송장입니다!')
        else:
            data[str(ctx.author.id)].append(jsondata)
        json.save('userdata.json', data)
        return await ctx.send('저장이 완료되었습니다!')

    @command(name='삭제', aliases=['tkrwp', 'remove', 'ㄱ드ㅐㅍㄷ'], no_pm=True)
    @cooldown(1, 3)
    async def remove(self, ctx):
        data = self.user.get(str(ctx.author.id))
        string = []
        string2 = ""
        num = 0
        for i in data:
            택배회사 = i['name']
            송장번호 = i['code']
            for i in self.company['Company']:
                if 택배회사 == str(i['Code']):
                    num += 1 
                    string.append({"name": i['Code'], "code": 송장번호})
                    string2 += f"{num}. {i['Name']} - {송장번호}\n"
        if string2 == "":
            return await ctx.send('저장된 송장이 없습니다!')
        em = Embed(colour=0x3CB371, title='송장번호 선택')
        em.add_field(name='송장번호를 선택해주세요!', value=f"삭제를 원하는 송장번호의 코드를 적어주십시오.\n```{string2}```")
        msg = await ctx.send(embed=em)
        def check(m):
            return m.channel == ctx.channel and m.author == ctx.author 
        try:
            content = await self.bot.wait_for('message', check=check, timeout=30)            
            number = int(content.content)
            await content.delete()
        except TimeoutError:
            return await msg.edit(embed=None, content='시간 초과로 인하여 취소되었습니다!')
        except:
            pass
        try:
            await msg.delete()
        except:
            pass
        code = string[number - 1]
        data = self.user
        data[str(ctx.author.id)].remove(code)
        json.save('userdata.json', data)
        await ctx.send('삭제하였습니다!')


    async def tbcompany(self, ctx, company_name):
        string = []
        string2 = ""
        num = 0
        for i in self.company['Company']:
            if company_name in i['Name']:
                num += 1 
                string.append(f"{i['Code']}")
                string2 += f"{num}. {i['Name']}\n"
        if not string: return await ctx.send('검색된 택배회사가 없습니다!')
        if not num == 1:
            em = Embed(colour=0x3CB371, title='택배 회사 중복!')
            em.add_field(name='택배회사 중복이 발생하였습니다!', value=f"원하는 택배회사 코드를 적어주십시오,\n```{string2}```")
            msg = await ctx.send(embed=em)
            def check(m):
                return m.channel == ctx.channel and m.author == ctx.author 
            try:
                content = await self.bot.wait_for('message', check=check, timeout=30)            
                number = int(content.content)
            except TimeoutError:
                return await msg.edit(embed=None, content='시간 초과로 인하여 취소되었습니다!')
        else:
            number = 1
        if not number > num:
            code = string[number - 1]
            return code
        else:
            return await ctx.send('숫자가 크거나 작습니다! 다시 시도해주세요!')  
        try:
            await ctx.message.delete()
            await msg.delete()
        except:
            pass


    async def tbcheck(self, ctx, data):
        string = []
        string2 = ""
        num = 0
        for i in data:
            택배회사 = i['name']
            송장번호 = i['code']
            for i in self.company['Company']:
                if 택배회사 == str(i['Code']):
                    num += 1 
                    string.append(f"{i['Code']}{송장번호}")
                    string2 += f"{num}. {i['Name']} - {송장번호}\n"
        if not num == 1:
            em = Embed(colour=0x3CB371, title='송장번호 선택')
            em.add_field(name='송장번호를 선택해주세요!', value=f"조회를 원하는 송장번호의 코드를 적어주십시오.\n```{string2}```")
            msg = await ctx.send(embed=em)
            def check(m):
                return m.channel == ctx.channel and m.author == ctx.author 
            try:
                content = await self.bot.wait_for('message', check=check, timeout=30)            
                number = int(content.content)
            except TimeoutError:
                return await msg.edit(embed=None, content='시간 초과로 인하여 취소되었습니다!')
        else:
            number = 1
        try:
            await msg.delete()
        except:
            pass
        if not number > num:
            code = string[number - 1][:2]
            송장 = string[number - 1][2:]
            result = await self.lookup(ctx, code, 송장)
            try:
                await ctx.send(embed=result)
            except:
                return await ctx.send(result)
            status = await self.status_check(ctx, code, 송장번호) 
            if status == 6:
                await self.remove(ctx)
        else:
            return await ctx.send('숫자가 크거나 작습니다! 다시 시도해주세요!')  
            
    async def lookup(self, ctx, code, tb_number):
        api = self.api.get('apikey')
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://info.sweettracker.co.kr/api/v1/trackingInfo?t_key={api}&t_code={code}&t_invoice={tb_number}") as response:
                data = await response.json() 
                if not data.get('code') == None:
                    return data.get("msg")
        estimate = f"오늘 {data['estimate']}시 도착 예정"
        status = {1: "배송준비중", 2: "집화완료", 3: "배송중", 4: "배송지 도착", 5: estimate, 6:"배송 완료"}
        color = {1:0xff4040 , 2: 0x3CB371, 3: 0x3CB371, 4: 0x3CB371, 5: 0x3CB371, 6: 0x50bcdf}
        sender = data['senderName']
        receiver = data['receiverName']
        if sender == "":
            sender = '알 수 없음'
        if receiver == "":
            receiver = '알 수 없음'
        em = Embed(colour=color[data['level']],title=f'받으신 분: {sender} | 보내신 분: {receiver}')
        em.set_footer(text='본 정보는 스마트택배에서 제공받는 정보로, 실제 배송상황과 다를 수 있습니다.')
        em.add_field(name='배송 상태', value=status[data['level']])
        smart = data.get('trackingDetails')
        other = []
        ymd = []
        if not smart == []:
            for item in smart:
                a = item.get('timeString')
                if a:
                    if not a[:10] in other: other.append(a[:10])
                    time = a[11:16]
                else:
                    time = ''                    
                if item.get('where'):
                    location = item.get('where')
                else:
                    location = ''               
                if item.get('kind'):
                    desc = item.get('kind').replace('\n', ' ')
                else:
                    desc = ''
                ymd.append(f'{a[:10]} [{location}] **{time}** - {desc}')
            for asdf in other:    
                real = []
                for cd in ymd:
                    if cd.startswith(asdf):
                        if not data['level'] == 5:
                            real.append(cd[11:].replace(f'(배달예정시간 :{data["estimate"]}시)', ''))
                        elif data['level'] == 5:
                            real.append(cd[11:])
                        else:
                            real.append(cd[11:])                            
                em.add_field(name=asdf, value='\n'.join(real), inline=False)            
        return em

    async def status_check(self, ctx, code, tb_number):
        api = self.api.get('apikey')
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://info.sweettracker.co.kr/api/v1/trackingInfo?t_key={api}&t_code={code}&t_invoice={tb_number}") as response:
                data = await response.json() 
                return data.get('level')
        

def setup(bot):
    bot.add_cog(Post(bot))