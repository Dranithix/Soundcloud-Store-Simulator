#-------------------------------------------------------------------------------
# Name:        breakBeats
# Purpose:     A SoundCloud-integrated music store simulation.
# Author:      Kenta Iwasaki
# Created:     08/03/2014
# Copyright:   (c) Kenta Iwasaki 2014
#-------------------------------------------------------------------------------

# Internal Python Module Imports
import sys, random, urllib.request, json

# PyQT Framework Module Imports
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtMultimedia import *
from PyQt5.QtGui import *
from PyQt5.QtNetwork import *

# PyQT Generated UI Module Imports
from ui_login import Ui_LoginDialog
from ui_register import Ui_RegisterDialog
from ui_main import Ui_MainWindow
from ui_checkout import Ui_CheckoutDialog
from ui_purchase import Ui_PurchaseHistory
from ui_profile import Ui_ProfileDialog
from ui_progress import Ui_ProgressDialog
from ui_manager import Ui_ManagerPanel

# Account status constants
NULL_ACCOUNT = -1
MANAGER_ACCOUNT = 0
CUSTOMER_ACCOUNT = 1

# SoundCloud API Key
soundcloud_api_key = "068f5a834914babe8da5876826cf2061"

# Initialized null variables for use in program
accounts = []
urls = []

currentAccount = None
songs = None

app = None
mainWindow = None
loginForm = None
registerForm = None
checkoutForm = None
purchaseHistory = None
profileDialog = None
managerPanel = None
progressDialog = None

# Represents the user's account.
class Account:
    # Constructor for an user's account. Contains pre-filled parameters in case of null account.
    def __init__(self, userId=-1, username=None, password=None, email=None, status=NULL_ACCOUNT, balance=0.0, orders=[], purchases=[], name="", birth="", country="", gender="Male"):
        self.userId = userId
        self.username = username
        self.password = password
        self.email = email
        self.status = status
        self.balance = balance

        self.orders = orders
        self.purchases = purchases

        self.name = name
        self.birth = birth
        self.country = country
        self.gender = gender

    # Deposits funds into the user's account, and updates the GUI.
    def fund(self, money):
        self.balance += money
        mainWindow.updateAccountInfo()

    # Determines if user account can afford a given liquid cost.
    def canAfford(self, money):
        return self.balance >= money

    # Withdraws funds from the user's account, and updates the GUI.
    def pay(self, money):
        self.balance -= money
        mainWindow.updateAccountInfo()

    # Determines if the user has a track in their Purchases or Cart.
    def hasTrack(self, song):
        check = False

        # Loop through Purchases and Carts to determine the parameter
        # 'song' has it's 'title' attribute equivalent to any song
        # in their Purchases or Cart.
        for purchase in self.purchases:
            if (song.title == purchase.title):
                check = True
        for order in self.orders:
            if (song.title == order.title):
                check = True
        return check

# Represent's a song entity loaded from SoundCloud.
class Song:
    # Constructor for a song entity.
    def __init__(self, cost, title, duration, artist, streamUrl, imageUrl):
        # If the song is a Free Download on SoundCloud, set price to $0.
        if ("free" in title.lower()):
            self.cost = 0.00
        else:
            self.cost = cost
        self.title = title
        self.duration = duration
        self.artist = artist
        self.streamUrl = streamUrl
        self.imageUrl = imageUrl

# Represent's the store's inventory list of songs.
class SongList:
    # Constructor for the store's inventory list of songs.
    def __init__(self):
        self.songList = []

    # Add's a song to the store's inventory.
    def add(self, track):
        add = True

        # Checks to make sure if the song is already in the store's inventory
        # by comparing the song's title.
        for song in self.songList:
            if (song.title == track.title):
                add = False
        if (add):
            self.songList.append(track)

    # Remove's a song from the store's inventory.
    def remove(self, song):
        return self.songList.remove(song)

    # Get's a song from the store's inventory by a given index.
    def get(self, index):
        return self.songList[index]

    # Returns the size of the store's inventory.
    def size(self):
        return len(self.songList)

    # Returns an enumerated version of the store's inventory
    # for looping accordingly by it's index and 'Song' container.
    def enum(self):
        return enumerate(self.songList)

    # Prints the songs available from the store's inventory via String Formatting.
    def print(self):
        for song in self.songList:
            print("Title: %s" % (song.title))
            print("Artist: %s" % (song.artist))
            print("Cost: %s" % (song.cost))
            print("")

