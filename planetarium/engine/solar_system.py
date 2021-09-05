# Compute positions of planets in equatorial coordinates.
# Basic data and formulae underlying this module are in background_literature folder.

import datetime as dt
import math as mt

import numscrypt as ns

import utils as ut
import transforms as tr

__pragma__ ('opov')

mPerAu = 149597871e14

class Planet:
    def __init__ (self, solarSystem, name, basicOrbitElements, extraOrbitElements, period, radius, color):
        self.name = name
        self.solarSystem = solarSystem
        self.basicOrbitElements = basicOrbitElements
        self.extraOrbitElements = extraOrbitElements
        self.period = period
        self.radius = radius
        self.color = color

    def setEquatPosition (self):
        self.equatPosition = self.computeEquatOrbit (1)[0]

    def setEquatOrbit (self):
        self.equatOrbit = self.computeEquatOrbit (180)

    def setEarthViewPosition (self):
        rotatedPosition = self.solarSystem.rotZyxMat @ (self.equatPosition - self.solarSystem.earth.equatPosition)
        self.earthViewPosition = tr.getProjection (rotatedPosition, self.solarSystem.getViewDistance ())

    def setFarViewOrbit (self):

        self.farViewOrbit = [tr.getProjection (self.equatPostion - ns.array ((30, 30, 10)), self.solarSystem.getViewDistance) for equatPosition in self.equatOrbit]

    def computeEquatOrbit (self, orbitSteps):
        a_0 = self.basicOrbitElements [0][0]
        a_der = self.basicOrbitElements [1][0]

        e_0 = self.basicOrbitElements [0][1]
        e_der = self.basicOrbitElements [1][1]

        I_0 = self.basicOrbitElements [0][2]
        I_der = self.basicOrbitElements [1][2]

        L_0 = self.basicOrbitElements [0][3]
        L_der = self.basicOrbitElements [1][3]

        om_bar_0 = self.basicOrbitElements [0][4]
        om_bar_der = self.basicOrbitElements [1][4]

        Om_0 = self.basicOrbitElements [0][5]
        Om_der = self.basicOrbitElements [1][5]
        
        t_0 = ut.julianDayNr (dt.datetime (*self.solarSystem.getYmdHms ())) - ut.julianDayNr (dt.datetime (2000, 1, 1, 0, 0, 0))
        
        for i in range (orbitSteps):
            t = t_0 + i * self.period / orbitSteps
                
            daysPerCentury = 36525
            T = t / daysPerCentury
            
            a = a_0 + a_der * T
            e = e_0 + e_der * T
            I = I_0 + I_der * T
            L = L_0 + L_der * T
            om_bar = om_bar_0 + om_bar_der * T
            Om = Om_0 + Om_der * T

            b = self.extraOrbitElements [0]
            c = self.extraOrbitElements [1]
            s = self.extraOrbitElements [2]
            f = self.extraOrbitElements [3]
            
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

            xAccent = a * (mt.cos (ut.radFromDeg (E)) - e)
            yAccent = a * mt.sqrt (1 - e * e) * mt.sin (ut.radFromDeg (E))
            zAccent = 0

            equatOrbit = []
            
            equatOrbit.append (ns.array (ut.equatFromEclipt (
                (mt.cos (ut.radFromDeg (om)) * mt.cos (ut.radFromDeg (Om)) - mt.sin (ut.radFromDeg (om)) * mt.sin (ut.radFromDeg (Om)) * mt.cos (ut.radFromDeg (I))) * xAccent +
                (-mt.sin (ut.radFromDeg (om)) * mt.cos (ut.radFromDeg (Om)) - mt.cos (ut.radFromDeg (om)) * mt.sin (ut.radFromDeg (Om)) * mt.cos (ut.radFromDeg (I))) * yAccent,
 
                (mt.cos (ut.radFromDeg (om)) * mt.sin (ut.radFromDeg (Om)) + mt.sin (ut.radFromDeg (om)) * mt.cos (ut.radFromDeg (Om)) * mt.cos (ut.radFromDeg (I))) * xAccent +
                (-mt.sin (ut.radFromDeg (om)) * mt.sin (ut.radFromDeg (Om)) + mt.cos (ut.radFromDeg (om)) * mt.cos (ut.radFromDeg (Om)) * mt.cos (ut.radFromDeg (I))) * yAccent,
                
                mt.sin (ut.radFromDeg (om)) * mt.sin (ut.radFromDeg (I)) * xAccent +
                mt.cos (ut.radFromDeg (om)) * mt.sin (ut.radFromDeg (I)) * yAccent
            )))

        return equatOrbit

