"""
Contributors: Jordan
Read the markdown source file "readme.md" for instructions
to build the runtime environment

This program is a simple soccer scoreboard program that allows the user to add and delete players and their scores.
"""
import tkinter as tk        #for the GUI
from tkinter import ttk     #for more advanced widgets
import pandas as pd         #for displaying the scoreboard data in a table and manipulating the csv file
import os                   #for checking if the csv file exists in the directory
import threading            #for running the system message clearing in a seperate thread
import time                 #for the sleep method in the system message clearing function

class SysMsg:                                                               #system message class
    """
    A system message class to display messages in a tkinter label widget.
    """
    def __init__(self, msg):                                                #initialize the system message label
        """
        Initialize the system message label.

        Args:
            msg (str): The message to display in the system message label.
        """
        self.msg = msg
        self.tk_sys_msg_lb = tk.Label(window, textvariable=tk_sys_msg_var)  #create a label widget for the system message
        self.tk_sys_msg_lb.place(rely=1.0, relx=0, x=3, y=-10, anchor='sw') #place the system message label at the bottom left corner of the window
        self.tk_sys_msg_lb.config(font=("Courier", 10))                     #set the font of the system message label
        self.tk_sys_msg_lb.config(foreground="yellow")                      #set the text color of the system message label
        self.tk_sys_msg_lb.config(background="black")                       #set the background color of the system message label
        self.tk_sys_msg_lb.config(justify="center")                         #set the text alignment of the system message label
        self.tk_sys_msg_lb.config(anchor="center")                          #set the anchor of the system message label
        self.sysMsgHandler()

    def sysMsgHandler(self):                                                #system message handler method
        """
        A system message handler to control the system message label, printing various error messages.
        It also will print information about use of the program.
        """
        def clear():                                    #nested function
            """
            the nested function encapsulates the system message clearing. this is so it can run in a 
            seperate thread to asynchronically execute the sleep method and clear each message after 6 seconds
            """
            time.sleep(6)
            self.tk_sys_msg_lb.place_forget()           #will remove the system message label

        tk_sys_msg_var.set(self.msg)
        thread = threading.Thread(target=clear)         #create a new thread for clearing the system message on the clear()
        thread.start()                                  #this will clear the system message without freezing the program
        #thread method source: 
        #Grinberg, M. (n.d.). How To Make Python Wait. Retrieved May 3, 2024, from https://blog.miguelgrinberg.com/post/how-to-make-python-wait
   
