# -*- coding: utf-8 -*-

# Importamos las librerías necesarias
from telegram.ext import Updater,MessageHandler,Filters,CommandHandler
#from telegram.ext import *

#RSS
from xml.etree import cElementTree
import requests
def parse_meneame_rss():
    
    response = requests.get('https://www.meneame.net/rss')
    parsed_xml = cElementTree.fromstring(response.content)
    items = []
    for node in parsed_xml.iter():
        if node.tag == 'item':
            item = {}
            for item_node in list(node):
                if item_node.tag == 'title':
                    item['title'] = item_node.text
                if item_node.tag == 'link':
                    item['link'] = item_node.text                            

                for source in node.findall('{http://meneame.net/faq-es.php}url'):                    
                    item['fuente'] = source.text

            items.append(item)
    return items[:10]
#####

def ultimas(bot, update):
    items = parse_meneame_rss()
    # for i in items:
    bot.sendMessage(chat_id=update.message.chat_id, text=items[0]['link'])
    bot.sendMessage(chat_id=update.message.chat_id, text=items[0]['fuente'])
    # bot.sendMessage(chat_id=update.message.chat_id, text=items[0]['fuente'])

# Método que imprimirá por pantalla la información que reciba
def listener(bot, update):
    id = update.message.chat_id
    mensaje = update.message.text

    print("ID: " + str(id) + " MENSAJE: " + mensaje)

# Método que utilizaremos para cuando se mande el comando de "start"
def start(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text='¡weuweu!')

# Método que mandará el mensaje "¡Hola, lector de Bytelix!"
def destacadas(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text='¡Hola, lector de Bytelix!')

# Método que mandará el logo de la página
def logo(bot, update):
    # Enviamos de vuelta una foto. Primero indicamos el ID del chat a donde
    # enviarla y después llamamos al método open() indicando la dónde se encuentra
    # el archivo y la forma en que queremos abrirlo (rb = read binary)
    bot.sendPhoto(chat_id=update.message.chat_id, photo=open('Icono.png', 'rb'))

def main():
    # Creamos el Updater, objeto que se encargará de mandarnos las peticiones del bot
    # Por supuesto no os olvidéis de cambiar donde pone "TOKEN" por el token que os ha dado BotFather
    updater = Updater("373475213:AAFfI_HDaWqIrRQzQm2iJ2nFlAmu-RawLGU")

    # Cogemos el Dispatcher, en el cual registraremos los comandos del bot y su funcionalidad
    dispatcher = updater.dispatcher
    
    # Registramos el método que hemos definido antes como listener para que muestre la información de cada mensaje
    listener_handler = MessageHandler(Filters.text, listener)
    dispatcher.add_handler(listener_handler)

    # Ahora registramos cada método a los comandos necesarios
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("destacadas", ultimas))
    dispatcher.add_handler(CommandHandler("logo", logo))

    # Y comenzamos la ejecución del bot a las peticiones
    updater.start_polling()
    updater.idle()

# Llamamos al método main para ejecutar lo anterior
if __name__ == '__main__':
    main()

