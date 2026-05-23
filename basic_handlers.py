from aiogram import Router, types, F
from aiogram.filters import CommandStart, Command, state
from database import get_books, check_user, add_user
router = Router()


@router.message(CommandStart())
async def starting(message: types.Message):
    user_id = message.from_user.id
    user_name = message.from_user.full_name
    user_id_exists = check_user(user_id)
    if not user_id_exists:
        add_user(user_id, user_name)
    await message.answer("Bot xususiyatlari: \n"
                         "/books - Kitoblar ro'yxatini ko'rsatadi\n"
                         "/search kitob_nomi - kitob bor yoki yo'qligini tekshiradi.")



@router.message(Command('books'))
async def show_books(message: types.Message):
    books = get_books()
    books = [f"{index}. {book[0]} (Muallif: {book[1]}) - soni: {book[2]}" for index, book in enumerate(books)]
    # books = [f"Kitob nomi: {book}" for book in books]
    await message.answer(f"{'\n'.join(books)}")

# @router.message(Command)