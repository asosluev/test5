import threading
from sched import scheduler

import telebot
import os
import codecs

import common.tg_analytics as tga
import country.country
import vacc.covid
from functools import wraps
from telebot import types
from jinja2 import Template
from services.country_service import CountryService
from services.statistics_service import StatisticsService
from flask import Flask, request

#from dotenv import load_dotenv

#load_dotenv()


# bot initialization
token = os.getenv('API_BOT_TOKEN')
bot = telebot.TeleBot(token)
user_steps = {}
known_users = []
stats_service = StatisticsService()
country_service = CountryService()
commands = {'start': 'Запуск бота',
            'country': 'Написати країну по якій потрвбна інформація (мова: англійська)',
            'statistics': 'Статистика бота',
            'help': 'Команди які вміє використовувати бот',
            'contacts': 'Контакти розробника',
            'countryLocation': 'Вибрати локацію де потрібна інформація по Covid-19',
            'helpcovid': 'Інформація про Covid-19'
            }
def get_user_step(uid):
    if uid in user_steps:
        return user_steps[uid]
    else:
        known_users.append(uid)
        user_steps[uid] = 0
        return user_steps[uid]


# decorator for bot actions
def send_action(action):
    def decorator(func):
        @wraps(func)
        def command_func(message, *args, **kwargs):
            bot.send_chat_action(chat_id=message.chat.id, action=action)
            return func(message, *args, **kwargs)
        return command_func
    return decorator


# decorator for save user activity
def save_user_activity():
    def decorator(func):
        @wraps(func)
        def command_func(message, *args, **kwargs):
            tga.statistics(message.chat.id, message.text)
            return func(message, *args, **kwargs)
        return command_func
    return decorator


# start command handler
@bot.message_handler(commands=['start'])
@send_action('typing')
@save_user_activity()
def start_command_handler(message):
    cid = message.chat.id
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton(text='🤷‍♂Допомога!🤷‍♀', callback_data=1))
    markup.add(telebot.types.InlineKeyboardButton(text='🚨Статистика користувачів!🚨', callback_data=2))
    markup.add(telebot.types.InlineKeyboardButton(text='🎫Контакти!', callback_data=3))
    markup.add(telebot.types.InlineKeyboardButton(text='🌐Початок!🌐', callback_data=4))
    markup.add(telebot.types.InlineKeyboardButton(text='🔥Covid-19🔥', callback_data=7))
    markup.add(telebot.types.InlineKeyboardButton(text='🏥Місце для Вакцинации', callback_data=9))
    markup.add(telebot.types.InlineKeyboardButton(text='📊 Вибір країни!🗺', callback_data=5))
    markup.add(telebot.types.InlineKeyboardButton(text='🧭Відправти геолокацію!', callback_data=6))
    bot.send_message(cid, 'Привіт, {0}, Виберіть команду з меню'.format(message.chat.username),reply_markup=markup)

#menu


def menu_command_handler(message):
    cid = message.chat.id
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton(text='🤷‍♂Допомога!🤷‍♀', callback_data=1))
    markup.add(telebot.types.InlineKeyboardButton(text='🚨Статистика користувачів!🚨', callback_data=2))
    markup.add(telebot.types.InlineKeyboardButton(text='🎫Контакти!', callback_data=3))
    markup.add(telebot.types.InlineKeyboardButton(text='🌐Початок!🌐', callback_data=4))
    markup.add(telebot.types.InlineKeyboardButton(text='🔥Covid-19🔥', callback_data=7))
    markup.add(telebot.types.InlineKeyboardButton(text='🏥Місце для Вакцинации', callback_data=9))
    markup.add(telebot.types.InlineKeyboardButton(text='📊 Вибір країни!🗺', callback_data=5))
    markup.add(telebot.types.InlineKeyboardButton(text='🧭Відправти геолокацію!', callback_data=6))
    bot.send_message(cid, '{0}, Виберіть команду з меню'.format(message.chat.username), reply_markup=markup)

@bot.message_handler(commands=['country'])
@send_action('typing')
@save_user_activity()
def country_command_handler(message):
    cid = message.chat.id
    user_steps[cid] = 1
    bot.send_message(cid, '{0}, write name of country please'.format(message.chat.username))

