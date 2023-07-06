from django.conf import settings
import requests as r
from openpyxl import load_workbook
from django.db.utils import IntegrityError

from core.models import MFY, City, Profile, School, Sector, TelegramChannel
from core.utils import *


class TelegramService:
    def __init__(self, data):
        self.data = data
    
    @property
    def message(self):
        return self.data.get("message", {})
    
    @property
    def callback_query(self):
        return self.data.get("callback_query", {})
    
    @property
    def chat(self):
        return self.message.get("chat", {})
    
    @property
    def chat_id(self):
        chat_id = self.chat.get("id", 0)
        if chat_id == 0:
            chat_id = self.data \
                .get("callback_query", {}) \
                .get("message", {}) \
                .get("chat", {}) \
                .get("id", 0)
        return chat_id
    
    @property
    def username(self):
        return self.chat.get("username", "")
    
    @property
    def first_name(self):
        return self.chat.get("first_name", "")
    
    @property
    def last_name(self):
        return self.chat.get("last_name", "")
    

    @property
    def text(self):
        text = self.message.get("text", "")
        if text == "":
            text = self.callback_query.get("data", "")
        return text
    

    @property
    def message_id(self):
        message_id = self.message.get("message_id", "")
        if message_id == "":
            message = self.callback_query.get("message", {})
            message_id = message.get("message_id", "")
        return message_id

    @property
    def profile(self):
        profile = self.get_or_create_profile()
        return profile
    
    @property
    def unsubscribed(self):
        channels = TelegramChannel.objects.all()
        unsubscribed_channels = []
        for channel in channels:
            if not BotService.check_member(channel.chat_id, self.chat_id):
                unsubscribed_channels.append(channel)
        
        return unsubscribed_channels


    @property
    def member(self):
        return len(self.unsubscribed) == 0
        

    def get_or_create_profile(self):
        profiles = Profile.objects.filter(tg_id=self.chat_id)
        if profiles.exists():
            profile = profiles.first()
            return profile
        profile = Profile(
            tg_id=self.chat_id,
            tg_username=self.username,
            first_name=self.first_name,
            last_name=self.last_name
        )
        profile.save()
        return profile
    

    def check_step(self, step):
        profile = self.get_or_create_profile()
        return profile.step == step
    
    def set_step(self, step):
        profile = self.get_or_create_profile()
        profile.step = step
        profile.save()
    
    def get_step(self):
        profile = self.get_or_create_profile()
        return profile.step


class BotService:
    BASE_URL = "https://api.telegram.org/bot{}/".format(settings.BOT_TOKEN)
    
    def __init__(self, data):
        self.chat_id = TelegramService(data).chat_id
    

    def send_message(self, text, menu=None, inline=False):
        ACTION_VERB = "sendMessage"
        URL = "{}{}".format(self.BASE_URL, ACTION_VERB)
        DATA = {
            "chat_id": self.chat_id,
            "text": text,
            "parse_mode": "HTML"
        }
        if menu:
            if inline:
                DATA["reply_markup"] = {
                    "inline_keyboard": menu
                }
            else:
                DATA["reply_markup"] = {
                    "resize_keyboard": True,
                    "one_time_keyboard": True,
                    "keyboard": menu
                }
        response = r.post(
            URL,
            json=DATA
        )
        if response.status_code == 200:
            return True
        return False
    

    def send_photo(self, image_url):
        ACTION_VERB = "sendPhoto"
        URL = "{}{}".format(self.BASE_URL, ACTION_VERB)
        DATA = {
            "chat_id": self.chat_id,
            "photo": image_url,
            "parse_mode": "HTML"
        }
        response = r.post(
            URL,
            json=DATA
        )
        print(response.content)
        if response.status_code == 200:
            return True
        return False


    def send_video(self, video_url):
        ACTION_VERB = "sendVideo"
        URL = "{}{}".format(self.BASE_URL, ACTION_VERB)
        DATA = {
            "chat_id": self.chat_id,
            "video": video_url,
            "parse_mode": "HTML"
        }
        response = r.post(
            URL,
            json=DATA
        )
        print(response.content)
        if response.status_code == 200:
            return True
        return False
    

    def send_images(self, image_urls):
        ACTION_VERB = "sendMediaGroup"
        URL = "{}{}".format(self.BASE_URL, ACTION_VERB)
        DATA = {
            "chat_id": self.chat_id,
            "media": [
                {
                    "type": "photo",
                    "media": image_url
                } for image_url in image_urls
            ]
        }
        from pprint import pprint
        pprint(DATA)
        response = r.post(
            URL,
            json=DATA
        )
        print(response.content)
        if response.status_code == 200:
            return True
        return False


    def send_videos(self, video_urls):
        ACTION_VERB = "sendMediaGroup"
        URL = "{}{}".format(self.BASE_URL, ACTION_VERB)
        DATA = {
            "chat_id": self.chat_id,
            "media": [
                {
                    "type": "video",
                    "media": image_url
                } for image_url in video_urls
            ]
        }
        response = r.post(
            URL,
            json=DATA
        )
        if response.status_code == 200:
            return True
        return False


    def delete_message(self, message_id):
        ACTION_VERB = "deleteMessage"
        URL = "{}{}".format(self.BASE_URL, ACTION_VERB)
        DATA = {
            "chat_id": self.chat_id,
            "message_id": message_id
        }
        print(DATA)
        response = r.post(
            URL,
            json=DATA
        )
        print(response.content)
        if response.status_code == 200:
            return True
        return False
    

    @staticmethod
    def check_member(chat_id, user_id):
        ACTION_VERB = "getChatMember"
        BASE_URL = "https://api.telegram.org/bot{}/".format(settings.BOT_TOKEN)
        URL = "{}{}".format(BASE_URL, ACTION_VERB)
        DATA = {
            "chat_id": chat_id,
            "user_id": user_id
        }
        response = r.post(
            URL,
            json=DATA
        )
        if response.status_code == 200:
            data = response.json()
            if not data["ok"]:
                return data["ok"]
            else:
                return data["result"]["status"] != "left" and data["result"]["status"] != "banned"
        return False


