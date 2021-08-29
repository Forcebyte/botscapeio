from PIL import ImageGrab
import cv2
import numpy
import pyautogui

class TreeManager():
    def __init__(self, rs_screenshot):
        self.rs_screenshot = rs_screenshot
        cv2.imshow('RsBot', cv2.cvtColor(numpy.array(self.rs_screenshot), cv2.COLOR_BGR2RGB))

    def preallocate_trees(self):
        tree_array = []
        # Convert image to wireframe (faster processing)
        raw_rs_screenshot = numpy.array(self.rs_screenshot)
        bw_screenshot = cv2.cvtColor(raw_rs_screenshot, cv2.COLOR_BGR2GRAY)
        wireframe_screenshot = cv2.Canny(bw_screenshot, 300, 80)

        # Clean up wieframe to be similar to contours (outlines of specific objects in a top-down scenario)
        # Humbly taken from MuneebAnsari
        kernel = numpy.ones((3, 3), numpy.uint8)
        rs_gradient = cv2.morphologyEx(wireframe_screenshot, cv2.MORPH_GRADIENT, kernel)

        # Obtain a frame where any small holes inside the foreground objects are closed using MORPH_CLOSE
        closed = cv2.morphologyEx(rs_gradient, cv2.MORPH_CLOSE, numpy.ones((10, 10), numpy.uint8))
        thresh = cv2.adaptiveThreshold(closed, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)

        # Use RETR_TREE to get contours' parent-child relationships within hierarchy
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # For each object (shape) within the screenshot, loop and determine if the item is a tree
        for item in zip(contours, hierarchy[0]):
            tree_coords = None
            c, h = item[0], item[1]
            # h[2] is the children of contour (negative then inner contour)
            # h[3] is the parents of contour  (negative that external contour)
            rectangle = cv2.boundingRect(c)
            x, y, width, length = rectangle

            if cv2.contourArea(c) > 500 and h[2] == -1:
                poly = cv2.approxPolyDP(c, 0.01 * cv2.arcLength(c, True), True)
                # Arbitrary
                if len(poly) > 15:
                    tree_coords = self.fetch_tree_coord(raw_rs_screenshot, rectangle, x, y, width, length)
            if tree_coords:
                tree_array.append(tree_coords)
        return(tree_array)

    @staticmethod
    def fetch_tree_coord(raw_rs_screenshot, rect, x, y, width, length):
        # With the tree polynomial object, fetch the center of the tree and return it back
        if rect[2] < 60 and rect[3] < 60:
            cv2.rectangle(raw_rs_screenshot, (x - 10, y - 30), (x + width + 15, y + length), (0, 255, 0), 2)
            cv2.putText(raw_rs_screenshot, 'Tree', (x + width // 2, y + length // 2), 0, 0.4, (255, 255, 0))

        elif rect[2] < 100 and rect[3] < 100:
            cv2.rectangle(raw_rs_screenshot, (x, y), (x + width, y + length), (0, 255, 0), 2)
            cv2.putText(raw_rs_screenshot, 'Tree', (x + width // 2, y + length // 2), 0, 0.4, (255, 255, 0))

        x, y = pyautogui.center(rect)
        return(x, y)
