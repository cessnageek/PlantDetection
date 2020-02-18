from threading import Thread
import cv2

class VideoWrite:

	#path = 'C:\\Users\\cessn\\Documents\\PlantDetection\\outputVid40003.avi';

	def __init__(self, fourcc, output, width, height, origFrame):
		self.outputVideo = cv2.VideoWriter(output, fourcc, 30, (width, height), True);
		self.stopped = False;
		self.frame = origFrame;


	def start(self):
		Thread(target=self.put, args=()).start();

	def put(self):
		while not self.stopped:
			self.outputVideo.write(self.frame);

	def stop(self):
		self.outputVideo.release();
		self.stopped = True;


