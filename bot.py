import logging
from aiogram import Bot, Dispatcher, types, executor
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup

# Настройки
logging.basicConfig(level=logging.INFO)
bot = Bot(token="8106374937:AAFp-j0tdHfzRHdbW_joA86t92j0OVnTWfg")
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# Класс состояний
class Form(StatesGroup):
    language = State()
    button_type = State()

# Команда /start и /bypass
@dp.message_handler(commands=['start', 'bypass'])
async def cmd_start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("Русский 🇷🇺", "English 🇬🇧")
    await message.answer("Выберите язык / Choose language:", reply_markup=keyboard)
    await Form.language.set()

# Выбор языка
@dp.message_handler(state=Form.language)
async def process_language(message: types.Message, state: FSMContext):
    if message.text not in ["Русский 🇷🇺", "English 🇬🇧"]:
        await message.answer("Пожалуйста, выберите язык из предложенных.\nPlease select a language from the list.")
        return

    await state.update_data(language=message.text)
    
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("Inline кнопки", "Обычные кнопки")
    
    text = "Выберите тип кнопок:" if message.text == "Русский 🇷🇺" else "Choose button type:"
    await message.answer(text, reply_markup=keyboard)
    await Form.button_type.set()

# Выбор типа кнопок
@dp.message_handler(state=Form.button_type)
async def process_button_type(message: types.Message, state: FSMContext):
    valid_buttons = ["Inline кнопки", "Обычные кнопки", "Inline buttons", "Regular buttons"]
    if message.text not in valid_buttons:
        await message.answer("Пожалуйста, выберите тип кнопок из предложенных.\nPlease select a button type from the list.")
        return

    data = await state.get_data()
    language = data.get('language', 'Русский 🇷🇺')
    
    if "Inline" in message.text:
        # Inline-кнопки
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton(
            text="Получить ключ 🔑" if language == "Русский 🇷🇺" else "Get key 🔑",
            callback_data="get_key"
        ))
        keyboard.add(types.InlineKeyboardButton(
            text="Автор 👨‍💻" if language == "Русский 🇷🇺" else "Author 👨‍💻",
            url="https://t.me/gixvin"
        ))
        text = "Выберите действие:" if language == "Русский 🇷🇺" else "Choose action:"
        await message.answer(text, reply_markup=keyboard)
    else:
        # Обычные кнопки
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add("Получить ключ 🔑" if language == "Русский 🇷🇺" else "Get key 🔑")
        keyboard.add("Автор 👨‍💻" if language == "Русский 🇷🇺" else "Author 👨‍💻")
        text = "Выберите действие:" if language == "Русский 🇷🇺" else "Choose action:"
        await message.answer(text, reply_markup=keyboard)
    
    await state.finish()

# Обработка кнопки "Получить ключ"
@dp.message_handler(lambda message: message.text in ["Получить ключ 🔑", "Get key 🔑"])
@dp.callback_query_handler(lambda c: c.data == 'get_key')
async def send_key(message_or_query: types.Message | types.CallbackQuery):
    if isinstance(message_or_query, types.CallbackQuery):
        await message_or_query.answer()
        message = message_or_query.message
    else:
        message = message_or_query
    
    key_url = "https://auth.platorelay.com/Yab212lER4VfWNOAJCIlO9i5sTgdnqtx5IBznUKotj6e797%2FcRYIQAqOqhVOe5sZ85nEtMujAjRrxCBghzVAW9KeIjyC4aipj19GLJ3mqRWz5TjgTYjXzREfUnPbak%2BxyOQyQETRaWXuZ3OIVLlI%2FAto2Z%2BrBsRQ7eF%2FOP0oK9bPJN3dI2fuy8QpkpLhylujXGxca3YNurzdf4%2BnoPY52WvD3tppRNm%2BmUuS0%2FCUWg7a0C7sA5FXX6K8KM1xpIrNvmwppSeAhNK%2BogncZI4XUp03JMdjvuCl2OE5pGwatYCgZ8kTmZxFuPLMI90WQgs45DWUiLHE34QFZJCqB9YOQwVHzeqN5VyEmQs8eiWjoDp3aLvLxhlvLD6DjXfimtG3Blo4QO6IRgqP2L2yiruoj4%2BawPYSS1S86yLjr7RJ4HA6pDoonYUTEieToengyS2Nlwi1%2B3genriJUH3keVblawnEiiu95Qp3gOnh3tzFVWgHJl0pZWRKLwmuKZ0%3D"
    await message.answer(f"🔑 Ваш ключ:\n{key_url}" if "Русский" in message.text else f"🔑 Your key:\n{key_url}")

# Обработка кнопки "Автор"
@dp.message_handler(lambda message: message.text in ["Автор 👨‍💻", "Author 👨‍💻"])
async def send_author(message: types.Message):
    await message.answer("👨‍💻 Автор: @gixvin\nTGK: отключено", disable_web_page_preview=True)

# Обработка любых ссылок (аналог /bypass)
@dp.message_handler(regexp=r'https?://[^\s]+')
async def bypass_link(message: types.Message):
    # Здесь можно добавить логику обработки ссылки
    await message.answer("🔗 Ссылка получена! Вот ваш ключ:\nhttps://auth.platorelay.com/...")

# Запуск бота
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