# A pooled thread in memory which download's a list of URL's. Inherit's properties
# from QObject which allows for it's own signals and slot's to be defined independently.
class DownloadThread(QObject):
    # Defined signals that allows functions/procedures outside this pooled thread
    # to interact with it accordingly by it's defined parameters.
    response = pyqtSignal(bytes)
    progress = pyqtSignal(object)
    finished = pyqtSignal()

    # A slot that is connectable to a signal outside of this thread.
    # Download's a given list of URL's and reads them in chunks.
    @pyqtSlot(object)
    def process(self, urls):
        # Initiated variables for the download process.
        totalSize = 0
        totalBytesRead = 0

        # Hold's the URL's responses once a GET request has been sent to them via URLLib.
        responses = []
        try:
            # Reads the 'Content-Length'  header from the URL's responses and calculates the total size of their content.
            for url in urls:
                response = urllib.request.urlopen(url)
                totalSize += int(response.getheader('Content-Length').strip())
                responses.append(response)
            # Reads the content of the URL's in chunks of 8192 bytes.
            for response in responses:
                content = bytes()
                while (True):
                    chunk = response.read(8192)
                    totalBytesRead += len(chunk)
                    content += chunk
                    if (not chunk):
                        break
                    # Emits a signal outside of the thread so that the GUI may interpret
                    # the progress of the thread downloading from it's given URL's.
                    self.progress.emit(round((totalBytesRead / totalSize * 100), 1))
                response.close()
                self.response.emit(content)
        finally:
            # Emit's a signal to the GUI to state that the process is finished.
            self.finished.emit()

# A progress dialog that appears when the program downloads an item through multi-threading.
class ProgressDialog(QDialog):
    # A signal which allows the Progress Dialog to interact with the defined Download Thread.
    downloadRequest = pyqtSignal(object)

    # Constructor for a progress dialog. Initiates the pooled Download Thread
    # for retrieval of content online, and setups the context of the GUI.
    def __init__(self):
        QDialog.__init__(self)
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        self.context = Ui_ProgressDialog()
        self.context.setupUi(self)

        # Defines an instance of a Download Thread and connects callback functions
        # to the thread's defined signal's.
        self.downloadThread = DownloadThread()
        self.downloadRequest.connect(self.downloadThread.process)
        self.downloadThread.finished.connect(self.finishDownload)
        self.downloadThread.progress.connect(self.updateDownload)

        # Initialized null variables used by it's functions.
        self.file = None
        self.startup = True

    # Callback function for the Download Thread to write it's web content to file.
    def parseFile(self, data):
        self.file.write(data)

    # Callback function for the Download Thread to parse JSON Content from SoundCloud
    # and appends it to the store's inventory.
    def parseMusic(self, database):
        #print(database.decode("utf-8"))
        base = json.loads(database) # Decode's the content from SoundCloud by Unicode, and loads it as a JSON Object.
        tracks = base.get("tracks")
        for track in tracks:
            if (track.get("streamable") == True):
                songs.add(Song(1.99, track.get("title"), str(track.get("duration")), track.get("user").get("username"), track.get("stream_url"), str(track.get("artwork_url")).replace("large", "t200x200")))

        # Refreshes the Main Window's store inventory list.
        mainWindow.fillMusicList()

    # Callback function for the Download Thread once a download is complete in order to safely close a File instance, while
    # while hiding the Progress Dialog.
    def finishDownload(self):
        # Disconnects all signals from the Download Thread.
        self.downloadThread.response.disconnect()

        # Determines if the download is for a single file only.
        if (self.file != None):
            self.file.close()
            self.file = None
            QMessageBox.information(self, "Download Track", "Your track has successfully been downloaded.") # User-friendly message to state that a download is complete.

        # Reveals the Login Form if the requested download was performed on startup.
        if (self.startup):
            loginForm.show()
        self.hide()

    # Download's a single file and sets the Progress Dialog's task label.
    def downloadFile(self, url, savePath, label):
        # Reset's the Progress Dialog GUI and open's a File instance in memory.
        self.context.progressBar.setValue(0)
        self.file = open(savePath, "wb")
        self.startup = False

        # Intitiates a new thread and moves the Download process towards it.
        newThread = QThread(self)
        self.downloadThread.moveToThread(newThread)
        self.downloadThread.response.connect(self.parseFile)

        # Start's the new thread and emit's the File URL to the thread.
        newThread.start()
        self.downloadRequest.emit([url])

        self.context.label.setText(label)
        self.exec_()

    # Download's a set of SoundCloud URL's and sets the Progress Dialog's task label.
    def downloadMusic(self, urls, label, startup):
        # Reset's the Progress Dialog GUI.
        self.context.progressBar.setValue(0)
        self.startup = startup # Determines if the music is being downloaded on startup or runtime.

        # Intitiates a new thread and moves the Download process towards it.
        newThread = QThread(self)
        self.downloadThread.moveToThread(newThread)
        self.downloadThread.response.connect(self.parseMusic)

        # Start's the new thread and emit's the list of SoundCloud URL's to the thread.
        newThread.start()
        self.downloadRequest.emit(urls)

        self.context.label.setText(label)
        self.exec_()

    # A callback function for the Download Thread to set the Progress Bar on the GUI.
    def updateDownload(self, percent):
        self.context.progressBar.setValue(percent)

    # An overrided handle for the Progress Dialog so that the Dialog is not closable.
    def closeEvent(self, event):
        event.ignore()

