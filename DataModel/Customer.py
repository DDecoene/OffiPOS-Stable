import wx
from wx.grid import Grid
from datetime import date, timedelta
import sqlite3
import ini

__author__ = 'dennis'

class Customer:
    def __init__(self):
        self.id = 0
        self.name = ""
        self.firstName = ""
        self.address = ""
        self.postalCode = ""
        self.city = ""
        self.telephone = ""
        self.birthDate = ini.MINDATE
        self.emailAddress = ""
        self.loyaltyCardNo = ""
        self.loyaltyPoints = 0
        self.loyaltyDiscount = 0
        self.loyaltyDiscountDate = ini.MINDATE
        self.dateRegistered = ini.MINDATE

    def GetCustomerFromLoyaltyCard(self, loyaltyCardNo):
        if loyaltyCardNo == "":
            return

        conn = sqlite3.connect(ini.DB_NAME, detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
        cur = conn.cursor()
        cur.execute(
            'select no, name,firstName,address,postalCode,city,telephone,birthDate,emailAddress,loyaltyCardNo,loyaltyPoints,loyaltyDiscount,loyaltyDiscountDate as "loyaltyDiscountDate [date]" from customer where loyaltyCardNo=?'
            , (loyaltyCardNo,))
        cust = cur.fetchone()

        if cust:
            self.id = cust[0]
            self.name = cust[1]
            self.firstName = cust[2]
            self.address = cust[3]
            self.postalCode = cust[4]
            self.city = cust[5]
            self.telephone = cust[6]
            self.birthDate = cust[7]
            self.emailAddress = cust[8]
            self.loyaltyCardNo = cust[9]
            self.loyaltyPoints = cust[10]
            self.loyaltyDiscount = cust[11]
            self.loyaltyDiscountDate = cust[12]
        else:
            self.loyaltyCardNo = loyaltyCardNo
            self.loyaltyPoints = ini.LOYALTYCARD_STARTING_POINTS
            self.Save()

    def AddLoyaltyPoints(self, ticketPoints):
        if self.CanPayDiscount():
            self.PayLoyaltyPoints()
        else:
            if self.loyaltyPoints:
                newTotal = self.loyaltyPoints + ticketPoints
            else:
                newTotal = ticketPoints

            conn = sqlite3.connect(ini.DB_NAME)
            cur = conn.cursor()
            cur.execute("update customer set loyaltyPoints = ? where loyaltyCardNo=?",
                    (newTotal, self.loyaltyCardNo, ))

            bonus = (newTotal - (newTotal % ini.LOYALTYCARD_POINTS_FOR_BONUS)) / ini.LOYALTYCARD_POINTS_FOR_BONUS
            cur.execute("update customer set loyaltyDiscount = ?, loyaltyDiscountDate = ? where loyaltyCardNo=?",
                    (ini.LOYALTYCARD_BONUS_AMOUNT * bonus, date.today(), self.loyaltyCardNo, ))

            conn.commit()

            self.loyaltyPoints = newTotal

    def GetPointsToDeductOnBonus(self):
        pointsToDeduct = (self.loyaltyDiscount / ini.LOYALTYCARD_BONUS_AMOUNT) * ini.LOYALTYCARD_POINTS_FOR_BONUS
        return pointsToDeduct

    def PayLoyaltyPoints(self):
        conn = sqlite3.connect(ini.DB_NAME)
        cur = conn.cursor()

        pointsToDeduct = self.GetPointsToDeductOnBonus()

        remainingPoints = self.loyaltyPoints - pointsToDeduct

        cur.execute("update customer set loyaltyPoints = ?, loyaltyDiscount = ? where loyaltyCardNo=?",
                (remainingPoints, 0, self.loyaltyCardNo, ))

        conn.commit()

        self.loyaltyPoints = remainingPoints

    def CanPayDiscount(self):
        return self.loyaltyDiscount and (date.today() - self.loyaltyDiscountDate >= timedelta(days=1))

    def GetCustomerTable(self):
        return CustomerTable()

    def GetAll(self):
        conn = sqlite3.connect(ini.DB_NAME, detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
        cur = conn.cursor()
        cur.execute(
            'select no, name,firstName,address,postalCode,city,telephone,birthDate,emailAddress,loyaltyCardNo,loyaltyPoints from customer')
        customers = cur.fetchall()
        return customers

    def FillFromId(self, customerId):
        conn = sqlite3.connect(ini.DB_NAME, detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
        cur = conn.cursor()
        cur.execute(
            """select no,
                      name,
                      firstName,
                      address,
                      postalCode,
                      city,
                      telephone,
                      birthDate as "birthDate [date]",
                      emailAddress,
                      loyaltyCardNo,
                      loyaltyPoints,
                      loyaltyDiscount,
                      loyaltyDiscountDate as "loyaltyDiscountDate [date]",
                      dateRegistered
                from customer where no=?"""
            , (customerId,))
        cust = cur.fetchone()

        if cust:
            self.id = cust[0]
            self.name = cust[1]
            self.firstName = cust[2]
            self.address = cust[3]
            self.postalCode = cust[4]
            self.city = cust[5]
            self.telephone = cust[6]
            self.birthDate = cust[7]
            self.emailAddress = cust[8]
            self.loyaltyCardNo = cust[9]
            self.loyaltyPoints = cust[10]
            self.loyaltyDiscount = cust[11]
            self.loyaltyDiscountDate = cust[12]
            self.dateRegistered = cust[13]

    def Save(self):
        conn = sqlite3.connect(ini.DB_NAME)
        cur = conn.cursor()

        if not self.id:
            #invoegen
            cur.execute(
                """insert into customer (
                      name,
                      firstName,
                      address,
                      postalCode,
                      city,
                      telephone,
                      birthDate,
                      emailAddress,
                      loyaltyCardNo,
                      loyaltyPoints,
                      loyaltyDiscount,
                      loyaltyDiscountDate,
                      dateRegistered)
                                    values
                                        (?,?,?,?,?,?,?,?,?,?,?,?,?)"""
                , (self.name,
                   self.firstName,
                   self.address,
                   self.postalCode,
                   self.city,
                   self.telephone,
                   self.birthDate,
                   self.emailAddress,
                   self.loyaltyCardNo,
                   self.loyaltyPoints,
                   self.loyaltyDiscount,
                   self.loyaltyDiscountDate,
                    self.dateRegistered))
            
            cur.execute("SELECT last_insert_rowid()")
            self.id = cur.fetchone()[0]
        else:
            #update
            cur.execute(
                """update customer set firstName = ?,
                                        name = ?,
                                        address = ?,
                                        postalCode = ?,
                                        city = ?,
                                        telephone = ?,
                                        birthDate = ?,
                                        emailAddress = ?,
                                        loyaltyCardNo=?,
                                         dateRegistered=?
                                         where no=?"""
                ,
                    (self.firstName,
                     self.name,
                     self.address,
                     self.postalCode,
                     self.city,
                     self.telephone,
                     self.birthDate,
                     self.emailAddress,
                     self.loyaltyCardNo,
                     self.dateRegistered,
                     self.id))

        conn.commit()


class CustomerTable(wx.grid.PyGridTableBase):
    def __init__(self):
        wx.grid.PyGridTableBase.__init__(self)
        self.colLabels = ["Nr.", "Voornaam", "Naam", "Adres", "Postcode", "Gemeente", "Telefoon", "Geboortedatum",
                          "Emailadres", "Klantkaart", "Punten"]

        self.customerLines = Customer().GetAll()

    def GetNumberRows(self):
        return len(self.customerLines)

    def GetNumberCols(self):
        return len(self.colLabels)

    def IsEmptyCell(self, row, col):
        return False

    def GetValue(self, row, col):
        return self.customerLines[row][col]

    def SetValue(self, row, col, value):
        pass

    def GetColLabelValue(self, col):
        return self.colLabels[col]

    def GetRowLabelValue(self, row):
        return self.rowLabels[row]

