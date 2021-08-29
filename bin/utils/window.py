# Base Windows manager

import pyautogui
import logging
import PIL
import tensorflow as tf


logger = logging.getLogger()
logger.setLevel(logging.INFO)

class ScreenManager():
    def __init__(self, botArguments):
        # Fetch botAction requested
        self.botAction = botArguments.botAction
        # Fetch the dimenisons of the screen that we're runing in, along with current position of the mouse
        screen_width, screen_height = pyautogui.size()
        coords = pyautogui.position()
        mouseCoords = {
            'x': coords[0],
            'y': coords[1]
        }
        # Confirm that runescape window is focused before running commands
        self.__auto_prompt(text="Confirm that Runescape Window is focused")
        self.rs_window = self.preallocate_runescape_window()

    @staticmethod
    def __test_mouse_sampling():
        distance = 200
        while distance > 0:
            pyautogui.drag(distance, 0, duration=0.5)   # move right
            distance -= 5
            pyautogui.drag(0, distance, duration=0.5)   # move down
            pyautogui.drag(-distance, 0, duration=0.5)  # move left
            distance -= 5
            pyautogui.drag(0, -distance, duration=0.5)  # move up

    @staticmethod
    def __auto_prompt(text):
        while pyautogui.confirm(text=text,title="Confirmation", buttons=['OK', 'Cancel']) != 'OK':
            pass

    def preallocate_runescape_window(self):
        try:
            rs_window = pyautogui.getWindowsWithTitle("Old School RuneScape")[0]
        except IndexError as err:
            raise pyautogui.FailSafeException("Unable to locate 'Old School Runescape' window, ensure that OSRS is running")
        print(f"height={rs_window.height}, 'width={rs_window.width}")
        # Reset height and width to simple values
        logger.info("Setting default Height and Width of OSRS window...")
        rs_window.width=1065
        rs_window.height=843
        return rs_window

    def begin_mining_run(self):
        self.__auto_prompt(text="Insert a screenshot of the ore you are looking to ")
        # Fetch all screenshots of copper
        tf.keras.utils.get_file
        train_ds = tf.keras.preprocessing.image_dataset_from_directory(
            
        )