# The manager panel for Manager-Status Accounts that allows them to add or remove
# SoundCloud sets from the store system.
class ManagerPanel(QDialog):

    # Constructor that setups the GUI context of the Manager Panel.
    def __init__(self):
        QDialog.__init__(self)
        self.context = Ui_ManagerPanel()
        self.context.setupUi(self)

        # Connects callback functions from the Manager Panel to the GUI buttons.
        self.context.btnAddSet.clicked.connect(self.addSet)
        self.context.btnRemoveSet.clicked.connect(self.removeSet)

    # Adds a SoundCloud set to the store system.
    def addSet(self):
        setUrl = QInputDialog.getText(self, "Add SoundCloud Set", "SoundCloud Set Link:", QLineEdit.Normal, "https://soundcloud.com/")[0]

        # Determines if the SoundCloud set URL is valid.
        if (not setUrl.startswith("https://soundcloud.com/") or "/sets/" not in setUrl):
            QMessageBox.information(self, "Add SoundCloud Set", "The set you have attempted to enter is invalid.")
        else:
            global urls
            urls.append(setUrl)
            self.updateSetList()

    # Removes a SoundCloud set from the store system by a manager's selection.
    def removeSet(self):
        selected = self.context.setList.currentItem()
        if (selected is not None):
            global urls
            urls.remove(selected.text())
            self.updateSetList()

    # Update's the GUI list on the Manager Panel with all of the present SoundCloud sets
    # in the system.
    def updateSetList(self):
        global urls
        self.context.setList.clear()
        for url in urls:
            self.context.setList.addItem(url)

# The profile dialog which allows the user to customize/look at their profile information.
class ProfileDialog(QDialog):
    # A lambda function that determines if the user is a male or female.
    genderCheck = lambda self: 0 if currentAccount.gender.startswith("Male") else 1

    # Constructor for the Profile Dialog which sets up the GUI context.
    def __init__(self):
        QDialog.__init__(self)
        self.context = Ui_ProfileDialog()
        self.context.setupUi(self)

        # Connects callback functions to the buttons in the GUI.
        self.context.btnSaveInfo.clicked.connect(self.saveInfo)

    # Set's the GUI fields to the current user's information.
    def updateDialog(self):
        self.context.txtUsername.setText(currentAccount.username)
        self.context.txtPassword.setText(currentAccount.password)
        self.context.txtEmail.setText(currentAccount.email)
        self.context.txtName.setText(currentAccount.name)
        self.context.txtBirth.setText(currentAccount.birth)
        self.context.txtCountry.setText(currentAccount.country)
        self.context.txtGender.setCurrentIndex(self.genderCheck())

    # Sets the current user's information according to the GUI fields.
    def saveInfo(self):
        currentAccount.username = self.context.txtUsername.text()
        currentAccount.password = self.context.txtPassword.text()
        currentAccount.email = self.context.txtEmail.text()
        currentAccount.name = self.context.txtName.text()
        currentAccount.birth = self.context.txtBirth.text()
        currentAccount.country = self.context.txtCountry.text()
        currentAccount.gender = self.context.txtGender.currentText()

        # A user-friendly message that states that their information has been updated.
        QMessageBox.information(self, "Profile Info", "Your profile information has been saved.")

# The login form where user's input their login details to their account.
class LoginForm(QDialog):

    # Constructor for setting up the login dialog's GUI context.
    def __init__(self):
        QDialog.__init__(self)
        self.context = Ui_LoginDialog()
        self.context.setupUi(self)

        # Connects callback functions to the buttons in the GUI.
        self.context.btnLogin.clicked.connect(self.login)
        self.context.btnRegister.clicked.connect(self.register)

    # Allow the user to login to the store based on their username and password.
    def login(self):
        global currentAccount

        # Determines if the account is in the database with the right details on the Login Form.
        accountFound = False
        for account in accounts:
            if (account.username == self.context.txtUsername.text() and account.password == self.context.txtPassword.text()):
                currentAccount = account
                accountFound = True
                break

        # Logs the user into the system if their inputted login details are valid.
        if (accountFound):
            # Greet's the user with a message box.
            QMessageBox.information(self, "Login", "Welcome to breakBeats, %s" % (currentAccount.username))

            # Updates the GUI based on their account details.
            purchaseHistory.updateHistory()
            checkoutForm.updateCheckout()
            mainWindow.updateAccountInfo()
            mainWindow.show()

            # Sets the fields of the login form null, and hides the overall form.
            self.context.txtUsername.setText("")
            self.context.txtPassword.setText("")
            self.hide()
        else:
            # A message stating that their login details are incorrect.
            QMessageBox.information(self, "Login", "Either your username or password is invalid.")

    # Opens up the Register Form.
    def register(self):
        registerForm.exec_()

# The register form where user's may register a new account.
class RegisterForm(QDialog):
    # Constructor for setting up the Register Form GUI's context.
    def __init__(self):
        QDialog.__init__(self)
        self.context = Ui_RegisterDialog()
        self.context.setupUi(self)

        # Connects callback functions to the buttons in the GUI.
        self.context.btnRegister.clicked.connect(self.register)

    # Register's the user's account according to the GUI fields, with it's initial account status being of a normal customer.
    def register(self):
        accounts.append(Account(len(accounts) + 1, self.context.txtUsername.text(), self.context.txtPassword.text(), self.context.txtEmail.text(), CUSTOMER_ACCOUNT, 0))
        QMessageBox.information(self, "Register", "You have successfully been registered!")

        # Nullifies the GUI context and hides away the Register Form.
        self.context.txtUsername.setText("")
        self.context.txtPassword.setText("")
        self.context.txtEmail.setText("")
        self.hide()

