from concurrent.futures import process
import os
import telebot

from multiprocessing import Process, current_process


def main():

    # proceso = current_process
    print("process name: " + current_process().name)

    telegram_token = os.getenv('telegram_token')
    bot = telebot.TeleBot('5468842402:AAHbBDUoyRmrvHcwAtIAe2cjYcuzNc3aWDk')

    @bot.message_handler(commands=['start'])
    def start(message):
        bot.reply_to(message, "Let the justice be done though the heavens fall.")

        # os.system('powershell Stop-Process -Name "telegramBot"')
        os.system("python .\main.py")

    bot.polling()

if __name__ == '__main__':

    p = Process(target=main, name="telegramBot")
    p.start()
    p.join()