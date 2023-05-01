import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QWidget
from PyQt5.QtGui import QPixmap
import pymysql

local_pwd = input("Enter your local mysql password: ")
try:
    mydb = pymysql.connect(
        host="localhost",
        user="root",
        passwd=local_pwd,
        database='nu_recipes')
except Exception as mysqlErr:
    print(mysqlErr)
    exit()
curruser = ""

# defines welcome screen with login or create account
def goToWelcome():
    welcome = loginPage()
    widget.addWidget(welcome)
    widget.setCurrentIndex(widget.currentIndex() + 1)
    curruser = ""

# goes to create account signup screen
def goToCreate():
    create = createAccScreen()
    widget.addWidget(create)
    widget.setCurrentIndex(widget.currentIndex() + 1)


# goes to fill profile signup screen
def goToFillProfile():
    signup = fillProfileScreen()
    widget.addWidget(signup)
    widget.setCurrentIndex(widget.currentIndex() + 1)


# goes to login page
def goToLogin():
    login = actualLoginScreen()
    widget.addWidget(login)
    widget.setCurrentIndex(widget.currentIndex() + 1)


# goes to first page
def goToFirst():
    first = loginPage()
    widget.addWidget(first)
    widget.setCurrentIndex(widget.currentIndex() + 1)


# goes to main menu
def goToMainMenu():
    menu = mainSelectionMenuScreen()
    widget.addWidget(menu)
    widget.setCurrentIndex(widget.currentIndex() + 1)

# goes to my profile
def goToMyProfile():
    profile = myProfileScreen()
    widget.addWidget(profile)
    widget.setCurrentIndex(widget.currentIndex() + 1)

# goes to my recipes
def goToRecipes():
    recipesM = myRecipeMenu()
    widget.addWidget(recipesM)
    widget.setCurrentIndex(widget.currentIndex() + 1)

# goes to create recipes
def goToCreateRecp():
    createRecp = createRecpMenu()
    widget.addWidget(createRecp)
    widget.setCurrentIndex(widget.currentIndex() + 1)

# goes to chef list
def goToChefList():
    chefs = chefList()
    widget.addWidget(chefs)
    widget.setCurrentIndex(widget.currentIndex() + 1)

# stack confirm box on top of current window
def showConfirmBox():
    box = confirmRemoveDialog()
    widget.addWidget(box)
    widget.setCurrentIndex(widget.currentIndex() + 1)

# goes to menus
def goToMenus():
    viewMenus = menusScreen()
    widget.addWidget(viewMenus)
    widget.setCurrentIndex(widget.currentIndex() + 1)


class loginPage(QDialog):
    # methods: goToLogin()
    def __init__(self):
        super(loginPage, self).__init__()
        loadUi("loginPage.ui", self)
        # loginB is the name of the login button
        self.login.clicked.connect(goToLogin)
        self.createAccB.clicked.connect(goToCreate)


# defines the login screen
class actualLoginScreen(QDialog):
    def __init__(self):
        super(actualLoginScreen, self).__init__()
        loadUi("actualLoginScreen.ui", self)
        self.passwordField.setEchoMode(QtWidgets.QLineEdit.Password)  # hides typed text in passwordField
        self.loginB.clicked.connect(self.loginFunc)
        self.back.clicked.connect(goToFirst)

    def loginFunc(self):
        user = self.usernameField.text()  # gets entered username
        password = self.passwordField.text()  # gets entered password
        global curruser

        # login verification
        if len(user) == 0 or len(password) == 0:  # if username and password fields are empty
            self.errorLabel.setText("Please input all fields")
        else:
            try:
                mydb = pymysql.connect(
                    host="localhost",
                    user="root",
                    passwd=local_pwd,
                    database='nu_recipes')
                cur = mydb.cursor()
                loginVerify = "select getPassword(%s)"
                cur.execute(loginVerify, str(user))
                passResult = cur.fetchone()[0]
                mydb.commit()
                mydb.close()
                if passResult == password:
                    print("Successful login")
                    self.errorLabel.setText("")
                    curruser = str(user)
                    goToMainMenu()
                else:
                    self.errorLabel.setText("Invalid login")
            except Exception as e:
                self.errorLabel.setText(str(e))



