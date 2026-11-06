import logging
import random
import asyncio
import json
import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command  # ✅ Import qilindi!
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton
from aiogram.enums import ParseMode

# --- SOZLAMALAR ---
API_TOKEN = '8854687442:AAEarzvBTt16bTwkdiDAJPI4-ZcvLQgD2ZU' 
ADMIN_ID = 8214712481 
CHANNEL_ID = -1003138510513
CHANNEL_LINK = "https://t.me/anizone_kawai"
INSTA_LINK = "https://instagram.com/anizone_kawai"
TIKTOK_LINK = "https://tiktok.com/@anizone_kawai"
DATA_FILE = "bot_data.json"

logging.basicConfig(level=logging.INFO)

# --- ANIMELAR BAZASI ---
MOVIES_BASE = {
    "35": {
        "title": "Ko'k zindon",
        "photo": "AgACAgQAAxkBAANsakqSMmQ8KAs6JPOt3L3fJRWIkOAAAmcOaxuc5FlSh5LVsHO0DFQBAAMCAAN5AAM8BA",
        "info": "🎬 Nomi: Ko'k zindon\n🎥 Qismi: 25\n🌍 Davlati: Yaponiya\n🗣 Til: O'zbek tilida\n Yil: 2024\n Janr: Ekshn, Sarguzasht, Fantastika\n\n🍿 @anizone_kawai",
        "episodes": {
            "1": "BAACAgQAAxkBAAM7akqR0vA4jA34HPstU1hy9O1tMCIAAkoSAAIwVAABULoC_XyxD0lXPAQ",
            "2": "BAACAgQAAxkBAAM8akqR0q-bxvYYyt4gpn0phhsuE44AAkwSAAIwVAABUGVeL7Tifkv6PAQ",
            "3": "BAACAgQAAxkBAAM_akqR5GKII3fm9Rr7hhsHiTTWP5YAAk0SAAIwVAABUO4UAAF4Bb80AzwE",
            "4": "BAACAgQAAxkBAANAakqR5EBqCMb8kmjjDrvBahSoYuAAAk8SAAIwVAABUL745jqcpiIBPAQ",
            "5": "BAACAgQAAxkBAANDakqR6yOUXMvxRyLjq8RdNEv9gdYAAlESAAIwVAABUERWCNzxVwn0PAQ",
            "6": "BAACAgQAAxkBAANEakqR6w3kbRO8Wbp1cGlK9oDMFTYAAlISAAIwVAABUPE4CFLccNNiPAQ",
            "7": "BAACAgQAAxkBAANHakqR8QNieq2rYiKMVvP9nAABzCgBAAJVEgACMFQAAVB9Cc5-21xTezwE",
            "8": "BAACAgQAAxkBAANIakqR8UJ2ZRGD71LBBcekFaBjHgIAAlYSAAIwVAABUIZ8Zzkt_D3jPAQ",
            "9": "BAACAgQAAxkBAANLakqR-HyG2s31bXTGgOA-QxsHECwAAlgSAAIwVAABUG5hAjqqVILRPAQ",
            "10": "BAACAgQAAxkBAANMakqR-NTa6MuA1YUW9W4m6PvMNzQAAlkSAAIwVAABUMxlYpWUYxKoPAQ",
            "11": "BAACAgQAAxkBAANPakqR_n_CxCsCYvkIulX8vyciIA4AAloSAAIwVAABUI_SZJwOBPbfPAQ",
            "12": "BAACAgQAAxkBAANQakqR_ozEnN6uq4kR0D5-J8hqffQAAlsSAAIwVAABUIVUPp6uaxZqPAQ",
            "13": "BAACAgQAAxkBAANTakqSBIxMWapebErfdYe2bPVygEoAAlwSAAIwVAABUNb3LYRmJS70PAQ",
            "14": "BAACAgQAAxkBAANUakqSBDQn3GJTCJLY7NwenTv481gAAl4SAAIwVAABUITHhN-P5FAePAQ",
            "15": "BAACAgQAAxkBAANXakqSDEfHN7Y92-YdfxhtJq-lG7cAAl8SAAIwVAABUBvHrJhdCF5RPAQ",
            "16": "BAACAgQAAxkBAANYakqSDEnukz6nB7dq08WyBte9JGcAAmASAAIwVAABUKb9_9028SqwPAQ",
            "17": "BAACAgQAAxkBAANXakqSDEfHN7Y92-YdfxhtJq-lG7cAAl8SAAIwVAABUBvHrJhdCF5RPAQ",
            "18": "BAACAgQAAxkBAANYakqSDEnukz6nB7dq08WyBte9JGcAAmASAAIwVAABUKb9_9028SqwPAQ",
            "19": "BAACAgQAAxkBAANfakqSG3hP44CNHgOvDs6Vv4XDaAMAAmESAAIwVAABUC9-o6SFyxvTPAQ",
            "20": "BAACAgQAAxkBAANgakqSG1Mla2W_XcyyQuyL84VA_tkAAm4SAAIwVAABUOk7Q5ZLnFpnPAQ",
            "21": "BAACAgQAAxkBAANjakqSIcBGXs9V8FAnPFfYRpz-h-QAAooSAAIwVAABUGhoE2CxUCcGPAQ",
            "22": "BAACAgQAAxkBAANkakqSIQxyY00wIDiS0Zk71gAB3e-AAAKLEgACMFQAAVCE2B6ANm6iKzwE",
            "23": "BAACAgQAAxkBAANnakqSJxAY7Hepgg8S9YEjpkycHUUAAowSAAIwVAABUCE4ton24CZtPAQ",
            "24": "BAACAgQAAxkBAANoakqSJ8UkOyCm5WSG9PjLY5JniyMAAo4SAAIwVAABUHSm5KMbZHQFPAQ",
            "25": "BAACAgQAAxkBAANrakqSMl3MQaVFUwpLlHDsDDkIhDAAApASAAIwVAABUIreeUk9E7OqPAQ"
        }
    },
    "526": {
            "title": "Moviy iblis ovchilari",
            "photo": "AgACAgIAAxkBAAIEqGpSY3L2G-nTeAOzouSVx6Tr8D0UAAJgGmsbjwABkUrTtmY8TY2UiQEAAwIAA3kAAzwE",
            "info": "🎬 Nomi: Moviy iblis ovchilari\n🎥 Qismi: 13/13\n🌍 Davlati: Yaponya\n🇺🇿 Tili: Uzbek tilida\n📆 Yili: 2022\n🎞 Janri: Akshin fantasy\n\n🔍Qidirishlar soni: 23\n\n🍿 @anizone_kawai",
            "episodes": {
                "1": "BAACAgIAAxkBAAIEjmpSYm2cgFZkMi_EeBxRuu8ymnpFAAJ1LgAClcBgSQABF483Z8TebzwE",
                "2": "BAACAgIAAxkBAAIEj2pSYm1sXE0Md6ltwEqe95yUgymhAAKaKgACJKhYSk7ENwpxKjmYPAQ",
                "3": "BAACAgIAAxkBAAIEkGpSYm2G0nQbvhgGDdpmHysIK7t9AAIkKAAC2I6JSgkmvwWwWxgaPAQ",
                "4": "BAACAgIAAxkBAAIEkWpSYm2lbOSNSIGEPPVriRTVW2bLAAKDKAACVvLhSq4kiSDCp2p3PAQ",
                "5": "BAACAgIAAxkBAAIEkmpSYm3A4KAFy74Fw6fqi3jqubLbAAI7LAACykQAAUuaoYT5i_LWaTwE",
                "6": "BAACAgIAAxkBAAIEk2pSYm2-HBUod-nY54SqS2Ext613AAJ6OAAC8VUxS-Fl75QRG9MPPAQ",
                "7": "BAACAgIAAxkBAAIElGpSYm3dx5VOnjVoCNwmoCOk1mSSAAJlJgACEbeRSy-qzDvKNK1jPAQ",
                "8": "BAACAgIAAxkBAAIElWpSYm3HBsKvnD14thaQ2XJoK8uDAAJUMAAC_VcgSOulaEuj7Mw8PAQ",
                "9": "BAACAgIAAxkBAAIElmpSYm0-wVYSUAzqgWMczSx4T_wtAAJ-KgACb-GwSJsPQ6_85YwFPAQ",
                "10": "BAACAgIAAxkBAAIEl2pSYm0PlQnKNAccw7uFztdppm68AAJ5MwAClkbZSMQ52iEINKOfPAQ",
                "11": "BAACAgIAAxkBAAIEmGpSYm32kkWmr7xX4GqvnsZI_XcbAAL9LwAC2FSYSmMHGlBLAcEePAQ",
                "12": "BAACAgIAAxkBAAIEmWpSYm1Shdupm-nCanxs_S7Nc2BxAAKmLwAC9U2ZSscg0g4F6EnGPAQ",
                "13": "BAACAgIAAxkBAAIEmmpSYm2qfCuqvaz5Fvo10pPLdnxvAAIYMAAC9B-xSpHcA-E46drzPAQ"
            }
        },
    "200": {
        "title": "Ochko'z berserk",
        "photo": "AgACAgIAAxkBAAO8akqVRVSr4D2I-rvsRA2uZvQ9VoQAAsbSMRugFhBIKkJUlEhJKPEBAAMCAAN3AAM8BA",
        "info": "🎬 Nomi: Ochko'z berserk\n🎥 Qismi: 12\n🌍 Davlati: Yaponiya\n🗣 Til: O'zbek tilida\n📅 Yil: 2024\n🎭 Janr: Ekshn, Fantastika, Drama\n\n🍿 @anizone_kawai",
        "episodes": {
            "1": "BAACAgUAAxkBAANvakqS9aI-fNEXcz-mxq7eTaZccwEAAogNAAKEzAFUQdjxf264Jqk8BA",
            "2": "BAACAgUAAxkBAANwakqS9dLxPQhwr5z3VirGhcMnzmUAAqcNAAKW_QFUD_J1XwoI8i88BA",
            "3": "BAACAgUAAxkBAANzakqTDthXxVN_-bAPKDVk_QlrmeoAAk8MAAKtbwFUYnKc7HkYz2A8BA",
            "4": "BAACAgQAAxkBAAN0akqTDoFskHp5j9LwyPn2wyBH2GkAAn4QAALeTwlQ80XEikOUgTc8BA",
            "5": "BAACAgQAAxkBAAN3akqTGIZ4NXPoVmRq3vnS_gQIkn0AAg8UAAL8TgFQhxNAdci00Aw8BA",
            "6": "BAACAgUAAxkBAAN4akqTGByUfD8JzV_WTVfRZPqhQRgAAlAMAAKtbwFUoQvJVqUw-Fc8BA",
            "7": "BAACAgQAAxkBAAN7akqTH8CkEyeMO8P6DkiGm2Hr3esAAoAQAALeTwlQM1DSPhoaIe08BA",
            "8": "BAACAgQAAxkBAAN8akqTH7qgp_Bbyri6sCD9RhHEaS8AAn8QAALeTwlQgHCh9mQtUx48BA",
            "9": "BAACAgQAAxkBAAN_akqTJDhkg7_HPd2mzEHdLuAn1UsAAoEQAALeTwlQp7ZWPzcj58o8BA",
            "10": "BAACAgUAAxkBAAOAakqTJKAQKgABNiv7-yrVksfI1CzuAAKpDQAClv0BVIvCnz2EcLn7PAQ",
            "11": "BAACAgQAAxkBAAODakqTK_DMRr_vyRgQfLERq_D7IwIAAoIQAALeTwlQaHGg4qVj1h88BA",
            "12": "BAACAgQAAxkBAAOEakqTK4sbtaBV8S0M70NlfecXVl0AAoMQAALeTwlQ4w6M8-k62Rw8BA"
        }
    },
    "49": {
        "title": "Omadsizning qayta tug'ilishi",
        "photo": "AgACAgQAAxkBAAIBhmpKqGPps7Njh-d5BEHu3cjjO0YoAAJ_D2sbeapQUpP7M17mCoHSAQADAgADeQADPAQ",
        "info": "🎬 Nomi: Omadsizning qayta tug'ilishi\n🎥 Qismi: 36\n Davlati: Yaponiya\n Til: O'zbek tilida\n Yili: 2025\n Janri: Isekai, Fantastika, Sarguzasht, Sehr\n📺 Sifat: 720p | 1080p\n\n✨ Omadsiz hayot ortda qoldi... Endi esa yangi dunyoda yangi imkoniyatlar kutmoqda!\n\n🍿 @anizone_kawai",
        "episodes": {
            "1": "BAACAgUAAxkBAAPZakqkrD2gPhJnMZ0b7EtmU_TrE3QAAuAOAAICJKBXvYe6ULSP4HE8BA",
            "2": "BAACAgUAAxkBAAPaakqkrNoEUPEs1gqL0ChGL5xh2uYAAuQOAAICJKBX4TEl284qSIY8BA",
            "3": "BAACAgUAAxkBAAPdakqktmRzlGDqHQLGqNPBajWGxJ8AAuYOAAICJKBXDj3L1lpKtNA8BA",
            "4": "BAACAgUAAxkBAAPeakqktlThnDzaMZk7fX5e8N1r7TYAAuoOAAICJKBXG8XX4jxENbc8BA",
            "5": "BAACAgUAAxkBAAPnakqlijosAXjeGCKg1g4GOFb_rcYAAu8OAAICJKBXwMbmuDVBd5U8BA",
            "6": "BAACAgUAAxkBAAPoakqliqUGPUvSDaxFxZeZOOf_DQ8AAvMOAAICJKBXeVjUqYAEIj88BA",
            "7": "BAACAgUAAxkBAAPpakqlitaUQmPSx4ttYkfU-RJlSj4AAvQOAAICJKBXHQap-nBJUxI8BA",
            "8": "BAACAgUAAxkBAAPqakqlior77_70M14kYsFfYtb85jIAAvUOAAICJKBXkc6BTT41XtM8BA",
            "9": "BAACAgUAAxkBAAPrakqlit4_8jy2ssALfSvCAAEKmU0PAAL2DgACAiSgV5GFRhdBTlQrPAQ",
            "10": "BAACAgUAAxkBAAPsakqlinxcRzSlH_Xu3QmXp3pSkewAAvcOAAICJKBXGTBarx4XePA8BA",
            "11": "BAACAgUAAxkBAAPtakqlisHVbhfnLZIU8tpi1xYLO3kAAvwOAAICJKBXvxTu485H-K48BA",
            "12": "BAACAgQAAxkBAAPuakqlijWQ1lThetdS6u3DA1E3wBMAAhYQAAJUeaBTZtRK-44IMlA8BA",
            "13": "BAACAgQAAxkBAAPvakqlihyffiBXQw1zaemXumtguGoAAhcQAAJUeaBTr56CBt1F3JU8BA",
            "14": "BAACAgQAAxkBAAPwakqlitisAwjRTRiPtwYiL4kRp-AAAhgQAAJUeaBTYVF_9TEmkeU8BA",
            "15": "BAACAgQAAxkBAAPxakqliouo9NqX-kv6sqR_mlvQ-UgAAhkQAAJUeaBTUt12EuOaSgY8BA",
            "16": "BAACAgQAAxkBAAPzakqlijH4FOAx_7GHnSyHjyrvE-0AAhoQAAJUeaBTuCuxUWoChhE8BA",
            "17": "BAACAgQAAxkBAAPyakqlikPyIvhhFCCDGMQDyFF3yZkAAhsQAAJUeaBTUXwliqo5hrI8BA",
            "18": "BAACAgQAAxkBAAP0akqliikQ85Du7YpJMzAT33OzubwAAhwQAAJUeaBTdY4S-S37ilk8BA",
            "19": "BAACAgQAAxkBAAP1akqlimd1L48jxkbV4AXdJOLdTBoAAh0QAAJUeaBTpx9GCOvDjXA8BA",
            "20": "BAACAgQAAxkBAAP2akqliqv_Aos3GpcJ8t9WWChyzvUAAh4QAAJUeaBT3x0tylAD7uQ8BA",
            "21": "BAACAgQAAxkBAAP3akqlip4f110Iz9yuQvQYQvHVNucAAh8QAAJUeaBTe_OPIy_t2CA8BA",
            "22": "BAACAgQAAxkBAAP5akqliqLKAzdAzDwQCBUNK3BczugAAiAQAAJUeaBTNT-Z58d82TM8BA",
            "23": "BAACAgQAAxkBAAP6akqlira5bMMzK1g8YjnCSO7DhjsAAiYQAAJUeaBTKor_rolXFFg8BA",
            "24": "BAACAgQAAxkBAAP4akqlisd614K3nbH8WZZQZrozU2wAAiMQAAJUeaBTW8KEfmOV9pc8BA",
            "25": "BAACAgQAAxkBAAP7akqlinj3uspq84wCDd9LR5E7zgwAAioQAAJUeaBTrLS0JspcGho8BA",
            "26": "BAACAgQAAxkBAAP8akqliutkUzHRE-QbenibNvr48SEAAisQAAJUeaBT8t9fsiuX6S48BA",
            "27": "BAACAgQAAxkBAAP9akqlitCjNM0JLASXdtQKor--5WgAAjgRAALMrcBTGE-ZrYrTZMs8BA",
            "28": "BAACAgQAAxkBAAP_akqligs22v-OBPw2cRGVUsbD2k0AAjkRAALMrcBTKTqtWXEjk_M8BA",
            "29": "BAACAgQAAxkBAAP-akqlimBWrsvyVcgcAAFW2KvAYMG5AAI6EQACzK3AUx7fl7unNUEQPAQ",
            "30": "BAACAgQAAxkBAAIBAAFqSqWK7_lMZ3pO_4Qj61bm5JskkwACPREAAsytwFMo1F7n7961PDwE",
            "31": "BAACAgQAAxkBAAIBAWpKpYryqu7AgkMyC1O_xsCxL-saAAI-EQACzK3AUw5K8sM5JuEyPAQ",
            "32": "BAACAgQAAxkBAAIBAmpKpYppkLsohvMZ24QEZqv7HD5BAAJLEQACzK3AU0N1f2X_AAHEzDwE",
            "33": "BAACAgQAAxkBAAIBA2pKpYorYi0wKCUNwx-iKiO8uEa7AAJTEQACzK3AUzNtDvE4jwulPAQ",
            "34": "BAACAgQAAxkBAAIBBGpKpYoCctfFJ1JoD0eTXY1I_baHAAJMEQACzK3AU1rvm9OLUtHjPAQ",
            "35": "BAACAgQAAxkBAAIBBWpKpYqACPEfafvt5hgzLswvbmU5AAJUEQACzK3AU4zVMxrXreJOPAQ",
            "36": "BAACAgQAAxkBAAIBBmpKpYpt35J6lVlstlpzEIfbvTeNAAJZEQACzK3AU0j97sL8_a48PAQ"
        }
    },
    "7": {
        "title": "Yolg'izlikda Daraja Ko'tarish",
        "photo": "AgACAgIAAxkBAAICeWpMXTjOXauTvXfvAW_iozw7kfZwAAJ0GWsbwIhoSuX2P_p4rAjSAQADAgADeQADPAQ",
        "info": "🎬 Nomi: Yolg'izlikda Daraja Ko'tarish\n🎥 Qismi: 25/25\n🌍 Davlati: Yaponiya\n🗣 Til: O'zbek tilida\n 📥Yil: 2024\n Janr: Ekshn, Sarguzasht, Fantastika\n\n🍿 @anizone_kawai",
        "episodes": {
            "1": "BAACAgQAAxkBAAICRmpMWdqlG42Y-skE5CzNqpmDFeLJAAKzFQAC5efIU1kjf6qhZTVfPAQ",
            "2": "BAACAgQAAxkBAAICR2pMWdpOAAHP_CX-jOdwUoCzIc7yTQACtBUAAuXnyFPPvcD5Nvp-wDwE",
            "3": "BAACAgQAAxkBAAICSmpMWenKtGFC00LMSHxEV15Ujc73AAK1FQAC5efIUwPWtjB6WtoyPAQ",
            "4": "BAACAgQAAxkBAAICS2pMWelNgerUxJCWeckuruZ40RalAAK2FQAC5efIU7n810wlefgLPAQ",
            "5": "BAACAgQAAxkBAAICTmpMWfX8mGQlqZAoA4wULdLv4FVfAAK3FQAC5efIU5VB5hwijVnIPAQ",
            "6": "BAACAgQAAxkBAAICT2pMWfXa2ms_ctzaekc7LaMhhH5zAAK4FQAC5efIU1uDmyIPwjbqPAQ",
            "7": "BAACAgQAAxkBAAICUmpMWgFLguPVrhWIQuf2SIWLmiW0AAK6FQAC5efIU0t2-1peem9kPAQ",
            "8": "BAACAgQAAxkBAAICU2pMWgEDvcT59tSXcKh8KItxMaAAA7wVAALl58hTy2zaPdU35J88BA",
            "9": "BAACAgQAAxkBAAICVmpMWhMxcQKP3fxyb71W7Kbc9e78AALCFQAC5efIU9BQxcrrx0a6PAQ",
            "10": "BAACAgQAAxkBAAICWGpMWh37jovZ6hpG67sVi4f6cg2DAALEFQAC5efIU8McaUgEj0RVPAQ",
            "11": "BAACAgQAAxkBAAICWmpMWlc1_mdcQBwIS5_K4kfNmxFtAALFFQAC5efIU3g2GbQzZ_HxPAQ",
            "12": "BAACAgQAAyEFAAS7Ed6xAANAakxaYCAwGIQFiC1uEBry35cz0SUAAsYVAALl58hTneUAAY2cfJnxPAQ",
            "13": "BAACAgQAAyEFAAS7Ed6xAANBakxag8bp2_WTWTDmmsoglPbPRI8AAvIVAALl59BT4MBHW9hdPfM8BA",
            "14": "BAACAgQAAxkBAAICXWpMWow64ou9juJt2hLAfYpQucNzAAIpGAAC9ogYUJk3rUsr9erCPAQ",
            "15": "BAACAgQAAxkBAAICX2pMWpzDYlozJVnuXb8GdXUTeVJFAALlFgACYBVhUBtm5HjU4DOTPAQ",
            "16": "BAACAgQAAxkBAAICYWpMWrYpqYVutJ4hp_1s6v2gTpCaAAJGFwAC_ZmwUCrGHuDb2eUvPAQ",
            "17": "BAACAgQAAxkBAAICY2pMWsnaa-uRCO22cQ3Xi6j8kNRfAAJEFgACJIj4ULz__RR62mvcPAQ",
            "18": "BAACAgIAAxkBAAICZWpMWtNm1jF-TJC1foTU0HM416u_AAICYwACBORZSdOty0CoV1jbPAQ",
            "19": "BAACAgIAAxkBAAICZ2pMWuOahO4cJ_I1L42g5B50vmVhAALJaQACJgqASr3FXMXb7fRdPAQ",
            "20": "BAACAgIAAxkBAAICaWpMWuxYJHMOvqbNadNgSX3seZbnAALNYgACNIPoSWqYw7ki0sY3PAQ",
            "21": "BAACAgIAAxkBAAICa2pMWvif8bFHdg6czhGYGjYVpbCUAALRaQACJgqASrI9BoHlBCWhPAQ",
            "22": "BAACAgIAAxkBAAICbWpMWwHjQ1RNvHbYvNCdoaChAAHjmQACvWEAAvmymUo484CH4GjQrDwE",
            "23": "BAACAgIAAxkBAAICcWpMW0u0xX52gAEa2jAE1XO2IJ17AAJ0cAACq_ypSnlUEGOBoMa6PAQ",
            "24": "BAACAgQAAxkBAAICc2pMW1E365ETvIJcG1VlYEgjGi2RAAJnGgAC93H4UhRUxY0o9fvbPAQ",
            "25": "BAACAgQAAxkBAAICdWpMW1u5wN6Lh8QQU-Vc-7Bw_CqYAAJZFwACp4ZBU0PLaV_DmSq7PAQ"
        }
    },
    "48": {
    "title": "Mening qotillik darajam qahramonnikidan Oshib ketdi",
    "photo": "AgACAgIAAxkBAAICrWpMrwlXxYNvIWtMr3qlB7uPnmQIAAIIGmsbwIhoSo_17um1gG7OAQADAgADeQADPAQ",
    "info": "🎬 Nomi: Mening qotillik darajam qahramonnikidan Oshib ketdi\n🎥 Qismi: 12/12\n🌍 Davlati: Yaponiya\n🗣 Til: O'zbek tilida\n📥 Yil: 2025\n🎞 Janr: Jangari, Sarguzasht\n\n🍿 @anizone_kawai",
    "episodes": {
        "1": "BAACAgIAAxkBAAIClWpMrdihQbCHzPz9EK_tEa9jeP5QAAI2hAAChF5QS5zpbJ0LuCdCPAQ",
        "2": "BAACAgIAAxkBAAIClmpMrdiGqT82YhH7YYepggLXPnjvAAJtgwACyNF5S6ZmFZYKMdbWPAQ",
        "3": "BAACAgIAAxkBAAICmWpMreoZzVTz1EO7f1YTIQuaaUjMAAKOhAAC4nTZS7k74w5hJU3ZPAQ",
        "4": "BAACAgIAAxkBAAICmmpMreoP8QEwPgb37CWXWbGL4sfrAALAhAAC0XkwSIEBlpUlZqK5PAQ",
        "5": "BAACAgIAAxkBAAICnWpMrl17i9uyAeM7PNg4gXQtTGTsAALLiAACSrlYSMEBooAWCHSUPAQ",
        "6": "BAACAgIAAxkBAAICnmpMrl0GkN25WaDpHmIiILSL25swAAKAhgACZaDBSKEsEr2AyHxPPAQ",
        "7": "BAACAgIAAxkBAAICoWpMrmgK7v0FNGvGsNMegiAY5DV0AAIokAAC8RPxSGqOzp2tT7lrPAQ",
        "8": "BAACAgIAAxkBAAICompMrmgxaFDh9819F3dh--0K5sSxAAKJgQACRt1ZSePXitXM3zUePAQ",
        "9": "BAACAgQAAxkBAAICpWpMrnPEJhWrVnzGuzlgg_47OGwpAAIXHgACUhGJUVLJCBTunOBZPAQ",
        "10": "BAACAgQAAxkBAAICpmpMrnP_ZvO74-FgN4cHzpeC0vl0AAJQGwACHe3hUfCK1ziFRdK5PAQ",
        "11": "BAACAgQAAxkBAAICqWpMrn5C3ClwhmMjsP0DRcz-YVNpAAJyHgAC790hUuZ00Io2lxUdPAQ",
        "12": "BAACAgIAAxkBAAICqmpMrn7z_yQPSWHcz1IxdyBhynJmAALnoAACrz1ZShF6MwtXdBe-PAQ"
    }
},
"536": {
    "title": "Spriggan",
    "photo": "AgACAgIAAxkBAAIC4mpNUqi7VoWjOzrUXijuDbWmSKmTAAJHG2sbwIhwSpMgD1ITpQh_AQADAgADeQADPAQ",
    "info": "🎬 Nomi: Spriggan\n🎥 Qismi: 4/?\n🌍 Davlati: Yaponiya\n🗣 Til: O'zbek tilida\n📥 Yil: 2025\n🎞 Janr: Ekshn, Fantastika\n\n🍿 @anizone_kawai",
    "episodes": {
        "1": "BAACAgIAAxkBAAIC2GpNUk3ufcwkxlnlNCFb9p3sj94QAAKrkAACoqVwS86W358I7bxnPAQ",
        "2": "BAACAgQAAxkBAAIC2WpNUk2pF25GLwv23WEE9J42ngg3AAIdHgACih6pUpC1yRUjaZC1PAQ",
        "3": "BAACAgIAAxkBAAIC3GpNUmEFIdj5iTZQZRZEDhYxxivkAAIriQACdwYhSMg_LLxjAStcPAQ",
        "4": "BAACAgIAAxkBAAIC3WpNUmEDVuJj_Nk9CnLYCFdnkv4PAAIQiAACceZoSfHvEzNC1MzAPAQ"
    }
},
"173": {
    "title": "Omadsiz ritser",
    "photo": "AgACAgIAAxkBAAIDCWpNWChJ79Jw9thk2TyrxqYmms6OAAJYG2sbwIhwSqDjRBUFRH1hAQADAgADeQADPAQ",
    "info": "🎬 Nomi: Omadsiz ritser\n🎥 Qismi: 12/12\n🌍 Davlati: Yaponiya\n🗣 Til: O'zbek tilida\n📥 Yil: 2024\n🎞 Janr: Sarguzasht, Jangari\n\n🍿 @anizone_kawai",
    "episodes": {
        "1": "BAACAgIAAxkBAAIC62pNVF7Wfvv7pRRsOQWSHcuRMVgMAAKOOwAC8veBSrMnFjEQccGwPAQ",
        "2": "BAACAgIAAxkBAAIC7GpNVF5vIcIOdtg7s9E0_Abg8Si9AAKbNAAC5RqoSmQe659MWPLVPAQ",
        "3": "BAACAgIAAxkBAAIC72pNVSU0Uykphskt3--olG64t447AAJQQgACQszZSoSGO6rKKoqzPAQ",
        "4": "BAACAgIAAxkBAAIC8GpNVSUV3eFLwD3TDK8oERQj9sXHAALxPQACBKxxSwABQg8lMRjTRzwE",
        "5": "BAACAgIAAxkBAAIC82pNVUQtecYVE1aSG31JHFKMry0qAALwRAAChGeIS7SMY9JebaWbPAQ",
        "6": "BAACAgIAAxkBAAIC9GpNVUQKBrdPkqFVd4uTtu3zWnmfAAKOQgACHhW5S6Ikb5llN6YePAQ",
        "7": "BAACAgEAAxkBAAIC_WpNV3VCl50n0RHF_elRov3pqJ5fAAKiAwAChXJ5RGnKO_fjMv9oPAQ",
        "8": "BAACAgIAAxkBAAIC_mpNV3VAQdKAy_CNGl3yJcAB3HZmAAKzRQACDcqZSEY_PdGAN_y4PAQ",
        "9": "BAACAgIAAxkBAAIDAWpNV4Po9kgZudMtJL-xE7B84hPUAAJCOQACAwIoSV1W_fOsEh3RPAQ",
        "10": "BAACAgIAAxkBAAIDAmpNV4OTZ5xUUeA2wjCmjMjdQ9hGAALnPgAC9LowSUjGCJQ1m2ojPAQ",
        "11": "BAACAgIAAxkBAAIDA2pNV4PL4jzHYT2YLA6yjhuW4c-eAAJNOgACy8ppSb-WF-QiM39yPAQ",
        "12": "BAACAgIAAxkBAAIDBGpNV4PWaNkQKm5ekBuv0_aflEiVAAJDQQACN1twScrF_u_PBWStPAQ"
    }
},
"499": {
    "title": "Dragon raja",
    "photo": "AgACAgIAAxkBAAIDZGpNXIYRyRvEUUopHw7wMAm94XwaAAJ5G2sbwIhwSlwytTOl49GxAQADAgADeAADPAQ",
    "info": "🎬 Nomi: Dragon raja\n\n🎥 Qismi: 41/41\n🌍 Davlati: Yaponya\n🇺🇿 Tili: Uzbek tilida\n📆 Yili: 2025\n🎞 Janri: Fantastic akshin\n\n🍿 @anizone_kawai",
    "episodes": {
        "1": "BAACAgIAAxkBAAIDEWpNWbQ1-Y4iu8SkPb88-fhEhau5AAJuWwAC5DYAAUu55p81Qg1_EzwE",
        "2": "BAACAgIAAxkBAAIDEmpNWbSlsSWADi5c6AOqRGNqH2KjAAJPXgAC-zIxS7Ba90q9qYB6PAQ",
        "3": "BAACAgIAAxkBAAIDE2pNWbQmyEN5K9okh7dDnhkR6hbcAAKBXAACxjFASxvaImTOsILLPAQ",
        "4": "BAACAgIAAxkBAAIDFGpNWbTXZqwXkmFuil-l4jVKq9RVAAIuXAACSpZQSzMccltzewkyPAQ",
        "5": "BAACAgEAAxkBAAIDFWpNWbQT0BGVEY0AAR1LrX5l5cFE3gACtQMAAnCVeEdp0V5YdMbnizwE",
        "6": "BAACAgIAAxkBAAIDFmpNWbSXrbZ8V0P6U7dQ85oFBY_zAAJ3WwAC_5-JS3X4v8mTIcDAPAQ",
        "7": "BAACAgIAAxkBAAIDF2pNWbTGViFcxEcTLtnLSPkAAXms9QACflQAAsM0mEvQ0F9qbCrHZDwE",
        "8": "BAACAgIAAxkBAAIDGGpNWbTsH5fROqI4PmPGHFTn29Q4AAKRWgACsBGhS6RZLtbppyGRPAQ",
        "9": "BAACAgIAAxkBAAIDGWpNWbTX5KuLX-9U60NjWPRh7deSAAIjVgACI1bpSxIpoUzdCXn1PAQ",
        "10": "BAACAgIAAxkBAAIDGmpNWbR4RuWRQM9hjVq4R-W6O20RAAJuXgACJ8XxS0PWYhO8qYasPAQ",
        "11": "BAACAgIAAxkBAAIDG2pNWbRW2b79N8m5TcIp6vXDrUoBAALcVgAC1cV5SLBE42Npjwq7PAQ",
        "12": "BAACAgIAAxkBAAIDHGpNWbR2wc86aQIMrKUwpp7Nq0NCAAIcXQACbrSYSJVo_HxVZyiLPAQ",
        "13": "BAACAgIAAxkBAAIDHWpNWbTHAQa0UxFnC89q22IXvi3EAAIwYQACwIWxSOToyjXIdxE1PAQ",
        "14": "BAACAgIAAxkBAAIDHmpNWbSF1dexi3AjhOeO1PFOm8LPAAK_XwAC0bPZSEbcsqeR2COiPAQ",
        "15": "BAACAgIAAxkBAAIDH2pNWbT1QtDl-vPxYmJiVcR1b0JhAAIUWwAC0WYZSQdnGpuMKJiyPAQ",
        "16": "BAACAgIAAxkBAAIDMGpNW4XUPUlCA6TIlpJ6MU_WwH-CAAJXWwAC0WYhSabkSfr_cClaPAQ",
        "17": "BAACAgIAAxkBAAIDMWpNW4Wyb3kR0mmJk5rFqahWc4IbAAIcXgAC0WYhSTt3vH6EnWMpPAQ",
        "18": "BAACAgQAAxkBAAIDMmpNW4U0fKAvz_HV-xEnFvW1k7z2AAIaGwACZkhJURCUs7egrRBSPAQ",
        "19": "BAACAgQAAxkBAAIDM2pNW4W01S9miZeIbJ7xTv1Du-wVAAIeGwACZkhJUYjWy4UCSGUpPAQ",
        "20": "BAACAgQAAxkBAAIDNGpNW4XjY-C1ivq6PCBNLVuJp9NNAAIgGwACZkhJUXZjAAHJas-wvDwE",
        "21": "BAACAgQAAxkBAAIDNWpNW4U-MgODzTcWaAAB3YcKzeAQogACIxsAAmZISVHzsl3Iz1avqjwE",
        "22": "BAACAgQAAxkBAAIDNmpNW4UP0N15Pw_otVlAydWcN77EAAIpGwACZkhJUXjL8GMhEYgGPAQ",
        "23": "BAACAgQAAxkBAAIDN2pNW4WkY48l98Fl8Bj6guYaHzJ1AAIzGwACZkhJUecyc7iR1n7TPAQ",
        "24": "BAACAgQAAxkBAAIDOGpNW4UO4lkHQUeknSR2dppGBFwUAAI2GwACZkhJUTlPeOa-YLfnPAQ",
        "25": "BAACAgQAAxkBAAIDOWpNW4Uhotaaxz_YqcKAgNpufQcWAAI6GwACZkhJUWOduyXtJehOPAQ",
        "26": "BAACAgQAAxkBAAIDOmpNW4XYrcJ9x1VJL2moFXrHRCmLAAJbHQACkZlJUWRI94cGuFvRPAQ",
        "27": "BAACAgQAAxkBAAIDO2pNW4U9K-k8W848kdRI5m4HcB5bAALZGgACOxJQUfIO58v07ppvPAQ",
        "28": "BAACAgQAAxkBAAIDPGpNW4WO6kFI8pwGUwHSj8aiDZhwAALaGgACOxJQUUhmDTd4dTfyPAQ",
        "29": "BAACAgUAAxkBAAIDPWpNW4UtWwknvOP7tFpLoCKjobvTAAK2HAACsh3BVXd1VFdTCNvUPAQ",
        "30": "BAACAgIAAxkBAAIDPmpNW4UVTtz964XWtfbq97u3fctlAAKRigACdsO5S2u4FgABuvkozDwE",
        "31": "BAACAgIAAxkBAAIDTmpNXB616pg46YJsTfG9msUBA-GxAAIWhQACXX75SwXopPH1QhAIPAQ",
        "32": "BAACAgIAAxkBAAIDT2pNXB6VC9wutIpEu6lP8I-orIRTAAJnkAACmlIBSGAREQp5JRs4PAQ",
        "33": "BAACAgIAAxkBAAIDUGpNXB5D0BSVgzriJevNKp58KkLOAALjhQACI0IxSP8cboVqbb63PAQ",
        "34": "BAACAgIAAxkBAAIDUWpNXB5jUjaFUS9TBB066aw4uM1bAALChwACeBBISPXpfzMMCaqXPAQ",
        "35": "BAACAgIAAxkBAAIDUmpNXB69rQWaKy7k97Q8jrtdbVJFAAI6gwACd-RQSAGcjv61bDklPAQ",
        "36": "BAACAgIAAxkBAAIDU2pNXB4zphK7hTk7ISny0Oc-bOoGAALSiwAC7aSISCL4Duq16dM8PAQ",
        "37": "BAACAgIAAxkBAAIDVGpNXB5Avd0lcvzHzBB5HAmOZQAB4QAC9ooAAhpouEhat1HIVrgRBDwE",
        "38": "BAACAgIAAxkBAAIDVWpNXB7Pha59gE8sFSKh-bnjBSs1AALthwACdCIJSeIp73KwMtDhPAQ",
        "39": "BAACAgIAAxkBAAIDVmpNXB5JgEdk4OJ0TU3Pr5xKwD3yAAKTjAAC31RRSd_um4inOItaPAQ",
        "40": "BAACAgQAAxkBAAIDV2pNXB64dC16NTdZw5GAShEpLuoGAAJ7GAACXVyhUTP5QHvpeuVFPAQ",
        "41": "BAACAgQAAxkBAAIDWGpNXB55nVJX5mbVuCZ3_9UFbl-3AAJBKAACmJjgUTEN6UdMwOQePAQ"
    }
},
"389": {
    "title": "Donishmandning qayta tug'ulishi",
    "photo": "AgACAgIAAxkBAAIDgGpNXn7Uf5s9RSvH-MOtDM6qNPWaAAKJG2sbwIhwSj9o8VqDdIbBAQADAgADeQADPAQ",
    "info": "🎬 Nomi: Donishmandning qayta tug'ulishi\n\n🎥 Qismi: 12/12\n Davlati: Yaponya\n🇺 Tili: Uzbekcha\n📆 Yili: 2023\n🎞 Janri: Isekai Sarguzasht\n\n🍿 @anizone_kawai",
    "episodes": {
        "1": "BAACAgIAAxkBAAIDaGpNXgXV_IB5pLHbhxaQPd_LQ-BSAAI2HQACDz6QSzvODG8bcmjfPAQ",
        "2": "BAACAgIAAxkBAAIDaWpNXgWSq-fwVhLQJpM6MTo1MLwrAALlHwAC7bAZS-YZ_CID6DIRPAQ",
        "3": "BAACAgIAAxkBAAIDampNXgUXD7Luz9YNWONJk7ZiiPQvAALnHwAC7bAZS0ZGYQf_x3JNPAQ",
        "4": "BAACAgIAAxkBAAIDa2pNXgWPEQzxAAGbDdvj6gtmV-ed2gAC7B4AAkqWSEgIY56_M-uTHzwE",
        "5": "BAACAgIAAxkBAAIDbGpNXgUF1TFDLXha2vg8jmho0Kk8AAI7JQACJAsQSWIgb6qytELaPAQ",
        "6": "BAACAgIAAxkBAAIDbWpNXgWZZHp3ofrfKwU9T9lYy-G-AAJAJQACJAsQSffd9eNe2tCIPAQ",
        "7": "BAACAgIAAxkBAAIDbmpNXgUX9vYf5qcZ2ar0Dmav7QvtAAJiIwACCi_ZSWx5dRZeBg5MPAQ",
        "8": "BAACAgIAAxkBAAIDb2pNXgU1QH6rlDYJt2uIgFtaxNumAAKPIwACCi_ZSUyyxKxXE78hPAQ",
        "9": "BAACAgIAAxkBAAIDcGpNXgXxq-R1TL6BQc4-o0YF1apAAALYIwACCi_ZScVr2IIvM33wPAQ",
        "10": "BAACAgIAAxkBAAIDcWpNXgVHvzH7tyOq-yq3DKXyyAABBQAC3yMAAgov2UnH_4-3zFjR9jwE",
        "11": "BAACAgIAAxkBAAIDcmpNXgXE9yUc7P7jTXE8x7G0blbPAAL2IwACCi_ZSWHrfVmwbPDKPAQ",
        "12": "BAACAgIAAxkBAAIDc2pNXgUDrUC3ZVGaVzpIXg41NayrAALxIAACT4oRSqrQtGDdyawPPAQ"
    }
},
 "101": {
    "title": "Qora Klever",
    "photo": "AgACAgIAAxkBAAIFbWpbpcg7tedAFHqx14lDmiJH65UQAALXzzEbTIxISBbEMgvl9Q6VAQADAgADeQADPQQ",
    "info": "🎬 Nomi: Qora Klever\n🎥 Qismi: 1-fasl (51/51)\n🌍 Davlati: Yaponiya\n🗣 Til: O'zbek tilida\n📆 Yil: 2024\n🎞 Janr: Sarguzasht, Fantastika\n\n🍿 @anizone_kawai",
    "episodes": {
        "1": "BAACAgIAAxkBAAIFb2pbpj0Y333Arm_8eGCLvFE8PkEwAAIhFAACnGd4SOLGH8b3bCvQPQQ",
        "2": "BAACAgIAAxkBAAIFcGpbpj3CaKOsugZFS3V-SPhG7lizAALVDgACpqqJSDz3uAqKdIOqPQQ",
        "3": "BAACAgIAAxkBAAIFcWpbpj0NUQmjOLrhnjqC1Oc2hSHNAALWDgACpqqJSOlfFXgG-frJPQQ",
        "4": "BAACAgIAAxkBAAIFcmpbpj2iQgEHijHercwjJQ5MbJJLAAKhEQAClLqYSNI8qGIqrL5MPQQ",
        "5": "BAACAgIAAxkBAAIFc2pbpj06d7TplupoIGngIzFdWAgsAAKjEQAClLqYSM7Oux_VnEeUPQQ",
        "6": "BAACAgIAAxkBAAIFdGpbpj3yYkZyeqBZJJI1GeI04SQdAAIHEgAC-sqwSE7t9nwyjdwoPQQ",
        "7": "BAACAgIAAxkBAAIFdWpbpj2d5AiaedCf4BzWnIVzdbNhAAJBEgAChDTJSLhWqOT1wos5PQQ",
        "8": "BAACAgIAAxkBAAIFdmpbpj3-oJhzELZXx89wfs48bQAB0QACzBIAAkSO6UgdYuMOEJd95z0E",
        "9": "BAACAgIAAxkBAAIFd2pbpj0rAAEIRO1rO_J0KmdhXlxXVQACRhMAAmsH-Uj7v8lP0OoxLD0E",
        "10": "BAACAgIAAxkBAAIFeGpbpj3cfKDoJPzbSajBwGJylGa8AAKDEgACBmQxSQbtf014WqrvPQQ",
        "11": "BAACAgIAAxkBAAIFeWpbpj35VFtLjARKHZUpn4V8WLPAAAJ1EgAClTZRSSrDeTEFh_vmPQQ",
        "12": "BAACAgIAAxkBAAIFempbpj2YF4AoLVUPzxOne2i611oLAAJeEAAClMdxSarY6cnumBg4PQQ",
        "13": "BAACAgIAAxkBAAIFe2pbpj1IjFSOWg_6ZNgNQkQvtsrxAAJjFAACkQmJSfUHU_Z8LFA2PQQ",
        "14": "BAACAgIAAxkBAAIFfGpbpj060IT4Bo0Yy9JnTElWHjL9AAL4EgACR-SoSb9tG8HLUxNWPQQ",
        "15": "BAACAgIAAxkBAAIFfWpbpj3AmIBzS7v99nKojdfGvoeUAAJwEwACjGvBSZJgcLL-A3j4PQQ",
        "16": "BAACAgIAAxkBAAIFfmpbpj2qyiHCu5MpTBlcTNSOtARHAAKCEgACsgrYSVc5vDd1ZKCsPQQ",
        "17": "BAACAgIAAxkBAAIFf2pbpj0IN1ZuMH9AG63N2Kx5i7uyAAKEEgACsgrYSTYAAZE1j-4QCz0E",
        "18": "BAACAgIAAxkBAAIFgGpbpj1tcOdJTbBCdTlU_n3j2E43AAL5GQACQvjwSW8fSGgKDylRPQQ",
        "19": "BAACAgIAAxkBAAIFgWpbpj3JyGhjaQY3vUNGqU5-VrfWAALgFAACW5IBSu7Bz8mvRkO6PQQ",
        "20": "BAACAgIAAxkBAAIFgmpbpj3WvSVHPqjDY0EytcymWWckAAKWFQACJSJRShFNAXA4pcYWPQQ",
        "21": "BAACAgIAAxkBAAIFg2pbpj2q_6LDV24bsnAB4tWOT-eoAAJWFwACmgdoStsK2_HpcmjtPQQ",
        "22": "BAACAgIAAxkBAAIFhGpbpj223lT85vA66_FpFI7JFdE0AAKcFQAC1KWYSgjQIs1tsbQGPQQ",
        "23": "BAACAgIAAxkBAAIFhWpbpj0WbA0dkIlZiSVB8_Ua66UIAAK6FAAC83-oSk4CT_2vjXPcPQQ",
        "24": "BAACAgIAAxkBAAIFhmpbpj1IU7bteaiEjCGhVP_ZEEesAAIuFQACGZv4Snv_DaIYp93ePQQ",
        "25": "BAACAgIAAxkBAAIFh2pbpj13k2w9hSkG_zcfbb32JzrAAAKsEAACnTcRS793xqoWF-rHPQQ",
        "26": "BAACAgIAAxkBAAIFiGpbpj1Yxdw2xjtpkbypg20oAn-kAAJ0EwACVA2RS1PgTjQOpr7OPQQ",
        "27": "BAACAgIAAxkBAAIFiWpbpj0L12EGxgm-U9Gir3FLa5ooAALsFQAC9b6pS8V0z2URrsOJPQQ",
        "28": "BAACAgIAAxkBAAIFimpbpj3B7l3YqFrbYhkVPWyoFrizAAKvEQACCZLJSysSeFsAASxgkD0E",
        "29": "",
        "30": "BAACAgIAAxkBAAIFjGpbpj2uieQWQMBYb6nMOCECelULAAKFEgACL7jIS1fo3nM0SRnlPQQ",
        "31": "BAACAgIAAxkBAAIFjWpbpj0nCXdGDBPByskLQzChobbAAAKqFwAC0IXgSwUbhHzlQltXPQQ",
        "32": "BAACAgIAAxkBAAIFjmpbpj0AAfja1-TIUamcx9HSHcg7TwACIRIAApd3-Ev2NyJPWAiQ_D0E",
        "33": "BAACAgIAAxkBAAIFj2pbpj05iJDpKfJlLyrJgSvDTm-9AAIjEgACl3f4S-7VSTkOYnWhPQQ",
        "34": "BAACAgIAAxkBAAIFkGpbpj1dJI0Zk-ydl2_gE-TYwCyjAALYEgACGRoJSCw-bMHIA0QXPQQ",
        "35": "BAACAgIAAxkBAAIFkWpbpj0MRAkCSmupJ4AJZeHtMOUuAALbEgACGRoJSGQVPm5hpziJPQQ",
        "36": "BAACAgIAAxkBAAIFkmpbpj0G_f24xcbQt0AlBojN6ExTAAKLKwAC1bkgSGGa6X8SpWaePQQ",
        "37": "BAACAgIAAxkBAAIFk2pbpj3vsI8wQUmOoVK7Cs60q4PrAAKvFwACGjU4SOdnKBvMt6HjPQQ",
        "38": "BAACAgIAAxkBAAIFlGpbpj1LU-FIC4WzQkQhGST1kQP1AAJlEgAC00NhSIr_n8EUb5XIPQQ",
        "39": "BAACAgIAAxkBAAIFlWpbpj06iq1jZnhNKvzIvOCcrMAMAALuFgAC92GQSKvb2fgBxBrZPQQ",
        "40": "BAACAgIAAxkBAAIFlmpbpj0WiiK7jPTQQFWJVohHMTnCAAILGwACDT74SUnQd3NpmYvSPQQ",
        "41": "BAACAgIAAxkBAAIFl2pbpj3wXVjsZ90UJrX6ppVWaG5NAALqFgACYpeZSkQhZNfjKcgGPQQ",
        "42": "BAACAgIAAxkBAAIFmGpbpj0k8TxG_P7zJ45HBdzLR5bEAALkFAACgNkAAUtyZOLKEm858D0E",
        "43": "BAACAgIAAxkBAAIFmWpbpj3UPdoEmhduyxPhb8E49QLUAALAFAACO-8wS-_1QWnSfjXHPQQ",
        "44": "BAACAgIAAxkBAAIFmmpbpj2G1B27fr8HzZA3Zioj3G99AALIFAACO-8wS-lyEiQdlqvgPQQ",
        "45": "BAACAgIAAxkBAAIFm2pbpj2MfMUE7W0pxSu34N0NXIfYAAKsFgACtj1ZSwblW_wLyEB1PQQ",
        "46": "BAACAgIAAxkBAAIFnGpbpj0BAAG-HLyshubHOa8kWWItIQAC3h4AAplceEusJoFMfYGskz0E",
        "47": "BAACAgIAAxkBAAIFnWpbpj0tHh4L6HsLad39uiX_pVjIAAIqFQACNNiQS2N9rDuXLga9PQQ",
        "48": "BAACAgIAAxkBAAIFnmpbpj2uJbheDR6GUX12b0XpmlBoAALuFQAC3L6hSxnH4lNw5IUOPQQ",
        "49": "BAACAgIAAxkBAAIFn2pbpj14bqJM-c10zgdWMZR6Tph0AAKqGAACYVXoSwABpRpSzM28Tj0E",
        "50": "BAACAgIAAxkBAAIFoGpbpj1vGhKGyr7VNkpZy_Yo8--eAALWGgACfv7xSwmbS6Dy96jHPQQ",
        "51": "BAACAgIAAxkBAAIFoWpbpj3BHZ9-g-6qDeYr05ynJgRLAAJoGQACxfEQSEbtuGXiVOdHPQQ"
    }
},
"159": {
        "title": "So'nggi serafim",
        "photo": "AgACAgIAAxkBAAO9akqVRdXAm0lnGlVm3bKTsUUe6rYAApPKMRvevthL9ZdR_Gv30LIBAAMCAAN4AAM8BA",
        "info": "🎬 Nomi: So'nggi serafim\n🎥 Qismi: 24\n🌍 Davlati: Yaponiya\n🗣 Til: O'zbek tilida\n Yil: 2025\n Janr: Ekshn, Sarguzasht, Fantaziya, Romantika, Jangari\n\n🍿 @anizone_kawai",
        "episodes": {
            "1": "BAACAgIAAxkBAAOOakqU31_h7wlHXTaYqXJzz1FfKOEAAsorAAIi4UBKnBcWoWmWCNQ8BA",
            "2": "BAACAgIAAxkBAAOPakqU308Nz_eJ5ViTlgGV4Sd2VNEAAhYtAAI8PYBKpMKPtGfVv6I8BA",
            "3": "BAACAgIAAxkBAAOSakqU67Iun4qp99BefRNTqtnQRHsAAucrAAL1-9BKzFJLJAU_AAHuPAQ",
            "4": "BAACAgIAAxkBAAOTakqU68MKLlapUb4PiFts4AXSPnkAAm0oAAJpgBhLmzMjFaRT_7w8BA",
            "5": "BAACAgIAAxkBAAOWakqU8apGkRyxBnBxhtP-vvyTSjMAApkvAAKO_mhLsW3bb5t02Y88BA",
            "6": "BAACAgIAAxkBAAOXakqU8XcgiLGuV9Dq1brSFrjxpewAAvsxAALwFLFLtS8qT6uFhEc8BA",
            "7": "BAACAgIAAxkBAAOaakqU-MBNqKBFBDOPn_6D748LHt8AAg08AAIE0zlICDz8bNMEl3E8BA",
            "8": "BAACAgIAAxkBAAObakqU-K2KWdodZL_dX-KfTUpxWusAAmgqAALafVFIdZMqq3oRb2Q8BA",
            "9": "BAACAgIAAxkBAAOeakqU_Ypl5ZZMkhON3PJZhX6XC8gAAs80AAI3IiFJ6oSEyCefDrs8BA",
            "10": "BAACAgIAAxkBAAOfakqU_btnuHQ5MGzV5dZBQqXtRTUAAtg0AAI3IiFJSASvkzkmeXw8BA",
            "11": "BAACAgIAAxkBAAOiakqVBOwba39SoVNgx6eSEXwV1VIAAuQ0AAI3IiFJY5nx1_ytZO48BA",
            "12": "BAACAgIAAxkBAAOjakqVBMOo5dXBFs4OXoQx1CQn2loAAuo0AAI3IiFJneyjzyiCTpw8BA",
            "13": "BAACAgIAAxkBAAOmakqVCnouY1dkJuWpAvacYl1X1LAAAhwtAAJ7MalJ8CDawQjsVkY8BA",
            "14": "BAACAgIAAxkBAAOnakqVCm2x0EFENUbJDL1BjUa_BJcAAhYqAALo9chJOQvGyazTMXE8BA",
            "15": "BAACAgIAAxkBAAOqakqVEL4MudHi2WElC4KMhxcSZjsAAoM4AAIOOdlJYLi5HcCkuOo8BA",
            "16": "BAACAgIAAxkBAAOrakqVED_0oQmU4HesRj5ONcj18fYAArg1AAIOOeFJg7OUVX31pz48BA",
            "17": "BAACAgIAAxkBAAOuakqVF70TktGqeKJVAYnxvLkW36AAAtYuAALcTPBJS5PbBxKbGvw8BA",
            "18": "BAACAgIAAxkBAAOvakqVF7j3_29cw42np6iAazJrlN8AAscxAAIkNRBKvoGnQSrFmHc8BA",
            "19": "BAACAgIAAxkBAAOyakqVHLMcbftPghdaDx3ollk4vqUAAmo1AAICliFKS49oqw0v-dM8BA",
            "20": "BAACAgIAAxkBAAOzakqVHATBWWGGzTKSSsVhD5PZsicAAms1AAICliFKgO40jVH7IE48BA",
            "21": "BAACAgIAAxkBAAO2akqVIWyWXBl1JOBnoHih5vPW7rIAArEuAAKMRihKTio-FbDiLuU8BA",
            "22": "BAACAgIAAxkBAAO3akqVIdD0zmDCUq3DMNtkt8LUMxQAAogvAAKMRihKKONXaWu89CQ8BA",
            "23": "BAACAgIAAxkBAAO6akqVJX-tq7bBPRmGf3BKApMEt_sAAv4xAAKMRihKpxhgPA8ZKzo8BA",
            "24": "BAACAgIAAxkBAAO6akqVJX-tq7bBPRmGf3BKApMEt_sAAv4xAAKMRihKpxhgPA8ZKzo8BA"
        }
    }
}

