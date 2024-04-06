import time
import plyer
import win32com.client as w

#Helpful to custom our own notification
def Notify_Reminder():
    plyer.notification.notify(
        app_name = "Reminder Notify",
        app_icon ="C:/Users/khana/OneDrive/Desktop/YtPython/water.ico",
        title="Water Reminder",
        message = "Time to drink water as you haven't drink since past 2 hours and could affect your body.",
        timeout = 10)

def voice():
    speaker_number = 1
    spk = w.Dispatch("SAPI.SpVoice")
    vcs = spk.GetVoices()
    spk.Voice
    spk.SetVoice(vcs.Item(speaker_number))
    spk.speak("Drink Water Reminder")
    spk.speak("Since you are working for 2 hours its time to take rest for 10 minutes and drink water")
    
def Ren():
    while True:
      time.sleep(10)#wait for 10 seconds and then notify me it is just an example you can change it according to you.
      Notify_Reminder()
      voice()
      
if __name__ == "__main__":
    Ren()
