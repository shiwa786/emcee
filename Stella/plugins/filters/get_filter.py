import re

from pyrogram import filters
from Stella import StellaCli
from Stella.database.filters_mongo import get_filter, get_filters_list
from Stella.helper import custom_filter
from Stella.helper.filters_helper.send_filter_message import SendFilterMessage

@StellaCli.on_message(filters.all & filters.group, group=8)
async def FilterCheckker(client, message):
    if not message.text:
        return
    text = message.text
    chat_id = message.chat.id

    # If 'chat_id' has no filters, simply return
    if len(get_filters_list(chat_id)) == 0:
        return

    ALL_FILTERS = get_filters_list(chat_id)
    
    for filter_ in ALL_FILTERS:
        if (
            message.command
            and message.command[0] == 'filter'
            and len(message.command) >= 2
            and message.command[1] ==  filter_
        ):
            return

        pattern = rf"( |^|[^\w]){re.escape(filter_)}( |$|[^\w])"
        if re.search(pattern, text, flags=re.IGNORECASE):
            filter_name, content, filter_text, data_type = get_filter(chat_id, filter_)
            await SendFilterMessage(
                message=message,
                filter_name=filter_name,
                content=content,
                text=filter_text,
                data_type=data_type
        )
