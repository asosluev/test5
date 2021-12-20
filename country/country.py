import telebot
import os


import common.tg_analytics as tga

from functools import wraps

from services.country_service import CountryService
from services.statistics_service import StatisticsService


token = os.getenv('API_BOT_TOKEN')
bot = telebot.TeleBot(token)
user_steps = {}
known_users = []
stats_service = StatisticsService()
country_service = CountryService()
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


@bot.message_handler(commands=['countryLocation'])
@send_action('typing')
@save_user_activity()
def countryLocation_command_handler(message):
    cid = message.chat.id
    user_steps[cid] = 1
    markup = telebot.types.InlineKeyboardMarkup()
    markup.row(
        telebot.types.InlineKeyboardButton(text='🗺Країни СНД', callback_data='sng'),
        telebot.types.InlineKeyboardButton(text='🌍Європа ', callback_data='europe'),
    )
    markup.row(
        telebot.types.InlineKeyboardButton(text='🌏Азія', callback_data='Asia'),
        telebot.types.InlineKeyboardButton(text='🌍Африка', callback_data='Africa'),
        #telebot.types.InlineKeyboardButton(text='Антарктида', callback_data='Antarctica'),
    )
    markup.row(telebot.types.InlineKeyboardButton(text='🌏Австралія і Океанія', callback_data='Australia'))
    markup.row(telebot.types.InlineKeyboardButton(text='↩Назад', callback_data='menu'))
    bot.send_message(cid, '{0}, Виберіть локацію зі списку по якій потрібна інформація'.format(message.chat.username), reply_markup=markup)


@bot.message_handler(commands=['countryLocationSNG'])
@send_action('typing')
@save_user_activity()
def countryLocationSng_command_handler(message):
    cid = message.chat.id
    user_steps[cid] = 1
    markup = telebot.types.InlineKeyboardMarkup()
    markup.row(
        telebot.types.InlineKeyboardButton(text='🇺🇦 Україна', callback_data='ua'),
        telebot.types.InlineKeyboardButton(text='🇧🇾 Білорусь ', callback_data='by'),
        telebot.types.InlineKeyboardButton(text='🇰🇿Казахстан', callback_data='kz')
    )
    markup.row(
        telebot.types.InlineKeyboardButton(text='🇲🇩Молдова', callback_data='md'),
        telebot.types.InlineKeyboardButton(text='🇷🇺 Росія', callback_data='ru'),
        telebot.types.InlineKeyboardButton(text='🇦🇿Азербайджан', callback_data='az'),
        # telebot.types.InlineKeyboardButton(text='Туркменістан', callback_data='tm')
    )
    markup.row(
        telebot.types.InlineKeyboardButton(text='🇭🇺Угорщина ', callback_data='hu'),
        telebot.types.InlineKeyboardButton(text='🇰🇬Киргизстан', callback_data='kgz'),
    )
    markup.row(
        telebot.types.InlineKeyboardButton(text='🇹🇯Таджикистан', callback_data='tj'),
        telebot.types.InlineKeyboardButton(text='🇺🇿Узбекистан', callback_data='uz')
    )
    markup.row(
        telebot.types.InlineKeyboardButton(text='↩Назад', callback_data='nazad'),
        telebot.types.InlineKeyboardButton(text='📲Меню', callback_data=4)
    )
    bot.send_message(cid, '{0}, Виберіть країну зі списку по якій потрібна інформація'.format(message.chat.username), reply_markup=markup)


