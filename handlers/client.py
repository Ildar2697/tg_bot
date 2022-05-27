from aiogram import types, Dispatcher
from create_bot import dp, Bot
from aiogram.dispatcher import FSMContext
from sets.client_sets import FSMAdmin_add, FSMAdmin_remove
from database.db import connect_db, save_task, del_task, show_tasks

async def command_start(message: types.Message):
    strings_list = [
        "To add task send /add",
        "To remove task send /remove",
        "To watch list of tasks send /tasks"
    ]
    await message.answer('\n'.join(strings_list))

async def command_add(message: types.Message):
    await FSMAdmin_add.task.set()
    await message.answer("Enter a task's name to add")

async def task_add(message: types.Message, state=FSMContext):
    await FSMAdmin_add.task.set()
    answer = message.text
    await state.update_data(task1=answer)
    await message.answer('Task successfully added to list!')
    print(answer)
    print(message.from_user.id)
    connection = connect_db()
    save_task(connection, message.from_user.id, answer)
    await state.finish()


async def command_remove(message: types.Message):
    await message.answer("Enter a task's name to remove")
    await FSMAdmin_remove.task.set()

async def task_remove(message: types.Message, state=FSMContext):
    await FSMAdmin_remove.task.set()
    answer = message.text
    await state.update_data(task1=answer)
    await message.answer('Task removed from list!')
    # print(answer)
    # print(message.from_user.id)
    connection = connect_db()
    del_task(connection, answer)
    await state.finish()

async def tasks(message: types.Message):
    connection = connect_db()
    result = show_tasks(connection, message.from_user.id)
    tasks_list = []
    for el in result:
        tasks_list.append(el[0])
    await message.answer('Your tasks: ')
    await message.answer('\n'.join(tasks_list))
    await message.answer('Send command /remove to delete task from list')
    # print(result)


# async def command_list(message: types.Message):




# async def echo_send(message:types.Message):
#     await message.answer(message.text)

def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=['start'])
    dp.register_message_handler(command_add, commands=['add'])
    dp.register_message_handler(command_remove, commands=['remove'])
    dp.register_message_handler(task_add, state=FSMAdmin_add.task)
    dp.register_message_handler(task_remove, state=FSMAdmin_remove.task)
    dp.register_message_handler(tasks, commands=['tasks'])