# The checkout dialog where user's may checkout their tracks in their store cart.
class CheckoutForm(QDialog):
    # Constructor for setting up the Checkout Form GUI's context.
    def __init__(self):
        QDialog.__init__(self)
        self.totalCost = 0.00
        self.context = Ui_CheckoutDialog()
        self.context.setupUi(self)

        # Connects callback functions to the buttons in the GUI.
        self.context.btnEmptyCart.clicked.connect(self.emptyCart)
        self.context.btnRemoveTrack.clicked.connect(self.deleteOrder)
        self.context.btnPurchase.clicked.connect(self.purchase)

    # Purchases all of the track's within the user's cart.
    def purchase(self):
        balance = self.totalCost

        # Determine if the user can afford all of the tracks in their cart.
        if (currentAccount.canAfford(balance)):
            # Determine if the user has anything in their cart.
            if (len(currentAccount.orders) > 0):
                # Withdraws money from their balance and adds all the tracks in their cart to their purchases.
                currentAccount.pay(balance)
                currentAccount.purchases.extend(currentAccount.orders)

                # Updates the GUI accordingly and empties their cart.
                purchaseHistory.updateHistory()
                QMessageBox.information(self, "Checkout", "Please check your Purchase History in order to download your track(s).")
                self.hide()
                self.emptyCart()
            else:
                QMessageBox.information(self, "Checkout", "You do not have any tracks in your cart.")
        else:
            QMessageBox.information(self, "Checkout", "You do not have enough money to purchase these track(s).")

    # Returns the present song selected within their cart. Return's null if no selection is made.
    def getCurrentSong(self):
        selectSong = None
        if (self.context.orderList.item(self.context.orderList.currentRow(), 1) != None):
            for index, song in songs.enum():
                if (song.title == self.context.orderList.item(self.context.orderList.currentRow(), 1).text()):
                    selectSong = song
        return selectSong

    # Calculate's the total cost for all of the track's in their cart.
    def calculateTotal(self):
        global currentAccount

        total = 0
        for song in currentAccount.orders:
            total += song.cost
        return total

    # Delete's the user's selected track from their cart.
    def deleteOrder(self):
        global currentAccount

        if (len(currentAccount.orders) > 0):
            currentAccount.orders.remove(self.getCurrentSong())
            self.updateCheckout()

    # Completely empties the cart.
    def emptyCart(self):
        del currentAccount.orders[:]
        self.updateCheckout()

    # Updates the store cart list and total cart cost on the GUI.
    def updateCheckout(self):
        # Clears all content from the store cart list
        self.context.orderList.clearContents()
        self.context.orderList.setRowCount(0)

        # Re-populates the store cart list.
        self.context.orderList.setRowCount(len(currentAccount.orders))
        for index, song in enumerate(currentAccount.orders):
            titleObj = QTableWidgetItem(song.title)
            durationObj = QTableWidgetItem(msToHms(int(song.duration)))
            artistObj = QTableWidgetItem(song.artist)
            priceObj = QTableWidgetItem(str(song.cost))

            # Set all the columns of the table to read-only.
            titleObj.setFlags(Qt.ItemIsEnabled)
            durationObj.setFlags(Qt.ItemIsEnabled)
            artistObj.setFlags(Qt.ItemIsEnabled)
            priceObj.setFlags(Qt.ItemIsEnabled)

            trackLabel = QLabel()
            # Loads a thumbnail for the track and places it as a table item.
            try:
                image = QPixmap()
                image.loadFromData(urllib.request.urlopen(song.imageUrl).read())
                image = image.scaled(QSize(64, 64), Qt.KeepAspectRatio, Qt.SmoothTransformation);
                trackLabel.setPixmap(image)
            except ValueError:
                pass

            # Sets all the widgets accordingly to the table.
            self.context.orderList.setCellWidget(index, 0, trackLabel)
            self.context.orderList.setItem(index, 1, titleObj)
            self.context.orderList.setItem(index, 2, durationObj)
            self.context.orderList.setItem(index, 3, artistObj)
            self.context.orderList.setItem(index, 4, priceObj)

        # Sets the width of the each column on the table.
        self.context.orderList.setColumnWidth(0, 64)
        self.context.orderList.setColumnWidth(1, 250)
        self.context.orderList.setColumnWidth(2, 60)
        self.context.orderList.setColumnWidth(3 , 150)
        self.context.orderList.setColumnWidth(4, 40)
        self.context.orderList.verticalHeader().setVisible(False)

        # Sets the total cart cost label on the GUI.
        self.totalCost = self.calculateTotal()
        self.context.totalCost.setText("$" + str(self.totalCost))

