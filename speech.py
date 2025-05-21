import speech_recognition as sr
import pyaudio
# Initialize the recognizer
recognizer = sr.Recognizer()

def recognize_speech_and_process():
    # Use the microphone as source
    with sr.Microphone() as source:
        print("Please speak a command...")
        audio_data = recognizer.listen(source)
        
        try:
            # Recognize the speech using Google's speech recognition
            text = recognizer.recognize_google(audio_data)
            print(f"Recognized speech: {text}")
            
            # Call specific functions from your existing code based on keywords
            if "report incident" in text.lower():
                # Call function to handle 'Report Incident'
                report_incident()
            elif "view incident" in text.lower():
                # Call function to handle 'View Incident'
                view_incident()
            elif "get resources" in text.lower():
                # Call function to handle 'Get Resources'
                get_resources()
            elif "get help" in text.lower():
                # Call function to handle 'Get Help'
                get_help()
            else:
                print("Command not recognized.")
                
        except sr.UnknownValueError:
            print("Could not understand audio")
        except sr.RequestError:
            print("Could not request results from the speech recognition service")

# Functions corresponding to actions
def report_incident():
    print("Report Incident called.")
    # Existing code for report incident can be referenced here

def view_incident():
    print("View Incident called.")
    # Existing code for view incident can be referenced here

def get_resources():
    print("Get Resources called.")
    # Existing code for get resources can be referenced here

def get_help():
    print("Get Help called.")
    # Existing code for get help can be referenced here

if __name__ == "__main__":
    recognize_speech_and_process()
