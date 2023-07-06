from django.conf import settings
from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Profile(models.Model):
    class Meta:
        verbose_name = "Telegram profil"
        verbose_name_plural = "Telegram profillar"

    tg_id = models.CharField(max_length=16, unique=True, verbose_name="ID")
    tg_username = models.CharField(max_length=255, null=True, blank=True, verbose_name="Telegram nomi (@username)")
    first_name = models.CharField(max_length=255, null=True, blank=True, verbose_name="Ismi")
    last_name = models.CharField(max_length=255, null=True, blank=True, verbose_name="Familiyasi")
    step = models.CharField(max_length=255, default="")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.tg_id or ""


class Region(models.Model):
    class Meta:
        verbose_name = "Hudud"
        verbose_name_plural = "Hududlar"

    title = models.CharField(max_length=255, verbose_name="Hudud nomi")
    cities_count = models.IntegerField(default=0, verbose_name="Tuman/shaharlar soni")
    order_num = models.IntegerField(default=1)
    moderators = models.ManyToManyField(User, related_name="regions")

    def __str__(self):
        return self.title or ""


class City(models.Model):
    class Meta:
        verbose_name = "Shahar/Tuman"
        verbose_name_plural = "Shaharlar/Tumanlar"

    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=255, verbose_name="Shahar/tuman nomi")
    mfys_count = models.IntegerField(default=0, verbose_name="MFYlar soni")

    def __str__(self):
        return self.title or ""


class Sector(models.Model):
    class Meta:
        verbose_name = "Sektor rahbari"
        verbose_name_plural = "Sektor rahbarlari"

    number = models.IntegerField(null=True)
    director = models.CharField(max_length=255, null=True, blank=True, verbose_name="Sektor rahbari")
    director_phone = models.CharField(max_length=255, null=True, blank=True, verbose_name="Sektor rahbari telefon nomeri:")

    def __str__(self):
        return self.director or "-"


class MFY(models.Model):
    class Meta:
        verbose_name = "Mahalla fuqarolar yig'ini"
        verbose_name_plural = "Mahalla fuqarolar yig'inlari"

    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True)
    sector = models.ForeignKey(Sector, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=255, verbose_name="MFY nomi")
    inspector = models.CharField(max_length=255, null=True, blank=True, verbose_name="IIB inspektori FISH")
    inspector_phone = models.CharField(max_length=255, null=True, blank=True, verbose_name="Telefon nomeri")
    rais = models.CharField(max_length=255, null=True, blank=True, verbose_name="MFY raisi FISH")
    rais_phone = models.CharField(max_length=255, null=True, blank=True, verbose_name="Telefon nomeri")
    helper = models.CharField(max_length=255, null=True, blank=True, verbose_name="Xokim yordamchisi FISH")
    helper_phone = models.CharField(max_length=255, null=True, blank=True, verbose_name="Telefon nomeri")
    leader = models.CharField(max_length=255, null=True, blank=True, verbose_name="Yoshlar yetakchisi FISH")
    leader_phone = models.CharField(max_length=255, null=True, blank=True, verbose_name="Telefon nomeri")

    def __str__(self):
        return self.title or ""


class School(models.Model):
    mfy = models.ForeignKey(MFY, on_delete=models.CASCADE, related_name="schools")
    title = models.CharField(max_length=255, verbose_name="Maktab nomi")
    head_master = models.CharField(max_length=255, verbose_name="Direktori")
    phone = models.CharField(max_length=255, verbose_name="Telefon raqami")

    def __str__(self):
        return self.title or "-"


class Feedback(models.Model):
    class Meta:
        verbose_name = "Murojaat"
        verbose_name_plural = "Murojaatlar"

    profile = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)
    text = models.TextField(verbose_name="Murojaat")


class HelperInfographic(models.Model):
    class Meta:
        verbose_name = "Hokim yordamchisi infogrfikasi"
        verbose_name_plural = "Hokim yordamchisi infogrfikalari"
    
    image = models.FileField(verbose_name="Media Fayl", null=True, blank=True)
    file_id = models.CharField(max_length=255, null=True, blank=True, verbose_name="Video ID")

    @property
    def full_url(self):
        if self.file_id:
            return self.file_id
        return "{}{}".format(settings.SITE_URL, self.image.url)


class LeaderInfographic(models.Model):
    class Meta:
        verbose_name = "Yoshlar yetakchisi infografikasi"
        verbose_name_plural = "Yoshlar yetakchisi infografikalari"
    
    image = models.FileField(verbose_name="Media Fayl", null=True, blank=True)
    file_id = models.CharField(max_length=255, null=True, blank=True, verbose_name="Video ID")

    @property
    def full_url(self):
        if self.file_id:
            return self.file_id
        return "{}{}".format(settings.SITE_URL, self.image.url)


class TelegramChannel(models.Model):
    class Meta:
        verbose_name = "Obuna telegram kanal"
        verbose_name_plural = "Obuna telegram kanallar"
    
    title = models.CharField(max_length=255, verbose_name="Kanal nomi")
    chat_id = models.CharField(max_length=255, verbose_name="ID")
    url = models.TextField(default="", verbose_name="Havola")

    def __str__(self):
        return self.title or "-"