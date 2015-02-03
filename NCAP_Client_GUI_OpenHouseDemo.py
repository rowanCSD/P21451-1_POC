#Author: Tom Morris
#Date: 10.17.2014
#Description: The following program creates a Graphical User Interface to be
#             used with an NCAP Client module.  This version of the GUI will
#             be used for an open house at Rowan University on October 25th
#             2014. This GUI is compatable with NCAP Client Lite Lite v2

#-------------------------------NEEDED LIBRARIES----------------------------
#system libraries
import sys
import socket
import threading
from time import sleep

#Gui Libraries
from Tkinter import *
import tkMessageBox

#communication libraries
import smtplib
from email.mime.text import MIMEText

#-------------------------------GLOBAL VARIABLES----------------------------
#IP Addresses
global TOMM  #datatype string
global ANAS  #datatype string
global KEITH #datatype string
global JEFF  #datatype string
global TOMS  #dattype string

#port and ncap id
global NCAP_COMM_PORT       #data type: int
global MY_CLIENT_NUMBER     #data type: string

#for stopping threads
global KILL_THREAD  #data type: bool

#variable for dropdown menu
global var

#variables for email and text message communication
global EMAIL
global EMAIL_SERVER
global TEXT_PORT
global EMAIL_PASSWORD
global FROM
global TEXT_RECEIVER_1
global TEXT_RECEIVER_2
global TEXT_RECEIVER_3

#global GUI Variables (for display so they need be accessed globally)
global SSN_GUI
global InfoDisplayFrame
global InfoLogListBox
global InfoDisplayFrame
global XDCRControlFrame
global ServerConnectLabel

#--------------------------INITIALIZE GLOBAL VARIABLES----------------------
#IP Addresses
TOMM =  "192.168.1.200"
ANAS =  "192.168.1.201"
KEITH = "192.168.1.202"
JEFF =  "192.168.1.203"
TOMS =  "192.168.1.204"

#Relevant Ports
NCAP_COMM_PORT = 5005 #data type: integer
TEXT_PORT = 465 #datatype integer

#Relevant Identifiers
MY_CLIENT_NUMBER = '1' #data type: string
KILL_THREAD = False #data type: bool

#initializes email and text communication variables
EMAIL = "rucsdsnn@gmail.com"
EMAIL_SERVER = "smtp.gmail.com"
EMAIL_PASSWORD = "raspberrypi"
FROM = EMAIL[:EMAIL.find("@")]

#phone number list to receive text message updates (verizon only)
TEXT_RECEIVER_1 = "8563819908@vtext.com" #Lindsey Turse
TEXT_RECEIVER_2 = "3018213403@vtext.com" #Jeff Welder

#--------------------------GUI Display Initializations----------------------
#Creates the GUI Main Frame (GLOBALLY ACCESSABLE)
SSN_GUI = Tk()
SSN_GUI.geometry("720x540") 
SSN_GUI.title("Smart Transducer Networks - Rowan University")
SSN_GUI.configure(bg = "brown")

#creates info display log (GLOBALLY ACCESSABLE)
InfoDisplayFrame = Frame(SSN_GUI, height = 250, width = 300, bg = "brown")
InfoDisplayFrame.configure(highlightthickness = 2)
InfoDisplayFrame.configure(highlightbackground = "yellow")
InfoDisplayFrame.place(x = 35, y = 70)

#creates Log List Box (GLOBALLY ACCESSABLE)
InfoLogListBox = Listbox(InfoDisplayFrame)
InfoLogListBox.configure(height = 15, width= 37)
InfoLogListBox.insert(1, "SSN Session Log: ")

#creates transducer control frame (GLOBALLY ACCESSABLE)
XDCRControlFrame = Frame(SSN_GUI, height = 150, width = 300, bg = "brown")
XDCRControlFrame.configure(highlightthickness = 2)
XDCRControlFrame.configure(highlightbackground = "yellow")
XDCRControlFrame.place(x = 35, y = 360)

#creates Server connect label (GLOBALLY ACCESSABLE)
ServerConnectLabel = Label(text = "Need to Connect to Server", fg = "yellow", bg = "brown")
ServerConnectLabel.configure(font = ("Times", 12))
ServerConnectLabel.place(x = 375, y = 65)