def locationVaccination(message):
    cid = message.chat.id
    with codecs.open('templates/locationVaccination.html', 'r', encoding='UTF-8') as file:
        template = Template(file.read())

    markup = types.InlineKeyboardMarkup()
    markup.row(
        telebot.types.InlineKeyboardButton(text='Coronavac', callback_data='CoronavacVac'),
        telebot.types.InlineKeyboardButton(text='Pfizer', callback_data='PfizerVac'),
        telebot.types.InlineKeyboardButton(text='AstraZeneca ', callback_data='AstraZenecaVac'),
        telebot.types.InlineKeyboardButton(text='Moderna', callback_data='ModernaVac')
    )
    bot.send_message(cid, template.render(user_name=message.chat.username), parse_mode='HTML', reply_markup=markup)

def locationVaccinationCoronavac(message):
    cid = message.chat.id
    with codecs.open('templates/LocationVaccination/Coronovac.html', 'r', encoding='UTF-8') as file:
        template = Template(file.read())
    markupVacUrl = types.InlineKeyboardMarkup()
    markupVacUrl.row(
        telebot.types.InlineKeyboardButton(text='🎥 кінотеатр ім. Щорса',
                                           url='https://goo.gl/maps/KHXb4qSVHrjgiVWi6'),
        telebot.types.InlineKeyboardButton(text='🏰ТЦ «Голлівуд»',
                                           url='https://goo.gl/maps/An88CJRujdSza97i8'),
        telebot.types.InlineKeyboardButton(text='🏚 Деснянська районна рада',
                                           url='https://goo.gl/maps/ggmdATf7fhUBRgiZA')
      )
    markupVacUrl.row(
        telebot.types.InlineKeyboardButton(text='🏥 Сімейна поліклініка',
                                           url='https://goo.gl/maps/hJZCqwLSjTSSK8xZ6'),
        telebot.types.InlineKeyboardButton(text='🏥 3 поліклінічне відділення',
                                           url='https://goo.gl/maps/xpkmx3nK6e5Pd8gf7'),
        telebot.types.InlineKeyboardButton(text='🏥 Первична медича допомога (МАСАНИ)',
                                           url='https://goo.gl/maps/sFfcZEeAifk89Ae37')
    )
    markupVacUrl.row(
        telebot.types.InlineKeyboardButton(text='🏥 Первична медича допомога (ПОДУСОВКА)',
                                           url='https://goo.gl/maps/MdBnwuApFYrDg1WH7'),

    )
    markupVacUrl.row(
        telebot.types.InlineKeyboardButton(text='↩Повернутися', callback_data='nazadvacc'),
        telebot.types.InlineKeyboardButton(text='📲Меню', callback_data='menu')
    )
    bot.send_message(cid, template.render(user_name=message.chat.username), parse_mode='HTML',reply_markup=markupVacUrl)

def locationVaccinationPfizer(message):
    cid = message.chat.id
    with codecs.open('templates/LocationVaccination/Pfizer.html', 'r', encoding='UTF-8') as file:
        template = Template(file.read())
    markupVacUrl = types.InlineKeyboardMarkup()
    markupVacUrl.row(
        telebot.types.InlineKeyboardButton(text='🎥 кінотеатр ім. Щорса',
                                           url='https://goo.gl/maps/KHXb4qSVHrjgiVWi6'),
        telebot.types.InlineKeyboardButton(text='🏰 ТЦ «Голлівуд»',
                                           url='https://goo.gl/maps/An88CJRujdSza97i8'),
        telebot.types.InlineKeyboardButton(text='🏚 Деснянська районна рада',
                                           url='https://goo.gl/maps/ggmdATf7fhUBRgiZA')
    )
    markupVacUrl.row(
        telebot.types.InlineKeyboardButton(text='🏤 Чернігівська обласна рада',
                                           url='https://goo.gl/maps/CYStyVqazADUdqVW9'),
        telebot.types.InlineKeyboardButton(text='🏰 ТЦ ЦУМ',
                                           url='https://g.page/tsum-chernihiv?share')
    )
    markupVacUrl.row(
        telebot.types.InlineKeyboardButton(text='🏥 Сімейна поліклініка',
                                           url='https://goo.gl/maps/hJZCqwLSjTSSK8xZ6'),
        telebot.types.InlineKeyboardButton(text='🏥 3 поліклінічне відділення',
                                           url='https://goo.gl/maps/xpkmx3nK6e5Pd8gf7'),
        telebot.types.InlineKeyboardButton(text='🏥 Первична медича допомога (МАСАНИ)',
                                           url='https://goo.gl/maps/sFfcZEeAifk89Ae37')
    )
    markupVacUrl.row(
        telebot.types.InlineKeyboardButton(text='🏥 Первична медича допомога (ПОДУСОВКА)',
                                           url='https://goo.gl/maps/MdBnwuApFYrDg1WH7'),

    )
    markupVacUrl.row(
        telebot.types.InlineKeyboardButton(text='↩Повернутися', callback_data='nazadvacc'),
        telebot.types.InlineKeyboardButton(text='📲Меню', callback_data='menu')
    )
    bot.send_message(cid, template.render(user_name=message.chat.username), parse_mode='HTML',reply_markup=markupVacUrl)

