import math as mt

import pyact as pa
import pymui as pm

import solar_system as ss

twoPi = 2 * mt.pi

def tabEl (self, index):
    return pa.el (pm.Tab, {'value': str (index), 'label': 'test'})

class Planetarium:
    def __init__ (self):
        self.solarSystem = ss.SolarSystem (lambda: (2020, 12, 21, 0, 0, 0), lambda: 40)
        self.solarSystem.setEquatPositions ()
        self.solarSystem.setViewPositions ()
        # self.solarSystem.printPositions ()

        self.Pages = (SkyMapPage, SolarSystemPage, PlanetVisibilityPage)
        self.pages = [Page (self, pageIndex) for pageIndex, Page in enumerate (self.Pages)]
        pa.render (self.el, None, 'root')

    def el (self):
        self.pageIndex, self.setPageIndex = pa.useState (0)

        return pa.el (pm.Box, {'style': {'margin': 0, 'padding': 0}},
            pa.el (pm.TabContext, {'value': str (self.pageIndex)},
                pa.el (pm.AppBar, {'position': 'static', 'style': {'background': '#333333'}},
                    pa.el (pm.Tabs, {'value': str (self.pageIndex)},
                        *(page.tabEl () for page in self.pages)
                    )
                ),
                *(page.contentEl () for page in self.pages)
            )
        )

class BasePage:
    def __init__ (self, planetarium, index, title):
        self.planetarium = planetarium
        self.index = index
        self.title = title
        self.viewPane = ViewPane (self, 800, 800)

    def tabEl (self):
        pa.useEffect (self.draw)
        return pa.el (pm.Tab, {'value': str (self.index), 'label': self.title, 'onClick': lambda: self.planetarium.setPageIndex (self.index)})

    def contentEl (self):
        return pa.el (pm.TabPanel, {'value': str (self.index), 'style': {'boxSizing': 'border-box', 'margin': 0, 'paddingTop': 30, 'backgroundColor': 'gray', 'width': '100%', 'width': '100%'}},
            pa.el (pm.Grid, {'container': True, 'style': {'margin': 0, 'padding': 0}},
                pa.el (pm.Box, {'style': {'width': '20%', 'margin': 0, 'padding': 0}},
                    self.title
                ),
                pa.el (pm.Box, {'style': {'width': '70%', 'margin': 0, 'padding': 0}},
                    self.viewPane.el (),
                )
            )
        )

    def draw (self):
        if self.planetarium.pageIndex == self.index:
            self.viewPane.draw ()

class SkyMapPage (BasePage):
    def __init__ (self, planetarium, index):
        super () .__init__ (planetarium, index, 'Sky Map')

class SolarSystemPage (BasePage):
    def __init__ (self, planetarium, index):
        super () .__init__ (planetarium, index, 'Solar System')
    
class PlanetVisibilityPage (BasePage):
    def __init__ (self, planetarium, index):
        super () .__init__ (planetarium, index, 'Planet Visibility')

class ControlPane:
    pass

class ViewPane:
    def __init__ (self, page, width, height):
        self.page = page
        self.width = width
        self.height = height
        self.canvasRef = pa.createRef ()

    def el (self):
        return pa.el ('canvas', {'ref': self.canvasRef, 'style': {'backgroundColor': 'black', 'width': self.width + 150, 'height': self.height + 150}})

    def draw (self):
        self.canvas = self.canvasRef.current
        self.context = self.canvas.getContext ('2d')
        self.canvas.width = self.width
        self.canvas.height = self.height
        self.context.fillStyle = 'white'

        for planet in reversed (self.page.planetarium.solarSystem.planets):
            if planet.viewPosition != None:
                self.drawSphere (planet.viewPosition, mt.sqrt (planet.radius) / 40, planet.color)

    def getCanvasCoords (self, viewCoords):
        result = self.width / 2 + viewCoords [0], self.height / 2 - viewCoords [1]
        return result

    def drawSphere (self, viewCoords, radius, color):
        self.context.beginPath ()
        self.context.arc (*self.getCanvasCoords (viewCoords), radius, 0, twoPi)
        self.context.fillStyle = color
        self.context.fill ()

class TimeControls:
    pass

class SkyMapControls:
    pass

class SolarSystemControls:
    pass

class PlanetVisibilityControls:
    pass

planetarium = Planetarium ()