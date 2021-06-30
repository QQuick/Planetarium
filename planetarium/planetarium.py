import pyact as pa
import pymui as pm

class Planetarium:
    def __init__ (self):
        self.pages = (
            ('Sky Map', self.drawSkyMap),
            ('Solar System', self.drawSolarSystem),
            ('Planet Visibility', self.drawPlanetVisibility)
        )

        self.labelIndex, self.drawIndex = range (len (self.pages))
        pa.render (self.el, None, 'root')

    def tabEl (self, index):
        return pa.el (pm.Tab, {'value': str (index), 'label': self.pages [index][self.labelIndex], 'onClick': lambda: self.setPageIndex (index)})

    def tabPanelEl (self, index):
        return pa.el (pm.TabPanel, {'value': str (index)}, pa.el ('canvas', {'ref': self.canvasRef}))

    def el (self):
        self.canvasRef = pa.createRef ()
        self.pageIndex, self.setPageIndex = pa.useState (0)
        pa.useEffect (self.render)

        return pa.el ('div', None,
            pa.el (pm.TabContext, {'value': str (self.pageIndex)},
                pa.el (pm.AppBar, {'position': 'static'},
                    pa.el (pm.Tabs, {'value': str (self.pageIndex)},
                        *(self.tabEl (index) for index in range (len (self.pages)))
                    )
                ),
                *(self.tabPanelEl (index) for index in range (len (self.pages))),
            )
        )

    def render (self):
        self.context = self.canvasRef.current.getContext ('2d')
        self.pages [self.pageIndex][self.drawIndex]()

    def drawSkyMap (self):
        self.context.beginPath ()
        self.context.rect (20, 20, 20, 20)
        self.context.stroke ()
    
    def drawSolarSystem (self):
        self.context.beginPath ()
        self.context.rect (20, 20, 40, 40)
        self.context.stroke ()
    
    def drawPlanetVisibility (self):
        self.context.beginPath ()
        self.context.rect (20, 20, 60, 60)
        self.context.stroke ()
    
planetarium = Planetarium ()