#Europe
@bot.message_handler(commands=['countryLocationEurope'])
@send_action('typing')
@save_user_activity()
def countryLocationEurope_command_handler(message):
    cid = message.chat.id
    user_steps[cid] = 1
    markup = telebot.types.InlineKeyboardMarkup()
    markup.row(
        telebot.types.InlineKeyboardButton(text='🇦🇹 Австрія', callback_data='at'),
        telebot.types.InlineKeyboardButton(text='🇧🇪	Бельгія', callback_data='be'),
        telebot.types.InlineKeyboardButton(text='🇱🇮 Ліхтенштейн', callback_data='li')
    )
    markup.row(
        telebot.types.InlineKeyboardButton(text='🇱🇺 Люксембург', callback_data='lu'),
        telebot.types.InlineKeyboardButton(text='🇲🇨 Монако', callback_data='mc'),
        telebot.types.InlineKeyboardButton(text='🇳🇱 Нідерланди', callback_data='nl'),
        # telebot.types.InlineKeyboardButton(text='Туркменістан', callback_data='tm')
    )
    markup.row(
        telebot.types.InlineKeyboardButton(text='🇩🇪 Німеччина', callback_data=' de'),
        telebot.types.InlineKeyboardButton(text='🇫🇷 Франція', callback_data='fr'),
        telebot.types.InlineKeyboardButton(text='🇨🇭Швейцарія', callback_data='ch')
    )
    markup.row(
        telebot.types.InlineKeyboardButton(text='🇦🇱Албанія', callback_data='al'),
        telebot.types.InlineKeyboardButton(text='🇦🇩Андорра', callback_data='ad'),
        telebot.types.InlineKeyboardButton(text='🇬🇷Греція', callback_data='gr'),
       telebot.types.InlineKeyboardButton(text='🇧🇦Боснія і Герцеговина', callback_data='ba')
    )
    markup.row(
        telebot.types.InlineKeyboardButton(text='🇻🇦	Ватикан', callback_data='va'),
        telebot.types.InlineKeyboardButton(text='🇪🇸Іспанія', callback_data='es'),
        telebot.types.InlineKeyboardButton(text='🇮🇹Італія', callback_data='it')
    )
    markup.row(
        telebot.types.InlineKeyboardButton(text='🇲🇰Македонія', callback_data='mk'),
        telebot.types.InlineKeyboardButton(text='🇵🇹Португалія', callback_data='pt'),
        telebot.types.InlineKeyboardButton(text='🇲🇹Мальта', callback_data='mt')
    )
    markup.row(
        telebot.types.InlineKeyboardButton(text='🇸🇲Сан-Марино', callback_data='Sint-Maarten'),
        telebot.types.InlineKeyboardButton(text='🇸🇮Словенія', callback_data='sl'),
        telebot.types.InlineKeyboardButton(text='🇭🇷Хорватія', callback_data='hr')
    )
    markup.row(
        telebot.types.InlineKeyboardButton(text='🇲🇪Чорногорія', callback_data='me'),
        telebot.types.InlineKeyboardButton(text='🇬🇧Велика Британія', callback_data='gb'),
        telebot.types.InlineKeyboardButton(text='🇩🇰 Данія*', callback_data='dk')
    )
    markup.row(
        telebot.types.InlineKeyboardButton(text='🇪🇪Естонія', callback_data='ee'),
        telebot.types.InlineKeyboardButton(text='🇮🇪Ірландія', callback_data='ie'),
        telebot.types.InlineKeyboardButton(text='🇮🇸Ісландія', callback_data='is')
    )
    markup.row(
        telebot.types.InlineKeyboardButton(text='🇱🇻Латвія', callback_data='lv'),
        telebot.types.InlineKeyboardButton(text='🇱🇹Литва', callback_data='lt'),
        telebot.types.InlineKeyboardButton(text='🇳🇴Норвегія', callback_data='no')
    )
    markup.row(
        telebot.types.InlineKeyboardButton(text='🇫🇮Фінляндія', callback_data='fi'),
        telebot.types.InlineKeyboardButton(text='🇸🇪Швеція', callback_data='se'),
        telebot.types.InlineKeyboardButton(text='🇳🇴Норвегія', callback_data='no')
    )
    markup.row(
        telebot.types.InlineKeyboardButton(text='🇧🇾 Білорусь ', callback_data='by'),
        telebot.types.InlineKeyboardButton(text='🇧🇬Болгарія*', callback_data='bg'),
        telebot.types.InlineKeyboardButton(text='🇲🇩Молдова', callback_data='md')
    )
    markup.row(
        telebot.types.InlineKeyboardButton(text='🇵🇱Польща ', callback_data='pl'),
        telebot.types.InlineKeyboardButton(text='🇷🇴Румунія', callback_data='ro'),
        telebot.types.InlineKeyboardButton(text='🇸🇰	Словаччина*', callback_data='sk')
    )
    markup.row(
        telebot.types.InlineKeyboardButton(text='🇭🇺Угорщина ', callback_data='hu'),
        telebot.types.InlineKeyboardButton(text='🇺🇦 Україна', callback_data='ua'),
        telebot.types.InlineKeyboardButton(text='🇨🇿Чехія', callback_data='cz')
    )

    markup.row(telebot.types.InlineKeyboardButton(text='Європа ', callback_data='statisticeurope'))
    markup.row(
        telebot.types.InlineKeyboardButton(text='↩Назад', callback_data='nazad'),
        telebot.types.InlineKeyboardButton(text='📲Меню', callback_data=4)
    )
    bot.send_message(cid, '{0}, Виберіть країну Европи зі списку по якій потрібна інформація'.format(message.chat.username), reply_markup=markup)