# --- BAZA BILAN ISHLASH ---
def load_data():
    default = {"users": [], "banned": [], "required_channels": [CHANNEL_ID], "movies": MOVIES_BASE}
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                if "req_channels" in data: 
                    data["required_channels"] = data.pop("req_channels")
                for code, info in MOVIES_BASE.items(): 
                    data["movies"][code] = info
                return data
        except Exception as e:
            print(f"❌ Data yuklashda xato: {e}")
            return default
    return default

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f: 
        json.dump(data, f, ensure_ascii=False, indent=4)

DATA = load_data()
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# --- YORDAMCHI FUNKSIYALAR ---
async def check_sub(user_id):
    for ch in DATA.get("required_channels", [CHANNEL_ID]):
        try:
            member = await bot.get_chat_member(chat_id=ch, user_id=user_id)
            if member.status in ["left", "kicked"]: 
                return False
        except Exception as e:
            continue
    return True

def get_main_keyboard():
    kb = [
        [KeyboardButton(text="🔢 Kod orqali"), KeyboardButton(text="🆕 Yangi yuklanganlar")],
        [KeyboardButton(text="📋 Jadval"), KeyboardButton(text="🎲 Tasodifiy")]
    ]
    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

def get_sub_keyboard():
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="📺 Telegram kanal", url=CHANNEL_LINK))
    builder.row(InlineKeyboardButton(text="✅ Tekshirish", callback_data="check_subscription"))
    return builder.as_markup()

