import telebot
import os
import codecs
from telebot import types
from functools import wraps
from jinja2 import Template
token = os.getenv('API_BOT_TOKEN')
bot = telebot.TeleBot(token)


def helpCovidInformation_command_handler(message):
    cid =message.chat.id
    with codecs.open('./templates/covid19.html', 'r', encoding='UTF-8') as file:
        template = Template(file.read())
    mkinfo=telebot.types.InlineKeyboardMarkup()
    mkinfo.row(
        telebot.types.InlineKeyboardButton(text='💉Вакцинація', callback_data='vaccination'),
        telebot.types.InlineKeyboardButton(text='🚫Зони', callback_data='zones'),
        telebot.types.InlineKeyboardButton(text='🩸 Симптоми', callback_data='symptoms')
           )
    mkinfo.add( telebot.types.InlineKeyboardButton(text='♨ Новини',callback_data='news'))
    bot.send_message(cid,template.render(user_name=message.chat.username), parse_mode='HTML', reply_markup=mkinfo)

@bot.message_handler(commands=['covidnews'])
def helpCovidNews_command_handler(message):
    cid = message.chat.id
    with codecs.open('templates/newsCovid.html', 'r', encoding='UTF-8') as file:
        template = Template(file.read())
    markupurl = types.InlineKeyboardMarkup()
    btn_site_1 = types.InlineKeyboardButton(text='Obozrevatel →',
                                             url='https://www.obozrevatel.com/topic/koronavirus-2019-ncov/?_gl=1*v9fmcc*_ga*MTc4NzkxMTA1NC4xNjM5OTM3OTI4*_ga_JBX3X27G7H*MTYzOTkzNzkyNi4xLjEuMTYzOTkzNzk3OS4w&_ga=2.85707673.164119684.1639937960-1787911054.1639937928')
    btn_site_2 = types.InlineKeyboardButton(text='Украинская правда →',
                                            url='https://www.pravda.com.ua/rus/tags/koronavirus/')
    btn_site_3 = types.InlineKeyboardButton(text='ТСН →',
                                            url='https://coronavirus.tsn.ua/')
    btn_site_4 = types.InlineKeyboardButton(text='Цензор.NET →',
                                            url='https://censor.net/ru/tag/9099/covid19/news/page/1')
    markupurl.add(btn_site_1)
    markupurl.add(btn_site_2)
    markupurl.add(btn_site_3)
    markupurl.add(btn_site_4)
    markupurl.row(
        telebot.types.InlineKeyboardButton(text='↩Повернутися', callback_data='nazadinfo'),
        telebot.types.InlineKeyboardButton(text='📲Меню', callback_data='menu')
    )

    bot.send_message(cid, template.render(user_name=message.chat.username), parse_mode='HTML',reply_markup=markupurl)


@bot.message_handler(commands=['helpcovid'])
def helpCovidVaccination_command_handler(message):
    cid = message.chat.id
    with codecs.open('templates/helpcovid1.html', 'r', encoding='UTF-8') as file:
        template = Template(file.read())
    markup = telebot.types.InlineKeyboardMarkup()
    markup.row(
        telebot.types.InlineKeyboardButton(text='💉Pfizer', callback_data='Pfizer'),
        telebot.types.InlineKeyboardButton(text='💉Coronavac', callback_data='Coronavac'),
        telebot.types.InlineKeyboardButton(text='💉Moderna', callback_data='Moderna'),
        telebot.types.InlineKeyboardButton(text='💉AstraZeneca', callback_data='AstraZeneca')
    )
    bot.send_message(cid, template.render(user_name=message.chat.username), parse_mode='HTML',reply_markup=markup)

def helpcovidPfizer_command_handler(message):
    cid=message.chat.id
    with codecs.open('templates/helpCovidPfizer.html', 'r', encoding='UTF-8') as file:
        template = Template(file.read())
    markupurl1 = types.InlineKeyboardMarkup()
    btn_my_site = types.InlineKeyboardButton(text='Докладніше про вакцину →',
                                             url='https://vaccination.covid19.gov.ua/articles/pfizer')
    markupurl1.add(btn_my_site)
    bot.send_message(cid, template.render(user_name=message.chat.username), parse_mode='HTML',reply_markup=markupurl1)

def helpcovidCoronavac_command_handler(message):
    cid=message.chat.id
    with codecs.open('templates/helpCovidCoronavac.html', 'r', encoding='UTF-8') as file:
        template = Template(file.read())
    markupurl2 = types.InlineKeyboardMarkup()
    btn_my_site = types.InlineKeyboardButton(text='Докладніше про вакцину →',
                                             url='https://vaccination.covid19.gov.ua/articles/sinovac')
    markupurl2.add(btn_my_site)
    bot.send_message(cid, template.render(user_name=message.chat.username), parse_mode='HTML', reply_markup=markupurl2)


def helpcovidModerna_command_handler(message):
    cid=message.chat.id
    with codecs.open('templates/helpCovidModerna.html', 'r', encoding='UTF-8') as file:
        template = Template(file.read())
    markupurl3 = types.InlineKeyboardMarkup()
    btn_my_site = types.InlineKeyboardButton(text='Докладніше про вакцину →',
                                             url='https://vaccination.covid19.gov.ua/articles/moderna')
    markupurl3.add(btn_my_site)
    bot.send_message(cid, template.render(user_name=message.chat.username), parse_mode='HTML', reply_markup=markupurl3)


