import requests
from mutagen.mp3 import MP3

with open("text.txt") as file:
    text = file.read()

key = "be5f4c47488e4d349dbb06b527492c7c"
wav_url = "https://francecentral.tts.speech.microsoft.com/cognitiveservices/v1"
auth_url = "https://francecentral.api.cognitive.microsoft.com/sts/v1.0/issueToken"
lang_url = "https://francecentral.tts.speech.microsoft.com/cognitiveservices/voices/list"
auth_headers = { "Ocp-Apim-Subscription-Key": key, "Content-Length": "0", "Content-type": "application/x-www-form-urlencoded" }

auth_response = requests.post(auth_url, headers=auth_headers)
token = auth_response.text
#print(token)
lang_headers= { "Authorization": "Bearer " + token }

lang_response = requests.get(lang_url, headers=lang_headers)
json_langs = lang_response.json()

print(json_langs[11])

format = "audio-16khz-64kbitrate-mono-mp3"
type = "application/ssml+xml"

headers2 = {
    "Authorization" : f"Bearer {token}", 
    "X-Microsoft-OutputFormat" : "audio-16khz-64kbitrate-mono-mp3", 
    "Content-Type" : "application/ssml+xml",
    "User-Agent": "app"
    }

body = f"<speak version='1.0' xml:lang='{json_langs[11].get('Locale')}'><voice xml:"\
    f"lang='{json_langs[11].get('Locale')}' xml:gender='{json_langs[11].get('Gender')}' "\
    f"name='{json_langs[11].get('Name')}'>{text}</voice></speak>".encode('utf-8') 
    
#print(body)
    
total_response = requests.post(wav_url, data = body, headers = headers2)
res = total_response.text
#print(res)

with open(f"{json_langs[11].get('file', 'voice')}.mp3", 'wb') as f:
          f.write(requests.post(wav_url, data = body, headers = headers2).content)

audio = MP3('voice.mp3')
res_sec = audio.info.length / len(text)
print ("Средняя длительность символа в секундах: "+ str(res_sec))
