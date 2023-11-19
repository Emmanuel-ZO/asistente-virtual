import datetime
import webbrowser

import pyjokes
import pyttsx3
import pywhatkit
import speech_recognition as sr
import wikipedia
import yfinance as yf

# opcions de voz / idioma
id1 = r'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_ES-ES_HELENA_11.0'
id2 = r'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0'
id3 = r'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_ES-MX_SABINA_11.0'


# escuchar microfono y devolver el audio como texto
def transformar_audio_a_texto():
    # almacena recognizer en variable
    r = sr.Recognizer()

    # configurar microfono
    with sr.Microphone() as origen:
        # tiempo de espera
        r.pause_threshold = 0.5

        # informar que comenzó grabación
        print('Ya puedes hablar')

        # guardar lo que escuche como audio
        audio = r.listen(origen)

        try:
            # buscar en google lo que haya escuchado
            pedido = r.recognize_google(audio, language="es-Mx")
            print("Dijiste: " + pedido)
            return pedido
        except sr.UnknownValueError:
            print("Google Speech Recognition no pudo entender lo que dijiste")
            return "Sigo esperando"
        except sr.RequestError as e:
            print("No se pudo obtener resultados del servicio de reconocimiento de voz: {0}".format(e))
            return "Sigo esperando..."
        except Exception as e:
            print("Ups, algo salió mal: {0}".format(e))
            return "Ups, algo salio mal!"


# funcion para que el asistente pueda ser escuchado
def hablar(mensaje):
    # encender motor pyttsx3
    engine = pyttsx3.init()
    engine.setProperty('voice', id3)
    # pronunciar mensaje
    engine.say(mensaje)
    engine.runAndWait()


# informar el dí a de la semana
def pedir_dia():
    # crear variable con datos de hoy
    dia = datetime.date.today()
    print(dia)

    # crear variable para mostral el dia
    dia_semana = dia.weekday()
    print(dia_semana)

    # diccionario con nombre de los dias
    calendario = {0: 'Lunes',
                  1: 'Martes',
                  2: 'Miércoles',
                  3: 'Jueves',
                  4: 'Viernes',
                  5: 'Sábado',
                  6: 'Domingo'}
    # decir día de la semana
    hablar(f'Hoy es {calendario[dia_semana]}')


# informar hora que es
def pedir_hora():
    # crear variable con datos de la hora
    hora = datetime.datetime.now()
    hora = f'En este momento son las {hora.hour} horas con ' \
           f'{hora.minute} minutos y {hora.second} segundos'
    print(hora)

    hablar(hora)


# saludo inicial
def saludo_inicial():
    # crear variable con datos de hora
    hora = datetime.datetime.now()
    if hora.hour > 20 or hora.hour < 6:
        momento = "Buenas noches"
    elif 6 <= hora.hour < 12:
        momento = 'Buen día'
    else:
        momento = 'Buenas tardes'

    # decir saludo
    hablar(f"{momento}, Bienvenido nuevamente. Por favor dime en que te puedo ayudar.")


# funcion central del asistente
def pedir_cosas():
    # activar saludo inicial
    saludo_inicial()

    # variable de corte
    comenzar = True

    # loop central
    while comenzar:
        # activar el microfono y guardar el pedido en un string
        pedido = transformar_audio_a_texto().lower()

        if 'abrir youtube' in pedido:
            hablar('Con gusto, estoy abriendo YouTube')
            webbrowser.open('https://www.youtube.com')
            continue
        elif 'abrir navegador' in pedido:
            hablar('Claro, estoy en eso')
            webbrowser.open('https://www.google.com')
            continue
        elif 'qué día es hoy' in pedido:
            pedir_dia()
            continue
        elif 'qué hora es' in pedido:
            pedir_hora()
            continue
        elif 'busca en wikipedia' in pedido:
            hablar('Buscando en wikipedia')
            pedido = pedido.replace(' busca en wikipedia', '')
            wikipedia.set_lang('es')
            resultado = wikipedia.summary(pedido, sentences=1)
            hablar('wikipedia dice lo siguiente:')
            hablar(resultado)
            continue
        elif 'busca en internet' in pedido:
            hablar('Estoy en eso')
            pedido = pedido.replace('busca en internet', '')
            pywhatkit.search(pedido)
            hablar('Esto es lo que he encotrado: ')
            continue
        elif 'reproduce' in pedido:
            hablar('Excelente elección, reproduciendo.')
            pywhatkit.playonyt(pedido)
            continue
        elif 'chiste' in pedido:
            hablar(pyjokes.get_joke('es'))
            continue
        elif 'precio de las acciones' in pedido:
            accion = pedido.split('de')[-1].strip()
            cartera = {'apple': 'APPL',
                       'Amazon': 'AMZN',
                       'google': 'GOOGL'}
            try:
                accion_buscada = cartera[accion]
                accion_buscada = yf.Ticker(accion_buscada)
                precio_actual = accion_buscada.info['regularMarketPrice']
                hablar(f'La encontré, el precio de la {accion} es {precio_actual}')
                continue
            except:
                hablar('Perdón, pero no la he encotrado')
        elif 'adiós' in pedido:
            hablar("Me voy a descansar, cualquier cosa me avisas")
            break


pedir_cosas()
