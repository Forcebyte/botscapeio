# Scapio - RuneScape Woodcutting/FireMaking Level Bot

Scapio is a client for automated leveling bots created for all RuneScape versions with a focus on OSRS

---

This is a 24 hour project I was working on that automates a few of the really simple grinding tasks that exist in RuneScape, it uses OCR recognition without having to use high-capacity libraries such as TensorFlow

## Note..
I've tested this and haven't gotten banned in about a week of use, however it is highly encouraged that you use this at your own risk - there are a few anti-botting measures in place today, including the ablity to randomly move and click during botting

## Functionality

Today, this bot only handles the following leveling paths, if I ever get the time and motivation i'll probably add additional leveling paths (e.g. RuneCrafting, Smithing, etc)

- Tinder / FireMaking Leveling
- WoodCutting Leveling

## Running Locally

(Ensure that you have [Python 3.6](https://www.python.org/ftp/python/3.9.6/python-3.9.6-amd64.exe) or higher installed)

Simply run the following

```bash
pip3 install -r requirements.txt
cd bin
python3 main.py
```

PyAutoGUI will take care of most of the prompting, window maintainence - simply press on the leveling you'd like to accomplish and relax!
![sample screenshot](https://github.com/Forcebyte/scapio/raw/src/img1.png)
