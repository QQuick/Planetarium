import pyact as pa
import pymui as pm

class Planetarium:
    def __init__ (self):
        pass

    def el (self):
        tabId, setTabId = pa.us ('sm')

        return pa.el ('div', None,
            pa.el (pm.TabContext, {'value': tabId},
                pa.el (pm.AppBar, {'position': 'static'},
                    pa.el (pm.Tabs, {'value': tabId},
                        pa.el (pm.Tab, {'value': 'sm', 'label': 'Sky Map', 'onClick': lambda: setTabId ('sm')}),
                        pa.el (pm.Tab, {'value': 'ss', 'label': 'Solar System', 'onClick': lambda: setTabId ('ss')}),
                        pa.el (pm.Tab, {'value': 'pv', 'label': 'Planet Visibility', 'onClick': lambda: setTabId ('pv')})
                    )
                ),
                pa.el (pm.TabPanel, {'value': 'sm'}, 'The Sky Map'),
                pa.el (pm.TabPanel, {'value': 'ss'}, 'The Solar System'),
                pa.el (pm.TabPanel, {'value': 'pv'}, pa.el ('canvas'))
            )
        )

planetarium = Planetarium ()
pa.render (planetarium.el, None, 'root')
