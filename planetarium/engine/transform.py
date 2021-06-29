import math
import numpy

from .window import *

def homogenize (mat):
	return numpy.vstack ((mat, numpy.ones (mat.shape [1])))

def inhomogenize (mat):
	return mat [:-1]
	
def getTranslMat (translVec):	
	return numpy.matrix ([
		[1, 0, 0, translVec [0]],
		[0, 1, 0, translVec [1]],
		[0, 0, 1, translVec [2]],
		[0, 0, 0, 1],
	], dtype = typesNp [typesGen ['coordinate']])

def getScalMat (scalVec):
	return numpy.matrix ([
		[scalVec [0], 0, 0, 0],
		[0, scalVec [1], 0, 0],
		[0, 0, scalVec [2], 0],
		[0, 0, 0, 1],
	], dtype = typesNp [typesGen ['coordinate']])

def getRotXMat (angle):
	c = math.cos (angle)
	s = math.sin (angle)
	return numpy.matrix ([
		[1, 0, 0, 0],
		[0, c, -s, 0],
		[0, s, c, 0],
		[0, 0, 0, 1]
	], dtype = typesNp [typesGen ['coordinate']])

def getRotYMat (angle):
	c = math.cos (angle)
	s = math.sin (angle)
	return numpy.matrix ([
		[c, 0, s, 0],
		[0, 1, 0, 0],
		[-s, 0, c, 0],
		[0, 0, 0, 1]
	], dtype = typesNp [typesGen ['coordinate']])

def getRotZMat (angle):
	c = math.cos (angle)
	s = math.sin (angle)
	return numpy.matrix ([
		[c, -s, 0, 0],
		[s, c, 0, 0],
		[0, 0, 1, 0],
		[0, 0, 0, 1]
	], dtype = typesNp [typesGen ['coordinate']])
	
def getRotXYZMat (angleVec):	# Z rotation first
	return (
		getRotXMat (angleVec [2]) *
		getRotYMat (angleVec [1]) *
		getRotzMat (angleVec [0])
	)

def getRotXZYMat (angleVec):
	return (
		getRotXMat (angleVec [2]) *
		getRotZMat (angleVec [1]) *
		getRotYMat (angleVec [0])
	)

def getRotYXZMat (angleVec):
	return (
		getRotYMat (angleVec [2]) *
		getRotXMat (angleVec [1]) *
		getRotZMat (angleVec [0])
	)

def getRotYZXMat (angleVec):
	return (
		getRotYMat (angleVec [2]) *
		getRotZMat (angleVec [1]) *
		getRotXMat (angleVec [0])
	)

def getRotZXYMat (angleVec):
	return (
		getRotZMat (angleVec [2]) *
		getRotXMat (angleVec [1]) *
		getRotYMat (angleVec [0])
	)

def getRotZYXMat (angleVec):
	return (
		getRotZMat (angleVec [2]) *
		getRotYMat (angleVec [1]) *
		getRotXMat (angleVec [0])
	)

def getPerspMat (fieldOfViewY, aspectRatio, zNearFarVec):	# Camera at (0, 0, 0), looking at (0, 0, -1)
	
	cotan = 1. / math.tan (fieldOfViewY / 2.)
	zN = float (zNearFarVec [0])
	zF = float (zNearFarVec [1])
	
	return numpy.matrix ([
		[cotan / aspectRatio, 0, 0, 0],
		[0, cotan, 0, 0],
		[0, 0, (zN + zF) / (zN - zF), 2. * zN * zF / (zN - zF)],
		[0, 0, -1., 0]
	], dtype = typesNp [typesGen ['coordinate']])
		
def getOrthMat (fieldOfViewY, aspectRatio, zNearFarVec):	# Camera at (0, 0, 0), looking at (0, 0, -1)
	zN = float (zNearFarVec [0])
	zF = float (zNearFarVec [1])

	yTop = zN * math.tan (fieldOfViewY / 2.)
	xRight = aspectRatio * yTop
	
	return numpy.matrix ([
		[1. / xRight, 0, 0, 0],
		[0, 1. / yTop, 0, 0],
		[0, 0, 2. / (zN - zF), (zN + zF) / (zN - zF)],
		[0, 0, 0, 1.]
	], dtype = typesNp [typesGen ['coordinate']])

