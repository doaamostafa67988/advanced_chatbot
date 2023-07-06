## Import Libraries, and read the key-token
import openai
import os
from dotenv import load_dotenv
import sounddevice as sd
import soundfile as sf
from scipy.io.wavfile import write
import time


## Load the Key token
_ = load_dotenv()
key_token = os.getenv('OpenAI_KEY_TOKEN')

## Assign that key_token to api_key of OpenAI
openai.api_key = key_token


## Looping to make it much more easier
all_messages = list()

## Create system prompt
system_prompt = '''you are ai assistant answer only in these feilds computer science and 
all programming languges for example java ,python, c#
 otherwise answer that "sorry, I can help you in computer science feild only " '''
all_messages.append({'role': 'system', 'content': system_prompt})

## Capture voice for 30 secound
fs = 44100  # Sample rate
seconds = 30  # Duration of recording
def  capture_voice():
    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
    sd.wait()  # Wait until recording is finished
    write('audio/output.wav', fs, myrecording)

# Extract audio data and sampling rate from file 
    data, fs = sf.read('audio/output.wav')

# Save as FLAC file at correct sampling rate
    sf.write('audio/output.mp3', data, fs)  
    os.remove(os.path.abspath("audio/output.wav"))
    destination = os.path.abspath("audio/output.mp3")
    return destination

## ------------------------------ Call the API -------------------------------- ##
def custom_chatbot(user_prompt:str=None,destination:str=None):
    
    
    if destination:
            audio_path=destination
            ## Transcrip using whipser
            with open(audio_path, 'rb') as file:
                transcribt = openai.Audio.transcribe('whisper-1', file)
            ## delete the audio file
            os.remove(audio_path)
            user_prompt=str(transcribt)
           
    
    ## Looping while true
    while True:
        ## If the user wants to exit the chatbot -> break
        if user_prompt.lower() in ['quit', 'exit', 'ex', 'out', 'escape']:
            time.sleep(2)  ## wait 2 seconds

            ## If the user exit the chatbot, Clear it.
            all_messages.clear()
            return 'Thanks for using my ChatBot'
        
        ## If the user doesn't write any thing -> Continue
        elif user_prompt.lower() == '': 
            continue

        ## Answer
        else:
            
            ## append the question of user to message as a user roke
            all_messages.append({'role': 'user', 'content': user_prompt})
            
            ## Call the API
            each_response = openai.ChatCompletion.create(
                            model='gpt-3.5-turbo',           
                            messages=all_messages,
                            temperature=0.7,  
                            max_tokens=2048,   
                                )
            each_response = each_response['choices'][0]['message']['content']
           
            
            ## We must append this respond to the messages
            all_messages.append({'role': 'assistant', 'content': each_response})
            
    
            return each_response  ## return the response of the api
    
            