class TableData:                                                           #table data class
    def __init__(self):
        """
        Initialize the scoreboard table.
        Args:
            None
        Returns:
            None
        """
        try:                                                                #try to get the scores attribute
            self.scores
        except AttributeError:                                              #if the scores attribute does not exist, create it
            self.scores = self.savedData()                                  # read csv to update the scoreboard

    def savedData(self):                                                    #save data method
        """
        check saved data, otherwise print system message creating new data file
        
        Returns:
            scores: the csv data as pandas dataframe
        """
        if os.path.exists('soccer_scores.csv'):             #check if a previous scoreboard file exists, if so read that one
            self.scores = pd.read_csv('soccer_scores.csv', index_col=False) #Rob Mulla (Director). (2021, December 28). A Gentle Introduction to Pandas Data Analysis (on Kaggle). https://www.youtube.com/watch?v=_Eb0utIRdkw
            self.refresh()
        else:
            self.scores = pd.DataFrame({                                   #if the file does not exist, create a new one
                'Player:': [],
                'Score:': [],
                })
            self.scores.to_csv('soccer_scores.csv', index=False) #How to Append Pandas DataFrame to Existing CSV File? (2021, November 25). GeeksforGeeks. https://www.geeksforgeeks.org/how-to-append-pandas-dataframe-to-existing-csv-file/
            SysMsg('Creating new CSV')                                     #send a system message that a new csv file is being created
            self.savedData()                                                #read the new csv file

        return self.scores                                                #return the scores attribute

    def refresh(self):                                                     #refresh method
        """
        refresh the scoreboard, reading csv data and updating the table widget
        """
        tk_scoreboard_data.set(pd.read_csv('soccer_scores.csv'))         #set the scoreboard data variable to the csv data
        if pd.read_csv('soccer_scores.csv').empty == True:               #check if the csv file is empty
            SysMsg('No data to\n display')                               #send a system message that there is no data to display
            scoreboard_label.place_forget()                              #remove the scoreboard from the window
        else:
            scoreboard_label.place(relx=1, x=0, y=-1, anchor='ne')      #place the scoreboard in the window at the top right corner

    def addRow(self):
        #add a new row to the scoreboard
        """
        add a new row to the scoreboard
        """       
        if player_entry.get() != '' and score_entry.get() != '': #check if the entry fields are empty
            if player_entry.get().isalpha() and score_entry.get().isdigit(): #check if the player name is alphabetical and the score is numerical
                try:
                    if int(score_entry.get()) < 100 and int(score_entry.get()) > 0:
                        add_data = pd.DataFrame({'Player': [player_entry.get()], 'Score': [score_entry.get()]})#get data from entry field to dataframe
                        add_data.to_csv('soccer_scores.csv', mode='a', index=False, header=False) #addcsv file with mode='a' to append to the end of the csv file
                        SysMsg('Player added') #send system message that the player has been added
                       #SysMsg('**Invalid score**\nPlease enter a numerical score')SysMsg 
                except ValueError:
                    ('**Incorrect score**\nThe scores should be from\n0-100.Please try again!')
            else:
                SysMsg('Invalid entry\nPlayer name must\nbe alphabetical\nScore must be\nnumerical') #send error message using sys message class
            try:
                if int(score_entry.get()) > 100 or int(score_entry.get()) < 0:
                    SysMsg('**Incorrect score**\nThe scores should be from\n0-100.Please try again!')
            except ValueError:
                SysMsg('**Invalid score**\nPlease enter a numerical score')
        else:
            SysMsg('Field(s) must\nnot be empty') #send error message using sys message class

        tk_scoreboard_data.set(pd.read_csv('soccer_scores.csv')) #consider a more efficient way to update the scoreboard variable
        TableData().refresh()
    
    def deleteRow(self):
        """
        delete the last row from the scoreboard
        """
        if pd.read_csv('soccer_scores.csv').empty == False:                #check if the csv file is not empty
            self.scores = pd.read_csv('soccer_scores.csv')                 #read the csv file
            self.scores = self.scores.iloc[:-1]                            #remove the last row from the csv file
            self.scores.to_csv('soccer_scores.csv', index=False)           #save the updated csv file
            SysMsg('Row deleted')                                          #send a system message that the row has been deleted
            TableData().refresh()                                          #refresh the scoreboard
        else:                                                              #if the csv file is empty
            SysMsg('No data to\n delete')                                  #send a system message that there is no data to delete
            TableData().refresh()                                          #refresh the scoreboard


#initialize the window:#########################################
#setup window
window = tk.Tk()
window.title('Champions Soccer Slub Scoreboard')
window.geometry('250x300') #window size
window.resizable(0,1)
#system messages
tk_sys_msg_var = tk.StringVar()
################################################################

#initialize the GUI Frames:#####################################
#master frame
master_frame = ttk.Frame(window)
master_frame.place(relwidth='1', relheight='1', anchor='nw', bordermode='inside')
#user input fields
input_frame = ttk.Frame(master_frame, style='BW.TFrame')
input_frame.place(x=0, y=0, anchor='nw')
#Scoreboard Frame
score_frame = ttk.Frame(master_frame)
score_frame.pack(side='right') #every widget must be packed. I do this directly after creating the widget for code readability
#scoreboard data variable
tk_scoreboard_data = tk.StringVar()
#scoreboard widget containing the scoreboard data
scoreboard_label = ttk.Label(window, textvariable=tk_scoreboard_data, font=('Arial', 10, 'bold'))
scoreboard_label.place(relx=1, x=0, y=-1, anchor='ne') #place the scoreboard in the window at the top right corner

#initialize the input elements:################################
#player input
add_label = ttk.Label(input_frame, text='Add a new player', underline=0, font=('Arial', 10, 'underline'))
add_label.pack()
add_label = ttk.Label(input_frame, text='Player Name:')
add_label.pack()
player_entry = ttk.Entry(input_frame)
player_entry.pack()
#score input
score_label = ttk.Label(input_frame, text='Score:')
score_label.pack()
score_entry = ttk.Entry(input_frame)
score_entry.pack()
#add another entry to the scoreboard
add_button = ttk.Button(input_frame, text='Add', command=TableData().addRow)
add_button.pack()
#delete selected player entry from the scoreboard
#delete last entry from the scoreboard
delete_button = ttk.Button(input_frame, text='Delete Row', command=TableData().deleteRow)
delete_button.pack()

#display the scoreboard data in a table
tk_scoreboard_data.set(pd.read_csv('soccer_scores.csv'))

window.mainloop()               #start the main loop