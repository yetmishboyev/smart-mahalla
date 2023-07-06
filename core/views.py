from rest_framework.viewsets import GenericViewSet, mixins
from rest_framework.response import Response
from rest_framework import status

from core.services import BotService, TelegramService
from core.keyboards import *
from core.locales import *
from core.utils import send_infographics_photos, send_infographics_videos
from core.serializers import JustSerializer



class BotViewSet(
        mixins.CreateModelMixin,
        GenericViewSet
    ):
    authentication_classes = []
    permission_classes = []
    serializer_class = JustSerializer


    def create(self, request):
        data = request.data

        data_service = TelegramService(data)
        bot_service = BotService(data)

        print(data_service.text)

        if data_service.text == CONFIRM:
            if data_service.member:
                bot_service.delete_message(data_service.message_id)
                bot_service.send_message(WELCOME_TEXT, MAIN_MENU_KEYBOARD)
                data_service.set_step("main-menu")
            else:
                bot_service.delete_message(data_service.message_id)
                CHANNELS_KEYBOARD = get_subscription_keyboard(data_service.unsubscribed)
                bot_service.send_message(JOIN_CHANNELS, CHANNELS_KEYBOARD, inline=True)
                data_service.set_step("ask-subsciption")
        
        elif data_service.text == BACK and data_service.check_step("regions"):
            bot_service.send_message(WELCOME_TEXT, MAIN_MENU_KEYBOARD)
            bot_service.delete_message(data_service.message_id)
        
        elif data_service.text == BACK and data_service.check_step("city"):
            REGIONS_INLINE_KEYBOARD = get_regions_keyboard()
            bot_service.send_message(CHOOSE_REGION, REGIONS_INLINE_KEYBOARD, inline=True)
            data_service.set_step("regions")
            bot_service.delete_message(data_service.message_id)

        elif not data_service.member:
            CHANNELS_KEYBOARD = get_subscription_keyboard(data_service.unsubscribed)
            bot_service.send_message(JOIN_CHANNELS, CHANNELS_KEYBOARD, inline=True)
            data_service.set_step("ask-subsciption")

        elif data_service.text == START or data_service.text == BACK:
            bot_service.send_message(WELCOME_TEXT, MAIN_MENU_KEYBOARD)
            data_service.set_step("main-menu")

        elif data_service.text == MAIN_MENU_ITEM1:
            REGIONS_INLINE_KEYBOARD = get_regions_keyboard()
            bot_service.send_message(CHOOSE_REGION, REGIONS_INLINE_KEYBOARD, inline=True)
            data_service.set_step("regions")
        
        elif data_service.text.startswith("data-region"):
            region_title = data_service.text.split("-")[-1]
            cities = City.objects.filter(region__title=region_title)
            if not cities.exists():
                bot_service.send_message(DATA_NOT_EXISTS)
            else:
                bot_service.delete_message(data_service.message_id)
                CITY_INLINE_KEYBOARD = get_city_keyboard(cities)
                bot_service.send_message(region_title, CITY_INLINE_KEYBOARD, inline=True)
            data_service.set_step("city")
        
        elif data_service.text.startswith("data-city"):
            city_title = data_service.text.split("-")[-1]
            mfys = MFY.objects.filter(city__title=city_title).order_by("title")
            if not mfys.exists():
                bot_service.send_message(DATA_NOT_EXISTS)
            else:
                MFYS_KEYBOARD = get_mfy_keyboard(mfys)
                bot_service.send_message(city_title, MFYS_KEYBOARD)
            data_service.set_step(f"city-{city_title}")
        
        elif data_service.text == MAIN_MENU_ITEM2:
            bot_service.send_message(CHOOSE_INFO, INFO_KEYBOARD)
            data_service.set_step("info")
        
        elif data_service.text == MAIN_MENU_ITEM3:
            bot_service.send_message(SEND_FEEDBACK)
            data_service.set_step("feedback")
        
        elif data_service.text == HELPER:
            files = HelperInfographic.objects.all()
            send_infographics_videos(bot_service, files)
            send_infographics_photos(bot_service, files)
            data_service.set_step("helper-info")
        
        elif data_service.text == LEADER:
            files = LeaderInfographic.objects.all()
            send_infographics_videos(bot_service, files)
            send_infographics_photos(bot_service, files)
            data_service.set_step("leader-info")

        elif data_service.check_step("feedback") and data_service.text:
            print(13)
            bot_service.send_message(THANKS_FEEDBACK, MAIN_MENU_KEYBOARD)
            feedback = Feedback(
                profile=data_service.profile,
                text=data_service.text
            )
            feedback.save()
            data_service.set_step("main-menu")


        step = data_service.get_step()
        mfy = MFY.objects.filter(title__icontains=data_service.text)
        if step.startswith("city-"):
            city_title = step.split("-")[-1]
            print(city_title)
            print(mfy)
            mfy = mfy.filter(city__title__icontains=city_title)
            print(city_title)
            print(mfy)
        if mfy.exists():
            mfy = mfy.first()
            text = get_mfy_text(mfy)
            bot_service.send_message(text)

        return Response(status=status.HTTP_200_OK)