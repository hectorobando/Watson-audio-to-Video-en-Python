import json
import websocket
import ibm_cloud_sdk_core.authenticators as auth
from ibm_watson import SpeechToTextV1, AssistantV2
import speech_recognition as sr
import time

# Variables para autenticación con IBM Watson Speech-to-Text
apikey = 'tu-apikey'
url = 'tu-url'

# Inicializar instancia del servicio de reconocimiento de voz
r = sr.Recognizer()

# Solicitar entrada de audio
with sr.Microphone() as source:
    print('ESCUCHANDO...')
    audio = r.listen(source, timeout=10.0)
try:
    text = r.recognize_google(audio, language='es-ES')
    print('Assistant dijo: ' + text)
except sr.UnknownValueError:
    print('No se pudo entender lo que dijiste')
except sr.RequestError as e:
    print('No se pudo conectarse con el servicio de reconocimiento de voz; {0}'.format(e))


# Configurar autenticación con IBM Watson Speech-to-Text
authenticator = auth.IAMAuthenticator(apikey)
stt = SpeechToTextV1(authenticator=authenticator)
stt.set_service_url(url)

# Definir parámetros de reconocimiento de voz
content_type = 'audio/l16; rate=44100'
model = 'es-ES_BroadbandModel'

# Enviar audio a IBM Watson Speech-to-Text para reconocimiento de voz
def on_message(ws, message):
    response = json.loads(message)
    if 'results' in response:
        text = response['results'][0]['alternatives'][0]['transcript']
        print('IBM Watson dijo: ' + text)
        # Inicializar instancia del servicio de asistente virtual de IBM Watson
        assistant = AssistantV2(
            version='2021-09-01',
            authenticator=auth.IAMAuthenticator(apikey)
        )
        assistant.set_service_url(url)
        # Enviar texto a IBM Watson Assistant para recibir respuesta
        response = assistant.message(
            assistant_id='id-asistente',
            input={
                'text': text
            }
        ).get_result()
        # Imprimir respuesta
        print(response['output']['generic'][0]['text'])
        print(text)

def on_error(ws, error):
    print(error)

def on_close(ws):
    print('Conexión cerrada')

def on_open(ws):
    ws.send_header('Content-Type', content_type)
    ws.send_header('Custom-Header', 'custom_value')
    ws.send_header('Transfer-Encoding', 'chunked')
    ws.send_header('Authorization', 'Bearer ' + apikey)
    ws.send_header('X-Watson-Learning-Opt-Out', 'true')
    ws.send_header('X-Watson-Metadata', 'metadata_key:metadata_value')
    ws.send_header('model', model)
    ws.send_header('interim_results', True)
    ws.send_header('word_confidence', True)
    ws.send_header('timestamps', True)
    ws.send_header('speaker_labels', True)
    ws.send_header('results_per_return', 1)
    ws.send_header('max_alternatives', 1)
    ws.send_header('content-type', content_type)
    ws.send_header('cookie', 'cookies')
    ws.send_header('origin', 'origin_value')
    ws.send_header('referer', 'referer_value')
    ws.send_header('deflate', 'true')
    ws.send_header('encoding', 'json')
    ws.send_header('recording_id', 'recording_id')
    ws.send_header('language_customization_id', 'language_customization_id')