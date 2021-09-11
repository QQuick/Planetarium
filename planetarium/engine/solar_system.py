# Compute positions of planets in equatorial coordinates.
# Basic data and formulae underlying this module are in background_literature folder.

import datetime as dt
import math as mt

import numscrypt as ns

import utils as ut
import transforms as tf
import planet_catalog as pc

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
        rotatedPosition = self.solarSystem.planetarium.rotZyxMat @ (self.equatPosition - self.solarSystem.earth.equatPosition)
        self.earthViewPosition = tf.getStereographicProjection (rotatedPosition, self.solarSystem.getViewDistance ())

    def setFarViewOrbit (self):

        self.farViewOrbit = [tf.getProjection (self.equatPostion - ns.array ((30, 30, 10)), self.solarSystem.getViewDistance) for equatPosition in self.equatOrbit]

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
        
        # t_0 = ut.julianDayNr (dt.datetime (*self.solarSystem.getYmdHms ())) - ut.julianDayNr (dt.datetime (2000, 1, 1, 0, 0, 0))
        t_0 = ut.julianDayNr (dt.datetime.now ()) - ut.julianDayNr (dt.datetime (2000, 1, 1, 0, 0, 0))
        
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
    def __init__ (self, planetarium, getYmdHms, getViewDistance):
        self.planetarium = planetarium
        self.getYmdHms = getYmdHms
        self.getViewDistance = getViewDistance

        self.planets = [Planet (self, *args) for args in pc.planetCatalog]

        self.earth = self.planets [2]

    def setEquatPositions (self):
        for planet in self.planets:
            planet.setEquatPosition ()

    def setEquatOrbits (self):
        for planet in self.planets:
            planet.setEquatOrbit ()

    def setEarthViewPositions (self):
        for planet in self.planets:
            planet.setEarthViewPosition ()

    def setFarViewOrbits (self):
        for planet in self.planets:
            planet.setFarViewOrbit ()

    def printPositions (self):
        for planet in self.planets:
            print (planet.name, planet.equatPosition, planet.earthViewPosition)
