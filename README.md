# WhatsAPI

WhatsAPI is an API (duh) to send and receive messages using the very API-unfriendly but hugely popular messaging service of WhatsApp.

Once installed on a dedicated desktop, the program will monitor the WhatsApp web application, find new messages on the app, store them in easy to read and access json files, find new message sending requests in easy to write json files and send them to the specified contacts.

## How does it works?

The core of WhatsAPI is composed of the [PyAutoGUI](https://github.com/asweigart/pyautogui) module to simulate a user interacting with the browser as close as posible, my [HTML-Surveillor](https://github.com/SebastianMCarreira/HTML-Surveillor) Chrome extension to extract the resulting HTML as it changes with each user interaction and new message received and [BeautifulSoup 4](https://pypi.org/project/beautifulsoup4/)

## Install and setup

### Prerequisites
* Chrome v68
* Python v3.6
* Powershell v5.1
* PyAutoGUI v0.9
* BeautifulSoup v4.6
* Pyperclip v1.6
* HTML-Surveillor v1.0

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

## 