# Base Windows manager
from utils import tree
import pyautogui
import logging
import random
from time import sleep
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
        confirmation = pyautogui.confirm(text=text,title="Confirmation", buttons=['OK', 'Cancel'])
        while confirmation != 'OK':
            if confirmation == 'Cancel':
                logger.warning("Cancel detected, exiting")
                exit(0)
            else:
                pass

    def preallocate_runescape_window(self):
        try:
            rs_window = pyautogui.getWindowsWithTitle("Old School RuneScape")[0]
            print(rs_window)
        except IndexError as err:
            raise pyautogui.FailSafeException("Unable to locate 'Old School Runescape' window, ensure that OSRS is running")
        print(f"height={rs_window.height}, 'width={rs_window.width}")
        # Reset height and width to simple values
        logger.info("Setting default Height and Width of OSRS window...")
        rs_window.width=1065
        rs_window.height=843
        return rs_window

    def begin_woodcutting_run(self):
        self.__auto_prompt(text="Confirm that you are ready to begin treecutting")
        # First, take a capture of the underlying rs_window (coordinates fetched from preallocate_Runescape_window)
        inventory_not_full = True
        while inventory_not_full:
            sleep(5)
            logger.info("Taking screenshot")
            rs_screenshot = pyautogui.screenshot(
                region=(self.rs_window.left, self.rs_window.top, self.rs_window.width, self.rs_window.height)
            )
            logger.info("Beginning run")
            treeManager = tree.TreeManager(rs_screenshot)
            tree_coordinate_list = treeManager.preallocate_trees()
            for tree_coord in tree_coordinate_list:
                clicks = random.randint(1,2)
                if clicks > 1:
                    pyautogui.click(
                        clicks=clicks,
                        x=(tree_coord[0] + (random.randint(1,30))), 
                        y=(tree_coord[1] + (random.randint(1,30))),
                        interval=random.uniform(0.10, 0.25)
                    )
                else:
                    pyautogui.click(
                        clicks=clicks,
                        x=(tree_coord[0] + (random.randint(1,30))), 
                        y=(tree_coord[1] + (random.randint(1,30))),
                    )
                break