class createAccScreen(QDialog):
    def __init__(self):
        super(createAccScreen, self).__init__()
        loadUi("createAcc.ui", self)
        self.passwordF.setEchoMode(QtWidgets.QLineEdit.Password)
        self.confirmPassF.setEchoMode(QtWidgets.QLineEdit.Password)
        self.createAcc.clicked.connect(self.signUpFunc)
        self.back.clicked.connect(goToFirst)

    def signUpFunc(self):
        user = self.usernameF.text()
        passw = self.passwordF.text()
        confirmPass = self.confirmPassF.text()
        global curruser

        if len(user) == 0 or len(passw) == 0 or len(confirmPass) == 0:
            self.errorLabel.setText("Please fill out all fields")

        elif passw != confirmPass:
            self.errorLabel.setText("These passwords do not match")

        else:
            try:
                mydb = pymysql.connect(
                    host="localhost",
                    user="root",
                    passwd=local_pwd,
                    database='nu_recipes')
                cur = mydb.cursor()
                query = "call newChef(%s, %s)"
                cur.execute(query, (str(user), str(passw)))
                mydb.commit()
                mydb.close()

                curruser = str(user)
                goToFillProfile()
            except Exception as e:
                self.errorLabel.setText(str(e))


class confirmRemoveDialog(QDialog):
    def __init__(self):
        super(confirmRemoveDialog, self).__init__()
        loadUi("confirmRemoveAccount.ui", self)
        self.confirmBox.accepted.connect(self.confirm)
        self.confirmBox.rejected.connect(self.cancel)

    def confirm(self):
        try:
            mydb = pymysql.connect(
                    host="localhost",
                    user="root",
                    passwd=local_pwd,
                    database='nu_recipes')
            cur = mydb.cursor()
            query = "call removeChef(%s)"
            cur.execute(query, str(curruser))
            mydb.commit()
            mydb.close()
        except Exception as e:
            print(str(e))
        goToWelcome()

    def cancel(self):
        goToMyProfile()


class fillProfileScreen(QDialog):
    def __init__(self):
        super(fillProfileScreen, self).__init__()
        loadUi("fillProfile.ui", self)
        self.createAcc.clicked.connect(self.createAccFunc)
        self.back.clicked.connect(goToCreate)

    def createAccFunc(self):
        fName = self.firstNameField.text()
        lName = self.lastNameField.text()
        loc = self.locationField.text()
        bio = self.bioField.text()

        if len(fName) == 0 or len(lName) == 0 or len(loc) == 0 or len(bio) == 0:
            self.errorLabel.setText("Please fill out all fields")

        elif fName.isalpha() != True or lName.isalpha() != True:
            self.errorLabel.setText("Numbers should not exist in your name")
        else:
            try:
                mydb = pymysql.connect(
                    host="localhost",
                    user="root",
                    passwd=local_pwd,
                    database='nu_recipes')
                cur = mydb.cursor()
                query = "call updateChef(%s, %s, %s, %s, %s)"
                cur.execute(query, (str(curruser), str(fName), str(lName), str(loc), str(bio)))
                mydb.commit()
                mydb.close()
            except Exception as e:
                self.errorLabel.setText(str(e))
            print("Connected")
            goToMainMenu()


class mainSelectionMenuScreen(QDialog):
    def __init__(self):
        super(mainSelectionMenuScreen, self).__init__()
        loadUi("mainSelectionMenu.ui", self)
        self.myProfile.clicked.connect(goToMyProfile)
        self.myRecipes.clicked.connect(goToRecipes)
        self.chefs.clicked.connect(goToChefList)
        self.myMenus.clicked.connect(goToMenus)
        self.back.clicked.connect(goToFirst)


