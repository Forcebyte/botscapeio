# Base Windows manager

import pyautogui
import logging
import PIL
import tensorflow as tf
import pathlib
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.models import Sequential

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
        data_dir = tf.keras.utils.get_file('copper', origin='https://github.com/Forcebyte/crappy-runescape-bot/raw/develop/rocks/copper.tar.gz', untar=True)
        data_dir = pathlib.Path(data_dir)
        batch_size = 32
        img_height = 180
        img_width = 180
        train_ds = tf.keras.preprocessing.image_dataset_from_directory(
            data_dir,
            validation_split=0.2,
            subset="training",
            seed=123,
            image_size=(img_height, img_width),
            batch_size=batch_size
        )
        val_ds = tf.keras.preprocessing.image_dataset_from_directory(
            data_dir,
            validation_split=0.2,
            subset="validation",
            seed=123,
            image_size=(img_height, img_width),
            batch_size=batch_size
        )
        normalization_layer = layers.experimental.preprocessing.Rescaling(1./255)
        model = Sequential([
            layers.experimental.preprocessing.Rescaling(1./255, input_shape=(img_height, img_width, 3)),
            layers.Conv2D(16, 3, padding='same', activation='relu'),
            layers.MaxPooling2D(),
            layers.Conv2D(32, 3, padding='same', activation='relu'),
            layers.MaxPooling2D(),
            layers.Conv2D(64, 3, padding='same', activation='relu'),
            layers.MaxPooling2D(),
            layers.Flatten(),
            layers.Dense(128, activation='relu'),
            layers.Dense(5)
        ])
        model.compile(optimizer='adam',
              loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
              metrics=['accuracy'])
        model.summary()
