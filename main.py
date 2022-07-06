import speech_recognition as sr #библиотека для распознавания голоса
from gtts import gTTS #google text to speech
import playsound #воспроизводит аудиофайлы
import random
import os
import nltk
import json
from sklearn.feature_extraction.text import CountVectorizer #переведёт текст в набор чисел
from sklearn.linear_model import LogisticRegression#модель с линейной регрессией






def is_match_strings(string1, string2): #проверяет насколько схожи 2 строки
    string1 = string1.lower()
    string2 = string2 .lower()
    distance = nltk.edit_distance(string1, string2)
    average_length = (len(string1) + len(string2)) / 2 
    return (distance / average_length)<0.5 

def get_intent(text):#по вопросу понимает intent из конфигурации бота
    for name,data in bot_configuration["intents"].items():
        for example in data["examples"]:
            if is_match_strings(text,example):
                return name

def get_answer(intent):#Бот отвечает на intent одним из ответов наугад
    response=bot_configuration["intents"][intent]["responses"]
    return random.choice(response)

def bot_work(text):#процесс работы бота заключается в объединении get_intent и get_answer
    intent=get_intent(text)
    if intent:
        return get_answer(intent)
    else:
        test = vectorizer.transform([text])
        intent = model.predict(test)[0]
    failure_phrases=bot_configuration["failure_phrases"]
    return random.choice(failure_phrases)

def listen(): #бот слушает вопрос человека и переводит его в текст
    with sr.Microphone() as source:
        print('Скажите что-нибудь')
        audio = voice_recognizer.listen(source)
      
     
    try:
        
        voice_text = voice_recognizer.recognize_google(audio, language ='ru') #распознавание речи через серверы google
        print(f'Вы сказали: {voice_text}')
        return voice_text
    except sr.UnknownValueError:
        return 'Ошибка распознания текста'
    except sr.RequestError:
        return 'Ошибка запроса'


def say(text): #бот отвечает на вопрос человека
    voice = gTTS(text,lang='ru')
    file_name ='audio_ '+str(random.randint(0,100000))+'.mp3'
    voice.save(file_name)#сохраняем в файлы с уникальными названиями для воспроизведения
    playsound.playsound(file_name)
    os.remove(file_name)
    print(f'Бот ответил: {text}')


def start():
    print('Бот запущен')
    while True:
        question=listen()
        answer = bot_work(question)
        say(answer)
       


configuration = open("C:/Users/user/Desktop/SpeakingBot/big_bot_config.json","r") #файл с большим количеством вопросов и ответов, взятый из skillbox
bot_configuration=json.load(configuration)

#создаём модель машинного обучения, помогающую по вопросам определять намерение человека
X = []
Y=[]

for name,data in bot_configuration["intents"].items():
    for example in data["examples"]:
        X.append(example)
        Y.append(name)
        
vectorizer = CountVectorizer()
vectorizer.fit(X)#передаём набор текстов
X_vectorized = vectorizer.transform(X)
model = LogisticRegression()
model.fit(X_vectorized, Y)#учится по X находить Y

voice_recognizer = sr.Recognizer()

start()