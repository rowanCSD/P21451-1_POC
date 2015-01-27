#Author: Tom Morris
#Date: 10.17.2014
#Description: The following program creates a Graphical User Interface to be
#             used with an NCAP Client module.  This version of the GUI will
#             be used for an open house at Rowan University on October 25th
#             2014. This GUI is compatable with NCAP Client Lite Lite v2

#-------------------------------NEEDED LIBRARIES----------------------------
import sys
from Tkinter import *
import tkMessageBox

#-------------------------------GLOBAL VARIABLES----------------------------


#--------------------------INITIALIZE GLOBAL VARIABLES----------------------


#-----------------------------FUNCTION DEFINITIONS--------------------------
def GUI_Close():
    File_Close = tkMessageBox.askyesno(title = "Quit", message = "Are you sure you want to quit?")
    if File_Close == True:
        SSN_GUI.destroy()
    return

#--------------------------------------GUI----------------------------------
#-----------------------------------Main Window-----------------------------
#Creates the GUI object
SSN_GUI = Tk()

#Creates the window, names it, and specifies the size
SSN_GUI.geometry("720x540") 
SSN_GUI.title("Smart Transducer Networks - Rowan University")
SSN_GUI.configure(bg = "brown")

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

#-------------------------------TEDS Display Frame--------------------------
#Creates the Information Display Frame and corresponding label
InfoDisplayFrame_Label = Label(text = "Information Display Log", fg = "yellow", bg = "brown")
InfoDisplayFrame_Label.configure(font = ("Times", 12))
InfoDisplayFrame_Label.place(x = 35, y = 40)

InfoDisplayFrame = Frame(SSN_GUI, height = 250, width = 300, bg = "brown")
InfoDisplayFrame.configure(highlightthickness = 2)
InfoDisplayFrame.configure(highlightbackground = "yellow")
InfoDisplayFrame.place(x = 35, y = 70)

#--------------------------------XDCR Control Frame----------------------------
#creates frame for transducer control and corresponding label
XDCRControlFrame_Label = Label(text = "Transducer Control", fg = "yellow", bg = "brown")
XDCRControlFrame_Label.configure(font = ("Times", 12))
XDCRControlFrame_Label.place(x = 35, y = 330)

XDCRControlFrame = Frame(SSN_GUI, height = 150, width = 300, bg = "brown")
XDCRControlFrame.configure(highlightthickness = 2)
XDCRControlFrame.configure(highlightbackground = "yellow")
XDCRControlFrame.place(x = 35, y = 360)

#------------------------------Server Connect Label-------------------------
#creates a label for the server connection
ServerConnectLabel = Label(text = "There are Currently No Server Connections...", fg = "yellow", bg = "brown")
ServerConnectLabel.configure(font = ("Times", 12))
ServerConnectLabel.place(x = 375, y = 65)

#--------------------------Transducer Select Drop Down----------------------
#creates label for transducer select drop down menu
TransducerSelect_Label = Label(text = "Transducer Select: ", fg = "yellow", bg = "brown")
TransducerSelect_Label.configure(font = ("Times", 12))
TransducerSelect_Label.place(x = 375, y = 108)

#Defines possible choices in drop down menu and variable names
transducerOptions = ["No Server Connection","PMOD Thermocouple","Fan Control Relay"]
var = StringVar(SSN_GUI)
var.set("No Server Connection")

#creates the drop down menu
TransducerSelect = OptionMenu(SSN_GUI, var, *transducerOptions)
TransducerSelect.configure(font = ("Times",12))
TransducerSelect.configure(bg = "brown")
TransducerSelect.configure(fg = "yellow")
TransducerSelect.configure(highlightbackground = "yellow")
TransducerSelect.place(x = 500, y = 105)

#----------------------------Connect Server Button--------------------------
ConnectServerButton = Button(text = "Connect to Server", fg = "yellow", bg = "brown")
ConnectServerButton.configure(font = ("Times", 12))
ConnectServerButton.place(x = 385, y = 165)

#---------------------------Disconnect Server Button------------------------
DisconnectServerButton = Button(text = "Disconnect from Server", fg = "yellow", bg = "brown")
DisconnectServerButton.configure(font = ("Times", 12))
DisconnectServerButton.place(x = 515, y = 165)

#---------------------------Rowan Logo Display Label------------------------
#creates frame to display image in
#RULogo = PhotoImage(file = "C:\Users\Thomas\Documents\Rowan University_Graduate\ROWAN_LOGO.gif")
#LogoLabel = Label(image = RULogo)
#LogoLabel.image = RULogo #keeps reference
#LogoLabel.configure(height = 210, width = 210)
#LogoLabel.configure(highlightthickness = 2)
#LogoLabel.configure(highlightbackground = "yellow")
#LogoLabel.place(x = 425, y = 250)


#Creates main loop... NOTE ONLY FOR WINDOWS... In Linux comment this line
SSN_GUI.mainloop()
