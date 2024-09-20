
# الكود بواسطة @Sw_Ww
import os
from telethon import TelegramClient, events, Button

api_id = '22794861'
api_hash = 'e2c5039785a25fdbb48e679b8934cae2'
bot_token = '7152705968:AAFfWVqZc6BqZlk5EtUKdvGBNdhOJjPMeGQ'

lMl10l = TelegramClient('tw9el_joker', api_id, api_hash).start(bot_token=bot_token)

aljoker = {}
aljoker_v1 = {} 
aljoker_v2 = {}  
aljoker_v3 = 'banned_users.txt'  
aljoker_admin_id = 705475246 #هنا حط ايدي حسابك

def aljoker_save_banned_users(aljoker, aljoker_v3):
    with open(aljoker_v3, 'w') as f:
        for aljoker_user_id in aljoker:
            f.write(f"{aljoker_user_id}\n")

@lMl10l.on(events.NewMessage(pattern='/start'))
async def aljoker_start(aljoker_event):
    aljoker_user_id = aljoker_event.sender_id
    if aljoker_user_id in aljoker:
        await aljoker_event.reply("**⌔︙ ❌ لقد تم حظرك من استخدام هذا البوت**")
        return
    aljoker_sender = await aljoker_event.get_sender()
    aljoker_sender_name = aljoker_sender.first_name
    aljoker_username = aljoker_sender.username
    if aljoker_username:
        aljoker_button_link = f"https://t.me/{aljoker_username}"
    else:
        aljoker_button_link = f"https://t.me/user?id={aljoker_sender.id}"
    await aljoker_event.reply(
        f"**⌔︙ هلا بيك حبيبي [{aljoker_sender_name}]({aljoker_button_link}) يمكنك من خلال هذا البوت أرسال رسالتك بشكل مجهول أو الإفصاح عن هويتك ولا يُمكن لمالك البوت بأي طريقة معرفة الشخص المجهول **",
        buttons=[
            [Button.inline('مجهول', data='set:مجهول'), Button.inline('الافصاح عن هويتي', data='set:مكشوف')],
            [Button.url('المبرمج', 'https://t.me/lMl10l')] #لاتبدلها ولك 😒
        ]
    )

@lMl10l.on(events.CallbackQuery)
async def aljoker_handle_choice(aljoker_event):
    if aljoker_event.sender_id in aljoker:
        await aljoker_event.answer("⌔︙ ❌ لقد تم حظرك من استخدام هذا البوت", alert=True)
        return
    if aljoker_event.sender_id == aljoker_admin_id:
        await aljoker_event.answer("⌔︙ الأزرار ذني مو الك فقط للمستخدمين الي يراسلوك 🙂", alert=True)
        return
    aljoker_data = aljoker_event.data.decode('utf-8')
    if aljoker_data.startswith('set:'):
        aljoker_setting = aljoker_data.split(':')[1]
        aljoker_v2[aljoker_event.sender_id] = aljoker_setting
        await aljoker_event.answer(f"✅ تم تعيين إعداداتك على {aljoker_setting}", alert=True)

@lMl10l.on(events.NewMessage)
async def aljoker_ask_for_anonymity(aljoker_event):
    if aljoker_event.sender_id == aljoker_admin_id or aljoker_event.sender_id in aljoker:
        return
    if aljoker_event.is_private and not aljoker_event.message.message.startswith('/'):
        aljoker_setting = aljoker_v2.get(aljoker_event.sender_id, 'مجهول')
        aljoker[aljoker_event.message.id] = {
            'aljoker_user_id': aljoker_event.sender_id,
            'aljoker_message_text': aljoker_event.message.message,
            'aljoker_media': aljoker_event.message.media,
            'aljoker_setting': aljoker_setting
        }
        if aljoker_setting == 'مجهول':
            await lMl10l.send_message(
                aljoker_admin_id,
                f"💌 رسالة مجهولة:\n\n{aljoker_event.message.message}",
                file=aljoker_event.message.media
            )
            await aljoker_event.reply("**⌔︙ ♥🧸 تم إرسال رسالتك بشكل مجهول**")
        elif aljoker_setting == 'مكشوف':
            aljoker_sender_info = await lMl10l.get_entity(aljoker_event.sender_id)
            aljoker_username = f"@{aljoker_sender_info.username}" if aljoker_sender_info.username else "لا يوجد اسم مستخدم"
            await lMl10l.send_message(
                aljoker_admin_id,
                f"🙋🏻 رسالة من {aljoker_sender_info.first_name} ({aljoker_username}):\n\n{aljoker_event.message.message}",
                file=aljoker_event.message.media
            )
            await aljoker_event.reply("**⌔︙♥🧸 تم إرسال رسالتك مع الكشف عن هويتك**")

