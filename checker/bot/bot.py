import asyncio
import json
import logging
import os

import nest_asyncio
import requests
from asgiref.sync import sync_to_async
from dotenv import load_dotenv
from rest_framework.authtoken.models import Token
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes
)
from telegram import Update
from users.models import WhitelistedUser, BlacListUser

load_dotenv()
IMEI_CHECK_API_TOKEN_SANDBOX = os.getenv('IMEI_CHECK_API_TOKEN_SANDBOX')
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        'Привет! Отправь мне IMEI устройства для проверки.'
    )

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

nest_asyncio.apply()


async def check_imei(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
) -> None:
    telegram_id = update.message.from_user.id
    username = update.message.from_user.username
    token = asyncio.run(
        sync_to_async(check_user_pemission)(update, telegram_id, username)
    )
    if token:
        imei = update.message.text
        if not is_valid_imei(imei):
            update.message.reply_text('Неверный формат IMEI.')
            return
        response = check_imei_with_service(imei, token)
        await update.message.reply_text(str(response))
    else:
        await update.message.reply_text('У вас нет доступа к этому боту.')


def check_user_pemission(update, telegram_id, username):
    if BlacListUser.objects.filter(telegram_id=telegram_id).exists():
        return False
    elif WhitelistedUser.objects.filter(username=telegram_id).exists():
        user = WhitelistedUser.objects.get(username=telegram_id)
        token, created = Token.objects.get_or_create(user=user)
        return token.key
    else:
        try:
            WhitelistedUser.objects.create(
                telegramm_username=username,
                username=int(telegram_id)
            )
            user = WhitelistedUser.objects.get(username=telegram_id)
            token, created = Token.objects.get_or_create(user=user)
            return token.key
        except Exception as e:
            return {'error': str(e)}


def is_valid_imei(imei):
    return 8 <= len(imei) <= 15 and imei.isdigit()


def check_imei_with_service(imei, token):
    url = 'http://localhost:8000/api/check-imei/'
    headers = {'Authorization': f'Token {token}'}
    data = {'imei': imei, 'token': IMEI_CHECK_API_TOKEN_SANDBOX}

    try:
        response = requests.post(url, headers=headers, data=data)
        if response.status_code == 200:
            return json.dumps(response.json(), indent=4)
        else:
            return {
                'error': 'Ошибка сервиса.',
                'status_code': response.status_code
            }
    except Exception as e:
        return {'error': str(e)}


def start_bot():
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, check_imei))
    application.run_polling()