class MfyData:
    def __init__(self, data, cities):
        city_id = int(data[0])
        self.city = cities[city_id]
        self.title = data[1]
        self.inspector = data[2] or ""
        self.inspector_phone = clean_phone_number(data[3] or "")
        self.rais = data[4] or ""
        self.rais_phone = clean_phone_number(data[5] or "")
        self.helper = data[6] or ""
        self.helper_phone = clean_phone_number(data[7] or "")
        self.leader = data[8] or ""
        self.leader_phone = clean_phone_number(data[9] or "")
        self.schools = self.exptract_schools(data)
        self.sector = data[14] or ""
        self.sector_phone = data[15] or ""
        # self.translit()
    

    def exptract_schools(self, data):
        column = data[10]
        phones = data[11]
        schools_list = []
        if not column:
            return schools_list
        schools_raw = list(filter(lambda x: len(str(x)) > 0, str(column).split(";")))
        phones_raw = list(filter(lambda x: len(str(x)) > 0, str(phones).split(";")))
        for index, school in enumerate(schools_raw):
            try:
                if "maktab" in school:
                    title, head_master = list(map(lambda x: x.strip(), school.split("maktab")))
                    title += " maktab"
                elif "IDUM" in school:
                    title, head_master = list(map(lambda x: x.strip(), school.split("IDUM")))
                    title += " IDUM"
                schools_list.append({
                    "title": title,
                    "head_master": head_master,
                    "phone": clean_phone_number(phones_raw[index])
                })
            except:
                schools_list.append({
                    "title": "-",
                    "head_master": "-",
                    "phone": "-"
                })
        return schools_list


    def translit(self):
        trans = Trans()
        text = "{}=={}=={}=={}=={}=={}".format(
            self.title,
            self.inspector,
            self.rais,
            self.helper,
            self.leader,
            self.sector
        )
        result = trans.translit(text).split("==")
        self.title = result[0]
        self.inspector = result[1]
        self.rais = result[2]
        self.helper = result[3]
        self.leader = result[4]
        self.sector = result[5]
    

    def json(self):
        return {
            "city": self.city,
            "title": self.title,
            "inspector": self.inspector,
            "inspector_phone": self.inspector_phone,
            "rais": self.rais,
            "rais_phone": self.rais_phone,
            "helper": self.helper,
            "helper_phone": self.helper_phone,
            "leader": self.leader,
            "leader_phone": self.leader_phone,
            "schools": self.schools,
            "sector": {
                "director": self.sector,
                "director_phone": self.sector_phone
            }
        }


class ExcelService:
    error = None
    items_sheet = None
    cities_sheet = None
    cities = {}

    def __init__(self, file_name):
        try:
            self.wb = load_workbook(file_name)
            for sheet in self.wb:
                if sheet.title == "Sheet1":
                    self.items_sheet = sheet
                if sheet.title == "Sheet2":
                    self.cities_sheet = sheet
        except:
            self.error = "Cannot be opened"
            return

    
    def execute(self):
        if not self.items_sheet or not self.cities_sheet:
            self.error = "Sheet not found"
            return
        
        for row in self.cities_sheet.values:
            try:
                city = City.objects.get(id=row[1])
                self.cities[city.id] = city
            except Exception as e:
                print(e)
        
        for row in self.items_sheet.values:
            if row[0] and row[0] != "Tuman/Shaharlar IDsi":
                mfy_data = MfyData(row, self.cities)
                self.save_or_update(mfy_data.json())
    

    def save_or_update(self, mfy_data):
        print(mfy_data)
        schools_list = mfy_data.pop("schools", [])
        sector_data = mfy_data.pop("sector", {})
        mfys = MFY.objects.filter(city=mfy_data["city"], title=mfy_data["title"])
        sector = Sector.objects.filter(**sector_data)
        if sector.exists():
            sector = sector.first()
        else:
            sector = Sector(**sector_data)
            sector.save()
        if mfys.exists():
            mfy_obj = mfys.first()
            for key in mfy_data.keys():
                if hasattr(mfy_obj, key):
                    setattr(mfy_obj, key, mfy_data[key])
        else:
            mfy_obj = MFY(**mfy_data)
        try:
            mfy_obj.sector = sector
            mfy_obj.save()
        except IntegrityError:
            return
        for school_item in schools_list:
            school = School(mfy=mfy_obj, **school_item)
            school.save()