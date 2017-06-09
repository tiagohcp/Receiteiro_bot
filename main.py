import telegram
import json
from converte import *
from getAPI import *
from telegram.ext import * #Updater, CommandHandler, MessageHandler, Filters, InlineQueryHandler

texto = ""
chat = {}


#Conectando a API do Telegram
updater = Updater(token="346890741:AAEbcXsZx6Nt4DLCR1KOSei-NAn1TwknzuU")
dispatcher = updater.dispatcher

def start(bot, update): #Inicia o Bot
    me = bot.get_me()
    msg = "Escolha um comando: \n /support \n /settings \n /buscar"

    main_menu_keyboard = [[telegram.KeyboardButton('/support')],
                          [telegram.KeyboardButton('/settings')],
                          [telegram.KeyboardButton('/help')],
                          [telegram.KeyboardButton('/buscar')]]
    reply_kb_markup = telegram.ReplyKeyboardMarkup(main_menu_keyboard,
                                                   resize_keyboard=True,
                                                   one_time_keyboard=True)

    bot.send_message(chat_id=update.message.chat_id,
                     text=msg,
                     reply_markup=reply_kb_markup)

    

def buscar(bot,update): #Abre a busca por receitas
    msg = "Digite a receita ou ingrediente que deseja buscar:"
    bot.send_message(chat_id=update.message.chat_id,
                     text=msg)
    

def pesquisar(bot,update): #Pesquisa por lista de receitas ou uma determinada receita
    global texto, chat
    usuario = update.message.chat_id
    vetor = {}
    maxi = 10
    cont = 0
    ini = 0

    texto = update.message.text
    
    try: #Caso seja informado o ID da receita chama a função para mostrar a receita escolhida
        index = int(texto)
        resp = converte(texto)
        bot.sendPhoto(chat_id=update.message.chat_id,
                             photo=resp[1])
        bot.send_message(chat_id=update.message.chat_id,
                             text=resp[0])       
    except ValueError as ex: #Caso seja um ingrediente formata a pesquisa e chama 10 vezes a funcão que mostra as receitas possiveis
        texto=texto.replace(' ','+')
        msg = converteLista(texto,0)
        if msg[1] == 0:
            bot.send_message(chat_id=update.message.chat_id,
                         text="Pesquisa sem resultados. Por favor igite outra receita ou ingrediente que deseja buscar:")
        else:
            bot.sendPhoto(chat_id=update.message.chat_id,photo=msg[1])
            bot.send_message(chat_id=update.message.chat_id,
                             text=msg[0])
        vetor[0] = msg
        maxi = msg[2]
        for j in range(1,maxi):
            msg = converteLista(texto,j)
            if msg[1] == 0:
                bot.send_message(chat_id=update.message.chat_id,
                             text="Pesquisa sem resultados. Por favor digite outra receita ou ingrediente que deseja buscar:")
                break
            elif msg[1] == 1:
                break
            else:
                if j < 10:
                    bot.sendPhoto(chat_id=update.message.chat_id,photo=msg[1])
                    bot.send_message(chat_id=update.message.chat_id,
                                 text=msg[0])
            vetor[j] = msg
                

        if msg[1] != 0:
            cont = 10
            maximo = j
            chat[usuario]=[vetor, cont, ini, maximo]

            keyboard = [[telegram.InlineKeyboardButton("Anteriores", callback_data='1')],
                        [telegram.InlineKeyboardButton("Próximos", callback_data='2')]
            ]
            reply_markup = telegram.InlineKeyboardMarkup(keyboard)
            update.message.reply_text('Informe o ID da receita desejada ou escolha uma opção:', reply_markup=reply_markup)
    

                               
def button(bot,update):
    
    query = update.callback_query

    resp = query.data
  
    if resp == "1":
        update.callback_query.message.text='/ant'
        ant(bot,update)
        
    elif resp == "2":
        update.callback_query.message.text='/prox'
        prox(bot,update)

                          
                    
def ant(bot, update):
    global chat
    usuario = update.callback_query.message.chat_id
    vetor = chat[usuario][0]
    cont = chat[usuario][1]
    ini = chat[usuario][2]
    if ini-10 < 0:
        mini = 0
    else:
        mini = ini-10
    for j in range(mini,ini):
        msg = vetor[j]
        bot.sendPhoto(chat_id=update.callback_query.message.chat_id,
                                 photo=msg[1])
        bot.send_message(chat_id=update.callback_query.message.chat_id,
                                 text=msg[0])
    chat[usuario][2] = mini
    chat[usuario][1] = j + 1

    keyboard = [[telegram.InlineKeyboardButton("Anteriores", callback_data='1')],
                [telegram.InlineKeyboardButton("Próximas", callback_data='2')]
                ]
    reply_markup = telegram.InlineKeyboardMarkup(keyboard)
    update.callback_query.message.reply_text('Informe o ID da receita desejada ou escolha uma opção:', reply_markup=reply_markup)
           

def prox(bot, update):
    global chat
    usuario = update.callback_query.message.chat_id
    vetor = chat[usuario][0]
    cont = chat[usuario][1]
    ini = chat[usuario][2]
    maximo = chat[usuario][3]
    chat[usuario][2] = cont
    for j in range(cont,min(cont+10,maximo)):
        msg = vetor[j]
        bot.sendPhoto(chat_id=update.callback_query.message.chat_id,
                            photo=msg[1])
        bot.send_message(chat_id=update.callback_query.message.chat_id,
                            text=msg[0])
    
    chat[usuario][1] = j + 1

    keyboard = [[telegram.InlineKeyboardButton("Anteriores", callback_data='1')],
                [telegram.InlineKeyboardButton("Próximas", callback_data='2')]
                ]
    reply_markup = telegram.InlineKeyboardMarkup(keyboard)
    update.callback_query.message.reply_text('Informe o ID da receita desejada ou escolha uma opção:', reply_markup=reply_markup)
#*******callback_query.************


def receita_escolhida(bot, update): #Testa se o comando é uma ID ou um comando invalido
    texto = update.message.text
    #Se o comando é um ID chama a função converte para exibir a receita
    if texto[0:4] == "/id_":
        resp = converte(texto[4:])
        bot.sendPhoto(chat_id=update.message.chat_id,
                             photo=resp[1])
        bot.send_message(chat_id=update.message.chat_id,
                             text=resp[0])
    #Caso seja um comando inexistenta avisa o usuario do ocorrido 
    else:
        msg = "Comando invalido."
        bot.send_message(chat_id=update.message.chat_id,
                     text=msg)
        
#Criação e inicio dos Handler
start_handler = CommandHandler("start", start)
#help_handler = CommandHandler("help", help)
#support_handler = CommandHandler("support", support)
buscar_handler = CommandHandler("buscar", buscar)
pesquisar_handler = MessageHandler((Filters.text), pesquisar)
receita_escolhida_handler = MessageHandler((Filters.command),receita_escolhida)
button_CQHandler = CallbackQueryHandler(button)
dispatcher.add_handler(button_CQHandler)
dispatcher.add_handler(pesquisar_handler)
dispatcher.add_handler(start_handler)
#dispatcher.add_handler(help_handler)
dispatcher.add_handler(buscar_handler)
#dispatcher.add_handler(support_handler)
dispatcher.add_handler(receita_escolhida_handler)

prox_handler = CommandHandler("prox", prox)
dispatcher.add_handler(prox_handler)
ant_handler = CommandHandler("ant", ant)
dispatcher.add_handler(ant_handler)


updater.start_polling()









