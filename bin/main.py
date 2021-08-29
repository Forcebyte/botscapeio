from utils import parser, window
import os, sys
import logging
import keyboard
from time import sleep

FORMAT = "[%(asctime)s - %(levelname)s:%(filename)s:%(lineno)s - %(funcName)s] %(message)s"
logging.basicConfig(format=FORMAT)
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.propagate = False

# Process reporting arguments
botArguments = parser.ScrapingArguments()
# Allign screen and get ready
windowManager = window.ScreenManager(botArguments)

if __name__ == "__main__":
    # Begin the mining bot, if we detect someone holding 'X' during runtime, return 
    # TODO: Technically this function waits until the end of runtime before testing to see if someone is holding x down
    if botArguments.botAction.action == 'woodcutting':
        while keyboard.is_pressed('x') == False:
            logger.info("Beginning Run")
            windowManager.begin_woodcutting_run()