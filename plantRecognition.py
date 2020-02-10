import cv2
import numpy as np

def printValues(event, x, y, flags, param):
	global mouseX, mouseY;
	if event == cv2.EVENT_LBUTTONDBLCLK:
		print(f"x: {x} y: {y}");
		vals = hsv[y,x];
		print(f"vals:{vals}")

# Get input image from file
inputImage = cv2.imread('new_tworow.png');

screen_res = 1920, 1080;

# Get rescale value
width = screen_res[0] / inputImage.shape[1];
height = screen_res[1] / inputImage.shape[0];

scale = min(width, height);

newWidth = int(inputImage.shape[1] * scale);
newHeight = int(inputImage.shape[0] * scale);

cv2.namedWindow('Display', cv2.WINDOW_NORMAL);

cv2.resizeWindow('Display', newWidth, newHeight);

cv2.imshow('Display', inputImage);
cv2.waitKey(0);

# Convert to HSV
hsv = cv2.cvtColor(inputImage, cv2.COLOR_BGR2HSV);
cv2.imshow('Display', hsv);

# Create bounds 
lowerPurple = np.array([75, 0, 90]);
upperPurple = np.array([200, 50, 256]);

lowerRed = np.array([0, 0, 140]);
upperRed = np.array([50, 20, 255]);

lowerLightPurple = np.array([95, 50, 130]);
upperLightPurple = np.array([115, 125, 230]);

# Sets the callback for clicking.  Displays values from HSV image
cv2.setMouseCallback('Display', printValues);

cv2.imshow('Display', hsv);
cv2.waitKey(0);

# Masks using the bounds
maskPurple = cv2.inRange(hsv, lowerPurple, upperPurple);
maskRed = cv2.inRange(hsv, lowerRed, upperRed);
maskLightPurple = cv2.inRange(hsv, lowerLightPurple, upperLightPurple);

# Add up the masks
maskTotal = cv2.bitwise_or(maskPurple, maskRed);
maskTotal = cv2.bitwise_or(maskTotal, maskLightPurple);

# Invert the mask
maskTotal = cv2.bitwise_not(maskTotal);
cv2.imshow('Display', maskTotal);
cv2.waitKey(0);

# Create opening kernel and implement it
kernelOpen = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(10,10));
opened = cv2.morphologyEx(maskTotal, cv2.MORPH_OPEN, kernelOpen);
cv2.imshow('Display', opened);
cv2.waitKey(0);

# Overlay back on RGB image
combined = cv2.bitwise_and(inputImage, inputImage, mask = opened);
cv2.imshow('Display', combined);
cv2.waitKey(0);

cv2.destroyAllWindows();


