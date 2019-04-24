import numpy as np
import cv2
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons
import time

class CameraVisionTest:
#Make sure camera is 22 cm away from center of board
    def __init__(self):
        start = time.time()
        self.oldCam = cv2.VideoCapture(0)
        self.newCam = cv2.VideoCapture(1)
        self.blueMaskLower = np.array([90, 90, 0])
        self.blueMaskUpper = np.array([120, 255, 255])
        self.yellowMaskLower = np.array([20, 147, 132])
        self.yellowMaskUpper = np.array([100, 255, 255])
        self.redMaskLower = np.array([0, 0, 200])
        self.redMaskUpper = np.array([20, 255, 255])
        self.row_size = 59
        self.column_size = 65
        self.name = ''
        isCamera = False
        isChip = False
        while not isCamera:
            # camera = input('Choose a camera number [0 - Webcam, 1 - Connected Camera]:\n')
            camera = 1
            if camera < 0 or camera > 1:
                print('%d is not a valid camera, please enter a new number'.format(camera))
                continue
            else:
                self.webcam = cv2.VideoCapture(camera)
                isCamera = True
        while not isChip:
            # color = input('What chip color is the Player [0 - Red, 1 - Yellow]:\n')
            color = 0
            if color < 0 or color > 1:
                print('%d is currently not a valid chip, please choose a valid value')
                continue
            else:
                self.playColor = color
                isChip = True
        end = time.time()
        print(end - start)

    def test_run(self):
        isPass = False
        while isPass == False:
            camera = input('Choose a camera number [0 - Webcam, 1 - Connected Camera]:\n')
            if camera < 0 or camera > 1:
                print('%d is not a valid camera, please enter a new number'.format(camera))
                continue
            color = input('Pick a color to mask for [0 - Blue, 1 - Red, 2 - Yellow]:\n')
            if color < 0 or color > 2:
                print('%d is currently not supported, please choose a valid color')
                continue
            else:
                self.cam = camera
                isPass = True
        webcam = cv2.VideoCapture(self.cam)
        while True:
            _, img = webcam.read()
            #cv2.imshow('test', img)
            if color == 0:
                image_arr = self.maskFor(img, self.blueMaskLower, self.blueMaskUpper)
            elif color == 1:
                image_arr = self.maskFor(img, self.redMaskLower, self.redMaskUpper)
            elif color == 2:
                image_arr = self.maskFor(img, self.yellowMaskLower, self.yellowMaskUpper)
            else:
                break
            cv2.imshow('Original', image_arr[0])
            cv2.imshow('Masked', image_arr[1])
            cv2.imshow('Threshold', image_arr[2])
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        webcam.release()
        cv2.destroyAllWindows()

    def maskFor(self, image, lowerLimit, upperLimit):
        img_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(img_hsv, lowerLimit, upperLimit)
        img_masked = cv2.bitwise_and(image, image, mask=mask)
        img_grey = cv2.cvtColor(cv2.cvtColor(img_masked, cv2.COLOR_HSV2BGR), cv2.COLOR_BGR2GRAY)
        img_grey = cv2.medianBlur(img_grey, 7)
        img_thresh = cv2.threshold(img_grey, 0, 255, cv2.THRESH_BINARY)[1]
        imgArr = [image, img_masked, img_thresh]
        return imgArr

    def locate_chips(self, original_image, threshold_image, isPlayer):
        '''
        This function uses the binary threshold image to identify centroids of chips
        :param original_image: BGR image of Connect Four board
        :param threshold_image: BW threshold image after masking functions
        :param isPlayer: Boolean dictating whether the player tokens are "seen"
        :return: coords: An array of Tuples representing the identified XY coordinates
        '''
        contours, hierarchy = cv2.findContours(threshold_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        coords = []
        if not contours:
            print("No chips detected")
        else:
            for c in contours:
                # Disregard small errors in masking
                if cv2.contourArea(c) > 150:
                    # calculate moments for each contour
                    M = cv2.moments(c)
                    # calculate x,y coordinate of center
                    cX = int(M["m10"] / M["m00"])
                    cY = int(M["m01"] / M["m00"])
                    # If the detected centroid lies outside the game board, disregard it
                    if cX < 100 or cX > 520:
                        continue
                    elif cY < 100 or cY > 400:
                        continue
                    else:
                        # Visual cue to alert user what the program actually "sees"
                        cv2.circle(original_image, (cX, cY), 5, (255, 255, 255), -1)
                        if isPlayer:
                            cv2.putText(original_image, "Player", (cX - 25, cY - 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
                        else:
                            cv2.putText(original_image, "ABB", (cX - 25, cY - 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
                        coord = (cX, cY)
                        coords.append(coord)
        return coords

    def cvtLocation(self, pxArr, gameboard, isPlayer):
        '''
        Function to convert the locations of chip centroids in pixels to locations within the supplied game board
        :param pxArr: Array of tuples
        :param gameboard: 6x7 Array
        :param isPlayer: Boolean stating if centroids are player chips
        :return: gameboard modified with appropriate values
        '''
        # Convert each pixel value to an single digit value
        # by dividing each by an average column or row separation value
        for px in pxArr:
            col = px[0] / self.column_size
            row = px[1] / self.row_size
            if isPlayer:
                gameboard[row - 1, col - 1] = 2
            else:
                gameboard[row - 1, col - 1] = 1
        return gameboard

    def run(self):
        '''
        Main script to analyze gameboard
        Will take a single picture of connect four board and populate array with
        0 - Free space
        1 - Robot chip
        2 - Player chip
        :return: gameboard Array of 0,1,&2
        '''
        start = time.time()

        # Instantiate 2D array
        game_board = np.zeros((6, 7))

        # Grab the last of 20 pictures of the board
        # This ensures that the camera obtains a full, clear image of the board
        # Less than 20 frames results in a dark frame which is not able to be processed correctly
        i = 0
        while i < 20:
            _, img = self.webcam.read()
            i = i + 1

        # mask for player chips based on user chip selection
        if self.playColor == 0:
            playArr = self.maskFor(img, self.redMaskLower, self.redMaskUpper)
        else:
            playArr = self.maskFor(img, self.yellowMaskLower, self.yellowMaskUpper)
        playerCoord = self.locate_chips(img, playArr[2], True)

        # mask for robot chips based on user chip selection
        if self.playColor == 0:
            abbArr = self.maskFor(img, self.yellowMaskLower, self.yellowMaskUpper)
        else:
            abbArr = self.maskFor(img, self.redMaskLower, self.redMaskUpper)
        abbCoord = self.locate_chips(img, abbArr[2], False)
        print playerCoord
        print abbCoord
        # Display the original and masked images for visual inspection of results
        cv2.imshow('Original', img)
        cv2.imshow('Player', playArr[2])
        cv2.imshow('ABB', abbArr[2])
        # uncomment to enable the user to manually send the grid after inspecting the images
        # cv2.waitKey()
        game_board = self.cvtLocation(playerCoord, game_board, True)
        game_board = self.cvtLocation(abbCoord, game_board, False)

        # Display run time of current script
        end = time.time()
        print("runtime: ")
        print(end - start)
        return game_board

    def abort(self):
        self.webcam.release()
        cv2.destroyAllWindows()


if __name__ == '__main__':
    cvt = CameraVisionTest()
    # cvt.test_run()
    print('Program is ready')
    command = raw_input("Analyze board? (y/n))\n")
    isDone = False
    while not isDone:
        if str(command) == str("y"):
            while True:
                result = cvt.run()
                print result
                command = raw_input("Analyze board? (y/n)\n")
                if str(command) == str("y"):
                    continue
                elif str(command) == str("n"):
                    print('Exiting Program')
                    break
            isDone = True
        elif str(command) == str("n"):
            print('Aborting program')
            isDone = True
        else:
            print('Not a valid input.  Try again \n')
            continue
    cvt.abort()