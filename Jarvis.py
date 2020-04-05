import os
import time
import playsound
import speech_recognition as sr
from gtts import gTTS
from selenium import webdriver
from datetime import datetime
import subprocess

chromedriver = r"C:\Users\Malhaar\Downloads\chromedriver_win32\chromedriver.exe"
driver = webdriver.Chrome(chromedriver)


def speak(text, file = "ques.mp3"):
    tts = gTTS(text = text, lang = "en-US")
    filename = file
    tts.save(filename)
    playsound.playsound(filename)


def get_audio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
        said = ""

        try:
            said = r.recognize_google(audio)
            print(said)

        except Exception as e:
            print("Exception: " + str(e))

    return said


def youtube():
    speak("Which song do you want me to play?")
    search_string = get_audio()

    def launch():
        driver.get("https://www.youtube.com/")
        time.sleep(0.5)

    def search():
        driver.find_element_by_xpath("/html/body/ytd-app/div/div/ytd-masthead/div[3]/ytd-searchbox/form/div/div[1]/input").send_keys(search_string)
        driver.find_element_by_xpath("/html/body/ytd-app/div/div/ytd-masthead/div[3]/ytd-searchbox/form/button").click()
        time.sleep(1)

    def click_video():
        driver.find_element_by_xpath("/html/body/ytd-app/div/ytd-page-manager/ytd-search/div[1]/ytd-two-column-search-results-renderer/div/ytd-section-list-renderer/div[2]/ytd-item-section-renderer/div[3]/ytd-video-renderer[1]/div[1]/ytd-thumbnail/a").click()

    def skip_ad():
        try:
            driver.find_element_by_xpath("/html/body/ytd-app/div/ytd-page-manager/ytd-watch-flexy/div[4]/div[1]/div/div[1]/div/div/div/ytd-player/div/div/div[15]/div/div[3]/div/div[2]/span/button/div").click()
        except:
            try:
                driver.find_element_by_xpath("/html/body/ytd-app/div/ytd-page-manager/ytd-watch-flexy/div[4]/div[1]/div/div[1]/div/div/div/ytd-player/div/div/div[15]/div[2]/div/div/div[2]/span/button/div").click()
            except:
                pass

    launch()
    search()
    click_video()
    time.sleep(8)
    skip_ad()


def note():
    speak("What do you want to note down?")
    stuff = get_audio()
    date = datetime.now()
    notename = str(date).replace(":", "-") + "-note.txt"
    with open(notename, 'w') as myfile:
        myfile.write(stuff)
    subprocess.Popen(["notepad.exe", notename])

speak("Hey, I'm Jarvis. What can I do for you?", "greeting.mp3")

text = get_audio()

if "song" in text:
    youtube()

if "shutdown" in text:
    os.system("shutdown /s /t 1")

if "note" in text:
    note()
