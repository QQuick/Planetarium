import pyact as pa
import pymui as pm

class Planetarium:
    def __init__ (self):
        pass

    def el (self):
        return pa.el ('div', None,
            pa.el (pm.TabContext, {'value': '0'},
                pa.el (pm.AppBar, {'position': 'static'},
                    pa.el (pm.TabList, {'value': '0'},
                        pa.el (pm.Tab, {'value': '0', 'label': 'Tab 1'}),
                        pa.el (pm.Tab, {'value': '1', 'label': 'Tab 2'})
                    )
                ),
                pa.el (pm.TabPanel, {'value': '0'}, 'Item 1'),
                pa.el (pm.TabPanel, {'value': '1'}, 'Item 2')
            )
        )

planetarium = Planetarium ()
pa.render (planetarium.el, None, 'root')
