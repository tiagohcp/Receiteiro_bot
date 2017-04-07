import telegram
from converte import *
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters


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
        for j in range(10):
            msg = converteLista(texto)
            bot.sendPhoto(chat_id=update.message.chat_id,
                             photo=msg[1])
            bot.send_message(chat_id=update.message.chat_id,
                             text=msg[0])
        #text = "Digite o ID da receita desejada:"
        bot.send_message(chat_id=update.message.chat_id,
                             text="Informe o ID da receita desejada:")
        


def unknown(bot, update): #Texta se o comando é uma ID ou um comando invalido
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
unknown_handler = MessageHandler((Filters.command),unknown)
dispatcher.add_handler(pesquisar_handler)
dispatcher.add_handler(start_handler)
#dispatcher.add_handler(help_handler)
dispatcher.add_handler(buscar_handler)
#dispatcher.add_handler(support_handler)
dispatcher.add_handler(unknown_handler)




"""na formatação: /id_ + receitas[id]
   no unknown testa txt.[0:3] = /id_""" 







