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

def getRotXyzMat (angleVec):    # Z rotation first
    return (
        getRotXMat (angleVec [2]) @
        getRotYMat (angleVec [1]) @
        getRotZMat (angleVec [0])
    )

def getRotXzyMat (angleVec):
    return (
        getRotXMat (angleVec [2]) @
        getRotZMat (angleVec [1]) @
        getRotYMat (angleVec [0])
    )

def getRotYxzMat (angleVec):
    return (
        getRotYMat (angleVec [2]) @
        getRotXMat (angleVec [1]) @
        getRotZMat (angleVec [0])
    )

def getRotYzxMat (angleVec):
    return (
        getRotYMat (angleVec [2]) @
        getRotZMat (angleVec [1]) @
        getRotXMat (angleVec [0])
    )

def getRotZxyMat (angleVec):
    return (
        getRotZMat (angleVec [2]) @
        getRotXMat (angleVec [1]) @
        getRotYMat (angleVec [0])
    )

def getRotZyxMat (angleVec):
    return (
        getRotZMat (angleVec [2]) @
        getRotYMat (angleVec [1]) @
        getRotXMat (angleVec [0])
    )

'''
def getProjection (bodyVec, imageDist):
    scale = 400
    return (-scale * mt.atan2 (bodyVec [0], bodyVec [2]), scale * mt.atan2 (bodyVec [1], bodyVec [2])) if bodyVec [2] > 0 else None
'''

def getNorm (vec):
    vec = vec.transpose () .transpose ()
    norm = mt.sqrt ((vec @ vec.transpose ()) [0, 0])
    '''
    print ('vec', vec)
    print ('vec.T', vec.transpose ())
    print ('prod', vec @ vec.transpose ())
    print ('norm', norm)
    print ()
    '''
    return norm

def getNormalized (vec):
    return vec / getNorm (vec)

# Source: https://en.wikipedia.org/wiki/Stereographic_projection
def getStereographicProjection (bodyVec, imageDist):
    if bodyVec [2, 0] < 0:
        return None

    unitVec = getNormalized (bodyVec)
    result = ns.array ((
        400 * unitVec [0, 0] / (1 - unitVec [2, 0]),
        400 * unitVec [1, 0] / (1 - unitVec [2, 0])
    )) .tolist ()
    # print (result)
    return result
    