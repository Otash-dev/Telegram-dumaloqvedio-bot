import telebot
import os
import subprocess

TOKEN = os.getenv("TOKEN")
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(content_types=['video'])
def handle_video(message):
    bot.reply_to(message, "⏳ Processing...")

    file_info = bot.get_file(message.video.file_id)
    downloaded_file = bot.download_file(file_info.file_path)

    with open("input.mp4", "wb") as f:
        f.write(downloaded_file)

    command = [
        "ffmpeg",
        "-i", "input.mp4",
        "-vf", "crop=min(in_w\\,in_h):min(in_w\\,in_h),scale=640:640",
        "-t", "60",
        "-y",
        "output.mp4"
    ]

    subprocess.run(command)

    if os.path.exists("output.mp4"):
        with open("output.mp4", "rb") as video_note:
            bot.send_video_note(message.chat.id, video_note)

        os.remove("output.mp4")

    os.remove("input.mp4")

bot.polling(none_stop=True)
