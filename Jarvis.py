import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os
import time
import speech_recognition as sr
import pyttsx3
from selenium import webdriver
import subprocess
import cv2
import requests

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

def speak(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 160)
    engine.say(text)
    engine.runAndWait()


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

    chromedriver = r"C:\Users\Malhaar\Downloads\chromedriver_win32\chromedriver.exe"
    driver = webdriver.Chrome(chromedriver)

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
        while True:
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
    date = datetime.datetime.now()
    notename = str(date).replace(":", "-") + "-note.txt"
    with open(notename, 'w') as myfile:
        myfile.write(stuff)
    subprocess.Popen(["notepad.exe", notename])


def authenticate_google():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    return service

def get_events(n, service):
    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    print(f'Getting the upcoming events')
    speak(f'Getting the upcoming events')
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                        maxResults=n, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
        speak('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        weather_split_1 = start.split("T")
        weather_split_2 = weather_split_1[1].split("+")
        print(f"Date: {weather_split_1[0]}; Time: {weather_split_2[0]} - {event['summary']}")
        speak(f"{event['summary']} at {weather_split_2[0]}")

service = authenticate_google()


def weather():
    def weather_data(query):
    	res=requests.get('http://api.openweathermap.org/data/2.5/weather?'+query+'&APPID=b35975e18dc93725acb092f7272cc6b8&units=metric');
    	return res.json();
    def print_weather(result):
    	speak("Gurgaon's temperature: {}°C ".format(result['main']['temp']))
    	speak("Wind speed: {} m/s".format(result['wind']['speed']))
    	speak("Description: {}".format(result['weather'][0]['description']))

    def weather_main():
        query='q='+"gurgaon";
        w_data=weather_data(query);
        print_weather(w_data)
        print()

    weather_main()

    chromedriver = r"C:\Users\Malhaar\Downloads\chromedriver_win32\chromedriver.exe"
    driver = webdriver.Chrome(chromedriver)
    driver.get("https://weather.com/en-IN/weather/today/l/28.42,77.09?par=google&temp=c")
    time.sleep(5)


def google_search():
    from googlesearch import search
    query = text
    chromedriver = r"C:\Users\Malhaar\Downloads\chromedriver_win32\chromedriver.exe"
    driver = webdriver.Chrome(chromedriver)
    for i in search(query, tld = "com", num = 1, stop = 1, pause = 2):
        driver.get(i)
        time.sleep(30)

jarr = cv2.imread("img.jpg", 1)
cv2.imshow("Jarvis", jarr)
cv2.waitKey(3000)
cv2.destroyAllWindows()

speak("Hey, I'm Jarvis. What can I do for you?")

text = get_audio()

if "song" in text:
    youtube()

elif "shutdown" in text:
    os.system("shutdown /s /t 1")

elif "note" in text:
    note()

elif "you there" in text:
    speak("For you sir, always.")

elif "weather" in text:
    weather()

elif "tell me about my day" in text:
    get_events(5, service)

elif "good morning" in text:
    speak("Good morning sir")
    weather()
    get_events(4, service)

else:
    google_search()