#Asia
@bot.message_handler(commands=['countryLocationAsia'])
@send_action('typing')
@save_user_activity()
def countryLocationAsia_command_handler(message):
    cid = message.chat.id
    user_steps[cid] = 1
    markup = telebot.types.InlineKeyboardMarkup()
    markup.row(
        telebot.types.InlineKeyboardButton(text='🇦🇫Афганістан', callback_data='af'),
        telebot.types.InlineKeyboardButton(text='🇦🇿Азербайджан', callback_data='az'),
        telebot.types.InlineKeyboardButton(text='🇦🇲 Вірменія', callback_data='am')
    )
    markup.row(
        telebot.types.InlineKeyboardButton(text='🇧🇭Бахрейн', callback_data='bh'),
        telebot.types.InlineKeyboardButton(text='🇧🇩Бангладеш', callback_data='bd'),
        telebot.types.InlineKeyboardButton(text='🇧🇹Бутан', callback_data='bt'),
    )
    markup.row(
        telebot.types.InlineKeyboardButton(text='🇧🇳Бруней', callback_data='bn'),
        telebot.types.InlineKeyboardButton(text='🇲🇲Бірма', callback_data='mm'),
        telebot.types.InlineKeyboardButton(text='🇰🇭Камбоджа', callback_data='kh'),
    )
    markup.row(
        telebot.types.InlineKeyboardButton(text='🇨🇳КНР', callback_data='cn'),
        telebot.types.InlineKeyboardButton(text='🇨🇾Кіпр', callback_data='cy'),
        telebot.types.InlineKeyboardButton(text='🇹🇱Східний Тимор', callback_data='tl'),
    )
    markup.row(
        telebot.types.InlineKeyboardButton(text='🇬🇪Грузія', callback_data='ge'),
        telebot.types.InlineKeyboardButton(text='🇭🇰Гонконг', callback_data='hk'),
        telebot.types.InlineKeyboardButton(text='🇮🇳	Індія', callback_data='in'),
    )
    markup.row(
        telebot.types.InlineKeyboardButton(text='🇮🇩Індонезія', callback_data='id'),
        telebot.types.InlineKeyboardButton(text='🇮🇷Іран', callback_data='ir'),
        telebot.types.InlineKeyboardButton(text='🇮🇶Ірак', callback_data='iq'),
    )
    markup.row(
        telebot.types.InlineKeyboardButton(text='🇮🇱 Ізраїль', callback_data='il'),
        telebot.types.InlineKeyboardButton(text='🇯🇵Японія', callback_data='jp'),
        telebot.types.InlineKeyboardButton(text='🇯🇴Йорданія', callback_data='jo'),
    )
    markup.row(
        telebot.types.InlineKeyboardButton(text='🇰🇿Казахстан', callback_data='kz'),
        telebot.types.InlineKeyboardButton(text='🇰🇷Корея', callback_data='kr'),
        telebot.types.InlineKeyboardButton(text='🇰🇼Кувейт', callback_data='kw'),
    )
    markup.row(
        telebot.types.InlineKeyboardButton(text='🇰🇬Киргизстан', callback_data='kg'),
        telebot.types.InlineKeyboardButton(text='🇱🇦Лаос', callback_data='la'),
        telebot.types.InlineKeyboardButton(text='🇱🇧Ліван', callback_data='lb'),
    )
    markup.row(
        telebot.types.InlineKeyboardButton(text='🇲🇴Макао', callback_data='mo'),
        telebot.types.InlineKeyboardButton(text='🇲🇾Малайзія', callback_data='my'),
        telebot.types.InlineKeyboardButton(text='🇲🇻Мальдіви', callback_data='mv'),
    )
    markup.row(
        telebot.types.InlineKeyboardButton(text='🇲🇳Монголія', callback_data='mn'),
        telebot.types.InlineKeyboardButton(text='🇳🇵Непал', callback_data='np'),
        telebot.types.InlineKeyboardButton(text='🇴🇲Оман', callback_data='om'),
    )
    markup.row(
        telebot.types.InlineKeyboardButton(text='🇵🇰Пакистан', callback_data='pk'),
        telebot.types.InlineKeyboardButton(text='🇵🇭Філіппіни', callback_data='ph'),
        telebot.types.InlineKeyboardButton(text='🇶🇦Катар', callback_data='qa'),
    )
    markup.row(
        telebot.types.InlineKeyboardButton(text='🇷🇺Росія', callback_data='ru'),
        telebot.types.InlineKeyboardButton(text='🇸🇦Саудівська Аравія', callback_data='sa'),
        telebot.types.InlineKeyboardButton(text='🇸🇬Сінгапур', callback_data='sg'),
    )
    markup.row(
        telebot.types.InlineKeyboardButton(text='🇱🇰Шрі-Ланка', callback_data='lk'),
        telebot.types.InlineKeyboardButton(text='🇸🇾Сирія', callback_data='sy'),
        telebot.types.InlineKeyboardButton(text='🇹🇼Тайвань', callback_data='tw'),
    )
    markup.row(
        telebot.types.InlineKeyboardButton(text='🇹🇯Таджикистан', callback_data='tj'),
        telebot.types.InlineKeyboardButton(text='🇹🇭Таїланд', callback_data='th'),
        telebot.types.InlineKeyboardButton(text='🇹🇷Туреччина', callback_data='tr'),
    )
    markup.row(
        telebot.types.InlineKeyboardButton(text='Туркменістан', callback_data='tm'),
        telebot.types.InlineKeyboardButton(text='ОАЕ', callback_data='ae'),
        telebot.types.InlineKeyboardButton(text='🇺🇿Узбекистан', callback_data='uz')
    )
    markup.row(
        telebot.types.InlineKeyboardButton(text='🇻🇳 В`єтнам', callback_data='vn'),
        telebot.types.InlineKeyboardButton(text='🇾🇪Ємен', callback_data='ye')
    )

    markup.row(telebot.types.InlineKeyboardButton(text='Азія ', callback_data='statisticasia'))
    markup.row(
        telebot.types.InlineKeyboardButton(text='↩Назад', callback_data='nazad'),
        telebot.types.InlineKeyboardButton(text='📲Меню', callback_data=4)
    )
    bot.send_message(cid, '{0}, Виберіть країну Азії зі списку по якій потрібна інформація'.format(message.chat.username), reply_markup=markup)

