import pyautogui
import time
import json
import os
import re
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

    LstMsg=LstMsg.strip("\n").strip(" ").strip("\n")
    contact = contact[0]
    Name = firstChild(firstChild(firstChild(contact))).string
    Name = Name.strip("\n").strip(" ").strip("\n")
    TimeLstMsg = firstChild(list(contact)[1]).string
    TimeLstMsg=TimeLstMsg.strip("\n").strip(" ").strip("\n")
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

os.chdir('htmls')
while True:
    READED = os.listdir('READED')
    for f in os.listdir():
        if f.endswith('.json') and f not in READED:
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
            
            os.rename('.\\'+f,'.\\READED\\'+f)
    time.sleep(1)
    newjsons = [x for x in os.listdir() if x.endswith('json')]
    if len(newjsons) > 0:
        os.system('cls')
