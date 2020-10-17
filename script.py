# See the project: https://github.com/elmoallistair/watson-s2t-language-translator

# Importing required modules
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson import SpeechToTextV1 
from ibm_watson import LanguageTranslatorV3
from pandas import json_normalize

# Specifies the sample audio
filename = '<AUDIO_FILE>.mp3'

# 1. Transcribes audio to text

# Add IBM Watson™ Speech to Text Credentials
API_S2T = '<YOUR_S2T_APIKEY'>
URL_S2T = '<YOUR_S2T_URL'

# Speech To Text Authentication
s2t_auth = IAMAuthenticator(API_S2T)
speech_to_text = SpeechToTextV1(authenticator=s2t_auth)
speech_to_text.set_service_url(URL_S2T)

# Recognize the audio
print("recognizing audio.... ")
with open(filename, mode="rb") as wav:
    s2t_response = speech_to_text.recognize(audio=wav, content_type='audio/mp3')
    print("done")

# Explore the transcription result
# print("\nResponse: \n", s2t_response.result)

# Normalize the result
print("\nNormalized response: \n", json_normalize(s2t_response.result['results'],"alternatives"))

s2t_responses_list = []
for responses in s2t_response.result['results']:
    s2t_responses_list.append(responses['alternatives'][0]['transcript'])

# Final result
final_result_s2t = ' '.join(s2t_responses_list)
print(f"\nTranscription result ({filename}): \n", final_result_s2t)
final_result_s2t

# 2. Translate the text to another language

# Add IBM Watson™ Language Translator Credentials
API_LT = '<YOUR_LT_APIKEY>'
URL_LT = '<YOUR_LT_URL>'
VER_LT = '2018-05-01'

# Language Translator Authentication
lt_auth = IAMAuthenticator(API_LT)
language_translator = LanguageTranslatorV3(version=VER_LT, authenticator=lt_auth)
language_translator.set_service_url(URL_LT)

# Get a list of supported languages
json_normalize(language_translator.list_identifiable_languages().get_result(), "languages")

# Translate from EN to ID
print("\ntranslating text.... ")
tl_response = language_translator.translate(text=final_result_s2t, model_id='en-id')
print("done")
tl_result = tl_response.get_result()

# Explore the translation result
# print("\nLanguage Translator response: \n", tl_result)

# Get the translation result
final_result_tl = tl_result['translations'][0]['translation']

# Final result
print("\nTranslation result (en-id): \n", final_result_tl)