#Africa
@bot.message_handler(commands=['countryLocationAfrica'])
@send_action('typing')
@save_user_activity()
def countryLocationAfrica_command_handler(message):
    cid = message.chat.id
    user_steps[cid] = 1
    markup = telebot.types.InlineKeyboardMarkup()
    markup.row(
        telebot.types.InlineKeyboardButton(text='Азорські острови', callback_data='raa'),
        telebot.types.InlineKeyboardButton(text='🇩🇿Алжир', callback_data='dz'),
        telebot.types.InlineKeyboardButton(text='🇦🇴Ангола', callback_data='ao')
    )
    markup.row(
        telebot.types.InlineKeyboardButton(text='🇧🇯Бенін', callback_data='bj'),
        telebot.types.InlineKeyboardButton(text='🇧🇼Ботсвана', callback_data='bw'),
        telebot.types.InlineKeyboardButton(text='🇧🇫Буркіна-Фасо', callback_data='bf')
    )
    markup.row(
        telebot.types.InlineKeyboardButton(text='🇧🇮Бурунді', callback_data='bi'),
        telebot.types.InlineKeyboardButton(text='🇬🇦Габон', callback_data='ga'),
        telebot.types.InlineKeyboardButton(text='🇬🇲Гамбія', callback_data='gm')
    )
    markup.row(
        telebot.types.InlineKeyboardButton(text='🇬🇭Гана', callback_data='gh'),
        telebot.types.InlineKeyboardButton(text='🇬🇳Гвінея', callback_data='gn'),
        telebot.types.InlineKeyboardButton(text='🇬🇼Гвінея-Бісау', callback_data='gw')
    )
    markup.row(
        telebot.types.InlineKeyboardButton(text='🇨🇩Демократична Республіка Конго', callback_data='cd'),
        telebot.types.InlineKeyboardButton(text='🇩🇯Джибуті', callback_data='dj'),
        telebot.types.InlineKeyboardButton(text='🇬🇶Екваторіальна Гвінея', callback_data='gq')
    )
    markup.row(
        telebot.types.InlineKeyboardButton(text='🇪🇷Еритрея', callback_data='er'),
        telebot.types.InlineKeyboardButton(text='🇪🇹Ефіопія', callback_data='et'),
        telebot.types.InlineKeyboardButton(text='🇪🇬Єгипет', callback_data='eg')
    )
    markup.row(
        telebot.types.InlineKeyboardButton(text='🇿🇲Замбія', callback_data='zm'),
        telebot.types.InlineKeyboardButton(text='🇿🇼Зімбабве', callback_data='zw'),
        telebot.types.InlineKeyboardButton(text='🇨🇻Кабо-Верде', callback_data='cv')
    )
    markup.row(
        telebot.types.InlineKeyboardButton(text='🇨🇲Камерун', callback_data='cm'),
        telebot.types.InlineKeyboardButton(text='🇰🇪Кенія', callback_data='ke'),
        telebot.types.InlineKeyboardButton(text='Кот-д`Івуар', callback_data='ci')
    )
    markup.row(
        telebot.types.InlineKeyboardButton(text='🇱🇸Лесото', callback_data='ls'),
        telebot.types.InlineKeyboardButton(text='🇱🇷Ліберія', callback_data='lr'),
        telebot.types.InlineKeyboardButton(text='🇲🇺Маврикій', callback_data='mu')
    )
    markup.row(
        telebot.types.InlineKeyboardButton(text='🇲🇷Мавританія', callback_data='mr'),
        telebot.types.InlineKeyboardButton(text='🇲🇬Мадагаскар', callback_data='mg'),
        telebot.types.InlineKeyboardButton(text='🇲🇱Малі', callback_data='ml')
    )
    markup.row(
        telebot.types.InlineKeyboardButton(text='🇾🇹Майотта', callback_data='yt'),
        telebot.types.InlineKeyboardButton(text='🇲🇼Малаві', callback_data='mw'),
        telebot.types.InlineKeyboardButton(text='🇲🇦Марокко', callback_data='ma')
    )
    markup.row(
        telebot.types.InlineKeyboardButton(text='🇪🇦Мелілья', callback_data='mel'),
        telebot.types.InlineKeyboardButton(text='🇲🇿Мозамбік', callback_data='mz'),
        telebot.types.InlineKeyboardButton(text='🇳🇦	Намібія', callback_data='na')
    )
    markup.row(
        telebot.types.InlineKeyboardButton(text='🇳🇬Нігерія', callback_data='ng'),
        telebot.types.InlineKeyboardButton(text='🇿🇦ЮAР', callback_data='za'),
        telebot.types.InlineKeyboardButton(text='🇸🇸Південний Судан', callback_data='sss')
    )
    markup.row(
        telebot.types.InlineKeyboardButton(text='Республіка Конго', callback_data='cg'),
        telebot.types.InlineKeyboardButton(text='🇷🇪Реюньйон', callback_data='re'),
        telebot.types.InlineKeyboardButton(text='🇷🇼Руанда', callback_data='rw')
    )
    markup.row(
        telebot.types.InlineKeyboardButton(text='🇸🇹Сан-Томе і Принсіпі', callback_data='st'),
        telebot.types.InlineKeyboardButton(text='🇸🇨Сейшельські Острови', callback_data='sc'),
        telebot.types.InlineKeyboardButton(text='🇸🇳Сенегал', callback_data='sn')
    )
    markup.row(
        telebot.types.InlineKeyboardButton(text='🇸🇴Сомалі', callback_data='so'),
        telebot.types.InlineKeyboardButton(text='🇸🇩Судан', callback_data='sd'),
        telebot.types.InlineKeyboardButton(text='🇸🇱Сьєрра-Леоне', callback_data='sl')
    )
    markup.row(
        telebot.types.InlineKeyboardButton(text='🇹🇿Танзанія', callback_data='tz'),
        telebot.types.InlineKeyboardButton(text='🇹🇬Того', callback_data='tg'),
        telebot.types.InlineKeyboardButton(text='🇹🇳Туніс', callback_data='tn')
    )
    markup.row(
        telebot.types.InlineKeyboardButton(text='sdfsdf', callback_data='ug'),
        telebot.types.InlineKeyboardButton(text='🇨🇫Центральноафриканська Республіка', callback_data='cf'),
        telebot.types.InlineKeyboardButton(text='🇹🇩Чад', callback_data='td')
    )
    markup.row(telebot.types.InlineKeyboardButton(text='Африка ', callback_data='statisticafrica'))
    markup.row(
        telebot.types.InlineKeyboardButton(text='↩Назад', callback_data='nazad'),
        telebot.types.InlineKeyboardButton(text='📲Меню', callback_data=4)
    )
    bot.send_message(cid,'{0}, Виберіть країну Африки зі списку по якій потрібна інформація'.format(message.chat.username), reply_markup=markup)

