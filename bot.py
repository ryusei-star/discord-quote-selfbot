import discord
import aiohttp
import time
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")

client = discord.Client()

rate_limit = {}

@client.event
async def on_ready():
    print(f"ログイン成功: {client.user}")

@client.event
async def on_message(message):
    if message.author.bot:
        return

    if message.content.startswith(".miq"):
        now = time.time()
        user_id = message.author.id

        last_time = rate_limit.get(user_id, 0)
        if now - last_time < 10:
            await message.channel.send(f"このコマンドはクールダウン中です。あと {10 - (now - last_time):.1f} 秒待ってください。")
            return
        rate_limit[user_id] = now

        perms = message.channel.permissions_for(message.guild.me if message.guild else message.channel.guild.me)
        if not perms.read_message_history or not perms.send_messages:
            await message.channel.send("必要な権限がありません。")
            return

        if message.reference is None:
            await message.channel.send("返信先のメッセージを指定してください。")
            return

        try:
            replied_msg = await message.channel.fetch_message(message.reference.message_id)
            username = replied_msg.author.name or "Unknown"
            display_name = getattr(replied_msg.author, "display_name", username)
            text = replied_msg.content or "[メッセージなし]"
            avatar = replied_msg.author.display_avatar.url

            payload = {
                "username": username,
                "display_name": display_name,
                "text": text,
                "avatar": avatar,
                "color": True
            }

            async with aiohttp.ClientSession() as session:
                async with session.post("https://api.voids.top/fakequote", json=payload) as resp:
                    if resp.status in [200, 201]:
                        data = await resp.json(content_type=None)
                        image_url = data.get("url")
                        if image_url:
                            await message.channel.send(image_url)
                        else:
                            await message.channel.send("画像URLの取得に失敗しました。")
                    else:
                        text = await resp.text()
                        await message.channel.send(f"APIからの応答に失敗しました。\nステータス: {resp.status}\n内容: {text}")
        except discord.NotFound:
            await message.channel.send("元メッセージが見つかりませんでした。")
        except discord.Forbidden:
            await message.channel.send("メッセージを取得する権限がありません。")
        except Exception as e:
            await message.channel.send(f"予期しないエラーが発生しました。\n詳細: {str(e)}")

client.run(TOKEN)
