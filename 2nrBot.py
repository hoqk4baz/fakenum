import random
import string
import json
import time
from curl_cffi import requests
import re
import threading
from pyrogram import Client, filters
from pyrogram.enums import ChatMemberStatus
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import UserIsBlocked
from pymongo import MongoClient

MONGO_URI = "mongodb+srv://hoqk4baz:zsezsert55@cluster0.rvpzndm.mongodb.net/hoqk4baz?retryWrites=true&w=majority"
client_mongo = MongoClient(MONGO_URI)
db = client_mongo["whoisryuga"]
users_collection = db["users"]
banned_collection = db["banned_users"]

ADMIN_ID = 6783938695
domains = [
    "hbsen.dev.tc",
    "hbcan.app.tc",
    "nuvora.dev.tc",
    "haberler.san.tc",
    "vexora.dev.tc",
    "zylofy.dev.tc",
    "techspire.dev.tc",
    "bravixo.dev.tc",
    "xyberic.dev.tc"
]

API_ID = "26306308"
API_HASH = "b7656adf5a71335c25d5a402ab6ad12a"
BOT_TOKEN = "7582766109:AAFjCG-yRDWi8r7ajDN71yviWnCKrvtw2Cs"

app = Client("2nr_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
def random_ip():
    return ".".join(str(random.randint(0, 255)) for _ in range(4))
@app.on_message(filters.command("duyuru"))
def duyuru(client, message):
    user_id = message.from_user.id
    if user_id != ADMIN_ID:
        message.reply_text("❌ **Bu komutu sadece admin kullanabilir!**")
        return
    if len(message.command) < 2:
        message.reply_text("❌ **Lütfen duyuru mesajını girin!**\n\nÖrnek: `/duyuru Merhaba! Yeni güncelleme geldi.`")
        return

    duyuru_mesaji = message.text.split(None, 1)[1]

    basarili = 0
    basarisiz = 0

    users = users_collection.find()

    for user in users:
        user_id = user["user_id"]
        try:
            client.send_message(user_id, f"📢 **DUYURU** 📢\n\n{duyuru_mesaji}")
            basarili += 1
        except UserIsBlocked:
            basarisiz += 1
        except Exception:
            basarisiz += 1

    message.reply_text(f"✅ **Duyuru tamamlandı!**\n\n📤 Gönderildi: `{basarili}`\n❌ Başarısız: `{basarisiz}`")
@app.on_message(filters.command("get"))
def get_users(client, message):
    user_id = message.from_user.id
    if user_id != ADMIN_ID:
        message.reply_text("❌ **Bu komutu sadece admin kullanabilir!**")
        return

    users = users_collection.find({}, {"_id": 0, "user_id": 1, "first_name": 1})  
    user_list = [f"👤 `{user['user_id']}` - **{user['first_name']}**" for user in users]

    if not user_list:
        message.reply_text("🚫 **Veritabanında kayıtlı kullanıcı yok!**")
    else:
        message.reply_text(f"📋 **Kayıtlı Kullanıcılar:**\n\n" + "\n".join(user_list))

@app.on_message(filters.command("engelle"))
def ban_user(client, message):
    user_id = message.from_user.id

    if user_id != ADMIN_ID:
        message.reply_text("❌ **Bu komutu sadece admin kullanabilir!**")
        return
    if len(message.command) < 2:
        message.reply_text("⚠️ **Kullanım:** `/engelle user_id`")
        return

    try:
        target_user_id = int(message.command[1])
        user = users_collection.find_one({"user_id": target_user_id})
        
        if not user:
            message.reply_text("🚫 **Bu kullanıcı zaten engellenmiş!**")
            return
        

        banned_collection.insert_one({"user_id": target_user_id, "first_name": user.get("first_name", "Bilinmiyor")})
        users_collection.delete_one({"user_id": target_user_id})
        message.reply_text(f"✅ **Kullanıcı {target_user_id} başarıyla engellendi!**")

    except ValueError:
        message.reply_text("❌ **Geçersiz kullanıcı ID girdiniz!**")

@app.on_message(filters.command("kaldır"))
def unban_user(client, message):
    user_id = message.from_user.id

    if user_id != ADMIN_ID:
        message.reply_text("❌ **Bu komutu sadece admin kullanabilir!**")
        return
    
    try:
        args = message.text.split()
        if len(args) != 2:
            message.reply_text("⚠️ **Kullanım:** `/kaldır user_id`")
            return

        target_user_id = int(args[1])

        user = banned_collection.find_one({"user_id": target_user_id})
        if not user:
            message.reply_text("🚫 **Bu kullanıcı zaten engellenmemiş!**")
            return
        
        banned_collection.delete_one({"user_id": target_user_id})

        message.reply_text(f"✅ **Kullanıcı {target_user_id} engeli kaldırıldı!**")

    except ValueError:
        message.reply_text("❌ **Geçersiz kullanıcı ID girdiniz!**")

@app.on_message(filters.command("sil"))
def unban_user(client, message):
    user_id = message.from_user.id

    if user_id != ADMIN_ID:
        message.reply_text("❌ **Bu komutu sadece admin kullanabilir!**")
        return
    
    try:
        args = message.text.split()
        if len(args) != 2:
            message.reply_text("⚠️ **Kullanım:** `/sil user_id`")
            return

        target_user_id = int(args[1])

        user = users_collection.find_one({"user_id": target_user_id})
        if not user:
            message.reply_text("🚫 **Bu kullanıcı zaten silinmiş!**")
            return
        
        users_collection.delete_one({"user_id": target_user_id})
        message.reply_text(f"✅ **Kullanıcı {target_user_id} Databaseden  silindi!**")

    except ValueError:
        message.reply_text("❌ **Geçersiz kullanıcı ID girdiniz!**")

@app.on_message(filters.command("banlist"))
def list_banned_users(client, message):
    user_id = message.from_user.id

    if user_id != ADMIN_ID:
        message.reply_text("❌ **Bu komutu sadece admin kullanabilir!**")
        return

    banned_users = banned_collection.find({}, {"_id": 0, "user_id": 1, "first_name": 1})
    ban_list = [f"🆔 `{user['user_id']}` - 👤 {user.get('first_name', 'Bilinmiyor')}" for user in banned_users]

    if not ban_list:
        message.reply_text("🚫 **Engellenmiş kullanıcı yok!**")
    else:
        message.reply_text("🚷 **Engellenmiş Kullanıcılar:**\n\n" + "\n".join(ban_list))


def get_https_response(urld,headers):
    response = requests.get(urld, headers=headers,allow_redirects=False)
    cookies = response.headers.get("Set-Cookie", "")
    body = response.text
    match = re.search(r"token=([a-fA-F0-9]+)", cookies)
    if match:
        return match.group(1)
    return None

def rndm(length=10):
    characters = string.ascii_lowercase + string.digits
    return ''.join(random.choice(characters) for _ in range(length))
user_sessions = {}
@app.on_callback_query(filters.regex("get_number"))
def get_number(client, query):
    user_id = query.from_user.id
    channel_id = CHANNEL_ID

    if banned_collection.find_one({"user_id": user_id}):
        query.message.reply_text("🚫 **Engellendiniz!**")
        return

    try:
        chat_member = client.get_chat_member(channel_id, user_id)  # sync olarak bekletiyoruz
        status = chat_member.status

        if status in [ChatMemberStatus.MEMBER, ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
            if user_id in user_sessions:
                query.answer("İsteğiniz işleniyor, lütfen bekleyin...")
                return

            user_sessions[user_id] = True
            threading.Thread(target=devam_et, args=(client, query.message)).start()
            del user_sessions[user_id]
        else:
            buttons = InlineKeyboardMarkup([
                [InlineKeyboardButton("📢 Kanala Katıl", url=f"https://t.me/{channel_id[1:]}")],
                [InlineKeyboardButton("🔄 Kontrol Et", callback_data="check_membership")]
            ])
            query.message.reply_text("❌ **Botu kullanabilmek için kanala katılmanız gerekiyor!**", reply_markup=buttons)
            return

    except Exception as e:
        buttons = InlineKeyboardMarkup([
            [InlineKeyboardButton("📢 Kanala Katıl", url=f"https://t.me/{channel_id[1:]}")],
            [InlineKeyboardButton("🔄 Kontrol Et", callback_data="check_membership")]
        ])
        query.message.reply_text("❌ **Botu kullanabilmek için kanala katılmanız gerekiyor!**", reply_markup=buttons)
        return


    
    
@app.on_message(filters.command("info"))
def info(client, message):
    toplam_kullanici = users_collection.count_documents({})
    message.reply_text(f"📊 **Toplam Kullanıcı:** `{toplam_kullanici}`\n\n🧑🏽‍💻**Yapımcı:** @degeribilinmeyenlerdenim\n\n☄️**Hatalar Karşısında Ulaşın**")


CHANNEL_ID = "@whoisryuga"
@app.on_message(filters.command("start"))
def start(client, message):
    user_id = message.from_user.id
    first_name = message.from_user.first_name

    try:
        chat_member = client.get_chat_member(CHANNEL_ID, user_id)
        status = chat_member.status

        if banned_collection.find_one({"user_id": user_id}):
            message.reply_text("🚫 **Engellendiniz!**")
            return
        if status in [ChatMemberStatus.MEMBER, ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:  

            if not users_collection.find_one({"user_id": user_id}):  
                users_collection.insert_one({"user_id": user_id, "first_name": first_name})

            buttons = InlineKeyboardMarkup([
                [InlineKeyboardButton("𝐍𝐮𝐦𝐚𝐫𝐚 𝐀𝐥", callback_data="get_number")]
            ])
            message.reply_text(
                f"✅ **Hoşgeldin**, {first_name}! **Nasılsın?**\n\n"
                "**Numara Almak İçin Butona Tıkla**\n\n"
                "**Sahip**: @degeribilinmeyenlerdenim",
                reply_markup=buttons
            )
        else:
            buttons = InlineKeyboardMarkup([
                [InlineKeyboardButton("📢 Kanala Katıl", url=f"https://t.me/{CHANNEL_ID[1:]}")],
                [InlineKeyboardButton("🔄 Kontrol Et", callback_data="check_membership")]
            ])
            message.reply_text("❌ **Botu kullanabilmek için kanala katılmanız gerekiyor!**", reply_markup=buttons)

    except Exception:
        buttons = InlineKeyboardMarkup([
            [InlineKeyboardButton("📢 Kanala Katıl", url=f"https://t.me/{CHANNEL_ID[1:]}")],
            [InlineKeyboardButton("🔄 Kontrol Et", callback_data="check_membership")]
        ])
        message.reply_text("❌ **Botu kullanabilmek için kanala katılmanız gerekiyor!**", reply_markup=buttons)

@app.on_callback_query(filters.regex("check_membership"))
def check_membership(client, query):
    user_id = query.from_user.id 
    try:
        chat_member = client.get_chat_member(CHANNEL_ID, user_id)
        status = chat_member.status

        if status in [ChatMemberStatus.MEMBER, ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:  
            query.answer("✅\nKanala üyeliğiniz doğrulandı!\nBol Kullanımlar", show_alert=True)

            first_name = query.from_user.first_name
            if not users_collection.find_one({"user_id": user_id}):
                users_collection.insert_one({"user_id": user_id, "first_name": first_name})
            query.message.reply_text(
                f"✅ **Hoşgeldin**, {first_name}! **Nasılsın?**\n\n"
                "**Numara Almak İçin Butona Tıkla**\n\n"
                "**Sahip**: @degeribilinmeyenlerdenim",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("𝐍𝐮𝐦𝐚𝐫𝐚 𝐀𝐥", callback_data="get_number")]
                ])
            )

        else:
            query.answer("❌\nHenüz kanala katılmadınız!", show_alert=True)

    except Exception:
        query.answer("❌\nHenüz kanala katılmadınız!", show_alert=True)



def devam_et(client, message):
    user_id = message.from_user.id
    domain = random.choice(domains)
    rndom = rndm()
    rndm_ip = random_ip()
    email = f"{rndom}@{domain}"
    host = "api.2nr.xyz"
    endpoint = "/auth/register"
    headers = {
            "Content-Type": "application/json",
            "User-Agent": "okhttp/4.10.0",
            "X-Forwarded-For": rndm_ip
        }
    data = {
        "query": {
            "email": email,
            "imei": "950c2c1f4b27e27ryuga",
            "password": "Zsezsert3169#"
        },
        "id": 103
    }
    response_json = requests.post(f"https://{host}{endpoint}", json=data, headers=headers).json()
    try:
        if response_json.get("success", False):
            message_sent = message.reply_text(f"✅𝐍𝐮𝐦𝐚𝐫𝐚 𝐀𝐲𝐚𝐫𝐥𝐚𝐧**ı**𝐲𝐨𝐫")
            time.sleep(1)
        else:
            message_sent = message.reply_text("❌𝐇𝐞𝐬𝐚𝐩 𝐨𝐥𝐮𝐬̧𝐭𝐮𝐫𝐮𝐥𝐮𝐫𝐤𝐞𝐧 𝐡𝐚𝐭𝐚 𝐨𝐥𝐮𝐬̧𝐭𝐮!")
    except Exception as e:
        message_sent = message.reply_text(f"⚠️**İstek sırasında hata oluştu:** {str(e)}")

    token = None
    while True:
        time.sleep(5)
        mail_bekle = requests.get(f"https://mailsorgu.com/api/messages/{email}/gFqNIYXC7oM8H961fcux").json()
        try:
            mail = mail_bekle[0]["content"]
            pattern = r"https://api\.2nr\.xyz/register/\?email=[^&]+&amp;token=[a-f0-9]{64}"
            sonuc = re.search(pattern, mail)
            if sonuc:
                urlx = sonuc.group().replace("&amp;", "&")
                token = get_https_response(urlx, headers)
                #message_sent.reply_text(f"Token: {token}")

                break
        except:
            continue
    
    headers.update({
        'Cookie': f"token={token}; x-app-version=49"
    })

    payload2 = "{\"id\":300}"
    response_json = requests.post(f"https://{host}/numbers/getRandomNumber", data=payload2, headers=headers).json()

    if response_json and isinstance(response_json, list):
        num_id = response_json[0].get("id")
        number = response_json[0].get("number")
        message_sent.edit_text(f"✅𝐍𝐮𝐦𝐚𝐫𝐚 𝐁𝐞𝐥𝐢𝐫𝐥𝐞𝐧𝐝𝐢: +48 `{number}`")
        time.sleep(2)
    else:
        message_sent.edit_text(f"❌𝐍𝐮𝐦𝐚𝐫𝐚 𝐁𝐞𝐥𝐢𝐫𝐥𝐞𝐧𝐢𝐫𝐤𝐞𝐧 𝐇𝐚𝐭𝐚!")
    payloadx = "{\"query\":{\"availability_days\":[1,2,3,4,5,6,7],\"color\":\"#E63147\",\"hour_from\":null,\"hour_to\":null,\"integrity_token\":\"eyJhbGciOiJBMjU2S1ciLCJlbmMiOiJBMjU2R0NNIn0.RD4CJzgbGoUWs_27NfVaDyrAV-hEx5UYloXJLxK1CTHSP9zLXWEahg.JrYhtgRPj7mXjMcZ.k2Yd7ETCsSAvMxmMMYNl04Iz6WNpiGtAobgDtDT5WuhOX95vpFkBfXzCMDBxBS3obITFjsF09p4heFNaNZawQNJRt0WBcTFfuhJ9a01YYaaJFvQI-Lx8-xPIhQdENLE1dUchYfKBJP7e9-Jy0mr4-gXrlF570OnZuw_pgPkrWdEAifVuj49pOt64x7dS46LIfjG81aILT-hP8YkS97qyQfZ8MLec10ylIztjsKebU5XEavnfK_2VFnTB0Gc2QtPlyOjFuEIkBUl6ck1bRwRoeZtAtaL7w7nnVXPP0ZTcg3tTRN55OypLYTL7LvKHZ-hS16Bf4xmQWEBFeqWn0CEfu7Z4cub0yrkCq8j8uwPDQfPvimLIU-bvWF6BkE5eIMtPgqEXPDWuNwMEQAxIrvCaunCannHNtEjstt7ePIA9UYQ7umq6CL6aAZRCAYKVBPUAMOzaoT0iWKtvKhHhQ6o0CJPzjsi1M21BvAhpDz35EuwCm1xVXf2mSDmv1DDOr4yNGlik91zsLl1ZWq8a-vH9w0g3YWI5uftXTmTfnjWIB3iuZ77TM9dwmFVQObAGlKg5TMQ8X-AcZMLdtt8DPLPT-egpyNUgkEuAX6_txp_hsZff5HU59Q7wOETrzawgXJuFmqpGNYYD6-1Uo26wx2AqkkjfmtFk0SYzD4rnTbAXEOX2PPVLYH2cR5IEGoQEBGOdQvZCpGhn9krZv_MllLqnjP03NxGFAfuwMzamPNlt6Bd7Vq2yvH9_BGHv.Qn4Y2lP_16iVrMuxNT420g\",\"marketing\":true,\"name\":\"whoisryuga\",\"nonce\":\"azlwbm02ZnIwYXVwZDM2YjhrNWNrOGEwYnE\",\"number_id\":"+str(num_id)+"},\"id\":301}"
    response = requests.post(f"https://{host}/numbers/reserveNumber", data=payloadx, headers=headers).json()
    tt = response["success"]
    if tt == True:
        pass
    else:
        message_sent.edit_text(f"𝐍𝐮𝐦𝐚𝐫𝐚 𝐁𝐞𝐥𝐢𝐫𝐥𝐞𝐧𝐢𝐫𝐤𝐞𝐧 𝐇𝐚𝐭𝐚!")
    sayac = 300
    
    while sayac > 0:
        payload3 = "{\"id\":400}"
        gg = requests.post(f"https://{host}/sms/get", data=payload3, headers=headers).json()
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("𝐍𝐮𝐦𝐚𝐫𝐚 𝐘𝐞𝐧𝐢𝐥𝐞", callback_data="get_new_number")]
        ])
        minutes = sayac // 60
        seconds = sayac % 60
        time_left = f"{minutes:02} DK {seconds:02} Sny. Kaldı"
        message_content = f"✅ 𝐍𝐮𝐦𝐚𝐫𝐚 𝐁𝐞𝐥𝐢𝐫𝐥𝐞𝐧𝐝𝐢: +48 `{number}`\n\n⌚️: {time_left}\n\n"
        try:
            for item in gg['result']:
                message_content += f"✉️𝐆𝐨̈𝐧𝐝𝐞𝐫𝐞𝐧: {item['phone']}\n📨**Mesaj**: {item['body']}\n\n"
                message_sent.edit_text(message_content, reply_markup=keyboard)
        except:
            try:
                message_sent.edit_text(f"✅𝐍𝐮𝐦𝐚𝐫𝐚 𝐁𝐞𝐥𝐢𝐫𝐥𝐞𝐧𝐝𝐢: +48 `{number}`\n\n🗑𝐆𝐞𝐥𝐞𝐧 𝐤𝐮𝐭𝐮𝐬𝐮 𝐛𝐨𝐬̧!\n\n**Mesajın Silinmesine**: {time_left}", reply_markup=keyboard)
            except:
                pass
            
        time.sleep(3) 
        sayac -= 3
    try:
        message_sent.delete()
    except:
        pass

    