def get_episode_keyboard(code):
    builder = InlineKeyboardBuilder()
    anime = DATA["movies"].get(code)
    if not anime:
        return builder.as_markup()
    
    episodes = anime.get("episodes", {})
    episode_nums = sorted(episodes.keys(), key=lambda x: int(x))
    
    for ep in episode_nums:
        builder.add(InlineKeyboardButton(text=f"{ep}", callback_data=f"play_{code}_{ep}"))
    
    builder.adjust(3)
    
    builder.row(
        InlineKeyboardButton(text="📸 Instagram", url=INSTA_LINK),
        InlineKeyboardButton(text="🎵 TikTok", url=TIKTOK_LINK)
    )
    
    return builder.as_markup()

async def show_anime(message_or_callback, code):
    anime = DATA["movies"].get(code)
    if not anime:
        if isinstance(message_or_callback, types.Message):
            await message_or_callback.answer("❌ Bunday kod mavjud emas")
        else:
            await message_or_callback.message.answer("❌ Bunday kod mavjud emas")
        return
    
    photo = anime.get("photo", "")
    info = anime.get("info", "")
    keyboard = get_episode_keyboard(code)
    
    if isinstance(message_or_callback, types.Message):
        try:
            await message_or_callback.answer_photo(photo=photo, caption=info, reply_markup=keyboard)
        except Exception as e:
            print(f"❌ Rasm yuborishda xato: {e}")
            await message_or_callback.answer(info, reply_markup=keyboard)
    else:
        try:
            await message_or_callback.message.edit_media(
                media=types.InputMediaPhoto(media=photo, caption=info),
                reply_markup=keyboard
            )
        except Exception as e:
            print(f"❌ Media tahrirlashda xato: {e}")
            await message_or_callback.message.answer_photo(photo=photo, caption=info, reply_markup=keyboard)

