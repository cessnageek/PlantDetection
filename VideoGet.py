from threading import Thread
import cv2

class VideoGet:

	def __init__(self, src):
		self.stream = cv2.VideoCapture(src);
		self.grabbed, self.frame = self.stream.read();
		self.width = int(self.stream.get(cv2.CAP_PROP_FRAME_WIDTH));
		self.height = int(self.stream.get(cv2.CAP_PROP_FRAME_HEIGHT));
		self.stopped = False;

	def start(self):
		Thread(target=self.get, args=()).start();
		self.grabbed, self.frame = self.stream.read();
		self.isOpened = self.stream.isOpened();
		return self;

	def get(self):
		while not self.stopped:
			self.grabbed, self.frame = self.stream.read();

	def stop(self):
		self.stream.release();
		self.stopped = True;