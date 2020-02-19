#Background filtering the photos
import cv2
import numpy as np

def printValues(event, x, y, flags, param):
	global mouseX, mouseY;
	if event == cv2.EVENT_LBUTTONDBLCLK:
		print(f"x: {x} y: {y}");
		vals = hsv[y,x];
		print(f"vals:{vals}")


inputImage = cv2.imread('new_tworow.png');

screen_res = 1920, 1080;

width = screen_res[0] / inputImage.shape[1];
height = screen_res[1] / inputImage.shape[0];

scale = min(width, height);

newWidth = int(inputImage.shape[1] * scale);
newHeight = int(inputImage.shape[0] * scale);

cv2.namedWindow('Display', cv2.WINDOW_NORMAL);

cv2.resizeWindow('Display', newWidth, newHeight);

cv2.imshow('Display', inputImage);
#cv2.waitKey(0);

hsv = cv2.cvtColor(inputImage, cv2.COLOR_BGR2HSV);
cv2.imshow('Display', hsv);

lowerPurple = np.array([75, 0, 90]);
#upperPurple = np.array([200, 120, 256]);
upperPurple = np.array([200, 50, 256]);

lowerRed = np.array([0, 0, 140]);
upperRed = np.array([50, 20, 255]);

lowerLightPurple = np.array([95, 50, 130]);
upperLightPurple = np.array([115, 125, 230]);

cv2.setMouseCallback('Display', printValues);

cv2.imshow('Display', hsv);
#cv2.waitKey(0);

maskPurple = cv2.inRange(hsv, lowerPurple, upperPurple);
maskRed = cv2.inRange(hsv, lowerRed, upperRed);
maskLightPurple = cv2.inRange(hsv, lowerLightPurple, upperLightPurple);
maskTotal = cv2.bitwise_or(maskPurple, maskRed);
maskTotal = cv2.bitwise_or(maskTotal, maskLightPurple);
maskTotal = cv2.bitwise_not(maskTotal);
cv2.imshow('Display', maskTotal);
#cv2.waitKey(0);

#kernelClose = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(10,10));
#opened = cv2.morphologyEx(maskTotal, cv2.MORPH_OPEN, kernelClose);
#kernelErode = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (30, 30));
kernelErode = cv2.getStructuringElement(cv2.MORPH_RECT, (37,5));
eroded = cv2.morphologyEx(maskTotal, cv2.MORPH_ERODE, kernelErode);
kernelDilate = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (20, 10));
dilated = cv2.morphologyEx(eroded, cv2.MORPH_DILATE, kernelDilate);
cv2.imshow('Display', dilated);
#cv2.imshow('Display', opened);
#cv2.waitKey(0);

combined = cv2.bitwise_and(inputImage, inputImage, mask = dilated);
cv2.imshow('Display', combined);
cv2.waitKey(0);


#Canny works with greyscale
combined = cv2.cvtColor(combined, cv2.COLOR_HSV2BGR);
combined = cv2.cvtColor(combined, cv2.COLOR_BGR2GRAY);

#for i in range(0,10):
#	minVal = int(input("input minval: "));
#	maxVal = int(input("input maxval: "));
edges = cv2.Canny(combined,175,300);

#finds contours and draws them on the image
contours, hierarchy = cv2.findContours(edges,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE);
img = cv2.drawContours(edges, contours, -1, (255,255,0), 3);

print("Number of Contours found = " + str(len(contours)));

cv2.imshow('Display',img);
cv2.waitKey(0);

#runs a closing operation to close up heads
kernelDilate = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (30, 30));
dilated = cv2.morphologyEx(img, cv2.MORPH_DILATE, kernelDilate);
kernelErode = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (30, 30));
eroded = cv2.morphologyEx(dilated, cv2.MORPH_ERODE, kernelErode);

cv2.imshow('Display',eroded);
cv2.waitKey(0);

cv2.destroyAllWindows();