#------------------------NCAP CLIENT FUNCTION DEFINITIONS-------------------
#this is a void function that acts as the NCAP Client Main Function
def NCAP_Client_Main():
    return 
#end function NCAP_Client_Main

#This function is for receiving UDP messages 
def UDP_Receive(receive_IP, listening_PORT):

    KILL_THREAD = False

    #defines an error flag variable that will 
    Error_Flag = 0

    #defines a class for a timeout thread
    class New_Thread(threading.Thread):
        def run(self):
            counter = 0
            while counter < 10:
                sleep(1)
                if KILL_THREAD == False:
                    counter = counter + 1
                    if counter == 9:
                        Error_Flag = "666"
                        UDP_Send(TOMS, NCAP_COMM_PORT, Error_Flag)
                else:
                    counter = 11

    #creates new thread
    Thread_1 = New_Thread()
    #begins timeout thread
    Thread_1.start()
            
    #creats a socket for receiving messages
    SOCKET_RECEIVE = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    #listens on given port for a message
    SOCKET_RECEIVE.bind((receive_IP, listening_PORT))

    #assigns message to 'data', and prints 'data'
    data = '0'
    while data == '0':
        data, addr = SOCKET_RECEIVE.recvfrom(1024)
        if data == "666":
            data = "Error!, Connection has timed out."
        KILL_THREAD = True

    return data

#end UDP_Receive

#this function is for sending UDP messages
def UDP_Send(target_IP,target_PORT,MESSAGE):
    #Creates socket for sending messages
    SOCKET_SEND = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    #Sends to given Port
    SOCKET_SEND.sendto(MESSAGE,(target_IP,target_PORT))
    
#end UDP_Send

#function used for parsing strings
def Parse(string):

    delim = ','
    stop = ';'
    
    parsedString = string.split(stop)
    parsedString = parsedString[0].split(delim)
    parseNum = len(parsedString)

    #print('Input: ' + string +'\n')
    #print('Parsed Sections:\n')

    #for i in range (0,parseNum):
     #   print('Segment ' + str(i) + ': ' + str(parsedString[i]))

    return parsedString    
#end Parse

#finds available servers
def NCAP_Server_Discover():
    while True:
        parsedData = Parse(UDP_Receive(TOMM,NCAP_COMM_PORT))
            
        if parsedData[0] == MY_CLIENT_NUMBER: 
            connectedServer = parsedData[1]
            sleep(1)
            UDP_Send(connectedServer,NCAP_COMM_PORT,'Accept')
            print 'Connection Successful\n\n'
            return connectedServer
        
        if  parsedData[1] != " Connection has timed out.":
            UDP_Send(parsedData[1],NCAP_COMM_PORT,'Denied') 

#end NCAP_Server_Discover


#-------------------EMAIL COMMUNICATION FUNCTION DEFINITIONS----------------

#this function sends an email from the smart sensor network
def send(text, addr, sub = "python"):
    server = connect()
    msg = compose(text, addr, sub)
    server.sendmail(FROM, addr, msg.as_string())
    server.quit
#end send

#this function sends a text message
def sends(text,addrs,sub="python"):
    server = connect()
    for addr in addrs:
        msg = compose(text,addr,sub)
        server.sendmail(FROM, addr, msg.as_string())
    server.quit()
#end sends

def compose(text, addr, sub):
    msg = MIMEText(text)
    msg["Subject"] = sub
    msg["From"] = EMAIL
    msg["To"] = addr
    return msg
#end compose


def connect():
    server = smtplib.SMTP_SSL(EMAIL_SERVER, TEXT_PORT)
    server.login(EMAIL, EMAIL_PASSWORD)
    return server
#end connect
    

#---------------------------GUI FUNCTION DEFINITIONS------------------------
def GUI_Close():
    File_Close = tkMessageBox.askyesno(title = "Quit", message = "Are you sure you want to quit?")
    if File_Close == True:
        SSN_GUI.destroy()
    return
#end GUI_Close

def serverButton():
    connectedServer = NCAP_Server_Discover()
    ServerConnectLabel.configure(text = "Connected to Server: " + connectedServer)

#end serverButton

