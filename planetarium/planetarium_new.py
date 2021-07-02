import pyact as pa
import pymui as pm

class Planetarium:
    def __init__ (self):
        self.Pages = (SkyMapPage, SolarSystemPage, PlanetVisibilityPage)
        self.pages = (Page (self, pageIndex) for pageIndex, Page in enumerate (self.Pages))
        
        self.setCurrentPage = (self.pages [0])
        pa.render (self.el, None, 'root')

    def setCurentPage (page):
        self.currentPage = page

    def el (self):
        return pa.el ('div', None,
            pa.el (pm.TabContext, {'value': '0'},
                pa.el (pm.AppBar, {'position': 'static'},

                    pa.el (pm.Tabs, {'value': '0'},
                        (page.tabEl () for page in self.pages)
                    )
                ),
                *(page.contentEl () for page in self.pages),
            )
        )

class Page:
    def __init__ (self, planetarium, index, title):
        self.planetarium = planetarium
        self.index = index
        self.title = title

    def tabEl (self):
        self.canvasRef = pa.createRef ()
        pa.useEffect (self.render)
        return pa.el (pm.Tab, {'value': str (self.index), 'label': self.title, 'onClick': lambda: self.planetarium.setCurrentPage (self)})

    def contentEl (self):
        return pa.el (pm.TabPanel, {'value': str (self.index)}, pa.el ('canvas', {'ref': self.canvasRef}))

    def render (self):
        self.context = self.canvasRef.current.getContext ('2d')
        self.draw ()

class SkyMapPage (Page):
    def __init__ (self, planetarium, index):
        super () .__init__ (planetarium, index, 'Sky Map')

    def draw (self):
        self.context.beginPath ()
        self.context.rect (20, 20, 20, 20)
        self.context.stroke ()

class SolarSystemPage (Page):
    def __init__ (self, planetarium, index):
        super () .__init__ (planetarium, index, 'Solar System')

    def draw (self):
        self.context.beginPath ()
        self.context.rect (20, 20, 40, 40)
        self.context.stroke ()
    
class PlanetVisibilityPage (Page):
    def __init__ (self, planetarium, index):
        super () .__init__ (planetarium, index, 'Planet Visibility')

    def draw (self):
        self.context.beginPath ()
        self.context.rect (20, 20, 60, 60)
        self.context.stroke ()

planetarium = Planetarium ()
