# oof
from datetime import datetime as dt
import os
from bot import (
    APP_ID,
    API_HASH,
    AUTH_USERS,
    DOWNLOAD_LOCATION,
    LOGGER,
    TG_BOT_TOKEN,
    BOT_USERNAME,
    SESSION_NAME,
    
    data,
    app,
    crf,
    resolution,
    audio_b,
    preset,
    codec,
    watermark 
)
from bot.helper_funcs.utils import add_task, on_task_complete
from pyrogram import Client, filters
from pyrogram.handlers import MessageHandler, CallbackQueryHandler
from translation import Translation
from bot.plugins.incoming_message_fn import (
    incoming_start_message_f,
    incoming_compress_message_f,
    incoming_cancel_message_f
)


from bot.plugins.status_message_fn import (
    eval_message_f,
    exec_message_f,
    upload_log_file
)

from bot.commands import Command

sudo_users = "1666551439" 
crf.append("30")
codec.append("libx265")
resolution.append("1280x720")
preset.append("veryfast")
audio_b.append("30k")
# 🤣


uptime = dt.now()

def ts(milliseconds: int) -> str:
    seconds, milliseconds = divmod(int(milliseconds), 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    tmp = (
        ((str(days) + "d, ") if days else "")
        + ((str(hours) + "h, ") if hours else "")
        + ((str(minutes) + "m, ") if minutes else "")
        + ((str(seconds) + "s, ") if seconds else "")
        + ((str(milliseconds) + "ms, ") if milliseconds else "")
    )
    return tmp[:-2]


if __name__ == "__main__" :
    # create download directory, if not exist
    if not os.path.isdir(DOWNLOAD_LOCATION):
        os.makedirs(DOWNLOAD_LOCATION)
    #
    
    
    #
    app.set_parse_mode("html")
    #
    # STATUS ADMIN Command

    # START command

    
   
    @app.on_message(filters.incoming & filters.command(["start", f"start@{BOT_USERNAME}"]))
    async def start(bot, update):   
        await update.reply_text(
            text=Translation.START_TEXT.format(update.from_user.mention),
            disable_web_page_preview=True,
            reply_markup=Translation.START_BUTTONS
        )
             
            
        
     
 
    @app.on_message(filters.incoming & filters.command(["restart", f"restart@{BOT_USERNAME}"]))
    async def restarter(app, message):
        if message.from_user.id in AUTH_USERS:
            await message.reply_text("•Restarting")
            quit(1)
        
    @app.on_message(filters.incoming & filters.command(["clear", f"clear@{BOT_USERNAME}"]))
    async def restarter(app, message):
      data.clear()
      await message.reply_text("Successfully cleared Queue ...")
         
        
    @app.on_message(filters.incoming & (filters.video | filters.document))
    async def help_message(app, message):
        query = await message.reply_text("Added to Queue ⏰...\nPlease be patient, Compress will start soon", quote=True)
        data.append(message)
        if len(data) == 1:
         await query.delete()   
         await add_task(message)
            
    @app.on_message(filters.incoming & (filters.photo))
    async def help_message(app, message):
        os.system('rm thumb.jpg')
        await message.download(file_name='/app/thumb.jpg')
        await message.reply_text('Thumbnail Added')
        
    @app.on_callback_query()
    async def button(bot, update):
        if update.data == "home":
            await update.message.edit_text(
                text=Translation.START_TEXT.format(update.from_user.mention),
                reply_markup=Translation.START_BUTTONS,
                disable_web_page_preview=True
            )
        elif update.data == "help":
            await update.message.edit_text(
                text=Translation.HELP_TEXT,
                reply_markup=Translation.HELP_BUTTONS,
                disable_web_page_preview=True
            )
        elif update.data == "about":
            await update.message.edit_text(
                text=Translation.ABOUT_TEXT,
                reply_markup=Translation.ABOUT_BUTTONS,
                disable_web_page_preview=True
            )
        else:
            await update.message.delete()
  
    @app.on_message(filters.incoming & filters.command(["log", f"log@{BOT_USERNAME}"]))
    async def help_message(app, message):
        await upload_log_file(app, message)
    @app.on_message(filters.incoming & filters.command(["ping", f"ping@{BOT_USERNAME}"]))
    async def up(app, message):
      stt = dt.now()
      ed = dt.now()
      v = ts(int((ed - uptime).seconds) * 1000)
      ms = (ed - stt).microseconds / 1000
      p = f"🌋Pɪɴɢ = {ms}ms"
      await message.reply_text(v + "\n" + p)

    @app.on_message(filters.command(["compress", "compress@{BOT_USERNAME}"]) & ~ filters.edited)
    async def compox(s: shakida, message: Message):
              global temp
              tempid = uuid.uuid4()
              video = message.reply_to_message
       
              any = message.from_user.id
         
          
              if not video.video:
                 await s.send_message(message.chat.id, f'**No video provided ‼️')
                 return
              else:
                 f = await s.send_message(message.chat.id, f"**🔄 Prosesing**")
                 if len(message.command) != 2:
                    crf = 28
                 if len(message.command) == 2:
                    crf = int(message.text.split(None)[1])
                 if (crf < 20) or (crf > 50):
                    await f.edit(f'**ERROR!**\nCRF 20-50 value only or default 27')
                    return
                 file_n = video.video.file_name
                 ch = video.video.mime_type.split('/')[1]
                 duration = video.video.duration
                 file_s = video.video.file_size
                 height = video.video.height
                 width = video.video.width
                 file = f'{video.video.file_unique_id}.mkv'
                 butt = InlineKeyboardMarkup([[InlineKeyboardButton("⚙️ Status", callback_data=f"sys"),]])
                 temp.append(str(file))
                 await f.edit(f'**🏷️ File Name:** `{file_n}`\n**📥 DOWNLOADING...**\n'
                 + f'**🍻 CC:** {message.from_user.first_name}', reply_markup=butt)
                 try:
                    videox = await video.download(file)
                 except Exception as e:
                    temp.pop(0)
                    await f.edit(f'**ERROR!!: Downloading error.\n`{e}`')
                    return

                 try:
                    but = InlineKeyboardMarkup([[
                      InlineKeyboardButton("❌ Cancel", callback_data=f'cl {file}|{crf}|{any}'),
                      InlineKeyboardButton("⚙️ Status", callback_data=f"sys"),
                      ]])
                    await f.edit(f'**🏷️ File Name:** ` {file_n}`\n**🗜️ COMPRESSING...**\n**⚙️ CRF Range:** `{crf}`\n'
                    + f'**🍻 CC:** {message.from_user.first_name}', reply_markup=but)
                    proc = await asyncio.create_subprocess_shell(
                      f'ffmpeg -hide_banner -loglevel quiet -i "{videox}" -preset ultrafast -vcodec libx265 -crf {crf} "{file}" -y',
                      stdout=asyncio.subprocess.PIPE,
                      stderr=asyncio.subprocess.PIPE,
                      )
                    try:
                       await proc.communicate()
                    except Exception as e:
                       await f.edit(f'**ERROR!!:** {e}`')
                       return
                    out = f"{file}"
                    os.remove(videox)
                    await f.edit(f'**🏷️ File Name:** `{file_n}`\n**COMPRESSION SUCCESSFULLY DONE ✅**\n**📤 File Uploading...**\n'
                    + f'**🍻 CC:** {message.from_user.first_name}', reply_markup=but)
                    await video.reply_video(out, duration=duration, height=height, width=width, caption=f'**🏷️ File Name: `{file_n}`'
                    + f'\n**🚦 Preset:** `Ultrafast`\n**⚙️ CRF:** `{crf}`\n'
                    + f'**💾 Orginal size:** `{humanbytes(file_s)}`\n'
                    + f'**🍻 CC:** {message.from_user.mention()}')
                    os.remove(file)
                    temp.pop(0)
                    await f.delete()
                 except Exception as a:
                    os.remove(videox)
                    temp.pop(0)
                    await f.edit(f'**ERROR!:**\n`{a}`')
                    return

             

    app.run()