@lMl10l.on(events.NewMessage)
async def aljoker_reply_to_anon_message(aljoker_event):
    if aljoker_event.is_reply and aljoker_event.sender_id == aljoker_admin_id:
        aljoker_replied_msg = await aljoker_event.get_reply_message()
        try:
            for aljoker_original_message_id, aljoker_message_info in aljoker.items():
                if aljoker_message_info['aljoker_message_text'] in aljoker_replied_msg.text:
                    aljoker_original_sender_id = aljoker_message_info['aljoker_user_id']
                    aljoker_reply_text = aljoker_event.message.message
                    if "حظر" in aljoker_reply_text or "فك حظر" in aljoker_reply_text:
                        await lMl10l.send_message(aljoker_original_sender_id, 
                            f"**⌔︙ لقد تم حظرك من البوت دعبل 💦**",
                            reply_to=aljoker_original_message_id)
                        return
                    await lMl10l.send_message(aljoker_original_sender_id, 
                                               f"**{aljoker_reply_text}**",
                                               file=aljoker_replied_msg.media, 
                                               reply_to=aljoker_original_message_id)
                    await aljoker_event.reply('**⌔︙ ♥🧸 تم إرسال الرد إلى المرسل**')
                    del aljoker[aljoker_original_message_id]
                    return
            await aljoker_event.reply("**⌔︙ الرسالة غير موجودة للرد عليها**")
        except Exception as aljoker_error:
            await aljoker_event.reply(f"⌔︙ ❌ حدث خطأ: {str(aljoker_error)}")

@lMl10l.on(events.NewMessage(pattern='حظر'))
async def aljoker_ban_user(aljoker_event):
    if aljoker_event.sender_id != aljoker_admin_id:
        return
    if aljoker_event.is_reply:
        aljoker_reply_msg = await aljoker_event.get_reply_message()
        for aljoker_original_message_id, aljoker_message_info in aljoker.items():
            if aljoker_message_info['aljoker_message_text'] in aljoker_reply_msg.text:
                aljoker_banned_user_id = aljoker_message_info['aljoker_user_id']
                aljoker[aljoker_banned_user_id] = 'banned' 
                aljoker_save_banned_users(aljoker, aljoker_v3)
                await aljoker_event.reply(f"** ⌔︙ ✓ تم حظر المستخدم بنجاح**")
                del aljoker[aljoker_original_message_id]
                return
        await aljoker_event.reply("**⌔︙ ❌ لا يمكن العثور على المستخدم**")
    else:
        await aljoker_event.reply("**⌔︙ يرجى الرد على رسالة المستخدم الذي تريد حظره**")

@lMl10l.on(events.NewMessage(pattern='فك حظر'))
async def aljoker_unban_user(aljoker_event):
    if aljoker_event.sender_id != aljoker_admin_id:
        return
    if aljoker_event.is_reply:
        aljoker_reply_msg = await aljoker_event.get_reply_message()
        for aljoker_original_message_id, aljoker_message_info in aljoker.items():
            if aljoker_message_info['aljoker_message_text'] in aljoker_reply_msg.text:
                aljoker_unbanned_user_id = aljoker_message_info['aljoker_user_id']
                if aljoker_unbanned_user_id in aljoker:
                    del aljoker[aljoker_unbanned_user_id]
                    aljoker_save_banned_users(aljoker, aljoker_v3)
                    await aljoker_event.reply(f"**⌔︙ ✓ تم إلغاء حظر المستخدم بنجاح**")
                else:
                    await aljoker_event.respond("**⌔︙ ❌ المستخدم غير محظور**")
                del aljoker[aljoker_original_message_id]
                return
        await aljoker_event.reply("**⌔︙ ❌ لا يمكن العثور على المستخدم**")
    else:
        await aljoker_event.reply("**⌔︙ ❌ يرجى الرد على رسالة المستخدم الذي تريد الغاء حظره**")

@lMl10l.on(events.NewMessage(pattern='مسح المحظورين'))
async def aljoker_clear_banned_users(aljoker_event):
    if aljoker_event.sender_id != aljoker_admin_id:
        return
    with open(aljoker_v3, 'w') as f:
        f.write('')
    aljoker.clear()
    await aljoker_event.reply("**⌔︙ ✓ تم مسح قائمة المحظورين بنجاح**")

print("البوت شغال ✓")
lMl10l.run_until_disconnected()