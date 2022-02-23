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

    engine.setProperty('rate', 150)
    engine.save_to_file(newmessage, "tempaudio/text" + str(num) + '.mp3')
    engine.runAndWait()

    sound = pydub.AudioSegment.from_file("tempaudio/text" + str(num) + '.mp3')
    sound = sound.set_frame_rate(48000)
    data = sound.get_array_of_samples()

    sd.default.device = "CABLE Input (Elgato Sound Capture), Windows WASAPI"
    sd.play(data)
    sd.wait()