def locationVaccinationModerna(message):
    cid = message.chat.id
    with codecs.open('templates/LocationVaccination/Moderna.html', 'r', encoding='UTF-8') as file:
        template = Template(file.read())
    markupVacUrl = types.InlineKeyboardMarkup()
    markupVacUrl.row(
        telebot.types.InlineKeyboardButton(text='🏥 Сімейна поліклініка',
                                           url='https://goo.gl/maps/hJZCqwLSjTSSK8xZ6'),
        telebot.types.InlineKeyboardButton(text='🏥 3 поліклінічне відділення',
                                           url='https://goo.gl/maps/xpkmx3nK6e5Pd8gf7'),
        telebot.types.InlineKeyboardButton(text='🏥 Первична медича допомога (МАСАНИ)',
                                           url='https://goo.gl/maps/sFfcZEeAifk89Ae37')
    )
    markupVacUrl.row(
        telebot.types.InlineKeyboardButton(text='🏥 Первична медича допомога (ПОДУСОВКА)',
                                           url='https://goo.gl/maps/MdBnwuApFYrDg1WH7'),

    )
    markupVacUrl.row(
        telebot.types.InlineKeyboardButton(text='↩Повернутися', callback_data='nazadvacc'),
        telebot.types.InlineKeyboardButton(text='📲Меню', callback_data='menu')
    )
    bot.send_message(cid, template.render(user_name=message.chat.username), parse_mode='HTML',reply_markup=markupVacUrl)

def locationVaccinationAstraZeneca(message):
    cid = message.chat.id
    with codecs.open('templates/LocationVaccination/AstraZeneca.html', 'r', encoding='UTF-8') as file:
        template = Template(file.read())
    markupVacUrl = types.InlineKeyboardMarkup()
    markupVacUrl.row(
        telebot.types.InlineKeyboardButton(text='🏥 Сімейна поліклініка',
                                           url='https://goo.gl/maps/hJZCqwLSjTSSK8xZ6'),
        telebot.types.InlineKeyboardButton(text='🏥 3 поліклінічне відділення',
                                           url='https://goo.gl/maps/xpkmx3nK6e5Pd8gf7'),
        telebot.types.InlineKeyboardButton(text='🏥 Первична медича допомога (МАСАНИ)',
                                           url='https://goo.gl/maps/sFfcZEeAifk89Ae37')
    )
    markupVacUrl.row(
        telebot.types.InlineKeyboardButton(text='🏥 Первична медича допомога (ПОДУСОВКА)',
                                           url='https://goo.gl/maps/MdBnwuApFYrDg1WH7'),

    )
    markupVacUrl.row(
        telebot.types.InlineKeyboardButton(text='↩Повернутися', callback_data='nazadvacc'),
        telebot.types.InlineKeyboardButton(text='📲Меню', callback_data='menu')
    )
    bot.send_message(cid, template.render(user_name=message.chat.username), parse_mode='HTML',reply_markup=markupVacUrl)


@bot.message_handler(commands=['countrylocationSend'])

def countryLocationSend_command_handler(message):
    cid = message.chat.id
    markup1 = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button_geo = types.KeyboardButton(text='Відправити свою геопозицію', request_location=True)
    markup1.add(button_geo)
    bot.send_message(cid, 'Будь ласка, виберіть команди з меню', reply_markup=markup1)

# geo command handler
@bot.message_handler(content_types=['location'])

def geo_command_handler(message):
    cid = message.chat.id
    geo_result = country_service.get_country_information(message.location.latitude, message.location.longitude)
    statistics = stats_service.get_statistics_by_country_name(geo_result['countryName'], message.chat.username)
    user_steps[cid] = 0
    bot.send_message(cid, statistics, parse_mode='HTML')

# country statistics command handler
@bot.message_handler(func=lambda message: get_user_step(message.chat.id) == 1)

def country_statistics_command_handler(message):
    country_name = message.text.strip()
    cid = message.chat.id
    try:
        statistics = stats_service.get_statistics_by_country_name(country_name, message.chat.username)
    except Exception as e:
        raise e
    user_steps[cid] = 0
    bot.send_message(cid, statistics, parse_mode='HTML')

@bot.message_handler(func=lambda message: get_user_step(message.chat.id) == 1)