class myProfileScreen(QDialog):
    editing = False
    
    def __init__(self):
        super(myProfileScreen, self).__init__()
        loadUi("myProfile.ui", self)
        self.back.clicked.connect(goToMainMenu)
        self.edit.clicked.connect(self.editProfile)
        self.deleteAccount.clicked.connect(self.removeAccount)

        try:
            mydb = pymysql.connect(
                host="localhost",
                user="root",
                passwd=local_pwd,
                database='nu_recipes')
            cur = mydb.cursor()
            query = "call getChefInfo(%s)"
            cur.execute(query, str(curruser))
            res = cur.fetchall()[0]
            mydb.commit()
            mydb.close()
            uname = res[0]
            fname = res[1]
            lname = res[2]
            bio = res[3]
            loc = res[4]
            self.uname.setText(uname)
            self.fname.setText(fname)
            self.lname.setText(lname)
            self.loc.setText(loc)
            self.bio.setText(bio)

        except Exception as e:
            self.errorLabel.setText(str(e))

    def removeAccount(self):
        showConfirmBox()

    def editProfile(self):
        if not self.editing:
            self.editing = True
            self.edit.setText("Done")
            self.fname.setEnabled(True)
            self.lname.setEnabled(True)
            self.loc.setEnabled(True)
            self.bio.setEnabled(True)
        else:
            self.editing = False
            self.edit.setText("Edit")
            self.fname.setEnabled(False)
            self.lname.setEnabled(False)
            self.loc.setEnabled(False)
            self.bio.setEnabled(False)

            # push new data to database
            try:
                mydb = pymysql.connect(
                    host="localhost",
                    user="root",
                    passwd=local_pwd,
                    database='nu_recipes')
                cur = mydb.cursor()
                query = "call updateChef(%s, %s, %s, %s, %s)"
                cur.execute(query, (curruser, str(self.fname.text()), str(self.lname.text()),
                                    str(self.bio.text()), str(self.loc.text())))
                mydb.commit()
                mydb.close()
            except Exception as e:
                self.errorLabel.setText(str(e))


