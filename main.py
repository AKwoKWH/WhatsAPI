import pyautogui
import random
import time
import json
import os
import re
import pyperclip
from bs4 import BeautifulSoup
from random import randint
from pprint import pprint

def hasher(data, lenght):
    max = "f" * lenght
    max = int(max,16)
    data = [str(d) for d in data]
    accumulator = 0
    chars = 0
    for d in data:
        for c in d:
            accumulator += ord(c)
        chars += len(d)
    
    result = accumulator ** chars
    result %= max
    return hex(result)[2:]

def randSleep(min = 0.5, max = 1):
    time.sleep(random.uniform(min, max))

def firstChild(item):
    return list(item)[0]

def getContactInfo(contact, selected_contact):
    contact = list(list(firstChild(firstChild(contact)))[1])
    LstMsg_unread = list(contact[1])
    LstMsg = firstChild(firstChild(firstChild(LstMsg_unread))).string
    unread = firstChild(LstMsg_unread[1]).string
    if not unread:
        unread = 0
    else:
        unread = int(unread)

    LstMsg=LstMsg
    contact = contact[0]
    Name = firstChild(firstChild(firstChild(contact))).string
    Name = Name
    TimeLstMsg = firstChild(list(contact)[1]).string
    TimeLstMsg=TimeLstMsg
    if selected_contact == Name:
        selected = True
    else:
        selected = False
    return{"contact":Name,"unreads":unread,"selected": selected,"LastMsg":{"Time":TimeLstMsg,"Txt":LstMsg}}

def isMessage(element, contact):
    regex = re.compile('.*' + contact)
    if len(element('div',{'data-pre-plain-text':regex})) == 0:
        return False
    else:
        return True

def getMessageInfo(element,contact):
    regex = re.compile('.*' + contact)
    message_e = element('div',{'data-pre-plain-text':regex})[0]
    time = message_e['data-pre-plain-text'].replace('[','').replace('] ' + contact + ': ','')
    txt = list(list(message_e)[0])[0].string
    hash = hasher([time,txt,contact],6)
    return {'Time': time, 'Txt':txt, 'From': contact, "hash":hash}

def getChatInfo(chat):
    try:
        selected_contact_name = firstChild(firstChild(firstChild(list(chat[1])[1]))).string
    except:
        return {'selected_contact': None, 'messages':[]}

    messages = list(list(list(list(chat[2])[2])[2])[1])#_9tCEa
    messages = [getMessageInfo(x, selected_contact_name) for x in messages if isMessage(x, selected_contact_name)]
    return {'selected_contact': selected_contact_name, 'messages': messages}

def loadJQuery():
    pyautogui.hotkey('ctrl','shift','j')
    time.sleep(3)
    with open('jquery.js','r',encoding='utf-8') as f:
        jquery = f.read()
        pyperclip.copy(jquery)
        pyautogui.hotkey('ctrl','v')
        time.sleep(3)
        pyautogui.press('enter')
    pyautogui.hotkey('ctrl','shift','j')

def sendMessage(Txt, To):
    sleep = 1
    pyperclip.copy("$('input')[0].focus();")
    #Focus on search input
    print("copy")
    time.sleep(sleep)
    pyautogui.hotkey('ctrl','shift','j')
    print("o console")
    time.sleep(sleep)
    pyautogui.hotkey('ctrl','v')
    print("paste")
    time.sleep(sleep)
    pyautogui.press('enter')
    print("enter")
    time.sleep(sleep)
    pyautogui.hotkey('ctrl','shift','j')
    print("c console")
    #Type contact name on search input
    time.sleep(sleep)
    pyautogui.typewrite(To)
    print("contacto")
    time.sleep(sleep)
    #Tab to select contact and focus on message input
    pyautogui.press('tab')
    pyautogui.press('tab')
    pyautogui.press('tab')
    print("tabs")
    time.sleep(sleep)
    #Send message
    pyautogui.typewrite(Txt)
    print("contenido")
    time.sleep(sleep)
    pyautogui.press('enter')
    print("enter")
    time.sleep(sleep)
    #Focus on search input
    pyautogui.hotkey('ctrl','shift','j')
    print("o console")
    time.sleep(sleep)
    pyautogui.hotkey('ctrl','v')
    print("paste")
    time.sleep(sleep)
    pyautogui.press('enter')
    print("enter")
    time.sleep(sleep)
    pyautogui.hotkey('ctrl','shift','j')
    print("c console")
    #Clear search input
    time.sleep(sleep)
    pyautogui.press('esc')
    print("esc")

def checkHashes(messages):
    hashes = []
    with open(config['readed_hashes'],'r',encoding='utf-8') as file:
        hashes = json.loads(file.read())["hashes"]
        for msg in messages:
            if msg["hash"] not in hashes:
                hashes.append(msg["hash"])
                prompts.append("New message {}!".format(msg["hash"]))
                newMessage(msg)
        
    with open(config['readed_hashes'],'w',encoding='utf-8') as file:
        file.write(json.dumps({"hashes":hashes}))
        
def newMessage(msg):
    with open(config['received'] + msg["hash"] + ".json",'w',encoding='utf-8') as file:
        file.write(json.dumps(msg))


def checkNewMessages():
    for msg_to_send in os.listdir(config["to_send"]):
        if msg_to_send.endswith(".json"):
            with open(config['to_send'] + msg_to_send,'r',encoding='utf-8') as file:
                msg = json.loads(file.read())
                sendMessage(msg["txt"],msg["to"])
            os.remove(os.path.join(config["to_send"],msg_to_send))



sent = False
config = None
prompts = []
with open('config.json','r',encoding='utf-8') as file:
    config = json.loads(file.read())

time.sleep(config['initial_sleep'])
loadJQuery()

while True:
    READED = os.listdir(config['readed'])
    for f in os.listdir(config['htmls']):
        if f.endswith('.json') and f not in READED:
            try:
                with open(config['htmls'] + f, 'r', encoding='utf-8') as file:
                    obj = json.loads(file.read())
                    print(obj['URL'])
                    soup = BeautifulSoup(obj['HTML'], 'html.parser')
                    for svg in soup('svg'):
                        svg.decompose()
                    for head in soup('head'):
                        head.decompose()
                    for script in soup('script'):
                        script.decompose()
                    

                    #newfilename = f[:-4] + "html"
                    #with open(newfilename, 'w', encoding='utf-8') as nf:
                    #    nf.write(soup.prettify())

                    fidiv=list(soup.find('div',{'id':'app'}).children)[0]#_1FKgS
                    sediv=list(list(fidiv.children)[5].children)#_3dqpi
                    contactos=list(list(sediv[2])[0])[3]#_1vDUw
                    contactos=list(firstChild(firstChild(firstChild(contactos))))#RLfQR
                    contactos=[x for x in contactos if x != '\n']
                    
                    chat=list(firstChild(sediv[3]))#_1GX8_
                    chat = getChatInfo(chat)
                    checkHashes(chat["messages"])
                    pprint(chat)
                    for contact in contactos:
                        pprint(getContactInfo(contact,chat['selected_contact']))

                    for pro in prompts:
                        print(pro)
            except:
                #While having something on the contact search input, the HTML changes heavily and the getContactInfo fails
                pass
            os.rename(config['htmls'] + f,config['readed'] + f)


    checkNewMessages()

    time.sleep(1)
    newjsons = [x for x in os.listdir(config['htmls']) if x.endswith('json')]

    if len(newjsons) > 0:
        os.system('cls')