#Aьукшсф
@bot.message_handler(commands=['countryLocationAmerica'])
@send_action('typing')
@save_user_activity()
def countryLocationAmerica_command_handler(message):
    cid = message.chat.id
    user_steps[cid] = 1
    markup = telebot.types.InlineKeyboardMarkup()
    markup.row(
        telebot.types.InlineKeyboardButton(text='🇧🇲Бермудські Острови', callback_data='bm'),
        telebot.types.InlineKeyboardButton(text='🇬🇱Гренландія', callback_data='gl'),
        telebot.types.InlineKeyboardButton(text='🇨🇦Канада', callback_data='ca')
    )
    markup.row(
        telebot.types.InlineKeyboardButton(text='🇲🇽Мексика', callback_data='mx'),
        telebot.types.InlineKeyboardButton(text='США', callback_data='usa'),
        telebot.types.InlineKeyboardButton(text='🇧🇿Беліз', callback_data='bz')
    )
    markup.row(
        telebot.types.InlineKeyboardButton(text='🇬🇹Гватемала', callback_data='gt'),
        telebot.types.InlineKeyboardButton(text='🇭🇳Гондурас', callback_data='hn'),
        telebot.types.InlineKeyboardButton(text='🇨🇷Коста-Рика', callback_data='cr')
    )
    markup.row(
        telebot.types.InlineKeyboardButton(text='🇳🇮Нікарагуа', callback_data='ni'),
        telebot.types.InlineKeyboardButton(text='🇵🇦Панама', callback_data='pa'),
        telebot.types.InlineKeyboardButton(text='🇸🇻Сальвадор', callback_data='sv')
    )
    markup.row(
        telebot.types.InlineKeyboardButton(text='🇦🇬Антигуа і Барбуда', callback_data='ag'),
        telebot.types.InlineKeyboardButton(text='🇦🇼Аруба', callback_data='aw'),
        telebot.types.InlineKeyboardButton(text='🇧🇸Багамські Острови', callback_data='bs')
    )
    markup.row(
        telebot.types.InlineKeyboardButton(text='🇧🇧Барбадос', callback_data='bb'),
        telebot.types.InlineKeyboardButton(text='🇧🇶Бонайре', callback_data='bq'),
        telebot.types.InlineKeyboardButton(text='🇻🇬Британські Віргінські Острови', callback_data='vg')
    )
    markup.row(
        telebot.types.InlineKeyboardButton(text='🇭🇹Гаїті', callback_data='ht'),
        telebot.types.InlineKeyboardButton(text='🇬🇵Гваделупа', callback_data='gp'),
        telebot.types.InlineKeyboardButton(text='🇬🇩Гренада', callback_data='gd')
    )
    markup.row(
        telebot.types.InlineKeyboardButton(text='🇩🇲Домініка', callback_data='dm'),
        telebot.types.InlineKeyboardButton(text='🇩🇴Домініканська Республіка', callback_data='do'),
        telebot.types.InlineKeyboardButton(text='🇰🇾Кайманові Острови', callback_data='ky')
    )
    markup.row(
        telebot.types.InlineKeyboardButton(text='🇨🇺Куба', callback_data='cu'),
        telebot.types.InlineKeyboardButton(text='🇨🇼Кюрасао', callback_data='cw'),
        telebot.types.InlineKeyboardButton(text='🇲🇶Мартиніка', callback_data='mq')
    )
    markup.row(
        telebot.types.InlineKeyboardButton(text='🇲🇸Монтсеррат', callback_data='ms'),
        telebot.types.InlineKeyboardButton(text='🇹🇨Острови Теркс і Кайкос', callback_data='tc'),
        telebot.types.InlineKeyboardButton(text='🇵🇷Пуерто-Рико ', callback_data='pr')
    )
    markup.row(
        telebot.types.InlineKeyboardButton(text='🇳🇱Саба ', callback_data='bq'),
        telebot.types.InlineKeyboardButton(text='🇯🇲Ямайка', callback_data='jm'),
        telebot.types.InlineKeyboardButton(text=' Сент-Люсія', callback_data='lc')
    )

    markup.row(
        telebot.types.InlineKeyboardButton(text='Пд Америка', callback_data='statisticamericaso'),
        telebot.types.InlineKeyboardButton(text='ПН Ямайка', callback_data='statisticamericano')
    )
    markup.row(
        telebot.types.InlineKeyboardButton(text='↩Назад', callback_data='nazad'),
        telebot.types.InlineKeyboardButton(text='📲Меню', callback_data=4)
    )
    bot.send_message(cid,'{0}, Виберіть країну Америки зі списку по якій потрібна інформація'.format(message.chat.username),reply_markup=markup)

