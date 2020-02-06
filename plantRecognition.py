import cv2
import numpy as np

def printValues(event, x, y, flags, param):
	global mouseX, mouseY;
	if event == cv2.EVENT_LBUTTONDBLCLK:
		print(f"x: {x} y: {y}");
		vals = hsv[y,x];
		print(f"vals:{vals}")


capSource = cv2.VideoCapture('GX030003.MP4');
ret, inputImage = capSource.read();
screen_res = 1920, 1080;

width = screen_res[0] / inputImage.shape[1];
height = screen_res[1] / inputImage.shape[0];
scale = min(width, height);

newWidth = int(inputImage.shape[1] * scale);
newHeight = int(inputImage.shape[0] * scale);

cv2.namedWindow('Display', cv2.WINDOW_NORMAL);

cv2.resizeWindow('Display', newWidth, newHeight);

#capSource.set(cv2.CAP_PROP_FPS, 30);
print(capSource.get(cv2.CAP_PROP_FRAME_COUNT));
capSource.set(cv2.CAP_PROP_BUFFERSIZE, 5);
count = 0;
while(capSource.isOpened()):
	ret, inputImage = capSource.read();

	if ret:
		hsv = cv2.cvtColor(inputImage, cv2.COLOR_BGR2HSV);

		lowerPurple = np.array([75, 0, 90]);
		#upperPurple = np.array([200, 120, 256]);
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
	if cv2.waitKey(2) == 'q':
		break;

cv2.destroyAllWindows();
capSource.release();