# The purchase history dialog where all user's may view their past purchases and download them.
class PurchaseHistory(QDialog):
    # Constructor for setting up the Purchase History GUI's context.
    def __init__(self):
        QDialog.__init__(self)
        self.context = Ui_PurchaseHistory()
        self.context.setupUi(self)

        # Connects callback functions to the buttons in the GUI.
        self.context.btnDownload.clicked.connect(self.downloadTrack)

    # Download's a purchased track selected by the user.
    def downloadTrack(self):
        # Determines if there are any purchases on the user's account.
        if (len(currentAccount.purchases) > 0):
            downloadChoice = self.getCurrentSong()

            # Open's up a Save File Dialog which determines where their purchased track will be downloaded to.
            saveRequest = QFileDialog.getSaveFileName(self, "Save Track", downloadChoice.title.replace("\"", ""), ".mp3")
            if (saveRequest[0] != ""):
                savePath = saveRequest[0]
                if (not savePath.endswith(".mp3")):
                    savePath += ".mp3"
                progressDialog.downloadFile(downloadChoice.streamUrl + "?client_id=068f5a834914babe8da5876826cf2061", savePath, "Currently downloading '%s'..." % (downloadChoice.title))
        else:
            QMessageBox.information(self, "Download Track", "You have no purchases.")

    # Returns the present song selected within their purchases. Return's null if no selection is made.
    def getCurrentSong(self):
        selectSong = None
        for index, song in songs.enum():
            if (song.title == self.context.orderList.item(self.context.orderList.currentRow(), 1).text()):
                selectSong = song
        return selectSong

    # Update's the purchased track list on the GUI depending on the user's previous purchases.
    def updateHistory(self):
        # Nullifies the content on the GUI.
        self.context.orderList.clearContents()
        self.context.orderList.setRowCount(0)

        # Re-populates the purchased track list on the GUI.
        self.context.orderList.setRowCount(len(currentAccount.purchases))
        for index, song in enumerate(currentAccount.purchases):
            titleObj = QTableWidgetItem(song.title)
            durationObj = QTableWidgetItem(msToHms(int(song.duration)))
            artistObj = QTableWidgetItem(song.artist)
            priceObj = QTableWidgetItem(str(song.cost))

            # Set all the columns of the table to read-only.
            titleObj.setFlags(Qt.ItemIsEnabled)
            durationObj.setFlags(Qt.ItemIsEnabled)
            artistObj.setFlags(Qt.ItemIsEnabled)
            priceObj.setFlags(Qt.ItemIsEnabled)

            trackLabel = QLabel()
            # Loads a thumbnail for the track and places it as a table item.
            try:
                image = QPixmap()
                image.loadFromData(urllib.request.urlopen(song.imageUrl).read())
                image = image.scaled(QSize(64, 64), Qt.KeepAspectRatio, Qt.SmoothTransformation);
                trackLabel.setPixmap(image)
            except ValueError:
                pass

            # Sets all the widgets accordingly to the table.
            self.context.orderList.setCellWidget(index, 0, trackLabel)
            self.context.orderList.setItem(index, 1, titleObj)
            self.context.orderList.setItem(index, 2, durationObj)
            self.context.orderList.setItem(index, 3, artistObj)
            self.context.orderList.setItem(index, 4, priceObj)

        # Sets the width of the each column on the table.
        self.context.orderList.setColumnWidth(0, 64)
        self.context.orderList.setColumnWidth(1, 250)
        self.context.orderList.setColumnWidth(2, 60)
        self.context.orderList.setColumnWidth(3 , 150)
        self.context.orderList.setColumnWidth(4, 40)
        self.context.orderList.verticalHeader().setVisible(False)