#Australia
@bot.message_handler(commands=['countryLocationAustralia'])
@send_action('typing')
@save_user_activity()
def countryLocationAustralia_command_handler(message):
    cid = message.chat.id
    user_steps[cid] = 1
    markup = telebot.types.InlineKeyboardMarkup()
    markup.row(
        telebot.types.InlineKeyboardButton(text='🇦🇺Австралія', callback_data='au'),
        telebot.types.InlineKeyboardButton(text='🇻🇺Вануату', callback_data='vu'),
        telebot.types.InlineKeyboardButton(text='🇵🇬Папуа Нова Гвінея', callback_data='pg')
    )
    markup.row(
        telebot.types.InlineKeyboardButton(text='🇸🇧Соломонові острови', callback_data='sb'),
        telebot.types.InlineKeyboardButton(text='🇫🇯Фіджі', callback_data='fj'),
        telebot.types.InlineKeyboardButton(text='🇰🇮Кірібаті', callback_data='ki')
    )
    markup.row(
        telebot.types.InlineKeyboardButton(text='Маршаллові острови', callback_data='mh'),
        telebot.types.InlineKeyboardButton(text='🇳🇷Науру', callback_data='nr'),
        telebot.types.InlineKeyboardButton(text='🇳🇿Нова Зеландія', callback_data='nz')
    )
    markup.row(
        telebot.types.InlineKeyboardButton(text='🇵🇼Палау', callback_data='pw'),
        telebot.types.InlineKeyboardButton(text='🇼🇸Самоа', callback_data='ws'),
        telebot.types.InlineKeyboardButton(text='🇹🇴Тонга', callback_data='to')
    )
    markup.row(
        telebot.types.InlineKeyboardButton(text='🇹🇻Тувалу', callback_data='tv'),
        telebot.types.InlineKeyboardButton(text='🇫🇲Федеративні Штати Мікронезії', callback_data='fm'),
        telebot.types.InlineKeyboardButton(text='', callback_data='to')
    )
    markup.row(telebot.types.InlineKeyboardButton(text='Австараліа', callback_data='statisticaustralia'))
    markup.row(
        telebot.types.InlineKeyboardButton(text='↩Назад', callback_data='nazad'),
        telebot.types.InlineKeyboardButton(text='📲Меню', callback_data=4)
    )
    bot.send_message(cid,
                     '{0}, Виберіть країну Америки зі списку по якій потрібна інформація'.format(message.chat.username),
                     reply_markup=markup)