def serverDisconnect():
    UDP_Send(TOMS, NCAP_COMM_PORT, "DISCONNECT")
    ServerConnectLabel.configure(text = "No Server Connected")
    return
#end serverDisconnect

def InfoLogDisplay(string):
    InfoLogListBox.insert(1,string)
    InfoLogListBox.pack()
#end InfoLogDisplay
    

def transducerSelect(transducer):
    transducerControlLabel = Label(XDCRControlFrame, text = "", fg = "yellow", bg = "brown")
    transducerControlLabel.place(x = 5, y = 5)
    
    #functionality for PMOD Thermocouple drop down option
    if transducer == "PMOD Thermocouple":
        transducerControlLabel.configure(text = "View Only Functionality")
        temp = readTemperature()
        InfoLogDisplay(temp)

    #functionality for the fan control relay drop down option
    if transducer == "Fan Control Relay":
        transducerControlLabel.configure(text = "Please Select Fan Function")

        #creates Fan on button in the XDCR Control display frame
        FanOnButton = Button(XDCRControlFrame, text = "Fan On", command = FanOn, fg = "yellow", bg = "brown")
        FanOnButton.configure(font = ("Times", 12))
        FanOnButton.place(x=50,y=50)
        
        #creates Fan off button in the XDCR Control display frame
        FanOffButton = Button(XDCRControlFrame, text = "Fan Off", command = FanOff, fg = "yellow", bg = "brown")
        FanOffButton.configure(font = ("Times", 12))
        FanOffButton.place(x=135,y=50)
        
    return
#end transducerSelect

def sendText():
    sends('The RU CSD Lab Smart Sensor Network is Online!',[TEXT_RECEIVER_2,"rucsdsnn@gmail.com"])
#end sendText

def readTemperature():
    UDP_Send(TOMS, NCAP_COMM_PORT, "TEMPERATURE")
    temp = UDP_Receive(TOMM, NCAP_COMM_PORT)
    return temp
#end readTemperature

#turns on a fan connected to the network via a relay
def FanOn():
    UDP_Send(TOMS, NCAP_COMM_PORT, "FAN ON")
    InfoLogDisplay("Fan is On")
#end FanOn

#turns a fan off connected to the network via a relay
def FanOff():
    UDP_Send(TOMS, NCAP_COMM_PORT, "FAN OFF")
    InfoLogDisplay("Fan is Off")
#end FanOff

#--------------------------------------GUI----------------------------------
#-----------------------------------Main Window-----------------------------
#Creates the GUI object
#SSN_GUI = Tk()

#Creates the window, names it, and specifies the size
#SSN_GUI.geometry("720x540") 
#SSN_GUI.title("Smart Transducer Networks - Rowan University")
#SSN_GUI.configure(bg = "brown")

#Creates the menu bar to be displayed on the top
SSNMenu = Menu(SSN_GUI)

#Creates File Tab
SSNMenu_File = Menu(SSNMenu, tearoff = 0)
SSNMenu_File.add_command(label = "New")
SSNMenu_File.add_command(label = "Exit", command = GUI_Close)

#Creates Reference Tab
SSNMenu_Reference = Menu(SSNMenu, tearoff = 0)
SSNMenu_Reference.add_command(label = "IEEE P21451-1")
SSNMenu_Reference.add_command(label = "Transducer Electronic Data Sheets (TEDS)")
SSNMenu_Reference.add_command(label = "Working Group")

#Creates Help Tab
SSNMenu_Help = Menu(SSNMenu, tearoff = 0)
SSNMenu_Help.add_command(label = "How to Connect to a Server")
SSNMenu_Help.add_command(label = "How to Disconnect from a Server")
SSNMenu_Help.add_command(label = "How to Select Transducer")

SSNMenu.add_cascade(label = "File", menu = SSNMenu_File)
SSNMenu.add_cascade(label = "Reference", menu = SSNMenu_Reference)
SSNMenu.add_cascade(label = "Help", menu = SSNMenu_Help)

#configures the top menu on the SSN_GUI
SSN_GUI.configure(menu = SSNMenu)

#----------------------------------Title Label------------------------------
#creates the Title Label 
TitleLabel = Label(text = "SSN Control Center", fg = "yellow", bg = "brown")
TitleLabel.configure(font = ("Times", 24, "bold"))
TitleLabel.pack()