# The Main Window for the entire store where user's can preview their music or manage their account.
class MainWindow(QMainWindow):
    # Constructor which set's up the Main Window's GUI context.
    def __init__(self):
        QMainWindow.__init__(self)
        self.toggleHistory = False
        self.context = Ui_MainWindow()
        self.context.setupUi(self)

        # Define's a media player that play's music and connects the seeker bar to it's seek position.
        self.player = QMediaPlayer()
        self.player.positionChanged.connect(self.updateSeeker)

        # Connects callback functions to the buttons in the GUI.
        self.context.btnPlay.clicked.connect(self.playMusic)
        self.context.btnPause.clicked.connect(self.pauseMusic)
        self.context.btnStop.clicked.connect(self.stopMusic)
        self.context.btnShuffle.clicked.connect(self.shuffleMusic)
        self.context.btnHistory.clicked.connect(self.switchHistory)
        self.context.btnClearHistory.clicked.connect(self.clearHistory)
        self.context.btnFund.clicked.connect(self.fundAccount)
        self.context.btnRefreshStore.clicked.connect(self.refreshStore)
        self.context.btnBuy.clicked.connect(self.buyMusic)
        self.context.btnCheckout.clicked.connect(self.checkout)
        self.context.btnPurchaseHistory.clicked.connect(self.showPurchases)
        self.context.seekSlider.sliderMoved.connect(self.setPosition)
        self.context.btnProfile.clicked.connect(self.showProfile)
        self.context.btnManager.clicked.connect(self.showManagerPanel)
        self.context.btnLogout.clicked.connect(self.logout)

        # Connects the history list to the media player.
        self.historyCount = 0
        self.context.btnClearHistory.setVisible(False)
        self.context.historyList.setVisible(False)
        self.context.historyList.setColumnWidth(0, 250)
        self.context.historyList.setColumnWidth(1, 60)
        self.context.historyList.setColumnWidth(2 , 150)
        self.context.historyList.verticalHeader().setVisible(False)
        self.context.historyList.cellDoubleClicked.connect(self.selectHistory)

        # Update's the GUI according to the current user's account info.
        self.updateAccountInfo()

    # Log's the user out of the system and saves the store's database.
    # Also pauses the music in order to prevent any interference when logging
    # into a different account from the previous login.
    def logout(self):
        global currentAccount
        currentAccount = Account()
        saveDatabase()

        loginForm.show()
        self.stopMusic()
        self.hide()

    # Updates and shows the manager panel if it is not already visible.
    def showManagerPanel(self):
        if (not managerPanel.isVisible()):
            managerPanel.updateSetList()
            managerPanel.exec_()

    # Updates and shows the profile dialog if it is not already visible.
    def showProfile(self):
        if (not profileDialog.isVisible()):
            profileDialog.updateDialog()
            profileDialog.exec_()

    # Updates and shows the purchase dialog if it is not already visible.
    def showPurchases(self):
        if (not purchaseHistory.isVisible()):
            purchaseHistory.updateHistory()
            purchaseHistory.exec_()

    # Updates and shows the checkout dialog if it is not already visible.
    def checkout(self):
        if (not checkoutForm.isVisible()):
            checkoutForm.updateCheckout()
            checkoutForm.exec_()

    # Returns the present song selected within the store's list. Return's null if no selection is made.
    def getCurrentSong(self):
        selectSong = None
        for index, song in songs.enum():
            if (song.title == self.context.storeList.item(self.context.storeList.currentRow(), 0).text()):
                selectSong = song
        return selectSong

    # Add's a track to the user's cart according to their selection.
    def buyMusic(self):
        currentSong = self.getCurrentSong()

        # Determines if the user already has the track in their cart or purchases.
        if (not currentAccount.hasTrack(currentSong)):
            # Determines if there are more than 10 tracks in their cart.
            if (len(currentAccount.orders) == 9):
                QMessageBox.information(self, "Buy Track", "You can only purchase 10 tracks at a time.")
            else:
                # Display a confirmation message stating whether or not the user wants to buy the song.
                reply = QMessageBox.question(self, "Buy Track",
                     "Are you sure you would like to add\n%s\nto your cart for $%s?" % (currentSong.title, str(currentSong.cost)), QMessageBox.Yes, QMessageBox.No)
                if (reply == QMessageBox.Yes):
                    currentAccount.orders.append(currentSong)
                    checkoutForm.updateCheckout()
        else:
            QMessageBox.information(self, "Buy Track", "This track is already in your cart, or you have already bought the track.")

    # Re-populates the store's inventory list.
    def refreshStore(self):
        loadMusic(False)

    # Funds the user's balance with an inputted amount of money.
    def fundAccount(self):
        try:
            currentAccount.fund(float(QInputDialog.getText(self, "Fund Account", "Amount:", QLineEdit.Normal, "0")[0]))
            QMessageBox.information(self, "Fund Account", "Your account has been successfully funded.")
        except ValueError:
            QMessageBox.information(self, "Fund Account", "The amount you wished to fund is invalid.")

    # Clear's the history list.
    def clearHistory(self):
        self.context.historyList.clearContents()
        self.context.historyList.setRowCount(0)
        self.historyCount = 0

    # Toggles between the history list and store inventory list.
    def switchHistory(self):
        self.toggleHistory = not self.toggleHistory
        self.context.historyList.setVisible(self.toggleHistory)
        self.context.btnClearHistory.setVisible(self.toggleHistory)
        self.context.storeList.setVisible(not self.toggleHistory)
        self.context.btnRefreshStore.setVisible(not self.toggleHistory)
        if (self.toggleHistory):
            self.context.btnHistory.setText("Browse Store")
        else:
            self.context.btnHistory.setText("Play History")

    # Updates the GUI according to the current user's info.
    def updateAccountInfo(self):
        global currentAccount
        self.context.cashLabel.setText("$%.2f" % (currentAccount.balance))

        # Set's the Manager Panel button visible if the user is a manager.
        self.context.btnManager.setVisible(currentAccount.status == MANAGER_ACCOUNT)

    # Re-populates the store inventory list.
    def fillMusicList(self):
        # Nullifies the present content in the store's inventory list.
        self.context.storeList.clearContents()

        # Re-populates the store list.
        self.context.storeList.setRowCount(songs.size())
        self.context.storeList.setSortingEnabled(False)
        for index, song in songs.enum():
            titleObj = QTableWidgetItem(song.title)
            durationObj = QTableWidgetItem(msToHms(int(song.duration)))
            artistObj = QTableWidgetItem(song.artist)
            priceObj = QTableWidgetItem(str(song.cost))

            # Set's each widget on the store list as read-only.
            titleObj.setFlags(Qt.ItemIsEnabled)
            durationObj.setFlags(Qt.ItemIsEnabled)
            artistObj.setFlags(Qt.ItemIsEnabled)
            priceObj.setFlags(Qt.ItemIsEnabled)

            self.context.storeList.setItem(index, 0, titleObj)
            self.context.storeList.setItem(index, 1, durationObj)
            self.context.storeList.setItem(index, 2, artistObj)
            self.context.storeList.setItem(index, 3, priceObj)

        # Defines the store column widths.
        self.context.storeList.setColumnWidth(0, 250)
        self.context.storeList.setColumnWidth(1, 60)
        self.context.storeList.setColumnWidth(2 , 150)
        self.context.storeList.setSortingEnabled(True)
        self.context.storeList.verticalHeader().setVisible(False)
        self.context.storeList.cellDoubleClicked.connect(self.selectSong)

        # Shows the user how many track's are in stock.
        self.context.trackCount.setText("There are currently %s tracks in stock." % (str(songs.size())))

    # A callback function that handles whenever a song is double clicked within the store inventory list.
    def selectSong(self, row, column):
        selectSong = self.getCurrentSong()
        if (selectSong != None): # Determine if a selection is present.
            self.context.seekSlider.setMaximum(int(selectSong.duration))
            self.context.songName.setText(selectSong.title)

            # Play's the song.
            self.setMusic(selectSong.streamUrl, True)

            # Shows the user the song's thumbnail if the song has a thumbnail. Otherwise shows a blank canvas.
            if (selectSong.imageUrl != None):
                try:
                    image = QPixmap()
                    image.loadFromData(urllib.request.urlopen(selectSong.imageUrl).read())
                    image = image.scaled(QSize(225, 225), Qt.KeepAspectRatio, Qt.SmoothTransformation);
                    scene = QGraphicsScene(self.context.songImage)
                    scene.addPixmap(image)
                    self.context.songImage.setScene(scene)
                except ValueError:
                    image = QPixmap()
                    scene = QGraphicsScene(self.context.songImage)
                    scene.addPixmap(image)

                    self.context.songImage.setScene(scene)

                # Add's the song to the history.
                self.addHistory(selectSong)

    # Add's an entry to the history list.
    def addHistory(self, song):
        tObj = QTableWidgetItem(song.title)
        dObj = QTableWidgetItem(msToHms(int(song.duration)))
        aObj = QTableWidgetItem(song.artist)
        pObj = QTableWidgetItem(str(song.cost))

        # Set the widget for the history column to be read-only.
        tObj.setFlags(Qt.ItemIsEnabled)
        dObj.setFlags(Qt.ItemIsEnabled)
        aObj.setFlags(Qt.ItemIsEnabled)
        pObj.setFlags(Qt.ItemIsEnabled)

        self.context.historyList.setRowCount(self.historyCount + 1)
        self.context.historyList.setItem(self.historyCount, 0, tObj)
        self.context.historyList.setItem(self.historyCount, 1, dObj)
        self.context.historyList.setItem(self.historyCount, 2, aObj)
        self.context.historyList.setItem(self.historyCount, 3, pObj)
        self.historyCount += 1

    # A callback function that handles whenever a song is double clicked within the history list.
    def selectHistory(self, row, column):
        selectSong = self.getCurrentSong()
        if (selectSong != None): # Determines if a selection is present.
            self.context.seekSlider.setMaximum(int(selectSong.duration))
            self.context.songName.setText(selectSong.title)

            # Play's the song.
            self.setMusic(selectSong.streamUrl, True)

            # Shows the user the song's thumbnail if the song has a thumbnail. Otherwise shows a blank canvas.
            if (selectSong.imageUrl != None):
                try:
                    image = QPixmap()
                    image.loadFromData(urllib.request.urlopen(selectSong.imageUrl).read())
                    image = image.scaled(QSize(225, 225), Qt.KeepAspectRatio, Qt.SmoothTransformation);
                    scene = QGraphicsScene(self.context.songImage)
                    scene.addPixmap(image)
                    self.context.songImage.setScene(scene)
                except ValueError:
                    image = QPixmap()
                    scene = QGraphicsScene(self.context.songImage)
                    scene.addPixmap(image)
                    self.context.songImage.setScene(scene)

    # Play's or sets a song on the media player according to a given stream URL.
    def setMusic(self, streamUrl, play=False):
        self.player.setMedia(QMediaContent(QUrl(streamUrl + "?client_id=068f5a834914babe8da5876826cf2061")))
        if (play):
            self.playMusic()

    # A callback function that binds the media player's seek position to the seek slider's position.
    def setPosition(self):
        self.player.setPosition(self.context.seekSlider.sliderPosition())

    # Update's the seek slider's position as the media player streams a song.
    # Also update's the audio position label to the media player.
    def updateSeeker(self, position):
        self.context.seekSlider.setSliderPosition(position)
        self.context.audioPosition.setText(msToHms(position))

    # Randomly play's a song in the store's inventory list.
    def shuffleMusic(self):
        randomRow = random.randint(0, self.context.storeList.rowCount())
        self.context.storeList.setCurrentCell(randomRow, 0)
        self.selectSong(randomRow, 0)

    # Tell's the media player to play.
    def playMusic(self):
        self.player.play()

    # Tell's the media player to pause itself.
    def pauseMusic(self):
        self.player.pause()

    # Tell's the media player to pause itself and seek the current media towards it's
    # initial point.
    def stopMusic(self):
        self.player.stop()

