import datetime as dt
import math as mt

import numscrypt as ns

import utils as ut
import solar_system as ss
import transforms as tr

class Telescope:
    def __init__ (self):
        solarSystem = ss.SolarSystem ()

        planetPositions = ns.array (solarSystem.getPositions  (dt.datetime (2020, 12, 21, 0, 0, 0))) .transpose ()
        # planetPositions = ns.array ([[1, 1, 1], [0, 0, 0], [1, 1.5, 2]], dtype = ut.typesNs [ut.typesGen ['coordinate']])
        print (planetPositions)

        for columnIndex in range (planetPositions.shape [1]):
            print (tr.getProjection (planetPositions [:, columnIndex], 1.5))

telescope = Telescope ()

