import pyttsx3

class TalkAudio():
'''
 Class talks out the provided text
'''  
    def __init__(self):
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate',145)
        
    def talk(self,text):
        self.engine.say(text)
        self.engine.runAndWait()