def countrytest_statistics_command_handler(message, country_name):
    cid = message.chat.id
    try:
        statistics = stats_service.get_statistics_by_country_name(country_name, message.chat.username)
    except Exception as e:
        raise e
    user_steps[cid] = 0
    bot.send_message(cid, statistics, parse_mode='HTML')


# query statistics command handler
@bot.message_handler(commands=['statistics'])

def statistics_command_handler(message):
    cid = message.chat.id
    bot.send_message(cid, stats_service.get_statistics_of_users_queries(), parse_mode='HTML')

# contacts command handler
@bot.message_handler(commands=['contacts'])

def contacts_command_handler(message):
    cid = message.chat.id
    with codecs.open('templates/contacts.html', 'r', encoding='UTF-8') as file:
        template = Template(file.read())
        bot.send_message(cid, template.render(user_name=message.chat.username), parse_mode='HTML')

# help command handler
@bot.message_handler(commands=['help'])

def help_command_handler(message):
    cid = message.chat.id
    help_text = 'Команди які вміє бот \n'
    for key in commands:
        help_text += '/' + key + ': '
        help_text += commands[key] + '\n'
    help_text += 'Гарного користування ботом!!'
    bot.send_message(cid, help_text)

# hi command handler
@bot.message_handler(func=lambda message: message.text.lower() == 'hi')

def hi_command_handler(message):
    cid = message.chat.id
    with codecs.open('templates/himydear.html', 'r', encoding='UTF-8') as file:
        template = Template(file.read())
        bot.send_message(cid, template.render(user_name=message.chat.username), parse_mode='HTML')


# default text messages and hidden statistics command handler
@bot.message_handler(func=lambda message: True, content_types=['text'])

def default_command_handler(message):
    cid = message.chat.id
    if message.text[:int(os.getenv('PASS_CHAR_COUNT'))] == os.getenv('STAT_KEY'):
        st = message.text.split(' ')
        if 'txt' in st:
            tga.analysis(st, cid)
            with codecs.open('%s.txt' % cid, 'r', encoding='UTF-8') as file:
                bot.send_document(cid, file)
                tga.remove(cid)
        else:
            messages = tga.analysis(st, cid)
            bot.send_message(cid, messages)
    else:
        with codecs.open('templates/idunnocommand.html', 'r', encoding='UTF-8') as file:
            template = Template(file.read())
            bot.send_message(cid, template.render(text_command=message.text), parse_mode='HTML')


