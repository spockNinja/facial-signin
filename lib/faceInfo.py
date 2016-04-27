from math import pow, sqrt
import simplejson as json


class FaceInfo(object):

    # threshold used to tune recognition
    variance = 0.02

    def __init__(self):
        self._info = {}
        # setting these to 0 keeps comparisons from working
        # when the object has no actual face data in it.
        self._info['eye_width'] = 0.0
        self._info['nose_width'] = 0.0
        self._info['face_width'] = 0.0
        self._info['face_height'] = 0.0
        self._info['upper_lip_height'] = 0.0
        self._info['upper_lip_thickness'] = 0.0
        self._info['lower_lip_thickness'] = 0.0

    def _dist(self, p1, p2):
        return sqrt(pow(p1[0]-p2[0], 2) + pow(p1[1]-p2[1], 2))

    def generateInfoFromStasm(self, landmarks):
        # get eye distance as a reference distance,
        # and landmark 0 as a reference point
        eye_dist = self._dist(landmarks[30], landmarks[40])

        # generate a dictionary of measurements to use for face determination
        self._info['eye_width'] = self._dist(landmarks[30], landmarks[34]) / eye_dist
        self._info['nose_width'] = self._dist(landmarks[58], landmarks[54]) / eye_dist
        self._info['face_width'] = self._dist(landmarks[1], landmarks[11]) / eye_dist
        self._info['face_height'] = self._dist(landmarks[14], landmarks[6]) / eye_dist
        self._info['upper_lip_height'] = self._dist(landmarks[56], landmarks[62]) / eye_dist
        self._info['upper_lip_thickness'] = self._dist(landmarks[62], landmarks[67]) / eye_dist
        self._info['lower_lip_thickness'] = self._dist(landmarks[70], landmarks[74]) / eye_dist

    def generateInfoFromJson(self, jsonstring):
        self._info = json.loads(jsonstring)

    def getJsonString(self):
        return json.dumps(self._info)

    def getInfo(self):
        return self._info

    def isSamePerson(self, other):
        # compare every value in info against other
        failedSimilarityTest = False
        for key in self._info.keys:
            if not (self._info[key] * (1-self.variance) < other._info[key] < self._info[key] * (1+self.variance)):
                failedSimilarityTest = True
                break
        return not failedSimilarityTest
