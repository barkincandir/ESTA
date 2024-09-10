import tkinter as tk
import speech_recognition as sr
import pyttsx3
from playsound import playsound
import subprocess
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pyautogui
import time

CLIENT_ID = '......'
CLIENT_SECRET = '........'
REDIRECT_URI = '.......'

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                               client_secret=CLIENT_SECRET,
                                               redirect_uri=REDIRECT_URI,
                                               scope='user-modify-playback-state'))

seni_dinliyorum = r"C:\Users\candi\PycharmProjects\ESTA\senidinliyorum.mp3"
seni_anlayamadim = r"C:\Users\candi\PycharmProjects\ESTA\senianlayamadım.mp3"
sayiseslendirme = r"C:\Users\candi\PycharmProjects\ESTA\sayi.mp3"
hangisrki = r"C:\Users\candi\PycharmProjects\ESTA\hangisrki.mp3"
motor = pyttsx3.init()
voices = motor.getProperty('voices')
motor.setProperty('voice', voices[1].id)
motor.setProperty("rate", 150)

r = sr.Recognizer()


def sayi_okuma(sayi):
    if sayi < 0 or sayi > 999:
        return
    else:
        birler = ['sıfır', 'bir', 'iki', 'üç', 'dört', 'beş', 'altı', 'yedi', 'sekiz', 'dokuz']
        onlar = ['on', 'yirmi', 'otuz', 'kırk', 'elli', 'altmış', 'yetmiş', 'seksen', 'doksan']
        yüzler = ['yüz', 'ikiyüz', 'üçyüz', 'dörtyüz', 'beşyüz', 'altıyüz', 'yediyüz', 'sekizyüz', 'dokuzyüz']

        okunan_sayi = ''
        birler_basamagi = sayi % 10
        onlar_basamagi = (sayi // 10) % 10
        yüzler_basamagi = (sayi // 100) % 10

        if yüzler_basamagi > 0:
            okunan_sayi += yüzler[yüzler_basamagi - 1] + ' '

        if onlar_basamagi > 0:
            okunan_sayi += onlar[onlar_basamagi - 1] + ' '

        if birler_basamagi > 0:
            okunan_sayi += birler[birler_basamagi]

        return okunan_sayi.strip()


def kare_hesapla(sayi):
    try:
        sayi = int(sayi)
        kare = sayi ** 2
        print(f"{sayi} sayısının karesi: {kare}")
        if kare <= 999:
            motor.say(f"{sayi_okuma(sayi)} sayısının karesi {sayi_okuma(kare)}")
            motor.runAndWait()
        else:
            playsound(sayiseslendirme)
    except ValueError:
        print("Geçersiz sayı.")
    dongu()


def Valorant():
    valorant = "C:\\Riot Games\\Riot Client\\RiotClientServices.exe"
    subprocess.Popen(valorant)
    dongu()


def pctimer():
    pctimer = "C:\\Users\\candi\\OneDrive\\Masaüstü\\PcTimer v1.0.exe"
    subprocess.Popen(pctimer)
    dongu()


def play_music_spoty(track_name, device_id):
    results = sp.search(q=track_name, limit=1)
    if results['tracks']['items']:
        track_uri = results['tracks']['items'][0]['uri']
        sp.start_playback(device_id=device_id, uris=[track_uri])
    else:
        print("Şarkı bulunamadı.")


def muzikcl():
    devices = sp.devices()
    if devices['devices']:
        device_id = devices['devices'][0]['id']
        playsound(hangisrki)

        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source)

        try:
            recognized_text = r.recognize_google(audio, language="tr-TR")
            play_music_spoty(recognized_text, device_id)
            print(recognized_text)
        except sr.UnknownValueError:
            playsound(seni_anlayamadim)
        except sr.RequestError as e:
            print("Ses tanıma servisine erişilemiyor; {0}".format(e))
    else:
        pyautogui.press('win')
        time.sleep(1)
        pyautogui.write('spotify')
        time.sleep(1)
        pyautogui.press('enter')
    dongu()


def execute_command(recognized_text):
    if "süre tutucu" in recognized_text:
        print("Pctimer komutu algılandı.")
        pctimer()
    elif "karesini al" in recognized_text:
        print("Kare hesaplama komutu algılandı.")
        sayi = ''.join(filter(str.isdigit, recognized_text))
        kare_hesapla(sayi)
    elif "valorant" in recognized_text:
        print("Valorant komutu algılandı.")
        Valorant()
    elif "müzik" in recognized_text:
        print("Müzik çalma komutu algılandı.")
        muzikcl()
    else:
        print("Bu konuda henüz yardımcı olamıyorum.")


def listen_and_execute():
    print("Dinleniyor...")
    with sr.Microphone() as source:
        playsound(seni_dinliyorum)
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
    try:
        recognized_text = r.recognize_google(audio, language="tr-TR")
        print("Algılanan metin:", recognized_text)
        execute_command(recognized_text)
    except sr.UnknownValueError:
        playsound(seni_anlayamadim)
        print("Metin algılanamadı.")
    except sr.RequestError as e:
        motor.say("Ses tanıma servisine erişilemiyor; {0}".format(e))
        motor.runAndWait()
        print("Ses tanıma servisine erişilemiyor:", e)
    time.sleep(1)


def dongu():
    while True:
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source)
        try:
            recognized_text = r.recognize_google(audio, language="tr-TR")
            print(recognized_text)
            if "Merhaba" in recognized_text:
                listen_and_execute()
            elif "kapat" in recognized_text:
                break


        except sr.UnknownValueError:
            playsound(seni_anlayamadim)
        except sr.RequestError as e:
            motor.say("Ses tanıma servisine erişilemiyor; {0}".format(e))
            motor.runAndWait()


class Application:
    def __init__(self, arayuz):
        self.arayuz = arayuz
        self.arayuz.title("ESTA")
        self.arayuz.resizable(width=False, height=False)
        self.arayuz.configure(bg="#FAF0E6")
        ekran_yuk = arayuz.winfo_screenwidth()
        ekran_uzun = arayuz.winfo_screenheight()
        self.arayuz.geometry(f"200x200+{(ekran_yuk // 2) - 100}+{(ekran_uzun // 2) - 150}")
        self.font = ("Arial", 15)
        self.font1 = ("Arial", 8, "italic")

        self.button_listen = tk.Button(arayuz, text="ESTA'yı çalıştır", font=self.font, fg="black", bg="orange", bd=5,
                                       relief=tk.RAISED, command=dongu)
        self.button_listen.place(x=20, y=60)
        self.creator = tk.Label(arayuz, text="by Barkın Çandır", font=self.font1, fg="Black", bg="#FAF0E6")
        self.creator.place(x=110, y=180)


if __name__ == "__main__":
    arayuz = tk.Tk()
    app = Application(arayuz)
    arayuz.mainloop()