# --- HANDLERS ---
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    user_id = message.from_user.id
    if user_id not in DATA["users"]:
        DATA["users"].append(user_id)
        save_data(DATA)
    
    args = message.text.split()
    
    if await check_sub(user_id):
        if len(args) > 1:
            code = args[1]
            if code in DATA["movies"]:
                await show_anime(message, code)
                return
            else:
                await message.answer("❌ Bunday kod mavjud emas")
        
        await message.answer(
            " Assalomu alaykum! Xush kelibsiz!\n\n📚 Mana sizga menyu:",
            reply_markup=get_main_keyboard()
        )
    else:
        await message.answer(
            "👋 Assalomu alaykum! Xush kelibsiz!\n\n⚠️ Hali siz obuna bo'lmagansiz. Iltimos, obuna bo'ling:",
            reply_markup=get_sub_keyboard()
        )

@dp.callback_query(F.data == "check_subscription")
async def check_sub_callback(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    if await check_sub(user_id):
        await callback.message.delete()
        await callback.message.answer(
            " Assalomu alaykum! Xush kelibsiz!\n\n✅ Obuna tasdiqlandi!\n\n📚 Mana sizga menyu:",
            reply_markup=get_main_keyboard()
        )
        await callback.answer("✅ Obuna muvaffaqiyatli tasdiqlandi!")
    else:
        await callback.answer("❌ Hali obuna bo'lmagansiz!", show_alert=True)

# ✅ Kod orqali qidirish
@dp.message(F.text == "🔢 Kod orqali")
async def ask_code(message: types.Message):
    if not await check_sub(message.from_user.id):
        await message.answer("⚠️ Hali siz obuna bo'lmagansiz", reply_markup=get_sub_keyboard())
        return
    codes_list = ", ".join(list(DATA["movies"].keys()))
    await message.answer(f"🔢 Anime kodini kiriting:\n\n📋 Mavjud kodlar: {codes_list}")

# 🔧 MUHIM: Faqat raqam bo'lgan xabarlar uchun filter
@dp.message(F.text.regexp(r'^\d+$'))
async def process_code(message: types.Message):
    if not await check_sub(message.from_user.id):
        await message.answer("⚠️ Hali siz obuna bo'lmagansiz", reply_markup=get_sub_keyboard())
        return
    
    code = message.text.strip()
    
    if code in DATA["movies"]:
        await show_anime(message, code)
    else:
        await message.answer("❌ Bunday kod mavjud emas. /start bosing.")

@dp.message(F.text == "🎲 Tasodifiy")
async def random_anime(message: types.Message):
    if not await check_sub(message.from_user.id):
        await message.answer("⚠️ Hali siz obuna bo'lmagansiz", reply_markup=get_sub_keyboard())
        return
    codes = list(DATA["movies"].keys())
    random_code = random.choice(codes)
    await show_anime(message, random_code)

@dp.message(F.text == "📋 Jadval")
async def show_schedule(message: types.Message):
    if not await check_sub(message.from_user.id):
        await message.answer("⚠️ Hali siz obuna bo'lmagansiz", reply_markup=get_sub_keyboard())
        return
    text = "📋 **Barcha animelar:**\n\n"
    for code, anime in DATA["movies"].items():
        title = anime.get("title", "Noma'lum")
        total_eps = len(anime.get("episodes", {}))
        text += f" {title}\n   Kod: `{code}` | {total_eps} qism\n\n"
    await message.answer(text, parse_mode=ParseMode.MARKDOWN)

@dp.message(F.text == "🆕 Yangi yuklanganlar")
async def new_uploads(message: types.Message):
    if not await check_sub(message.from_user.id):
        await message.answer("⚠️ Hali siz obuna bo'lmagansiz", reply_markup=get_sub_keyboard())
        return
    codes = list(DATA["movies"].keys())[-5:]
    text = "🆕 **Oxirgi yuklangan animelar:**\n\n"
    for code in reversed(codes):
        anime = DATA["movies"][code]
        title = anime.get("title", "Noma'lum")
        text += f"🔹 {title} (Kod: `{code}`)\n"
    await message.answer(text, parse_mode=ParseMode.MARKDOWN)

@dp.callback_query(F.data.startswith("play_"))
async def play_episode(callback: types.CallbackQuery):
    if not await check_sub(callback.from_user.id):
        await callback.answer("⚠️ Avval obuna bo'ling!", show_alert=True)
        return
    
    data = callback.data.split("_")
    if len(data) < 3:
        await callback.answer("❌ Xatolik!", show_alert=True)
        return
    
    code = data[1]
    episode = data[2]
    
    anime = DATA["movies"].get(code)
    if not anime:
        await callback.answer(" Anime topilmadi", show_alert=True)
        return
    
    video_id = anime.get("episodes", {}).get(episode)
    if video_id:
        try:
            await callback.message.answer_video(
                video=video_id,
                caption=f" {anime['title']} - {episode}-qism\n\n🍿 @anizone_kawai"
            )
            await callback.answer()
        except Exception as e:
            print(f"❌ Video yuborishda xato: {e}")
            await callback.answer("❌ Video yuborishda xatolik!", show_alert=True)
    else:
        await callback.answer("❌ Bu qism topilmadi", show_alert=True)

# ✅ FAQAT ADMIN UCHUN - File ID olish
@dp.message(F.from_user.id == ADMIN_ID, (F.video | F.photo))
async def get_file_id(message: types.Message):
    if message.video:
        file_id = message.video.file_id
        await message.reply(f" **Video ID:**\n`{file_id}`", parse_mode=ParseMode.MARKDOWN)
    elif message.photo:
        file_id = message.photo[-1].file_id
        await message.reply(f"🖼 **Photo ID:**\n`{file_id}`", parse_mode=ParseMode.MARKDOWN)

async def main():
    print(f" Bot ishga tushdi!")
    print(f"📊 Bazada {len(DATA['movies'])} ta anime")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())