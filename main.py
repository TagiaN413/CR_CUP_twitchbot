
from twitchio.ext import commands
from config import *
import requests

class Bot(commands.Bot):
    def __init__(self):
        super().__init__(
        irc_token='XXXXXXXXXXXXXXXX',
        client_id='XXXXXXXXXXXXXXXX',
        nick='CRBOT',
        prefix='#CR'  ,
        initial_channels=['#Jasper7se',]
        )
    SCORE_URL = 'https://olkcs5v2e0.execute-api.ap-northeast-1.amazonaws.com/v1'
    team_list = ['vodka','chigusa','wokka','francisco','kuzuha','ratna','kinako','ru','stylishnoob','shaka','kawase','ras','virtualgorilla','bobsappaim','shibuyahal','darumaisgod','chihiro','amatsuki','kun','admin'] #20チームのリスト



   
    async def event_ready(self):
        print(f"{BOT_NICK}がオンラインになりました!")
    

    async def event_command_error(self,ctx, error):
        if isinstance(error, commands.errors.CommandNotFound):
            await ctx.channel.send('@'+f'{ctx.author.name},存在しないコマンドです　#CR helpで確認してください。')
        else:
            raise error
    

    
    @commands.command(name='leader')
    async def test(self,ctx):
        team_list = ['vodka','chigusa','wokka','francisco','kuzuha','ratna','kinako','ru','stylishnoob','shaka','kawase','ras','virtualgorilla','bobsappaim','shibuyahal','darumaisgod','chihiro','amatsuki','kun','admin'] #20チームのリスト
        await ctx.channel.send('@'+f'{ctx.author.name}' + str(team_list))
    
    @commands.command(name='end')
    async def end(self,ctx):
        await ctx.send('お疲れ様でした。')
    
    @commands.command(name='hello')
    async def hello(self,ctx):
        await ctx.channel.send(f'{ctx.author.name}さん、こんにちは！CRBOTです！')


    @commands.command(name='help')
    async def help_command(self,ctx):
        await ctx.channel.send('@'+f'{ctx.author.name},#CR rankingで現在の暫定順位、#CR team (リーダ名)でそのチームの順位、#CR leaderでリーダの一覧、＃CR ruleで今大会のルールを送ります！')
    
    @commands.command(name='rule')
    async def rules_command(self,ctx):
        await ctx.channel.send('@'+f'{ctx.author.name}, 1位:12pt 2位:9pt 3位:7pt 4位:5pt 5位:4pt 6-7位:3pt 8-10位:2pt 11-15位:1pt 16-20位:0pt　そしてこれに1kill=1ptとして加算されます！')

    @commands.command(name='ranking')
    async def post_ranking(self,ctx):
        SCORE_URL = 'https://olkcs5v2e0.execute-api.ap-northeast-1.amazonaws.com/v1'
        resource = '/ranking'
        url = SCORE_URL + resource
        response = requests.get(url)
        ranking = response.json()
        if str(response) == '<Response [502]>':
            await ctx.channel.send('@'+f'{ctx.author.name},'+'まだランキングはできていません！')
        game_num = ranking['game_num']
        comment = ''
        for i in range(5):
            team = ranking['team_points'][i]['team']
            point = ranking['team_points'][i]['points']
            comment = comment + f"{i+1}位->リーダー：{team}，ポイント：{point} "
        
    
        await ctx.channel.send('@'+f'{ctx.author.name},'+f'{game_num}試合目までの暫定順位です：'+comment)

    @commands.command()
    async def team(self,ctx,arg1):
        team_list = ['vodka','chigusa','wokka','francisco','kuzuha','ratna','kinako','ru','stylishnoob','shaka','kawase','ras','virtualgorilla','bobsappaim','shibuyahal','darumaisgod','chihiro','amatsuki','kun','admin'] #20チームのリスト
        if arg1 in team_list:
            SCORE_URL = 'https://olkcs5v2e0.execute-api.ap-northeast-1.amazonaws.com/v1'
            resource = '/ranking'
            url = SCORE_URL + resource
            response = requests.get(url)
            ranking = response.json()
            for i in range(len(ranking['team_points'])):
                if ranking['team_points'][i]['team'] == arg1:
                    team_ranking = i
                else:
                    pass
            team_point = ranking['team_points'][team_ranking]['points']
            leader_diff = ranking['team_points'][0]['points'] - team_point
            comment = ''
            comment  = comment + f"{str(team_ranking+1)}位です，ポイント：{str(team_point) }"  +  "１位との差は" + str(leader_diff) + "です。"
        
            await ctx.channel.send('@'+f'{ctx.author.name},'+comment)
        else:
            await ctx.channel.send('@'+f'{ctx.author.name},リーダー名を正しく入力してください！')







bot = Bot()
bot.run()