@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    bot.answer_callback_query(callback_query_id=call.id, text='Ви обрали команду!')
    match call.data:
        case "1":
            help_command_handler(call.message)
        case "2":
            statistics_command_handler(call.message)
        case '3':
            contacts_command_handler(call.message)
        case '4':
            start_command_handler(call.message)
        case "5":
            country.country.countryLocation_command_handler(call.message)
        case "6":
            countryLocationSend_command_handler(call.message)
        case "7":
            vacc.covid.helpCovidInformation_command_handler(call.message)
        case '9':
            locationVaccination(call.message)
        case "menu":
            menu_command_handler(call.message)
        case "news":
            vacc.covid.helpCovidNews_command_handler(call.message)
        case "Pfizer":
            vacc.covid.helpcovidPfizer_command_handler(call.message)
        case "Coronavac":
            vacc.covid.helpcovidCoronavac_command_handler(call.message)
        case "Moderna":
            vacc.covid.helpcovidModerna_command_handler(call.message)
        case "AstraZeneca":
            vacc.covid.helpcovidAstraZeneca_command_handler(call.message)
        case "vaccination":
            vacc.covid.helpCovidVaccination_command_handler(call.message)
        case "CoronavacVac":
            locationVaccinationCoronavac(call.message)
        case "PfizerVac":
            locationVaccinationPfizer(call.message)
        case "AstraZenecaVac":
            locationVaccinationAstraZeneca(call.message)
        case "ModernaVac":
            locationVaccinationModerna(call.message)
        case "nazadvacc":
            locationVaccination(call.message)
        case "nazadinfo":
            vacc.covid.helpCovidInformation_command_handler(call.message)
        case "zones":
            vacc.covid.helpCovidVZones_command_handler(call.message)
        case "nazadzones":
            vacc.covid.helpCovidVZones_command_handler(call.message)
        case "symptoms":
            vacc.covid.helpCovidSymptoms(call.message)
        case "green1":
            vacc.covid.helpCovidVZonesGreen_command_handler(call.message)
        case "yellow":
            vacc.covid.helpCovidVZonesYellow_command_handler(call.message)
        case "orange":
            vacc.covid.helpCovidVZonesOrange_command_handler(call.message)
        case 'red':
            vacc.covid.helpCovidVZonesRed_command_handler(call.message)
        case "nazad":
            vacc.covid.countryLocation_command_handler(call.message)
        case "sng":
            country.country.countryLocationSng_command_handler(call.message)
        case "europe":
            country.country.countryLocationEurope_command_handler(call.message)
        case "statisticeurope":
            countrytest_statistics_command_handler(call.message, 'europe')
        case "Asia":
            country.country.countryLocationAsia_command_handler(call.message)
        case "statisticasia":
            countrytest_statistics_command_handler(call.message, 'asia')
        case "Africa":
            country.country.countryLocationAfrica_command_handler(call.message)
        case "statisticafrica":
            countrytest_statistics_command_handler(call.message, 'africa')
        case "America":
            country.country.countryLocationAmerica_command_handler(call.message)
        case "statisticamericaso":
            countrytest_statistics_command_handler(call.message, 'America')
        case "statisticamericano":
            countrytest_statistics_command_handler(call.message, 'America')
        case "Australia":
            country.country.countryLocationAustralia_command_handler(call.message)
        case "statisticaustralia":
            countrytest_statistics_command_handler(call.message, 'statisticaustralia')
        case 'ua':
             countrytest_statistics_command_handler(call.message, 'UKRAINE')
        case "by":
            countrytest_statistics_command_handler(call.message, 'Belarus')
        case "kz":
             countrytest_statistics_command_handler(call.message, 'Kazakhstan')
        case "md":
            countrytest_statistics_command_handler(call.message, 'Moldova')
        case "ru":
            countrytest_statistics_command_handler(call.message, 'Russia')
        case "az":
            countrytest_statistics_command_handler(call.message, 'Azerbaijan')
        case "tm":
            countrytest_statistics_command_handler(call.message, 'Turkmenistan')
        case "am":
            countrytest_statistics_command_handler(call.message, 'Armenia')
        case "kgz":
            countrytest_statistics_command_handler(call.message, 'Kyrgyzstan')
        case "tj":
            countrytest_statistics_command_handler(call.message, 'Tajikistan')
        case "uz":
            countrytest_statistics_command_handler(call.message, 'Uzbekistan')
        case "at":
            countrytest_statistics_command_handler(call.message, "Austria")
        case "be":
            countrytest_statistics_command_handler(call.message, "Belgium")
        case "li":
            countrytest_statistics_command_handler(call.message,'Liechtenstein')
        case "lu":
            countrytest_statistics_command_handler(call.message,'Luxembourg')
        case "mc":
            countrytest_statistics_command_handler(call.message,'Monaco')
        case "nl":
            countrytest_statistics_command_handler(call.message,'Netherlands')
        case "de":
            countrytest_statistics_command_handler(call.message,'Germany')
        case "fr":
            countrytest_statistics_command_handler(call.message,'France')
        case "ch":
            countrytest_statistics_command_handler(call.message,'Switzerland')
        case "al":
            countrytest_statistics_command_handler(call.message,'Albania')
        case "ad":
            countrytest_statistics_command_handler(call.message,'Andorra')
        case"ba":
            countrytest_statistics_command_handler(call.message,'Bosnia-and-Herzegovina')
        case "gr":
            countrytest_statistics_command_handler(call.message,'Greece')
        case "va":
            countrytest_statistics_command_handler(call.message,'Vatican-City')
        case "es":
            countrytest_statistics_command_handler(call.message, 'Spain')
        case "it":
            countrytest_statistics_command_handler(call.message,'Italy')
        case "mk":
            countrytest_statistics_command_handler(call.message,'North-Macedonia')
        case "pt":
            countrytest_statistics_command_handler(call.message,'Portugal')
        case "mt":
            countrytest_statistics_command_handler(call.message,'Malta')
        case "sm":
            countrytest_statistics_command_handler(call.message,'SanMarino')
        case "rs":
            countrytest_statistics_command_handler(call.message, 'Serbia')
        case "sl":
            countrytest_statistics_command_handler(call.message,'Slovenia')
        case "hr":
            countrytest_statistics_command_handler(call.message,"Croatia")
        case "me":
            countrytest_statistics_command_handler(call.message,'Montenegro')
        case "gb":
            countrytest_statistics_command_handler(call.message, 'UK')
        case "dk":
            countrytest_statistics_command_handler(call.message,'Denmark')
        case "ee":
            countrytest_statistics_command_handler(call.message, 'Estonia')
        case "ie":
            countrytest_statistics_command_handler(call.message, 'Ireland')
        case "is":
            countrytest_statistics_command_handler(call.message, 'Iceland')
        case "lv":
            countrytest_statistics_command_handler(call.message, 'Latvia')
        case "lt":
            countrytest_statistics_command_handler(call.message, 'Lithuania')
        case "no":
            countrytest_statistics_command_handler(call.message, 'Norway')
        case "fi":
            countrytest_statistics_command_handler(call.message, 'Finland')
        case "se":
            countrytest_statistics_command_handler(call.message, 'Sweden')
        case "bg":
            countrytest_statistics_command_handler(call.message, 'Bulgaria')
        case "pl":
            countrytest_statistics_command_handler(call.message, 'Poland')
        case "ro":
            countrytest_statistics_command_handler(call.message, 'Romania')
        case "sk":
            countrytest_statistics_command_handler(call.message, 'Slovakia')
        case "hu":
            countrytest_statistics_command_handler(call.message, 'Hungary')
        case "cz":
            countrytest_statistics_command_handler(call.message, 'Czechia')
        case "af":
            countrytest_statistics_command_handler(call.message, 'Afghanistan')
        case "am":
            countrytest_statistics_command_handler(call.message, 'Armenia')
        case "bh":
            countrytest_statistics_command_handler(call.message, 'Bahrain')
        case "bh":
            countrytest_statistics_command_handler(call.message, 'Bangladesh')
        case "bt":
            countrytest_statistics_command_handler(call.message,'Bhutan')
        case "bn":
            countrytest_statistics_command_handler(call.message, 'Brunei-')
        case "mm":
            countrytest_statistics_command_handler(call.message, 'Burma')
        case "kh":
            countrytest_statistics_command_handler(call.message, 'Cambodia')
        case "cn":
            countrytest_statistics_command_handler(call.message, 'China')
        case "cy":
            countrytest_statistics_command_handler(call.message, 'Cyprus')
        case "tl":
            countrytest_statistics_command_handler(call.message, 'Timor-Leste')
        case "ge":
            countrytest_statistics_command_handler(call.message, 'Georgia')
        case "hk":
            countrytest_statistics_command_handler(call.message, 'Hong-Kong')
        case "in":
            countrytest_statistics_command_handler(call.message, 'India')
        case "id":
            countrytest_statistics_command_handler(call.data, 'Indonesia')
        case "ir":
            countrytest_statistics_command_handler(call.data, '	Iran')
        case "iq":
            countrytest_statistics_command_handler(call.message, 'Iraq')
        case "il":
            countrytest_statistics_command_handler(call.message, 'Israel')
        case "jp":
            countrytest_statistics_command_handler(call.message, 'Japan')
        case "jo":
            countrytest_statistics_command_handler(call.message, 'Jordan')
        case "kr":
            countrytest_statistics_command_handler(call.message, 'S.-Korea')
        case "kw":
            countrytest_statistics_command_handler(call.message, 'Kuwait')
        case "kg":
            countrytest_statistics_command_handler(call.message, 'Kyrgyzstan')
        case "la":
            countrytest_statistics_command_handler(call.message, 'Laos')
        case "lb":
            countrytest_statistics_command_handler(call.message, 'Lebanon')
        case "mo":
            countrytest_statistics_command_handler(call.message, 'Macau')
        case "my":
            countrytest_statistics_command_handler(call.message, 'Malaysia')
        case "mv":
            countrytest_statistics_command_handler(call.message, 'Maldives')
        case "mn":
            countrytest_statistics_command_handler(call.message, 'Mongolia')
        case "np":
            countrytest_statistics_command_handler(call.message, 'Nepal')
        case "om":
            countrytest_statistics_command_handler(call.message, 'Oman')
        case "pk":
            countrytest_statistics_command_handler(call.message, 'Pakistan')
        case "ph":
            countrytest_statistics_command_handler(call.message, 'Philippines')
        case "qa":
            countrytest_statistics_command_handler(call.message, 'Quatar')
        case "sa":
            countrytest_statistics_command_handler(call.message, 'Saudi-Arabia')
        case "sg":
            countrytest_statistics_command_handler(call.message, 'Singapore')
        case "lk":
            countrytest_statistics_command_handler(call.message, 'Sri-Lanka')
        case "sy":
            countrytest_statistics_command_handler(call.message, 'Syria')
        case "tw":
            countrytest_statistics_command_handler(call.message, 'Taiwan')
        case "th":
            countrytest_statistics_command_handler(call.message, 'Thailand')
        case "tr":
            countrytest_statistics_command_handler(call.message, 'Turkey')
        case "ae":
            countrytest_statistics_command_handler(call.message, 'UAE')
        case "vn":
            countrytest_statistics_command_handler(call.message, 'Vietnam')
        case "ye":
            countrytest_statistics_command_handler(call.message, 'Yemen')
        case "dz":
            countrytest_statistics_command_handler(call.message, 'Algeria')
        case "ao":
            countrytest_statistics_command_handler(call.message, 'Angola')
        case "bj":
            countrytest_statistics_command_handler(call.message, 'Benin')
        case "bw":
            countrytest_statistics_command_handler(call.message, 'Botswana')
        case "bf":
            countrytest_statistics_command_handler(call.message, 'Burkina-Faso')
        case "bi":
            countrytest_statistics_command_handler(call.message, 'Burundi')
        case "ga":
            countrytest_statistics_command_handler(call.message, 'Gabon')
        case "gm":
            countrytest_statistics_command_handler(call.message, 'Gambia')
        case "gh":
            countrytest_statistics_command_handler(call.message, 'Ghana')
        case "gn":
            countrytest_statistics_command_handler(call.message, 'Guinea')
        case "gw":
            countrytest_statistics_command_handler(call.message, 'Guinea-Bissau')
        case "cd":
            countrytest_statistics_command_handler(call.message, 'Congo, Democratic Republic of the')
        case "dj":
            countrytest_statistics_command_handler(call.message, 'Djibouti')
        case "gq":
            countrytest_statistics_command_handler(call.message, 'Equatorial-Guinea')
        case "er":
            countrytest_statistics_command_handler(call.message, 'Eritrea')
        case "et":
            countrytest_statistics_command_handler(call.message, 'Ethiopia')
        case "eg":
            countrytest_statistics_command_handler(call.message, 'Egypt')
        case "zm":
            countrytest_statistics_command_handler(call.message, 'Zambia')
        case "zw":
            countrytest_statistics_command_handler(call.message, 'Zimbabwe')
        case "cv":
            countrytest_statistics_command_handler(call.message, 'Cape-Verde')
        case "cm":
            countrytest_statistics_command_handler(call.message, 'Cameroon')
        case "ke":
            countrytest_statistics_command_handler(call.message, 'Kenya')
        case "ci":
            countrytest_statistics_command_handler(call.message, 'Cote')
        case "ls":
            countrytest_statistics_command_handler(call.message, 'Lesotho')
        case "lr":
            countrytest_statistics_command_handler(call.message, 'Liberia')
        case "mu":
            countrytest_statistics_command_handler(call.message, 'Mauritius')
        case "mr":
            countrytest_statistics_command_handler(call.message, 'Mauritania')
        case "mg":
            countrytest_statistics_command_handler(call.message, 'Madagascar')
        case "yt":
            countrytest_statistics_command_handler(call.message, 'Mayotte')
        case "mw":
            countrytest_statistics_command_handler(call.message, 'Malawi')
        case "ml":
            countrytest_statistics_command_handler(call.message, 'Mali')
        case "ma":
            countrytest_statistics_command_handler(call.message, 'Morocco')
        case "mel":
            countrytest_statistics_command_handler(call.message, 'Melilla')
        case "mz":
            countrytest_statistics_command_handler(call.message, 'Mozambique')
        case "na":
            countrytest_statistics_command_handler(call.message, 'Namibia')
        case "ng":
            countrytest_statistics_command_handler(call.message, 'Nigeria')
        case "za":
            countrytest_statistics_command_handler(call.message, 'South-Africa')
        case "sss":
            countrytest_statistics_command_handler(call.message, 'South-Sudan')
        case "cg":
            countrytest_statistics_command_handler(call.message, '🇨🇬Republic of the Congo')
        case "re":
            countrytest_statistics_command_handler(call.message, 'Reunion')
        case "rw":
            countrytest_statistics_command_handler(call.message, 'Rwanda')
        case "st":
            countrytest_statistics_command_handler(call.message, 'Sao Tome and Principe')
        case "sc":
            countrytest_statistics_command_handler(call.message, 'Seychelles')
        case "sn":
            countrytest_statistics_command_handler(call.message, 'Senegal')
        case "so":
            countrytest_statistics_command_handler(call.message, 'Somalia')
        case "sd":
            countrytest_statistics_command_handler(call.message, 'Sudan')
        case "sl":
            countrytest_statistics_command_handler(call.message, 'Sierra-Leone')
        case "tz":
            countrytest_statistics_command_handler(call.message, 'Tanzania')
        case "tg":
            countrytest_statistics_command_handler(call.message, 'Togo')
        case "tn":
            countrytest_statistics_command_handler(call.message, 'Tunisia')
        case "ug":
            countrytest_statistics_command_handler(call.message, 'Uganda')
        case "cf":
            countrytest_statistics_command_handler(call.message, 'Central African Republic')
        case "td":
            countrytest_statistics_command_handler(call.message, 'Chad')
        case "bm":
            countrytest_statistics_command_handler(call.message, 'Bermuda')
        case "gl":
            countrytest_statistics_command_handler(call.message, 'Greenland')
        case "ca":
            countrytest_statistics_command_handler(call.message, 'Canada')
        case "mx":
            countrytest_statistics_command_handler(call.message, 'Mexico')
        case "usa":
            countrytest_statistics_command_handler(call.message, 'usa')
        case "bz":
            countrytest_statistics_command_handler(call.message, 'Belize')
        case "gt":
            countrytest_statistics_command_handler(call.message, 'Guatemala')
        case "hn":
            countrytest_statistics_command_handler(call.message, 'Honduras')
        case "cr":
            countrytest_statistics_command_handler(call.message, 'Costa-Rica')
        case "ni":
            countrytest_statistics_command_handler(call.message, 'Nicaragua')
        case "pa":
            countrytest_statistics_command_handler(call.message, 'Panama')
        case "sv":
            countrytest_statistics_command_handler(call.message, 'El-Salvador')
        case "ag":
            countrytest_statistics_command_handler(call.message, 'Antigua-and-Barbuda')
        case "aw":
            countrytest_statistics_command_handler(call.message, 'Aruba')
        case "bs":
            countrytest_statistics_command_handler(call.message, 'Bahamas')
        case "bb":
            countrytest_statistics_command_handler(call.message, 'Barbados')
        case "bq":
            countrytest_statistics_command_handler(call.message, 'Bonaire')
        case "vg":
            countrytest_statistics_command_handler(call.message, 'Virgin-Islands')
        case "ht":
            countrytest_statistics_command_handler(call.message, 'Haiti')
        case "gp":
            countrytest_statistics_command_handler(call.message, 'Guadeloupe')
        case "gd":
            countrytest_statistics_command_handler(call.message, 'Grenada')
        case "dm":
            countrytest_statistics_command_handler(call.message, 'Dominica')
        case "do":
            countrytest_statistics_command_handler(call.message, 'Dominican-Republic')
        case "ky":
            countrytest_statistics_command_handler(call.message, 'Cayman-Islands')
        case "cu":
            countrytest_statistics_command_handler(call.message, 'Cuba')
        case "cw":
            countrytest_statistics_command_handler(call.message, 'Curaçao')
        case "mq":
            countrytest_statistics_command_handler(call.message, 'Martinique')
        case "ms":
            countrytest_statistics_command_handler(call.message, 'Montserrat')
        case "tc":
            countrytest_statistics_command_handler(call.message, 'Turks-and-Caicos-Islands')
        case "pr":
            countrytest_statistics_command_handler(call.message, 'Puerto Rico')
        case "jm":
            countrytest_statistics_command_handler(call.message, 'Jamaica')
        case "lc":
            countrytest_statistics_command_handler(call.message, 'Saint-Lucia')
        case "au":
            countrytest_statistics_command_handler(call.message, 'Australia')
        case "vu":
            countrytest_statistics_command_handler(call.message, 'Vanuatu')
        case "pg":
            countrytest_statistics_command_handler(call.message, 'Papua New Guinea')
        case "sb":
            countrytest_statistics_command_handler(call.message, 'Solomon-Islands')
        case "fj":
            countrytest_statistics_command_handler(call.message, 'Fiji')
        case "ki":
            countrytest_statistics_command_handler(call.message, 'Kiribati')
        case "mh":
            countrytest_statistics_command_handler(call.message, 'Marshall-Islands')
        case "nr":
            countrytest_statistics_command_handler(call.message, 'Nauru')
        case "nz":
            countrytest_statistics_command_handler(call.message, 'New Zealand')
        case "pw":
            countrytest_statistics_command_handler(call.message, 'Palau')
        case "ws":
            countrytest_statistics_command_handler(call.message, 'Samoa')
        case "to":
            countrytest_statistics_command_handler(call.message, 'Tonga')
        case "tv":
            countrytest_statistics_command_handler(call.message, 'Tuvalu')
        case "fm":
            countrytest_statistics_command_handler(call.message, 'Micronesia')

 #set web hook


# set web hook
server = Flask(__name__)


@server.route('/' + token, methods=['POST'])
def get_messages():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode('utf-8'))])
    return '!', 200


@server.route('/')
def web_hook():
    bot.remove_webhook()
    bot.set_webhook(url=os.getenv('HEROKU_URL') + token)
    return '!', 200


# application entry point
if __name__ == '__main__':
    threading.Thread(target=scheduler).start()
    server.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