class myRecipeMenu(QDialog):
    def __init__(self):
        super(myRecipeMenu, self).__init__()
        loadUi("myRecipesMenu.ui", self)
        self.loadData()
        self.createRecpB.clicked.connect(self.goNext)
        self.back.clicked.connect(self.goBack)
        numRows = 0

    def goBack(self):
        if self.numRows != 0:
            self.updateData()
        if len(self.errorLabel.text()) == 0:
            goToMainMenu()

    def goNext(self):
        if self.numRows != 0:
            self.updateData()
        if len(self.errorLabel.text()) == 0:
            goToCreateRecp()
        
    def updateData(self):
        try:
            self.errorLabel.setText('')
            recipes = []
            for row in range(0, self.numRows):
                rowData = []
                #retrieve row data
                for col in range(0, 9):
                    rowData.append(self.listOfRecp.item(row, col).text())
                #recipe name
                rname = rowData[0]
                if len(rname) == 0:
                    rname = None
                #serving size
                rsize = rowData[1]
                if len(rsize) == 0:
                    rsize = None
                else :
                    try:
                        rsize = int(rsize)
                    except Exception:
                        self.errorLabel.setText('"Serving Size" should be an integer')
                #total cost
                rcost = rowData[2]
                if len(rcost) == 0 or rcost == 'None':
                    rcost = None
                else :
                    try:
                        rcost = float(rcost)
                    except Exception:
                        self.errorLabel.setText('"Total Price" should be a decimal')
                #time to cook
                rtime = rowData[3]
                if len(rtime) == 0 or rtime == 'None':
                    rtime = None
                else :
                    try:
                        rtime = int(rtime)
                    except Exception:
                        self.errorLabel.setText('"Time To Cook" should be an integer')
                #directions
                rdir = rowData[4]
                if len(rdir) == 0:
                    rdir = None
                #verified
                rverified = rowData[5]
                if len(rverified) == 0:
                    rverified = None
                #ratings
                rratings = rowData[6]
                if len(rratings) == 0 or rratings == 'None':
                    rratings = None
                else:
                    try:
                        rratings = float(rratings)
                    except Exception:
                        self.errorLabel.setText('"Rating" should be an integer')
                #num of ratings
                rnumr = rowData[7]
                if len(rnumr) == 0:
                    rnumr = None
                else:
                    try:
                        rnumr = int(rnumr)
                    except Exception:
                        self.errorLabel.setText('"Number of ratings" should be an integer')
                #notes
                rnotes = rowData[8]
                if len(rnotes) == 0:
                    rnotes = None
                #dietary restrictions
                rres = rowData[8]
                if len(rres) == 0:
                    rres = None
                #check required fields
                if (rname is None) or (rsize is None) or (rdir is None):
                    self.errorLabel.setText('Please fill out all required fields')
                try:
                    mydb = pymysql.connect(
                        host="localhost",
                        user="root",
                        passwd=local_pwd,
                        database='nu_recipes')
                    cur = mydb.cursor()
                    update_query = "call updateRecipe(%s, %s, %s, %s, %s, %s, %s, %s, %s, NULL, %s, %s)"
                    cur.execute(update_query, (curruser, rname, rsize, rcost, rtime, rdir, rverified, rratings, rnumr, rnotes, rres))
                    mydb.commit()
                except Exception as e:
                    self.errorLabel.setText(str(e))
            mydb.close()
        except Exception as ex:
            print(str(ex))
            goToRecipes()


    def resizeColumns(self):
        for i in range(0,9):
            self.listOfRecp.setColumnWidth(i, 100)
        self.listOfRecp.setColumnWidth(7, 120)
        self.listOfRecp.setColumnWidth(9, 130)

    def loadData(self):
        try:
            mydb = pymysql.connect(
                host="localhost",
                user="root",
                passwd=local_pwd,
                database='nu_recipes')
            cur = mydb.cursor()
            q = "call myRecipesList(%s)"
            cur.execute(q, str(curruser))
            fa = cur.fetchall()
            mydb.commit()
            mydb.close()
            self.numRows = len(fa)
            self.listOfRecp.setRowCount(self.numRows)
            tableIndex = 0
            for row in fa:
                self.listOfRecp.setItem(tableIndex, 0, QtWidgets.QTableWidgetItem(row[0])) # Name
                self.listOfRecp.setItem(tableIndex, 1, QtWidgets.QTableWidgetItem(str(row[1]))) # Serving size
                self.listOfRecp.setItem(tableIndex, 2, QtWidgets.QTableWidgetItem(str(row[2]))) # Total price
                self.listOfRecp.setItem(tableIndex, 3, QtWidgets.QTableWidgetItem(str(row[3]))) # Time to cook
                self.listOfRecp.setItem(tableIndex, 4, QtWidgets.QTableWidgetItem(row[4])) # Directions
                self.listOfRecp.setItem(tableIndex, 5, QtWidgets.QTableWidgetItem(str(row[5]))) # Verified
                self.listOfRecp.setItem(tableIndex, 6, QtWidgets.QTableWidgetItem(str(row[6]))) # Rating
                self.listOfRecp.setItem(tableIndex, 7, QtWidgets.QTableWidgetItem(str(row[7]))) # Number of ratings
                self.listOfRecp.setItem(tableIndex, 8, QtWidgets.QTableWidgetItem(row[8])) # Notes
                self.listOfRecp.setItem(tableIndex, 9, QtWidgets.QTableWidgetItem(row[9])) # Dietary restrictions
                tableIndex += 1
            self.resizeColumns()
        except Exception as e:
            self.errorLabel.setText(str(e))
        
        
class createRecpMenu(QDialog):
    def __init__(self):
        super(createRecpMenu, self).__init__()
        loadUi("createRecipe.ui", self)
        self.back.clicked.connect(goToRecipes)
        self.createRecp.clicked.connect(self.addRecipe)

    def addRecipe(self):
        try:
            self.errorLabel.setText('')
            rname = self.dNameField.text()
            if len(rname) == 0:
                rname = None
            rsize = self.servingField.text()
            if len(rsize) == 0:
                rsize = None
            else :
                try:
                    rsize = int(rsize)
                except Exception:
                    self.errorLabel.setText('"Serving Size" should be an integer')
            rdir = self.dirField.text()
            if len(rdir) == 0:
                rdir = None
            rcost = self.totalCfield.text()
            if len(rcost) == 0:
                rcost = None
            else :
                try:
                    rcost = float(rcost)
                except Exception:
                    self.errorLabel.setText('"Total Cost" should be a decimal')
            rtime = self.ttcField.text()
            if len(rtime) == 0:
                rtime = None
            else :
                try:
                    rtime = int(rtime)
                except Exception:
                    self.errorLabel.setText('"Time To Cook" should be an integer')
            rnotes = self.notesField.text()
            if len(rnotes) == 0:
                rnotes = None
            rres = self.drField.text()
            if len(rres) == 0:
                rres = None
            if (rname is None) or (rsize is None) or (rdir is None):
                self.errorLabel.setText('Please fill out all required fields')
            else:
                mydb = pymysql.connect(
                    host="localhost",
                    user="root",
                    passwd=local_pwd,
                    database='nu_recipes')
                cur = mydb.cursor()
                query = "call newRecipe(%s, %s, %s, %s)"
                cur.execute(query, (curruser, rname, int(rsize), rdir))
                mydb.commit()
                update_query = "call updateRecipe(%s, %s, %s, %s, %s, %s, 0, NULL, NULL, NULL, %s, %s)"
                cur.execute(update_query, (curruser, rname, rsize, rcost, rtime, rdir, rnotes, rres))
                mydb.commit()
                mydb.close()
                goToRecipes()
        except Exception as e:
            self.errorLabel.setText(str(e))

            
