import urllib
import socket
import speech_recognition as sr

# setting a socket to send message to pi3:

TCP_IP = '192.168.1.2'
TCP_PORT = 5005
BUFFER_SIZE = 1024
GO = 'move'
STOP = 'stop'
QUIT = 'quit'
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT)) 

while True:
	# Record Audio
	r = sr.Recognizer()
	with sr.Microphone(device_index=3) as source:
		r.adjust_for_ambient_noise(source)
		print("Say something!")
		audio = r.listen(source)
	 
	# Speech recognition using Google Speech Recognition
		# for testing purposes, we're just using the default API key
		# to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
		# instead of `r.recognize_google(audio)`
		try:
			if r.recognize_google(audio) == 'go':
				print("Car moving")
				s.send(GO)
			elif r.recognize_google(audio) == 'stop':
				print("Car stopped")
				s.send(STOP)
			elif r.recognize_google(audio) == 'quit':
				print("Quiting")
				s.send(QUIT)
				break
		except sr.UnknownValueError:
			print("Google Speech Recognition could not understand audio")
		except sr.RequestError as e:
			print("Could not request results from Google Speech Recognition service; {0}".format(e))