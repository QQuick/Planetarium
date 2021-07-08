import math as mt

import pyact as pa
import pymui as pm

import telescope as ts

def tabEl (self, index):
    return pa.el (pm.Tab, {'value': str (index), 'label': 'test'})

class Planetarium:
    def __init__ (self):
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
        self.canvasRef = pa.createRef ()

    def tabEl (self):
        pa.useEffect (self.render)
        return pa.el (pm.Tab, {'value': str (self.index), 'label': self.title, 'onClick': lambda: self.planetarium.setPageIndex (self.index)})

    def contentEl (self):
        return pa.el (pm.TabPanel, {'value': str (self.index), 'style': {'boxSizing': 'border-box', 'margin': 0, 'paddingTop': 30, 'backgroundColor': 'gray', 'width': '100%', 'width': '100%'}},
            pa.el (pm.Grid, {'container': True, 'style': {'margin': 0, 'padding': 0}},
                pa.el (pm.Box, {'style': {'width': '20%', 'margin': 0, 'padding': 0}},
                    self.title
                ),
                pa.el (pm.Box, {'style': {'width': '70%', 'margin': 0, 'padding': 0}},
                    pa.el ('canvas', {'ref': self.canvasRef, 'style': {'backgroundColor': 'black', 'height': 950, 'width': 950}}),
                )
            )
        )

    def render (self):
        if self.planetarium.pageIndex == self.index:
            self.canvas = self.canvasRef.current
            self.context = self.canvas.getContext ('2d')
            self.canvas.width = 800
            self.canvas.height = 800
            self.context.fillStyle = 'white'
            self.draw ()

class SkyMapPage (BasePage):
    def __init__ (self, planetarium, index):
        super () .__init__ (planetarium, index, 'Sky Map')

    def draw (self):
        self.context.beginPath ()
        self.context.arc (100.5, 80.5, 0.5, 0, 2 * mt.pi)
        self.context.fill ()

class SolarSystemPage (BasePage):
    def __init__ (self, planetarium, index):
        super () .__init__ (planetarium, index, 'Solar System')

    def draw (self):
        self.context.beginPath ()
        self.context.arc (100, 80, 21, 0, 2 * mt.pi)
        self.context.fill ()
    
class PlanetVisibilityPage (BasePage):
    def __init__ (self, planetarium, index):
        super () .__init__ (planetarium, index, 'Planet Visibility')

    def draw (self):
        self.context.beginPath ()
        self.context.arc (100, 80, 41, 0, 2 * mt.pi)
        self.context.fill ()

class ControlPane:
    pass

class DisplayPane:
    pass

class TimeControls:
    pass

class SkyMapControls:
    pass

class SolarSystemControls:
    pass

class PlanetVisibilityControls:
    pass

planetarium = Planetarium ()