@app.on_callback_query(filters.regex("get_new_number"))
def get_new_number(client, query):
    user_id = query.from_user.id
    channel_id = "@whoisryuga"
    if banned_collection.find_one({"user_id": user_id}):
            query.message.reply_text("🚫 **Engellendiniz!**")
            return
    try:
        chat_member = client.get_chat_member(channel_id, user_id)
        status = chat_member.status

        if status in [ChatMemberStatus.MEMBER, ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
            if user_id in user_sessions:
                query.answer("Yeni Numara Alınıyor...")
                return

            user_sessions[user_id] = True
            threading.Thread(target=devam_et, args=(client, query.message)).start()
            del user_sessions[user_id]
        else:
            buttons = InlineKeyboardMarkup([
                [InlineKeyboardButton("📢 Kanala Katıl", url=f"https://t.me/{channel_id[1:]}")],
                [InlineKeyboardButton("🔄 Kontrol Et", callback_data="check_membership")]
            ])
            query.message.reply_text("❌ **Botu kullanabilmek için kanala katılmanız gerekiyor!**", reply_markup=buttons)
            return

    except Exception as e:
        buttons = InlineKeyboardMarkup([
            [InlineKeyboardButton("📢 Kanala Katıl", url=f"https://t.me/{channel_id[1:]}")],
            [InlineKeyboardButton("🔄 Kontrol Et", callback_data="check_membership")]
        ])
        query.message.reply_text("❌ **Botu kullanabilmek için kanala katılmanız gerekiyor!**", reply_markup=buttons)
        return
    



if __name__ == "__main__":
    app.run()
