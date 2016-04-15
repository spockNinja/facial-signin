import numpy
import stasm
from math import pow, sqrt
import json

class FaceInfo(object):
	
	#threshold used to tune recognition
	variance = 0.02
	
	def __init__(self):
		self._info = {}
		#setting these to 0 keeps comparisons from woroking when the object has no actual face data in it.
		self._info['eye_width'] = 0.0
		self._info['nose_width'] = 0.0
		self._info['face_width'] = 0.0
		self._info['face_height'] = 0.0
		self._info['upper_lip_height'] = 0.0
		self._info['upper_lip_thickness'] = 0.0
		self._info['lower_lip_thickness'] = 0.0
	
	def generateInfoFromStasm(self, stasmLandmarks):
		#get eye distance as a reference distance, and landmark 0 as a reference point
		eyeDistance = sqrt(pow(stasmLandmarks[30][0] - stasmLandmarks[40][0], 2) - Math.pow(stasmLandmarks[30][1]-stasmLandmarks[40][1]))
		reference = numpy.array([-stasmLandmarks[0][0], -stasmLandmarks[0][1]])
		for point in stasmLandmarks:
			point = point.add(reference)
		#generate a dictionary of measurements to use for face determination
		self._info['eye_width'] = sqrt(pow(stasmLandmarks[30][0] - stasmLandmarks[34][0], 2) - Math.pow(stasmLandmarks[30][1]-stasmLandmarks[34][1]))/ eyeDistance
		self._info['nose_width'] = sqrt(pow(stasmLandmarks[58][0] - stasmLandmarks[54][0], 2) - Math.pow(stasmLandmarks[58][1]-stasmLandmarks[54][1]))/ eyeDistance
		self._info['face_width'] = sqrt(pow(stasmLandmarks[1][0] - stasmLandmarks[11][0], 2) - Math.pow(stasmLandmarks[1][1]-stasmLandmarks[11][1]))/ eyeDistance
		self._info['face_height'] = sqrt(pow(stasmLandmarks[14][0] - stasmLandmarks[6][0], 2) - Math.pow(stasmLandmarks[14][1]-stasmLandmarks[6][1]))/ eyeDistance
		self._info['upper_lip_height'] = sqrt(pow(stasmLandmarks[56][0] - stasmLandmarks[62][0], 2) - Math.pow(stasmLandmarks[56][1]-stasmLandmarks[62][1]))/ eyeDistance
		self._info['upper_lip_thickness'] = sqrt(pow(stasmLandmarks[62][0] - stasmLandmarks[67][0], 2) - Math.pow(stasmLandmarks[62][1]-stasmLandmarks[67][1]))/ eyeDistance
		self._info['lower_lip_thickness'] = sqrt(pow(stasmLandmarks[70][0] - stasmLandmarks[74][0], 2) - Math.pow(stasmLandmarks[70][1]-stasmLandmarks[74][1]))/ eyeDistance
		
	def generateInfoFromJson(self, jsonstring):
		self._info = json.loads(jsonstring)
		
	def getJsonString(self):
		return json.dumps(self._info)
	
	def getInfo(self):
		return self._info
	

		
	
	def isSamePerson(self, other):
		#compare every value in info against other
		failedSimilarityTest = False
		for key in self._info.keys:
			if not (self._info[key] * (1-self.variance) < other._info[key] < self._info[key] * (1+self.variance)):
				failedSimilarityTest = True
				break
		return not failedSimilarityTest
	
	