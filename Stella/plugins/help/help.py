#    Stella (Development)
#    Copyright (C) 2021 - meanii (Anil Chauhan)
#    Copyright (C) 2021 - SpookyGang (Neel Verma, Anil Chauhan)

#    This program is free software; you can redistribute it and/or modify 
#    it under the terms of the GNU General Public License as published by 
#    the Free Software Foundation; either version 3 of the License, or 
#    (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.

#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

import html
import re

from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from Stella import BOT_USERNAME, StellaCli
from Stella.__main__ import HELPABLE, SUB_MODE
from Stella.helper import custom_filter
from Stella.helper.pagination_buttons import paginate_modules

HELP_TEXT = (
    "Here you can find information regarding how to use me. I'll guide you through all the modules I have to offer.\n\n"
    "» If you encounter any bugs, please feel free to report them in my support chat - @Elisha_support ^^"
)

async def help_parser(client, chat_id, text, keyboard=None):
    if not keyboard:
        keyboard = InlineKeyboardMarkup(paginate_modules(0, HELPABLE, "help"))
    await client.send_message(chat_id, text, reply_markup=keyboard)


@StellaCli.on_message(custom_filter.command(commands=('help')))
async def help_command(client, message):

    module_name = None
    if len(message.command) >= 2:
        module_name = message.command[1].lower()

    if message.chat.type != "private":

        button_text = 'Click me here for help!'
        text = 'Contact me in PM for help!'
        redirect_url = f"t.me/{BOT_USERNAME}?start=help_"

        if module_name is not None:

            try:
                module_name = HELPABLE[module_name].__mod_name__
                text = f"Help for `{module_name.capitalize()}` module!" 
                button_text = 'Click here!'
                redirect_url = f"t.me/{BOT_USERNAME}?start=help_{module_name.lower()}"
            except KeyError:
                pass
        
        buttons = InlineKeyboardMarkup(
            [[InlineKeyboardButton(text=button_text, url=redirect_url)]])
        await message.reply(text, reply_markup=buttons)
    else:
        if module_name is not None:
            await module_page(message, module=module_name)
        else:
            await help_parser(client, message.chat.id, HELP_TEXT)


@StellaCli.on_message(custom_filter.command('start'), group=9)
async def redirectHelp(client, message):
    if (
        len(message.command) >= 2
        and message.command[1].split('_')[0] == 'help'
    ):
        if len(message.command) >= 2:
            module_name = message.command[1].split('_')[1]
            await module_page(message, module=module_name)
        else:
            await help_parser(StellaCli, message.chat.id, HELP_TEXT)

async def help_button_callback(_, __, callback_query):
    if re.match(r"help_", callback_query.data):
        return True


@StellaCli.on_callback_query(filters.create(help_button_callback))
async def help_button(client, callback_query):
    print(callback_query.data)
    mod_match = re.match(r"help_module\((.+?)\)", callback_query.data)
    back_match = re.match(r"help_back", callback_query.data)
    if mod_match:
        module = mod_match.group(1)
        text = f"**{HELPABLE[module].__mod_name__}**\n\n"
        text += HELPABLE[module].__help__
        buttons = []
        button = []
        try:
            for sub_mod in SUB_MODE[module].__sub_mod__:
                button.append(InlineKeyboardButton(text=sub_mod, callback_data=f'help_module({sub_mod.lower()})'))
                if len(button) >= 2:
                    buttons.append(button)
                    button = []
            if button:
                buttons.append(button)
        except KeyError:
            pass
        buttons.append(
            [InlineKeyboardButton(text='Back ', callback_data="help_back")]
        )
        await callback_query.message.edit(
            text=html.escape(text),
            reply_markup=InlineKeyboardMarkup(buttons)
        )

    elif back_match:
        await callback_query.message.edit(text=HELP_TEXT,
                    reply_markup=InlineKeyboardMarkup(paginate_modules(0, HELPABLE, "help")))

async def module_page(module: str, message: str = None):
    button = []
    buttons = []
    try:
        text = f"**{HELPABLE[module].__mod_name__}**\n\n"
        text += HELPABLE[module].__help__

        for sub_mod in SUB_MODE[module].__sub_mod__:
                button.append(InlineKeyboardButton(text=sub_mod, callback_data=f'help_module({sub_mod.lower()})'))
                if len(button) >= 2:
                    buttons.append(button)
                    button = []
        if button:
            buttons.append(button)
            
    except KeyError:
        await help_parser(StellaCli, message.chat.id, HELP_TEXT)
        return 

    buttons.append(
            [InlineKeyboardButton(text='Back ', callback_data="help_back")]
        )

    await message.reply(
        text=html.escape(text),
        reply_markup=InlineKeyboardMarkup(buttons),
        quote=True
)
