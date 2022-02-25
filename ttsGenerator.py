from numpy import append
import pyttsx3
import pydub

import sounddevice as sd

from profanity_filter import ProfanityFilter



def generate_ttsmp3(text: str, usrnme : str, num: int):

    engine = pyttsx3.init(driverName='sapi5')
    message = f"User {usrnme} says: {text}"

    pf = ProfanityFilter()

    
    
    print(message)
    message = pf.censor(message)
    newmessage = ""
    group = False
    for char in message:
        if char == '*':
            if not group:
                newmessage = newmessage + ' CENSORED '
                group= True


        else:
            group = False
            newmessage += char
    
    engine.setProperty('rate', 170)
    engine.save_to_file(newmessage, "tempaudio/text" + str(num) + '.mp3')
    engine.runAndWait()

    sound = pydub.AudioSegment.from_file("tempaudio/text" + str(num) + '.mp3')
    sound = sound.set_frame_rate(48000)

    duration = len(sound.get_array_of_samples())/48000

    seconds = 5
    multiplier = seconds*1000
    if duration > seconds:
        sound = sound[:multiplier]
    
    data = sound.get_array_of_samples()

    sd.default.device = "CABLE Input (Elgato Sound Capture), Windows WASAPI"
    sd.play(data)
    ttsmessage = open("obsout.txt", "w")
    ttsmessage.write(f"Current tts message: {newmessage}")
    ttsmessage.close()

    sd.wait()
    ttsmessage = open("obsout.txt", "w")
    ttsmessage.close()









