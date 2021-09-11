import math as mt

import numscrypt as ns

import transforms as tf
import star_catalog as sc

__pragma__ ('opov')

skyRadius = 1e20
radFactor = mt.pi / 180

class Star:
    def __init__ (self, exoSystem, catalogLine):
        self.exoSystem = exoSystem
        
        catalogWords = [
            catalogWord for catalogWord in [
                rawCatalogWord.strip () for rawCatalogWord in catalogLine.split (';')
            ] if catalogWord]

        self.name = catalogWords [0]
        self.kind = catalogWords [1]
        self.rightAscension, self.declination = [radFactor * float (coordinate) for coordinate in catalogWords [2] .split ()]
        self.magnitude = float (catalogWords [3])

        self.equatPosition = skyRadius * ns.array ((
            mt.cos (self.declination) * mt.cos (self.rightAscension),
            mt.cos (self.declination) * mt.sin (self.rightAscension),
            mt.sin (self.declination)
        ))
        
    def setEarthViewPosition (self):
        rotatedPosition = self.exoSystem.planetarium.rotZyxMat @ self.equatPosition   # Neglect distance from earth to sun
        self.earthViewPosition = tf.getStereographicProjection (rotatedPosition, self.exoSystem.planetarium.solarSystem.getViewDistance ())

    def __repr__ (self):
        return f'{self.name}_{self.kind}_{self.rightAscension}_{self.declination}_{self.equatPosition}_{self.magnitude}'

class ExoSystem:
    def __init__ (self, planetarium):
        self.planetarium = planetarium
        self.stars = [Star (self, catalogLine) for catalogLine in sc.starCatalog.lower () .split ('\n') if catalogLine.strip ()]

    def setEarthViewPositions (self):       
        for star in self.stars:
            star.setEarthViewPosition ()

    def __repr__ (self):
        return '\n'.join (star.__repr__ () for star in self.stars)
    
exoSystem = ExoSystem ()
