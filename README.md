# WhatsAPI

WhatsAPI is an API (duh) to send and receive messages using the very API-unfriendly but hugely popular messaging service of WhatsApp.

Once installed on a dedicated desktop, the program will monitor the WhatsApp web application, find new messages on the app, store them in easy to read and access json files, find new message sending requests in easy to write json files and send them to the specified contacts.

## How does it works?

The core of WhatsAPI is composed of the [PyAutoGUI](https://github.com/asweigart/pyautogui) module to simulate a user interacting with the browser as close as posible, my [HTML-Surveillor](https://github.com/SebastianMCarreira/HTML-Surveillor) Chrome extension to extract the resulting HTML as it changes with each user interaction and new message received and [BeautifulSoup 4](https://pypi.org/project/beautifulsoup4/).

### Processes

![graph](https://github.com/SebastianMCarreira/WhatsAPI/blob/master/WhatsaAPI.png?raw=true)

1. Absolute paths to directories and files for unread messages, messages to send, unread htmls, readed htmls and readed hashes are set in config.json and served to main.py. Initial sleep is also set there.
2. Keyboard orders are passed down to the PyAutoGUI engine as they are needed.
3. Some commands are executed on the javascript console, first to "manually" load jQuery. The console is accessed using the ctrl+shift+j hotkey.
4. Using only characters to write and tab to navigate downwards in the HTML, the PyAutoGUI engine is capable of searching the desired contact, select his chat, write down the message on the input and sending it.
5. From the console and using jQuery, the contact search input is selected and focused.
6. The HTML is constantly monitored by HTML-Surveillor, every time it changes, a new json containing the HTML is downloaded.
7. New json files are moved to the corresponding directory by json-saver.ps1.
8. New json files are readed and their HTML parsed by main.py in order to identify new messages and contacts. Readed json files are moved to the corresponding directory.
9. Every time a new message (with a resulting hash not included in the readed hashes json) is identified in the HTML, a new json will be created in the corresponding directory containning the sender, the timestamp and the content of said message. Also, every time a new json is created in the directory for messages to send, it will be read by main.py, sent to the stated receipent and deleted the file.
10. External applications can read new messages' jsons to effectively receive the messages and create new jsons to send them.

### Getting the HTML and scrapping the data

When I began this project, I found it hard first to get the same HTML as with the browser, it was possible, but it would have involved a lot of work looking at the headers, cookies and requests sent and received by the browser, also a way to keep my connection alive instead of several HTTP requests a minute (something that probably would end with my API banned), etc. Because of that, I decided to leave that work to the browser. Instead, I developed a Chrome extension to simply extract the HTML every time it changed and from there, scrap it all. 

To do that, I had to invest several hours looking at WhatsApp's web app's HTML, finding how the contact list is structured, where do the messages appear, how can I make the bot recognize a message. And that was a challenge because WhatsApp changes the classe names by seemingly random strings every now and then, so I couldn't simply do soup('div', 'message') and voilà, but fortunately, it had a weakness there I found while trying to make the program find messages by walking the DOM in a specific way. Messages have a special attribute named "data-pre-plain-text" that contains the time the message was sent, who sent it and the content of the div with that attribute is the message content itself, everything I needed.

### Detecting old messages

To avoid detecting of old messages, I decided to (provisionally) generate a hash calculated from the message's content, time and sender, and store the resulting hash to check that list everytime a message is detected, and if it's not there, create the json file of that message. In the future, I plan to make this work with a database and store the whole message.

### Sending messages

This was the trickiest part, because I had to simulate a human sending a message as close as possible. What I did was using jQuery to get the element corresponding to the contact search input and focus in it. Once there, it was a matter of writting the desired contact, tab once to select that contact in the contact list, tab two more times to focus on the message input (that is actuallty not an input), writting the message and pressing enter to send.

## Install and setup

### Prerequisites
* Chrome v68
* Python v3.6
* Powershell v5.1
* PyAutoGUI v0.9
* BeautifulSoup v4.6
* Pyperclip v1.6
* HTML-Surveillor v1.0
* A smartphone with WhatsApp installed, a working number and uninterrupted internet access.

### Installing
Once all the prerequisites are installed, you must log an account to the WhatsApp web application. This is done going to http://web.whatsapp.com in Chrome, there you will be asked to scan the QR code with your phone using the WhatsApp phone app. Once scanned, the web app will automatically syncronize your account.

**Warning: I recommend using a disposable phone number and WhatsApp account. I did not (yet) get my account banned using WhatsAPI and how it works makes it extremely hard for WhatsApp to recognize the user as a bot. However, abuse of WhatsAPI or cleverness from WhatsApp may get your account and number banned from ever using WhatsApp**

### Setup

Once syncronized, start running HTML-Surveillor's json-saver.ps1 (make sure you configure correctly the config.json paths, expressions and targets before). After that, with the WhatsApp web application tab open, click on the HTML-Surveillor popup and click _set surveillance_. The extension will automatically download a new json containing the page's HTML and move it to the WhatsAPI folder you configured.

After that, it only rests to run, using the command prompt while standing on the WhatsAPI folder:

```
$python main.py
```

You will have then 5 seconds to click within the WhatsApp web application window. After that, the program will need to use the keyboard while on that window to function.

Congrats! The API is setup. You should already visualize the parsed information on the prompt.

If you want to stop it, simply switch to the command prompt window and press ctrl+c to stop it.

## Why use WhatsAPI?

The thing about WhatsApp, is not only the lack of an API with easy REST calls to urls, it's that they actually don't want APIs at all, not even made by users. Because of this, a lot of APIs work for a while, until WhatsApp identifies a certain user as a bot and bans that phone number.

Exactly to avoid being detected, I decided to make something that works as close as posible to a human. And this is exactly what WhatsAPI does. Almost every interaction between WhatsAPI and the WhatsApp web application, is made almost like a human would do, and those that are not exactly what a human would do, are almost certainly undetectable by WhatsApp, however everything WhatsAPI does, can be done by a human too using just the keyboard and a brain.

## To-Do List

### Beta

- [x] HTML-Surveillor Chrome Extension
- [x] Parsing and scrapping of web app's HTML
- [x] Identification of new messages
- [x] Sending of messages
- [x] Reception of messages to send
- [ ] Automatically check contacts with unread messages
- [ ] Making an actual console UI
- [ ] Setting up a VM as a dedicated working desktop

### v1

- [ ] Usage of PyAutoGUI mouse control and screen image finding
- [ ] HTTP server to use requests as a method of sending and receving data instead of json files
- [ ] Database to save processed messages

##