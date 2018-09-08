from bs4 import BeautifulSoup

def firstChild(item):
    return list(item)[1]

def getContactInfo(contact):
    contact = list(list(firstChild(firstChild(contact)))[3])
    LstMsg = contact[3]
    LstMsg = firstChild(firstChild(firstChild(LstMsg))).string
    LstMsg=LstMsg.strip("\n").strip(" ").strip("\n")
    contact = contact[1]
    Name = firstChild(firstChild(firstChild(contact))).string
    Name = Name.strip("\n").strip(" ").strip("\n")
    TimeLstMsg = firstChild(list(contact)[3]).string
    TimeLstMsg=TimeLstMsg.strip("\n").strip(" ").strip("\n")
    return{"contact":Name,"Last Msg":{"Time":TimeLstMsg,"Txt":LstMsg}}


with open('html6.html','r',encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(),'html.parser')
    fidiv=list(soup.find('div',{'id':'app'}).children)[1]#_1FKgS
    sediv=list(list(fidiv.children)[11].children)#_3dqpi
    contactos=list(list(sediv[5])[1])[7]#_1vDUw
    contactos=list(firstChild(firstChild(firstChild(contactos))))#RLfQR
    contactos=[x for x in contactos if x != '\n']
    for contact in contactos:
        print(getContactInfo(contact))
    chat=firstChild(sediv[3])

