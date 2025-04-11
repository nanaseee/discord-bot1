import discord
from googleapiclient.discovery import build
from discord.ext import commands
import datetime
import os  # osモジュールをインポート

# 環境変数からAPIキーとトークンを取得
API_KEY = os.getenv('AIzaSyCW1MKlVCtATVaU0gVwjDCEopc8VgNnzYU')  # 環境変数に設定したYouTube APIキー
CHANNEL_ID = 'UC1vawzfbCnRpHT9SJ5pHlHw'  # 赤城ウェンのチャンネルID

# DiscordのチャンネルIDを指定
DISCORD_CHANNEL_ID = 1359870847916970024  # メッセージを送るディスコードチャンネルID

# YouTube APIクライアントを設定
youtube = build('youtube', 'v3', developerKey=API_KEY)

# Discordボットの設定
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='', intents=intents)

# YouTubeの配信予定情報を取得する関数
def get_upcoming_stream():
    request = youtube.search().list(
        part='snippet',
        channelId=CHANNEL_ID,
        eventType='upcoming',
        type='video'
    )
    response = request.execute()

    if response['items']:
        video = response['items'][0]
        title = video['snippet']['title']
        video_id = video['id']['videoId']
        link = f"https://www.youtube.com/watch?v={video_id}"
        scheduled_time = video['snippet']['publishedAt']
        
        # 24時間形式で時間を整形
        scheduled_time_obj = datetime.datetime.strptime(scheduled_time, "%Y-%m-%dT%H:%M:%S%z")
        formatted_time = scheduled_time_obj.strftime('%H:%M')

        return title, link, formatted_time
    else:
        return None

# ボットコマンドの処理
@bot.command()
async def 乾杯チャンス(ctx):
    stream_info = get_upcoming_stream()
    if stream_info:
        title, link, time = stream_info
        message = f"🍱🦖次の配信予定🍻🤩\n✅ {title}\n🔗 {link}\n⏰ {time} (24時間表記)"
    else:
        message = "一旦禁酒Time～🍱🦖"
    
    # メッセージに「にゃ」が含まれている場合、返事を変更する
    if "にゃ" in message:
        message = "にゃ～ん"
    
    # 指定したチャンネルにメッセージを送信
    channel = bot.get_channel(DISCORD_CHANNEL_ID)
    if channel:
        await channel.send(message)
    else:
        print("チャンネルが見つかりません")

# ボットを実行
bot.run(os.getenv('MTM1OTY4Mjc1OTc2ODkzMjYyNQ.GdsDBQ.kxAO2W4xgIZREwWaLyl3uwVIe-PJtkAxoh_3zE'))  # 環境変数からDiscordトークンを取得


