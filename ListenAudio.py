import speech_recognition as sr

class ListenAudio():
    '''
    Class listens to microphone and returns the search term provided by user through audio
    '''
    def __init__(self):
        self.recog = sr.Recognizer()
        
    def take_command(self):
    '''
    Returns the search term microphone audio.
    '''
        search = ''
        with sr.Microphone() as source:
            try:
                self.recog.adjust_for_ambient_noise(source)
                audio_data = self.recog.listen(source)        
                search = self.recog.recognize_google(audio_data)       
                return search
            except:
                print('Could not understand audio')
                return ''