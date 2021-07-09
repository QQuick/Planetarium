import math as mt

import numscrypt as ns

import utils as ut

__pragma__ ('opov')

def getRotXMat (angle):
    c = mt.cos (angle)
    s = mt.sin (angle)
    return ns.array ([
        [1, 0, 0],
        [0, c, -s],
        [0, s, c]
    ], dtype = ut.typesNs [ut.typesGen ['coordinate']])

def getRotYMat (angle):
    c = mt.cos (angle)
    s = mt.sin (angle)
    return ns.array ([
        [c, 0, s],
        [0, 1, 0],
        [-s, 0, c]
    ], dtype = ut.typesNs [ut.typesGen ['coordinate']])

def getRotZMat (angle):
    c = mt.cos (angle)
    s = mt.sin (angle)
    return ns.array ([
        [c, -s, 0],
        [s, c, 0],
        [0, 0, 1]
    ], dtype = ut.typesNs [ut.typesGen ['coordinate']])

def getRotXYZMat (angleVec):    # Z rotation first
    return (
        getRotXMat (angleVec [2]) *
        getRotYMat (angleVec [1]) *
        getRotZMat (angleVec [0])
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

def getProjection (bodyVec, imageDist):
    scale = imageDist / bodyVec [2]
    # !!! return bodyVec [:2] / scale if scale <= 1 else None
    return ns.array ((scale * bodyVec [0], scale * bodyVec [1])) if scale < 1 else None