# Convert's milliseconds into a user-friendly format. Used for interpreting
# the duration of a song into a user-friendly format.
def msToHms(timeMs):
    s = timeMs / 1000
    m, s = divmod(s, 60)
    h, m = divmod(m, 60)
    return '%02d:%02d:%02d' % (h, m, s)

# Load's the entire store database into memory.
def loadDatabase():
    global accounts, urls

    # Open's all database files.
    dbFile = open("accounts.txt", "r")
    historyDb = open("history.txt", "r")
    storeDb = open("store.txt", "r")

    # Read's and store's the SoundCloud sets in the database.
    for url in storeDb.readlines():
        if ("/sets/" in url):
            urls.append(url.strip())

    # Reads all the user's accounts and appends them into a series of lists.
    for index, account in enumerate(dbFile.readlines()):
        # All account data is splitted through the separator ':'
        acc = account.split(":")

        # Determines if the present line in the account database has a total of 9 fields.
        if (len(acc) == 9):
            purchases = []
            orders = []
            for line in historyDb.readlines():
                # All history data is splitted through the separator '%'.
                data = line.split("%")
                if (data[0] == "purchase"):
                     if (data[1] == str(index)):
                        purchases.append(Song(float(data[2]), data[3], data[4], data[5], data[6], data[7]))
                elif (data[0] == "order"):
                    if (data[1] == str(index)):
                        orders.append(Song(float(data[2]), data[3], data[4], data[5], data[6], data[7]))
            accounts.append(Account(index, acc[0], acc[1], acc[2], int(acc[3]), float(acc[4]), orders, purchases, acc[5], acc[6], acc[7], acc[8]))

    # Closes all handles to the database file.
    dbFile.close()
    historyDb.close()
    storeDb.close()