#-------------------------------Information Display Frame--------------------------
#Creates the Information Display Frame and corresponding label
InfoDisplayFrame_Label = Label(SSN_GUI, text = "Information Display Log", fg = "yellow", bg = "brown")
InfoDisplayFrame_Label.configure(font = ("Times", 12))
InfoDisplayFrame_Label.place(x = 35, y = 40)

#InfoDisplayFrame = Frame(SSN_GUI, height = 250, width = 300, bg = "brown")
#InfoDisplayFrame.configure(highlightthickness = 2)
#InfoDisplayFrame.configure(highlightbackground = "yellow")
#InfoDisplayFrame.place(x = 35, y = 70)

#-------------------------------Information Log Listbox-----------------------------

#--------------------------------XDCR Control Frame---------------------------------
#creates frame for transducer control and corresponding label
XDCRControlFrame_Label = Label(text = "Transducer Control", fg = "yellow", bg = "brown")
XDCRControlFrame_Label.configure(font = ("Times", 12))
XDCRControlFrame_Label.place(x = 35, y = 330)

#XDCRControlFrame = Frame(SSN_GUI, height = 150, width = 300, bg = "brown")
#XDCRControlFrame.configure(highlightthickness = 2)
#XDCRControlFrame.configure(highlightbackground = "yellow")
#XDCRControlFrame.place(x = 35, y = 360)

#------------------------------Server Connect Label---------------------------------
#creates a label for the server connection
#ServerConnectLabel = Label(text = "There are Currently No Server Connections...", fg = "yellow", bg = "brown")
#ServerConnectLabel.configure(font = ("Times", 12))
#ServerConnectLabel.place(x = 375, y = 65)

#--------------------------Transducer Select Drop Down------------------------------
#creates label for transducer select drop down menu
TransducerSelect_Label = Label(text = "Transducer Select: ", fg = "yellow", bg = "brown")
TransducerSelect_Label.configure(font = ("Times", 12))
TransducerSelect_Label.place(x = 375, y = 108)

#Defines possible choices in drop down menu and variable names
transducerOptions = ["No Server Connection","PMOD Thermocouple","Fan Control Relay"]
var = StringVar()
var.set("No Server Connection")

#creates the drop down menu
TransducerSelect = OptionMenu(SSN_GUI, var, *transducerOptions, command = transducerSelect)
TransducerSelect.configure(font = ("Times",12))
TransducerSelect.configure(bg = "brown")
TransducerSelect.configure(fg = "yellow")
TransducerSelect.configure(highlightbackground = "yellow")
TransducerSelect.place(x = 500, y = 105)

#----------------------------Connect Server Button--------------------------
ConnectServerButton = Button(text = "Connect to Server", command = serverButton, fg = "yellow", bg = "brown")
ConnectServerButton.configure(font = ("Times", 12))
ConnectServerButton.place(x = 385, y = 165)

#---------------------------Disconnect Server Button------------------------
DisconnectServerButton = Button(text = "Disconnect Server", command = serverDisconnect, fg = "yellow", bg = "brown")
DisconnectServerButton.configure(font = ("Times", 12))
DisconnectServerButton.place(x = 535, y = 165)

#---------------------------Rowan Logo Display Label------------------------
#creates frame to display image in
RULogo = PhotoImage(file = "/home/pi/Desktop/SSN_Projects/SSN_NCAP/ROWAN_LOGO.gif")
LogoLabel = Label(image = RULogo)
LogoLabel.image = RULogo #keeps reference
LogoLabel.configure(height = 210, width = 210)
LogoLabel.configure(highlightthickness = 2)
LogoLabel.configure(highlightbackground = "yellow")
LogoLabel.place(x = 425, y = 215)

#-------------------------TEXT MESSAGE UPDATE BUTTON------------------------
TextMessageUpdateButton = Button(text = "Send Text Message Update", command = sendText, fg = "yellow", bg = "brown")
TextMessageUpdateButton.configure(font = ("Times", 12))
TextMessageUpdateButton.place(x = 432, y = 445)


#Creates main loop... NOTE ONLY FOR WINDOWS... In Linux comment this line
SSN_GUI.mainloop()
