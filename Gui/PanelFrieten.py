"""Subclass of PanelFrietenBase, which is generated by wxFormBuilder."""

import wx
from DataModel.Product import Product
from DataModel.ProductConstants import BaronProducts
from DataModel.Ticket import Ticket
import GeneratedGui

# Implementing PanelFrietenBase
class PanelFrieten( GeneratedGui.PanelFrietenBase ):
    def __init__( self, parent ):
        GeneratedGui.PanelFrietenBase.__init__( self, parent )

    def btnFrietGrootOnButtonClick (self, event):
        ticket = Ticket()
        ticket.AddTicketLine(BaronProducts["Frieten_Groot"])
        


