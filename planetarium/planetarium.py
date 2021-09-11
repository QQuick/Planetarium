import math as mt

import pyact as pa
import pymui as pm

import transforms as tf
import solar_system as ss
import exo_system as es

twoPi = 2 * mt.pi
controlWidth = '90%'
controlHeight = '100'

def tabEl (self, index):
    return pm.Tab ({'value': str (index), 'label': 'test'}) .el ()

class Planetarium:
    def __init__ (self):
        self.solarSystem = ss.SolarSystem (self, lambda: (2020, 12, 21, 0, 0, 0), lambda: 0.2)
        self.exoSystem = es.ExoSystem (self)
        self.solarSystem.setEquatPositions ()

        self.Pages = (SkyMapPage, SolarSystemPage, PlanetVisibilityPage)
        self.pages = [Page (self, pageIndex) for pageIndex, Page in enumerate (self.Pages)]     # All pages created in advance, since they're permanently on their tabs
        pa.render (self.el, None, 'root')

    def el (self):
        self.pageIndex, self.setPageIndex = pa.useState (0)

        self.xAngle, self.setXAngle = pa.useState (0)
        self.yAngle, self.setYAngle = pa.useState (0)
        self.zAngle, self.setZAngle = pa.useState (0)

        self.rotZyxMat = tf.getRotZyxMat ((self.xAngle, self.yAngle, self.zAngle))
        self.solarSystem.setEarthViewPositions ()
        self.exoSystem.setEarthViewPositions ()

        return pm.TabContext ({'value': str (self.pageIndex)},
            pm.AppBar ({'position': 'static', 'style': {'background': '#333333'}},
                pm.Tabs ({'value': str (self.pageIndex)},
                    *(page.tabEl () for page in self.pages)
                ) .el ()
            ) .el (),
            *(page.contentEl () for page in self.pages)
        ) .el ()

class Page:
    def __init__ (self, planetarium, index):
        self.planetarium = planetarium
        self.index = index
        self.viewPane = ViewPane (self)
        self.init ()

    def tabEl (self):
        pa.useEffect (self.draw)
        return pm.Tab ({'value': str (self.index), 'label': self.title, 'onClick': lambda: self.planetarium.setPageIndex (self.index)}) .el ()

    def contentEl (self):
        return pm.TabPanel ({'value': str (self.index), 'style': {'boxSizing': 'border-box', 'margin': 0, 'paddingTop': 30, 'backgroundColor': 'gray', 'width': '100%'}},
            pm.Grid ({'container': True, 'style': {'margin': 0, 'padding': 0}},
                self.controlPane.el (),
                self.viewPane.el ()
            ) .el ()
        ) .el ()

    def draw (self):
        if self.planetarium.pageIndex == self.index:
            self.viewPane.draw ()

class SkyMapPage (Page):
    def init (self, planetarium, index):
        self.title = 'Sky Map'
        self.controlPane = SkyMapControlPane (self)

class SolarSystemPage (Page):
    def init (self, planetarium, index):
        self.title = 'Solar System'
        self.controlPane = SolarSystemControlPane (self)
    
class PlanetVisibilityPage (Page):
    def init (self, planetarium, index):
        self.title = 'Planet Visibility'
        self.controlPane = PlanetVisibilityControlPane (self)

class Pane:
    pass

class ControlPane (Pane):
    def __init__ (self, page):
        self.page = page
        self.controlGroups = [TimeControlGroup (self)]
        self.appendControlGroups ()

    def el (self):
        return pm.Box ({'style': {'width': '20%', 'margin': 0, 'padding': 0}},
            pm.Grid ({'container': True, 'direction': 'column', 'style': {'margin': 0, 'padding': 0}},
                *[controlGroup.el () for controlGroup in self.controlGroups]
            ) .el ()
        ) .el ()

class SkyMapControlPane (ControlPane):
    def appendControlGroups (self):
        self.controlGroups.append (SkyMapControlGroup (self))

class SolarSystemControlPane (ControlPane):
    def appendControlGroups (self):
        self.controlGroups.append (SolarSystemControlGroup (self))

class PlanetVisibilityControlPane (ControlPane):
    def appendControlGroups (self):
        self.controlGroups.append (PlanetVisibilityControlGroup (self))

class ViewPane (Pane):
    def __init__ (self, page):
        self.page = page
        self.width = 800
        self.height = 800
        self.canvasRef = pa.createRef ()

    def el (self):
        return pm.Canvas ({'ref': self.canvasRef, 'style': {'backgroundColor': 'black', 'width': self.width + 150, 'height': self.height + 150}}) .el ()

    def draw (self):
        self.canvas = self.canvasRef.current
        self.context = self.canvas.getContext ('2d')
        self.canvas.width = self.width
        self.canvas.height = self.height
        self.context.fillStyle = 'white'

        for planet in reversed (self.page.planetarium.solarSystem.planets):
            if planet.earthViewPosition != None:
                self.drawSphere (planet.earthViewPosition, mt.sqrt (planet.radius) / 40, planet.color)

        for star in self.page.planetarium.exoSystem.stars:
            if star.earthViewPosition != None:
                self.drawSphere (star.earthViewPosition, (6 - star.magnitude) / 2, 'red' if 'm 31' in star.name else 'white')

    def getCanvasCoords (self, viewCoords):
        result = self.width / 2 + viewCoords [0], self.height / 2 - viewCoords [1]
        return result

    def drawSphere (self, viewCoords, radius, color, fill = True):
        self.context.beginPath ()
        self.context.arc (*self.getCanvasCoords (viewCoords), radius, 0, twoPi)
        
        if fill:
            self.context.fillStyle = color
            self.context.fill ()

class ControlGroup:
    def __init__ (self, controlPane):
        self.controlPane = controlPane
        self.setControls ()

    def el (self):
        return pm.Box ({'style': {'margin': 0, 'padding': 0}},
            pm.Grid ({'container': True, 'direction': 'column', 'style': {'margin': 0, 'padding': 0}},
                *[control.el () for control in self.controls]
            ) .el ()
        ) .el ()

class TimeControlGroup (ControlGroup):
    def setControls (self):
        self.controls = [
            pm.TextField ({'type': 'date', 'style': {'width': controlWidth}}),
            pm.TextField ({'type': 'time', 'style': {'width': controlWidth}})
        ]

class SkyMapControlGroup (ControlGroup):
    def setControls (self):
        self.controls = [
            pm.Slider ({'onChange': lambda event, value: self.controlPane.page.planetarium.setXAngle (value * twoPi / 100), 'style': {'width': controlWidth}}),
            pm.Slider ({'onChange': lambda event, value: self.controlPane.page.planetarium.setYAngle (value * twoPi / 100), 'style': {'width': controlWidth}}),
            pm.Slider ({'onChange': lambda event, value: self.controlPane.page.planetarium.setZAngle (value * twoPi / 100), 'style': {'width': controlWidth}})
        ]

class SolarSystemControlGroup (ControlGroup):
    def setControls (self):
        self.controls = [pm.String ('solarSystemControlGroup')]

class PlanetVisibilityControlGroup (ControlGroup):
    def setControls (self):
        self.controls = [pm.String ('planetVisibilityControlGroup')]

planetarium = Planetarium ()