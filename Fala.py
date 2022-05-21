# -*- coding: UTF-8 -*-
"""
Arquivo para o CP de IA, IOT e IOB
"""
import datetime
from ntpath import join
import speech_recognition as sr
import pyttsx3
import requests
import json
import pywhatkit
import wikipedia
import pyjokes
import os
from dotenv import load_dotenv


load_dotenv()
listener = sr.Recognizer()
engine = pyttsx3.init()
engine.setProperty('rate', 250)  # Seta velocidade de fala
engine.setProperty('voice', b'brasil')  # Seta linguagem

wikipedia.set_lang("pt")

ativo = False


def talk(text):
    #Summaries devem ficar acima da função, não dentro - Zack
    """
    Função para ser chamada sempre que formos realizar o TTS 
    """
    engine.say(text)
    engine.runAndWait()

def take_command():
    """
    Função generica para receber um comando
    """
    command = ""  # iniciando a variável vazia
    with sr.Microphone() as source:
        try:
            print("Escutando")  # Print para saber quando o programa inicia
            # Ouvindo o que o usuário vai falar
            voice = listener.listen(source)
            # Usa a API do google para realizar o STT
            command = listener.recognize_google(voice, language='pt')
            command = command.lower()
            if "sexta-feira" in command:
                # Tira o nome da nossa assistente do comando
                # command = command.replace("sexta-feira", "")
                print(command)  # Printa o que a API do google retorna

        except:
            pass

    return command

def tocar(command):
    song = command.replace("tocar", "")
    talk("Tocando" + song)
    pywhatkit.playonyt(song)

def horas():
    _hr = datetime.datetime.now().strftime("%H")
    _mi = datetime.datetime.now().strftime("%M")
    print(_hr)
    print(_mi)
    talk("São" + _hr + " horas e " + _mi + " minutos")

def buscar(command):
    teste = command.split()
    print(teste)
    search = str(teste[1])
    print(search)
    try:
        info = wikipedia.summary(search, 1)
        print(info)
        talk(info)
    except wikipedia.exceptions.PageError:
        talk("Essa pagina não existe")
        pass

def piada():
    joke = pyjokes.get_joke()
    print(joke)
    talk(joke)

def mensagem():
    _hr = int(datetime.datetime.now().strftime("%H"))
    _mi = int(datetime.datetime.now().strftime("%M"))
    talk("Ok, qual a mensagem?")
    msg = take_command()
    print(msg)
    print(_hr)
    print(_mi)
    pywhatkit.sendwhatmsg("+55 11 99242-0991", msg, _hr, _mi + 1, 7)

def cadastrar_evento():
    talk("Ok, qual evento devo cadastrar?")
    agenda = open("agenda.txt", "a+", encoding="utf-8")
    event = take_command()
    print(event)
    agenda.write(event)
    agenda.write("\n")
    talk("Evento cadastrado")
    agenda.close()

def ler_agenda():
    agenda = open("agenda.txt", "r", encoding="utf-8")
    for lines in agenda:
        talk(lines)
    agenda.close()

def tempo():
    API_KEY = os.getenv("API_KEY")
    cidade = 'sao paulo'
    link = 'https://api.openweathermap.org/data/2.5/weather?appid=' + API_KEY + '&q=&' + cidade + 'lang=pt_br'

    requisicao = requests.get(link)
    requisicao_dic = requisicao.json()
    descricao = requisicao_dic['weather'][0]['description']
    temperatura = requisicao_dic['main']['temp'] - 273.15
    clima = (
        f'A temperatura de agora é: {temperatura:.0f} º Celsius, com ' + descricao)
    print(clima)
    talk(clima)

def integrantes():
    integrantes = open("integrantes.txt", "r", encoding="utf-8")
    for lines in integrantes:
        talk(lines)
    integrantes.close()


comandos = {
    'tocar': lambda x: tocar(x),
    'horas': lambda x: horas(),
    'horario': lambda x: horas(),
    'buscar': lambda x: buscar(x),
    'pesquisar': lambda x: buscar(x),
    'procurar': lambda x: buscar(x),
    'piada': lambda x: piada(),
    'mensagem': lambda x: mensagem(),
    'cadastrar evento na agenda': lambda x: cadastrar_evento(),
    'ler agenda': lambda x: ler_agenda(),
    'tempo': lambda x: tempo(),
    'clima': lambda x: tempo(),
    'qual o melhor professor': lambda x: talk("Obviamente é o professor Hellynson"),
    'danilo': lambda x: talk("Presente, professor"),
    'integrantes': lambda x: integrantes()
}



"""
Função que recebe o comando e compara qual cenário será aplicada
"""
def run_friday():
    global ativo

    wake_call = take_command() 
    if not "ok sexta-feira" in wake_call:
        return
    else:
        talk("Sim, mestre. O que posso fazer?")

        while True:
            command = take_command()
            print(command)
            #try:
            for(key, value) in comandos.items():
                if key in command:
                    comandos[key](command)
                    break
            break
        """  except:
            talk("Não entendi o que você disse, poderia repetir por favor?") """


while True:
    run_friday()