def helpcovidAstraZeneca_command_handler(message):
    cid=message.chat.id
    with codecs.open('templates/helpCovidAstraZeneca.html', 'r', encoding='UTF-8') as file:
        template = Template(file.read())
    markupurl4 = types.InlineKeyboardMarkup()
    btn_my_site = types.InlineKeyboardButton(text='Докладніше про вакцину →',
                                             url='https://vaccination.covid19.gov.ua/articles/astrazeneca')
    markupurl4.add(btn_my_site)
    bot.send_message(cid, template.render(user_name=message.chat.username), parse_mode='HTML', reply_markup=markupurl4)

def helpCovidVZones_command_handler(message):
    cid = message.chat.id
    with codecs.open('templates/covidZones.html', 'r', encoding='UTF-8') as file:
        template = Template(file.read())
        markuozones=types.InlineKeyboardMarkup()
        markuozones.row(
            telebot.types.InlineKeyboardButton(text='🟢Зелений', callback_data='green1'),
            telebot.types.InlineKeyboardButton(text='🟡	Жовтий', callback_data='yellow'),
            telebot.types.InlineKeyboardButton(text='🟠Помаранчевий ', callback_data='orange'),
            telebot.types.InlineKeyboardButton(text='🔴Червоний', callback_data='red')
        )
    bot.send_message(cid, template.render(user_name=message.chat.username), parse_mode='HTML', reply_markup=markuozones)

def helpCovidVZonesGreen_command_handler(message):
    cid = message.chat.id
    with codecs.open('templates/covidZonesGreen.html', 'r', encoding='UTF-8') as file:
        template = Template(file.read())
    markupg = types.InlineKeyboardMarkup()
    #btn_my_site=types.KeyboardButton("фото")
    #markupg.add(btn_my_site)
    markupg.row(
        telebot.types.InlineKeyboardButton(text='↩Повернутися', callback_data='nazadzones'),
        telebot.types.InlineKeyboardButton(text='📲Меню', callback_data='menu')
    )
    bot.send_photo(cid, 'https://covid19.gov.ua/images/photo_2021-09-14_16-32-27_2.jpg')
    bot.send_message(cid, template.render(user_name=message.chat.username), parse_mode='HTML',
                     reply_markup=markupg)




def helpCovidVZonesYellow_command_handler(message):
    cid = message.chat.id
    with codecs.open('templates/covidZonesYellow.html', 'r', encoding='UTF-8') as file:
        template = Template(file.read())
    markupg =  types.InlineKeyboardMarkup()
    #btn_my_site=types.KeyboardButton("фото")
    #markupg.add(btn_my_site)
    markupg.row(
        telebot.types.InlineKeyboardButton(text='↩Повернутися', callback_data='nazadzones'),
        telebot.types.InlineKeyboardButton(text='📲Меню', callback_data='menu')
    )
    bot.send_photo(cid, 'https://covid19.gov.ua/images/sources_info/%D0%B6%D0%BE%D0%B2%D1%82%D0%B8%D0%B8%CC%86_%D1%80%D1%96%D0%B2%D0%B5%D0%BD%D1%8C.jpg')
    bot.send_message(cid, template.render(user_name=message.chat.username), parse_mode='HTML',
                     reply_markup=markupg)

def helpCovidVZonesOrange_command_handler(message):
    cid = message.chat.id
    with codecs.open('templates/covidZonesOrange.html', 'r', encoding='UTF-8') as file:
        template = Template(file.read())
    markupg = types.InlineKeyboardMarkup()
    #btn_my_site=types.KeyboardButton("фото")
    #markupg.add(btn_my_site)
    markupg.row(
        telebot.types.InlineKeyboardButton(text='↩Повернутися', callback_data='nazadzones'),
        telebot.types.InlineKeyboardButton(text='📲Меню', callback_data='menu')
    )
    # bot.send_photo(cid, 'https://covid19.gov.ua/images/sources_info/%D1%80%D1%96%D0%B2%D0%BD%D1%96_%D1%87%D0%B5%D1%80%D0%B2%D0%BE%D0%BD%D0%B8%D0%B8%CC%86.jpg')
    bot.send_message(cid, template.render(user_name=message.chat.username), parse_mode='HTML',
                     reply_markup=markupg)


def helpCovidVZonesRed_command_handler(message):
    cid = message.chat.id
    with codecs.open('templates/covidZonesRed.html', 'r', encoding='UTF-8') as file:
        template = Template(file.read())
    markupg = types.InlineKeyboardMarkup()
    #btn_my_site=types.KeyboardButton("фото")
    #markupg.add(btn_my_site)
    markupg.row(
        telebot.types.InlineKeyboardButton(text='↩Повернутися', callback_data='nazadzones'),
        telebot.types.InlineKeyboardButton(text='📲Меню', callback_data='menu')
    )
    bot.send_photo(cid,'https://covid19.gov.ua/images/sources_info/%D1%80%D1%96%D0%B2%D0%BD%D1%96_%D1%87%D0%B5%D1%80%D0%B2%D0%BE%D0%BD%D0%B8%D0%B8%CC%86.jpg')
    bot.send_message(cid, template.render(user_name=message.chat.username), parse_mode='HTML',
                     reply_markup=markupg)



def helpCovidSymptoms(message):
    cid = message.chat.id
    with codecs.open('templates/symptoms.html', 'r', encoding='UTF-8') as file:
        template = Template(file.read())
    bot.send_message(cid, template.render(user_name=message.chat.username), parse_mode='HTML')
