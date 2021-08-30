# Base Windows manager
from utils import tree
import pyautogui
import logging
import random
import cv2
from time import sleep
logger = logging.getLogger()
logger.setLevel(logging.INFO)

class ScreenManager():
    def __init__(self, botArguments):
        # Fetch botAction requested
        self.botAction = botArguments.botAction
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
        except IndexError as err:
            raise pyautogui.FailSafeException(f"Unable to locate 'Old School Runescape' window  err {err}, ensure that OSRS is running")
        logger.debug(f"height={rs_window.height}, 'width={rs_window.width}")
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
            sleep(3)
            logger.debug("Taking screenshot")
            rs_screenshot = pyautogui.screenshot(
                region=(self.rs_window.left, self.rs_window.top, self.rs_window.width, self.rs_window.height)
            )
            logger.info("Beginning run")
            treeManager = tree.TreeManager(rs_screenshot)
            tree_coordinate_list = treeManager.preallocate_trees()

            tree_coord = random.choice(tree_coordinate_list)
            max_variance = 3 # dictates the random x/y coordinate where we click on the tree (just in case botting detects thsi)
            clicks = random.randint(1,2)
            x_dir, y_dir = (random.randint(1,max_variance) + tree_coord[0]), (random.randint(1,max_variance) + tree_coord[1])
            if clicks > 1:
                pyautogui.click(
                    clicks=clicks,
                    x=x_dir,
                    y=y_dir,
                    interval=random.uniform(0.10, 0.25)
                )
            else:
                pyautogui.click(
                    clicks=clicks,
                    x=x_dir,
                    y=y_dir,
                )
            inventory_not_full = treeManager.clean_inventory()
