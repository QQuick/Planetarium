import datetime as dt

import numscrypt as ns

import solar_system as ss
import transforms as tr

class Telescope:
    def __init__ (self):
        solarSystem = ss.SolarSystem ()

        planetPositions = tr.homogenize (ns.array (solarSystem.getPositions  (dt.datetime (2020, 12, 21, 0, 0, 0))) .transpose ())
        print (planetPositions)

        projectionMat = tr.getPerspMat (10, 1, (0, 1))
        print (projectionMat)
        
        __pragma__ ('opov')
        planetProjections = tr.inhomogenize (projectionMat @ planetPositions)
        __pragma__ ('noopov')
        print (planetProjections)
        

telescope = Telescope ()

