from telegram import Update
from telegram.ext import filters, ContextTypes, MessageHandler, filters
from ..Utils.runtime_manager import rtm
from ..Utils.llm.filter_chain import filter_chain


async def filter_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = rtm.chat_lookup(update.effective_chat.id)
    if chat == None:
        return
    filters_repr = chat.repr_filters()

    fchain = filter_chain()
    llm_response = fchain(inputs={
        'message': update.message.text,
        'filters': filters_repr
    })

    filter_id_list = llm_response['text'].filters
    filter_list = [chat.filter_lookup(filter.filter_id)
                   for filter in filter_id_list]
    for f in filter_list:
        sublist = '\n'.join(f'@{sub}' for sub in f.subscribers)
        await update.message.reply_text(f"{sublist}\nFilter: {f.text}")


filter_message = MessageHandler(
    filters.TEXT & (~filters.COMMAND), filter_message)
