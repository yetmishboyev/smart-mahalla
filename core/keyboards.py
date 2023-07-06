from core.locales import *
from core.models import *
from core.utils import clean_phone_number


MAIN_MENU_KEYBOARD = [
    [
        {
            "text": MAIN_MENU_ITEM1
        },
        {
            "text": MAIN_MENU_ITEM2
        }
    ],
]


def get_regions_keyboard():
    REGIONS_INLINE_KEYBOARD = [
        [
            {
                "text": BACK,
                "callback_data": BACK
            }
        ],
        []
    ]
    regions = Region.objects.all().order_by("order_num")
    for index, region in enumerate(regions):
        REGIONS_INLINE_KEYBOARD[-1].append({
            "text": "{}".format(region.title),
            "callback_data": "data-region-{}".format(region.title)
        })
        if index % 2 == 1:
            REGIONS_INLINE_KEYBOARD.append([])
    return REGIONS_INLINE_KEYBOARD


def get_city_keyboard(cities):
    CITY_INLINE_KEYBOARD = [
        [
            {
                "text": BACK,
                "callback_data": BACK
            }
        ],
        []
    ]
    for index, city in enumerate(cities):
        CITY_INLINE_KEYBOARD[-1].append({
            "text": "{} ({})".format(city.title, city.mfys_count),
            "callback_data": "data-city-{}".format(city.title)
        })
        if index % 2 == 1:
            CITY_INLINE_KEYBOARD.append([])
    return CITY_INLINE_KEYBOARD


def get_mfy_keyboard(mfys):
    MFYS_INLINE_KEYBOARD = [
        [{"text": BACK}],
        []
    ]
    for index, mfy in enumerate(mfys):
        MFYS_INLINE_KEYBOARD[-1].append({
            "text": mfy.title
        })
        if index % 2 == 1:
            MFYS_INLINE_KEYBOARD.append([])
    return MFYS_INLINE_KEYBOARD


def get_mfy_text(mfy):
    text = "👆<b>MFY nomi: {}</b>".format(mfy.title)
    
    try:
        if mfy.sector and mfy.sector.director:
            number = ""
            if mfy.sector.number:
                number = "{}-".format(mfy.sector.number)
            text += "\n\n👮‍♂️{}Sektor rahbari: {}".format(number, mfy.sector.director)
            text += "\n☎️Telefon nomeri: {}".format(clean_phone_number(mfy.sector.director_phone))
    except:
        pass

    if mfy.rais and mfy.rais_phone:
        text += "\n\n🔰MFY raisi: {}".format(mfy.rais)
        text += "\n☎️Telefon nomeri: {}".format(clean_phone_number(mfy.rais_phone))
    
    if mfy.inspector and mfy.inspector_phone:
        text += "\n\n👮‍♂️IIB inspektori: {}".format(mfy.inspector)
        text += "\n☎️Telefon nomeri: {}".format(clean_phone_number(mfy.inspector_phone))
    
    if mfy.helper and mfy.helper_phone:
        text += "\n\n🔰Xokim yordamchisi: {}".format(mfy.helper)
        text += "\n☎️Telefon nomeri: {}".format(clean_phone_number(mfy.helper_phone))
    
    if mfy.leader and mfy.leader_phone:
        text += "\n\n🔰Yoshlar yetakchisi: {}".format(mfy.leader)
        text += "\n☎️Telefon nomeri: {}".format(clean_phone_number(mfy.leader_phone))
    
    try:
        if "qoraqalp" in mfy.city.region.title.lower() and mfy.schools.count() > 0:
            for school in mfy.schools.all():
                text += "\n\n🏫Maktab nomi: {}".format(school.title)
                text += "\n🔰Maktab direktori: {}".format(school.head_master)
                text += "\n☎️Telefon nomeri: {}".format(clean_phone_number(school.phone))
    except:
        pass
    
    return text


INFO_KEYBOARD = [
    [
        {
            "text": HELPER
        },
        {
            "text": LEADER
        },
    ],
    [{"text": BACK}]
]


def get_subscription_keyboard(channels):
    SUBSCRIPTION_INLINE_KEYBOARD = [
        []
    ]
    for index, channel in enumerate(channels):
        SUBSCRIPTION_INLINE_KEYBOARD[-1].append({
            "text": "⭕️{}".format(channel.title),
            "url": "{}".format(channel.url)
        })
        SUBSCRIPTION_INLINE_KEYBOARD.append([])
    SUBSCRIPTION_INLINE_KEYBOARD.append([
        {
            "text": CONFIRM,
            "callback_data": CONFIRM
        }
    ])
    return SUBSCRIPTION_INLINE_KEYBOARD