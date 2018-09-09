import pyautogui
import random
import time
import json
import os
import re
import pyautogui
import pyperclip
from bs4 import BeautifulSoup
from random import randint
from pprint import pprint

'''time.sleep(10)
pyautogui.press('tab')
time.sleep(randint(1,5))
pyautogui.press('tab')
time.sleep(randint(1,5))
pyautogui.press('tab')
time.sleep(randint(1,5))
pyautogui.press('tab')
time.sleep(randint(1,5))
pyautogui.typewrite("Hello World!")
time.sleep(randint(1,5))
pyautogui.press('enter')'''

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
    '''try:
        element = list(element)[1]
    except:
        element = list(element)[0]
    print(element)
    #_3_7SH _14b5J Zq3Mc tail
    element = list(element)[2]#Tkt2p
    message = list(list(list(element)[0])[0])[0].string
    time = list(list(list(element)[1])[0])[1].string
    messageInfo = {'Time':time,'Txt':message}
    print(messageInfo)'''
    regex = re.compile('.*' + contact)
    message_e = element('div',{'data-pre-plain-text':regex})[0]
    time = message_e['data-pre-plain-text'].replace('[','').replace('] ' + contact + ': ','')
    txt = list(list(message_e)[0])[0].string
    return {'Time': time, 'Txt':txt, 'From': contact}

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
    #Focus on search input
    pyautogui.hotkey('ctrl','shift','j')
    randSleep()
    pyautogui.typewrite("$('input')[0].focus()")
    pyautogui.press('enter')
    pyautogui.hotkey('ctrl','shift','j')
    #Type contact name on search input
    randSleep()
    pyautogui.typewrite(To)
    randSleep()
    #Tab to select contact and focus on message input
    pyautogui.press('tab')
    pyautogui.press('tab')
    pyautogui.press('tab')
    time.sleep(1)
    #Send message
    pyautogui.typewrite(Txt)
    randSleep()
    pyautogui.press('enter')
    #Focus on search input
    pyautogui.hotkey('ctrl','shift','j')
    randSleep()
    pyautogui.typewrite("$('input')[0].focus()")
    pyautogui.press('enter')
    pyautogui.hotkey('ctrl','shift','j')
    #Clear search input
    randSleep()
    pyautogui.press('esc')


sent = False

time.sleep(5)
loadJQuery()
os.chdir('htmls')
while True:
    READED = os.listdir('READED')
    for f in os.listdir():
        if f.endswith('.json') and f not in READED:
            try:
                with open(f, 'r', encoding='utf-8') as file:
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
                    pprint(chat)
                    for contact in contactos:
                        pprint(getContactInfo(contact,chat['selected_contact']))
            except:
                #While having something on the contact search input, the HTML changes heavily and the getContactInfo fails
                pass
            os.rename('.\\'+f,'.\\READED\\'+f)
    time.sleep(1)
    newjsons = [x for x in os.listdir() if x.endswith('json')]

    if not sent:
        sendMessage("Hola","Sebastian")
        sent = True

    if len(newjsons) > 0:
        os.system('cls')
