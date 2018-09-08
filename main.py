import pyautogui
import time
import json
import os
from bs4 import BeautifulSoup
from random import randint

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

def getContactInfo(contact):
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
    return{"contact":Name,"unreads":unread,"LastMsg":{"Time":TimeLstMsg,"Txt":LstMsg}}

os.chdir('htmls')
for f in os.listdir():
    if f.endswith('.json'):
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
            for contact in contactos:
                print(getContactInfo(contact))
            chat=sediv[3]
