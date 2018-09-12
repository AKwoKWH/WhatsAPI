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

Because of this, to make a bot that avoids being detected, one must make the bot extremely hard to differenciate from a human. And this is exactly what WhatsAPI does. Almost every interaction between WhatsAPI and the WhatsApp web application, is made almost like a human would do, and those that are not exactly what a human would do, are almost certainly undetectable by WhatsApp, however everything WhatsAPI does, can be done by a human too using just the keyboard and a brain.