# Load's all SoundCloud sets from database in a separate thread context and displays a Progress Dialog.
def loadMusic(startup):
    global songs, urls, soundcloud_api_key

    songs = SongList()
    sets = []
    for url in urls:
        sets.append("http://api.soundcloud.com/resolve.json?url=" + url + "&client_id=" + soundcloud_api_key)

    # Calls the Progress Dialog to start downloading the SoundCloud sets.
    progressDialog.downloadMusic(sets, "Downloading SoundCloud Database...", startup)

# Save's all account information and SoundCloud Set information into the text-based databases.
def saveDatabase():
    # Open's all database files.
    dbFile = open("accounts.txt", "w")
    historyDb = open("history.txt", "w")
    storeDb = open("store.txt", "w")

    # Write's all account data and history data linked to the account to the account database.
    for account in accounts:
        dbFile.write("%s:%s:%s:%i:%.2f:%s:%s:%s:%s\n" % (account.username, account.password, account.email, account.status, account.balance, account.name, account.birth, account.country, account.gender))
        for purchase in account.purchases:
            historyDb.write("purchase%" + str(account.userId) + "%" + str(purchase.cost) + "%" + purchase.title + "%" + purchase.duration + "%" + purchase.artist + "%" + purchase.streamUrl + "%" + purchase.imageUrl + "\n")
        for order in account.orders:
            historyDb.write("order%" + str(account.userId) + "%" + str(purchase.cost) + "%" + order.title + "%" + order.duration + "%" + order.artist + "%" + order.streamUrl + "%" + order.imageUrl + "\n")
    # Write's all present SoundCloud sets in the store system to the store database.
    for url in urls:
        storeDb.write(url + "\n")
    dbFile.close()
    historyDb.close()
    storeDb.close()

# A callback function that stop's the music and saves the database when the application is closed.
def dispose():
    mainWindow.stopMusic()
    saveDatabase()

# Sets a blank instance for the current account.
currentAccount = Account()

# Initiates the overall GUI's base context, and connects a dispose hook for disposing of unnecessary resources on close.
app = QApplication(sys.argv)
app.aboutToQuit.connect(dispose)

# Initiates an instance of all present dialog's/windows in the application.
mainWindow = MainWindow()
loginForm = LoginForm()
registerForm = RegisterForm()
checkoutForm = CheckoutForm()
purchaseHistory = PurchaseHistory()
profileDialog = ProfileDialog()
progressDialog = ProgressDialog()
managerPanel = ManagerPanel()

# Load both the store database and music database from SoundCloud.
loadDatabase()
loadMusic(True)

# Execute the application and allow the application to control the Python interpreter's exit hook.
sys.exit(app.exec_())