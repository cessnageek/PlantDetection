import cv2
import numpy as np
from imutils.video import FPS
from VideoGet import VideoGet
from VideoWrite import VideoWrite
#from threading import threading
#import sys
#from queue import Queue

def printValues(event, x, y, flags, param):
	global mouseX, mouseY;
	if event == cv2.EVENT_LBUTTONDBLCLK:
		print(f"x: {x} y: {y}");
		vals = hsv[y,x];
		print(f"vals:{vals}")


#capSource = cv2.VideoCapture('GX040003.MP4');
#ret, inputImage = capSource.read();

capSource = VideoGet('GX030003.MP4').start();
inputImage = capSource.frame;

screen_res = 1920, 1080;

width = screen_res[0] / inputImage.shape[1];
height = screen_res[1] / inputImage.shape[0];
scale = min(width, height);

newWidth = int(inputImage.shape[1] * scale);
newHeight = int(inputImage.shape[0] * scale);

cv2.namedWindow('Display', cv2.WINDOW_NORMAL);

cv2.resizeWindow('Display', newWidth, newHeight);

#capSource.set(cv2.CAP_PROP_FPS, 30);
#print(capSource.get(cv2.CAP_PROP_FRAME_COUNT));
#capSource.set(cv2.CAP_PROP_BUFFERSIZE, 5);

fourcc = cv2.VideoWriter_fourcc(*"MJPG");
path = 'C:\\Users\\cessn\\Documents\\PlantDetection\\outputVid40003.avi';

#outWidth = int(capSource.get(cv2.CAP_PROP_FRAME_WIDTH));
#outHeight = int(capSource.get(cv2.CAP_PROP_FRAME_HEIGHT));
outWidth = capSource.width;
outHeight = capSource.height;

combined = inputImage;

outputVideo = VideoWrite(fourcc, path, outWidth, outHeight, combined);

#outputVideo = cv2.VideoWriter(path, fourcc, 30, (outWidth, outHeight), True);


count = 0;
fps = FPS().start();

while(capSource.isOpened):
	#ret, inputImage = capSource.read();
	inputImage = capSource.frame;

	if capSource.grabbed:
		hsv = cv2.cvtColor(inputImage, cv2.COLOR_BGR2HSV);

		lowerPurple = np.array([75, 0, 90]);
		upperPurple = np.array([200, 50, 256]);

		lowerRed = np.array([0, 0, 140]);
		upperRed = np.array([50, 20, 255]);

		lowerLightPurple = np.array([95, 50, 130]);
		upperLightPurple = np.array([115, 125, 230]);

		maskPurple = cv2.inRange(hsv, lowerPurple, upperPurple);
		maskRed = cv2.inRange(hsv, lowerRed, upperRed);
		maskLightPurple = cv2.inRange(hsv, lowerLightPurple, upperLightPurple);
		maskTotal = cv2.bitwise_or(maskPurple, maskRed);
		maskTotal = cv2.bitwise_or(maskTotal, maskLightPurple);
		maskTotal = cv2.bitwise_not(maskTotal);

		kernelOpen = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(10,10));
		opened = cv2.morphologyEx(maskTotal, cv2.MORPH_OPEN, kernelOpen);

		combined = cv2.bitwise_and(inputImage, inputImage, mask = opened);
		cv2.imshow('Display', combined);
		print(count);
		count = count + 1;
		fps.update();

		#outputVideo.write(combined);
		outputVideo.frame = combined;

	if (cv2.waitKey(2) & 0XFF) == ord('q') or capSource.stopped:
		capSource.stop();
		outputVideo.stop();
		break;
fps.stop()
print("Elapsed time: {:.2f}".format(fps.elapsed()));
print("Approx FPS: {:.2f}".format(fps.fps()));

cv2.destroyAllWindows();
#capSource.release();
#outputVideo.release();


