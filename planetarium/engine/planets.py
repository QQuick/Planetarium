import datetime as dt
import math as mt

import utils as ut

'''All facilities for computing planetary orbits

Basic data and formulae underlying this module are in background_literature directory.
Here and in many places global data, class methods or the singleton pattern could have been used.
However none of these are particularly helpful.
It's even imaginable that multiple instances of the solar system may occasionally be of use,
e.g. with slight variations in the orbit elements, for sensitivity analysis.
'''

class Planets:
    def __init__ (self):
        '''Initialize planet data like orbit elements, radius etc
        ''' 
        self.allPlanetIndices = dict ([(planentName, planetIndex) for planetIndex, planetName in enumerate ('Mercury', 'Venus', 'Earth', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune')])

        self._allBasicOrbElems = (
            (   # Mercury
                (0.38709843,       0.20563661,        7.00559432,        252.25166724,      77.45771895,       48.33961819),
                (0.00000000,       0.00002123,        -0.00590158,       149472.67486623,   0.15940013,        -0.12214182)
            ),
            (   # Venus
                (0.72332102,       0.00676399,        3.39777545,        181.97970850,      131.76755713,      76.67261496),
                (-0.00000026,      0.00005107,        0.00043494,        58517.81560260,    0.05679648,        -0.27274174)
            ),
            (   # Earth
                (1.00000018,       0.01673163,        -0.00054346,       100.46691572,      102.93005885,      -5.11260389),
                (-0.00000003,      -0.00003661,       -0.01337178,       35999.37306329,    0.31795260,        -0.24123856)
            ),
            (   # Mars
                (1.52371243,       0.09336511,        1.85181869,        -4.56813164,       -23.91744784,      49.71320984),
                (0.00000097,       0.00009149,        -0.00724757,       19140.29934243,    0.45223625,        -0.26852431)
            ),
            (   # Jupiter
                (5.20248019,       0.04853590,        1.29861416,        34.33479152,       14.27495244,       100.29282654),
                (-0.00002864,      0.00018026,        -0.00322699,       3034.90371757,     0.18199196,        0.13024619)
            ),
            (   # Saturn
                (9.54149883,       0.05550825,        2.49424102,        50.07571329,       92.86136063,       113.63998702),
                (-0.00003065,      -0.00032044,       0.00541969,        1222.11494724,     0.54179478,        -0.25015002)
            ),
            (   # Uranus
                (19.18797948,      0.04685740,        0.77298127,        314.20276625,      172.43404441,      73.96250215),
                (-0.00020455,      -0.00001550,       -0.00180155,       428.49512595,      0.09266985,        0.05739699)
            ),
            (   # Neptune
                (30.06952752,      0.00895439,        1.77005520,        304.22289287,      46.68158724,       131.78635853),
                (0.00006447,       0.00000818,        0.00022400,        218.46515314,      0.01009938,        -0.00606302)
            )
        )

        self._allExtraOrbElems = (
            (0,                 0,                 0,                 0),           # Mercury
            (0,                 0,                 0,                 0),           # Venus
            (0,                 0,                 0,                 0),           # Earth
            (0,                 0,                 0,                 0),           # Mars
            (-0.00012452,       0.06064060,        -0.35635438,       38.35125000), # Jupiter
            (0.00025899,        -0.13434469,       0.87320147,        38.35125000), # Saturn
            (0.00058331,        -0.97731848,       0.16789245,        7.67025000),  # Uranus
            (0.00041348,        0.68346318,        -0.10162547,       7.67025000)   # Neptune
        }

        self.allPeriods = (88,  225, 365, 687, 4332, 10757, 30660, 59960)
        self.allRadii = (2440, 6052, 6371, 3386, 69173, 57316, 25266, 24553)
        self.allColors = (lightGray, orange, cyan, red, magenta, yellow, green, blue)
        
        self.allEquatorialOrbits = [[] for i in len (self.planetIndices)]
        self.allEquatorialPositions = [None for i in len (self.planetIndices)]
    
    def _computeEquatorialPositions (self, planetName, startDateTime, orbitSteps):
        '''Compute orbitSteps positions of the orbit of one planet, starting at startDateTime
        '''
        planetIndex = self.planetIndices [planetName]
        
        basicOrbElems = self._allBasicOrbElemems [planetIndex]
        extraOrbElems = self._allExtraOrbElems (planetIndex]
        period = self.allPeriods [planetIndex]
    
        a_0 = basicOrbElems [0][0]
        a_der = basicOrbElems [1][0]

        e_0 = basicOrbElems [0][1]
        e_der = basicOrbElems [1][1]

        I_0 = basicOrbElems [0][2]
        I_der = basicOrbElems [1][2]

        L_0 = basicOrbElems [0][3]
        L_der = basicOrbElems [1][3]

        om_bar_0 = basicOrbElems [0][4]
        om_bar_der = basicOrbElems [1][4]

        Om_0 = basicOrbElems [0][5]
        Om_der = basicOrbElems [1][5]
        
        t_0 = (ut.julianDayNr (dateTime) - ut.julianDayNr (datetime (2000, 1, 1, 0, 0, 0)))
        
        for i in range (orbitSteps):
            t = t_0 + i * period / orbitSteps
                
            daysPerCentury = 36525
            T = t / daysPerCentury
            
            a = a_0 + a_der * T
            e = e_0 + e_der * T
            I = I_0 + I_der * T
            L = L_0 + L_der * T
            om_bar = om_bar_0 + om_bar_der * T
            Om = Om_0 + Om_der * T

            b = extraOrbElems [0]
            c = extraOrbElems [1]
            s = extraOrbElems [2]
            df = extraOrbElems [3]
            
            om = om_bar - Om
            M = L - om_bar + b * T * T + c * mt.cos (ut.radFromDeg (f * T)) + s * mt.sin (ut.radFromDeg (f * T))
            
            M = M % 360
            if M > 180:
                M = M - 360
            
            e_star = ut.degFromRad (e)
            E = M +  e_star * mt.sin (ut.radFromDeg (M))

            tol = 1e-6;
            del_E = 1e10
            while del_E > tol:
                del_M = M - (E - e_star * mt.sin (ut.radFromDeg (E)))
                del_E = del_M / (1 - e * mt.cos (ut.radFromDeg (E)))
                E = E + del_E

            xAccent = a * (mt.cos (self.radFromDeg (E)) - e)
            yAccent = a * mt.sqrt (1 - e * e) * mt.sin (ut.radFromDeg (E))
            zAccent = 0
            
            equatialOrbitPositions = []
            
            equatorialOrbitPositions.append  (equatFromEclipt (
                (mt.cos (radFromDeg (om)) * mt.cos (ut.radFromDeg (Om)) - mt.sin (ut.radFromDeg (om)) * mt.sin (ut.radFromDeg (Om)) * mt.cos (ut.radFromDeg (I))) * xAccent +
                (-mt.sin (radFromDeg (om)) * mt.cos (ut.radFromDeg (Om)) - mt.cos (ut.radFromDeg (om)) * mt.sin (ut.radFromDeg (Om)) * mt.cos (ut.radFromDeg (I))) * yAccent,
 
                (mt.cos (radFromDeg (om)) * mt.sin (ut.radFromDeg (Om)) + mt.sin (ut.radFromDeg (om)) * mt.cos (ut.radFromDeg (Om)) * mt.cos (ut.radFromDeg (I))) * xAccent +
                (-mt.sin (radFromDeg (om)) * mt.sin (ut.radFromDeg (Om)) + mt.cos (ut.radFromDeg (om)) * mt.cos (ut.radFromDeg (Om)) * mt.cos (ut.radFromDeg (I))) * yAccent,
                
   
                mt.sin (ut.radFromDeg (om)) * mt.sin (ut.radFromDeg (I)) * xAcc +
                mt.cos (ut.radFromDeg (om)) * mt.sin (ut.radFromDeg (I)) * yAcc
            ))
                
        return equatorialOrbitPositions
       
    def computeEquatorialOrbit (self, planetName, startDateTime):
        '''Compute one complete orbit of a particular planet in small steps
        '''
        planetIndex = self.planetIndices [planetName]
        self.allEquatorialOrbits [planetName] = computeEquatorialPositions (self, planetIndex, startDateTime, 180)
        
    def computeEquatorialOrbits (self, startDateTime):
        '''Compute one complete orbit of all planets in small steps
        '''
        for planetIndex in self.planetIndices.values ():
            self.computeEquatorialOrbit (self, planetIndex, startDateTime)

    def computeEquatorialPosition (self, planetName, dateTime):
        '''Compute one position of a particular planet
        '''
        planetIndex = self.planetIndices [planetName]
        self.allEquatorialPositions [planetIndex] = computeEquatorialPositions (self, planentIndex, startDateTime, 1) [0]

    def computeEquatorialPositions (self, dateTime):
        '''Compute one position of each planet
        '''
        for planetIndex in self.planetIndices.values ():
            self.computeEquatorialPosition (planetIndex)
