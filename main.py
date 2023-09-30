from aiogram import  Dispatcher, Bot, Router
from aiogram.filters.command import Command
from aiogram.types import InlineKeyboardButton, KeyboardButton
from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from aiogram import F
from asyncio import run
from config import API

class Main:

    def __init__(self, token = API) -> None:
        self.dp = Dispatcher()
        self.bt = Bot(token=token)
        self.buttons = ["7","8","9","/",
                        "6","5","4","*",
                        "3","2","1","+",
                        "0",".","=","-"]
        
    def get_keyboards(self):
        kb = InlineKeyboardBuilder()
        for i in self.buttons:
            kb.add(InlineKeyboardButton(text=i, callback_data="op:"+i))
        kb.adjust(4,4,4,4)
        return kb.as_markup(resize_keyboard=True)
    
    async def start_message(self, msg:Message):
        await msg.answer(text="Calculator",reply_markup=self.get_keyboards())


    async def callback_answer(self, clb:CallbackQuery):
        sym = clb.data.split(":")[1]
        txt = clb.message.text
        if sym == "=":
            try:
                txt = str(eval(txt))
            except:
                txt = "Calculator"
        elif txt != "Calculator":
            txt += sym
        else:
            txt = sym
        await clb.message.edit_text(text=txt,reply_markup=self.get_keyboards())
        await clb.answer(text=f"Add new number {txt}")

    def register(self):
        self.dp.message.register(self.start_message,Command("start"))
        self.dp.callback_query.register(self.callback_answer, F.data.startswith("op:"))

    async def start(self):
        self.register()
        try:
            await self.dp.start_polling(self.bt)
        except:
            await self.bt.session.close()

if __name__ == "__main__":
    ob = Main()
    run(ob.start())