class SolarSystem:
    def __init__ (self, getYmdHms, getViewDistance):
        self.getYmdHms = getYmdHms
        self.getViewDistance = getViewDistance

        self.planets = [Planet (self, *args) for args in (
            (   'mercury',
                (   (0.38709843, 0.20563661, 7.00559432, 252.25166724, 77.45771895, 48.33961819),
                    (0.00000000, 0.00002123, -0.00590158, 149472.67486623, 0.15940013, -0.12214182)
                ), (0, 0, 0, 0), 88, 2440, 'lightGray'
            ), ('venus',
                (   (0.72332102, 0.00676399, 3.39777545, 181.97970850, 131.76755713, 76.67261496),
                    (-0.00000026, 0.00005107, 0.00043494, 58517.81560260, 0.05679648, -0.27274174)
                ), (0, 0, 0, 0), 225, 6052, 'orange'
            ), ('earth',
                (   (1.00000018, 0.01673163, -0.00054346, 100.46691572, 102.93005885, -5.11260389),
                    (-0.00000003, -0.00003661, -0.01337178, 35999.37306329, 0.31795260, -0.24123856)
                ), (0, 0, 0, 0), 365, 6371, 'cyan'
            ), ('mars',
                (   (1.52371243, 0.09336511, 1.85181869, -4.56813164, -23.91744784, 49.71320984),
                    (0.00000097, 0.00009149, -0.00724757, 19140.29934243, 0.45223625, -0.26852431)
                ), (0, 0, 0, 0), 687, 3386, 'red'
            ), ('jupiter',
                (   (5.20248019, 0.04853590, 1.29861416, 34.33479152, 14.27495244, 100.29282654),
                    (-0.00002864, 0.00018026, -0.00322699, 3034.90371757, 0.18199196, 0.13024619)
                ), (-0.00012452, 0.06064060, -0.35635438, 38.35125000), 4332, 69173, 'magenta'
            ), ('saturn',
                (   (9.54149883, 0.05550825, 2.49424102, 50.07571329, 92.86136063, 113.63998702),
                    (-0.00003065, -0.00032044, 0.00541969, 1222.11494724, 0.54179478, -0.25015002)
                ), (0.00025899, -0.13434469, 0.87320147, 38.35125000), 10757, 57316, 'yellow'
            ), ('uranus',
                (   (19.18797948, 0.04685740, 0.77298127, 314.20276625, 172.43404441, 73.96250215),
                    (-0.00020455, -0.00001550, -0.00180155, 428.49512595, 0.09266985, 0.05739699)
                ), (0.00058331, -0.97731848, 0.16789245, 7.67025000), 30660, 25266, 'green'
            ), ('neptunus',
                (   (30.06952752, 0.00895439, 1.77005520, 304.22289287, 46.68158724, 131.78635853),
                    (0.00006447, 0.00000818, 0.00022400, 218.46515314, 0.01009938, -0.00606302)
                ), (0.00041348, 0.68346318, -0.10162547, 7.67025000), 59960, 24553, 'blue'
            )
        )]

        self.earth = self.planets [2]

    def setEquatPositions (self):
        for planet in self.planets:
            planet.setEquatPosition ()

    def setEquatOrbits (self):
        for planet in self.planets:
            planet.setEquatOrbit ()

    def setEarthViewPositions (self, angleVec):
        self.rotZyxMat = tr.getRotZyxMat (angleVec)
        
        for planet in self.planets:
            planet.setEarthViewPosition ()

    def setFarViewOrbits (self):
        for planet in self.planets:
            planet.setFarViewOrbit ()

    def printPositions (self):
        for planet in self.planets:
            print (planet.name, planet.equatPosition, planet.earthViewPosition)
