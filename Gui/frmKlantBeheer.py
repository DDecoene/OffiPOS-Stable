from DataModel.Customer import Customer
import GeneratedGui
from Gui.dlgCustomerEdit import dlgCustomerEdit
import wx

__author__ = 'dennis'

class frmKlantBeheer(GeneratedGui.dlgKlantBeheerBase):
    def UpdateForm(self ):

        grid = self.grdCustomer
        table = Customer().GetCustomerTable(self.sortingCol)
        grid.SetTable(table)
        rows = table.GetNumberRows()
        grid.MakeCellVisible(rows-1, 1)
        grid.EnableEditing(False)
        grid.SetSelectionMode(wx.grid.Grid.SelectRows)
        grid.SetRowLabelSize(0)
        grid.AutoSizeColumns()
        self.Fit()

    def __init__( self, parent ):
        GeneratedGui.dlgKlantBeheerBase.__init__(self, parent)
        self.customer = Customer()

        self.sortingCol = 9

        self.UpdateForm()


    def btnNieuwOnButtonClick( self, event ):
        dlgBeheer = dlgCustomerEdit(self)
        dlgBeheer.ShowModal()

        self.UpdateForm()

    def btnBewerkOnButtonClick( self, event ):
        row = self.grdCustomer.GetGridCursorRow()
        id = int(self.grdCustomer.GetCellValue(row,0))

        dlgBeheer = dlgCustomerEdit(self)
        dlgBeheer.SetCustomer(id)
        dlgBeheer.ShowModal()

        self.UpdateForm()

    def btnVerwijderOnButtonClick( self, event ):
        row = self.grdCustomer.GetGridCursorRow()
        id = int(self.grdCustomer.GetCellValue(row,0))

        dlg = wx.MessageDialog(self, 'Bent u zeker dat u klant {0:} wilt verwijderen?'.format(id),
          'Verwijderen', wx.YES | wx.NO | wx.CANCEL | wx.ICON_INFORMATION)

        try:
            result = dlg.ShowModal()
            if  result == wx.ID_YES:
                cust = Customer()
                cust.FillFromId(id)
                cust.Delete()
        finally:
            dlg.Destroy()

        self.UpdateForm()

    def grdCustomerOnGridLabelLeftClick( self, event ):
        self.sortingCol = event.GetCol()
        self.UpdateForm()
        
    def btnSelectOnButtonClick(self, event):
        row = self.grdCustomer.GetGridCursorRow()
        id = int(self.grdCustomer.GetCellValue(row,0))
        self.customer.FillFromId(id)
        
        self.Close()