class chefList(QDialog):
    def __init__(self):
        super(chefList, self).__init__()
        loadUi("chefList.ui", self)
        self.loadData()
        self.back.clicked.connect(goToMainMenu)
        numRows = 0

    def loadData(self):
        try:
            mydb = pymysql.connect(
                host="localhost",
                user="root",
                passwd=local_pwd,
                database='nu_recipes')
            cur = mydb.cursor()
            q = "call gourmetChefList()"
            cur.execute(q)
            fa = cur.fetchall()
            mydb.commit()
            mydb.close()
            self.numRows = len(fa)
            self.listOfChef.setRowCount(self.numRows)
            tableIndex = 0
            for row in fa:
                self.listOfChef.setItem(tableIndex, 0, QtWidgets.QTableWidgetItem(row[0])) # First Name
                self.listOfChef.setItem(tableIndex, 1, QtWidgets.QTableWidgetItem(row[1])) # Last Name
                self.listOfChef.setItem(tableIndex, 2, QtWidgets.QTableWidgetItem(row[2])) # Bio
                self.listOfChef.setItem(tableIndex, 3, QtWidgets.QTableWidgetItem(row[3])) # Location
                self.listOfChef.setItem(tableIndex, 4, QtWidgets.QTableWidgetItem(str(row[4]))) # Years in experience
                self.listOfChef.setItem(tableIndex, 5, QtWidgets.QTableWidgetItem(row[5])) # Restaurant
                self.listOfChef.setItem(tableIndex, 6, QtWidgets.QTableWidgetItem(str(row[6]))) # Years in business
                self.listOfChef.setItem(tableIndex, 7, QtWidgets.QTableWidgetItem(row[7])) # Restaurant Location
                tableIndex += 1
        except Exception as e:
            self.errorLabel.setText(str(e))

class menusScreen(QDialog):
    def __init__(self):
        super(menusScreen, self).__init__()
        loadUi("myMenusScreen.ui", self)
        self.back.clicked.connect(goToMainMenu)
        self.loadMenus()

    def loadMenus(self):
        mydb = pymysql.connect(
            host="localhost",
            user="root",
            passwd=local_pwd,
            database='nu_recipes')
        cur = mydb.cursor()
        menuQuery = "call getMenu(%s)"
        cur.execute(menuQuery, str(curruser))
        fa = cur.fetchall()
        mydb.commit()
        mydb.close()
        self.listOfMenu.setRowCount(len(fa))
        tableIndex = 0
        for r in fa:
            self.listOfMenu.setItem(tableIndex, 0, QtWidgets.QTableWidgetItem(r[0])) # Name
            self.listOfMenu.setItem(tableIndex, 1, QtWidgets.QTableWidgetItem(str(r[1]))) # serving_size
            self.listOfMenu.setItem(tableIndex, 2, QtWidgets.QTableWidgetItem(str(r[2]))) # Total price



app = QApplication(sys.argv)
widget = QtWidgets.QStackedWidget()
welcome = loginPage()
widget.addWidget(welcome)
widget.setFixedHeight(800)
widget.setFixedWidth(1200)
widget.show()
try:
    sys.exit(app.exec_())
except:
    print("Exiting")
