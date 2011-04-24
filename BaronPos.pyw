__author__ = 'dennis'

import wx
from Gui.MainFrame import MainFrame

import logging

LOG_FILENAME = 'BaronPOS.log'

logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG)
log=logging.getLogger(__name__)

class BaronPOSApp(wx.App):
    def OnInit(self):
        self.frame = MainFrame(None)
        self.SetTopWindow(self.frame)
        self.frame.Show()
        return True

if __name__ == '__main__':
    app = BaronPOSApp(False)
    app.MainLoop()