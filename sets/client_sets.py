from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

class FSMAdmin_add(StatesGroup):
    task = State()
class FSMAdmin_remove(StatesGroup):
    task = State()