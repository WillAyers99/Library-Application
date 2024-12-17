import tkinter as tk
import sqlite3
import datetime
from functools import partial

#TODO:

#Database definition
# books table with (uniqueID, title, author, status[avail/borrow(1/2)])
# user table with (uniqueID, name, contact information)
# borrowed table? (uniqueID, bookID, userID, dueDate)

#initialize database
connection = sqlite3.connect("library.db")
print(connection.total_changes)
cursor = connection.cursor()

#Creates our 3 database tables
cursor.execute("CREATE TABLE IF NOT EXISTS books (id INTEGER PRIMARY KEY, title TEXT, author TEXT, status INTEGER)")
cursor.execute("CREATE TABLE IF NOT EXISTS user (id INTEGER PRIMARY KEY, name TEXT, contact_info TEXT)")
cursor.execute("CREATE TABLE IF NOT EXISTS relations (id INTEGER PRIMARY KEY, userID INTEGER, bookID INTEGER, dueDate INTEGER, FOREIGN KEY(userID) REFERENCES user(id), FOREIGN KEY(bookID) REFERENCES books(id))")

activeUser = -1

#Initialize window

window = tk.Tk() # Create the main window
window.title("Library Application") # Set the title of the window
window.minsize(400,300) # Set the window minimum size

#set window default size/location
#window.geometry("300x300+50+50")

window.configure(background="brown")#set window background color

searchField = tk.Frame(window, bg="white")  #Creates a frame for the search box
searchField.grid(row=0, column=0, sticky="nsew")
inputText = tk.Entry(searchField)
inputText.pack(fill="both", expand=True)

buttons = tk.Frame(window, bg="blue")       #Creates a frame for the buttons box
buttons.grid(row=1, column=0, sticky="nsew")

resultsFrame = tk.Frame(window, bg="White") #Creates a frame for the results box
resultsFrame.grid(row=1, column=1, sticky="nsew")
resultsField = tk.Listbox(resultsFrame)
resultsField.pack(fill="both", expand=True)

userFrame = tk.Frame(window, bg="White")    #Creates a frame for displaying the active user
userFrame.grid(row=0, column=1, sticky="nsew")
userLabel = tk.Label(userFrame, text=activeUser)
#userLabel.grid(row=0, column=1)
userLabel.pack(side="right", fill="both", expand=True)

window.rowconfigure(0, weight=1)    #Configures main window grid so that elements will stretch to fill window space
window.rowconfigure(1,weight=1)
window.columnconfigure(0, weight=1)
window.columnconfigure(1, weight=1)

#Begin Function Definitions

def changeUser(w, username):    #change active user function
    name = username.get()
    cursor.execute("Select * FROM user WHERE name='"+str(name)+"'")
    rows = cursor.fetchall()
    #print(len(rows))
    if(len(rows) > 0):
        activeUser = rows[0][0]
        #print("Active user= " + str(activeUser))
        userLabel.config(text=str(activeUser) +" "+ str(rows[0][1]))
        userLabel.pack()
        w.destroy()
    
    
def dbAddUser(w, n, c): #adds a user to the database
    name = n.get()
    cInfo = c.get()
    cursor.execute("INSERT INTO user VALUES (NULL, '"+str(name)+"', '"+str(cInfo)+"')")
    connection.commit()
    #print("Added "+ name + " to database")
    changeUser(w,n)
    
def doMakeUser():   #Sets up window for making user
    #print("Making user...")
    userWindow = tk.Tk()    #Setup window default parameters
    userWindow.title("Login")
    userWindow.minsize(300,100)
    userWindow.configure(background="brown")
    userWindow.attributes('-topmost', True)

    nLabel = tk.Label(userWindow, text="Username")  #Text label for name input box
    nLabel.grid(row=0, column=0)
    cLabel = tk.Label(userWindow, text="Contact Info")  #Text label for contact info input box
    cLabel.grid(row=1, column=0)

    userWindow.rowconfigure(0, weight=1)    #configure window grid to stretch columns to size of window
    userWindow.rowconfigure(1,weight=1)
    userWindow.columnconfigure(0, weight=1)
    userWindow.columnconfigure(1, weight=1)

    name = tk.Frame(userWindow, bg="White") #creates frame and text input field for username
    name.grid(row=0, column=1)
    nameEntry = tk.Entry(name)
    nameEntry.pack()
    
    cInfo = tk.Frame(userWindow, bg="White")#creates frame and text input field for contact info
    cInfo.grid(row=1, column=1)
    cInfoEntry = tk.Entry(cInfo)
    cInfoEntry.pack()

    finished = tk.Frame(userWindow, bg="White")#creates button to add new user
    finished.grid(row=2,column=0)
    finishButton = tk.Button(finished, text="Add New User", command=partial(dbAddUser, userWindow, nameEntry, cInfoEntry))
    finishButton.pack()

    login = tk.Frame(userWindow, bg="White")    #creates button to login existing user
    login.grid(row=2,column=1)
    loginButton = tk.Button(login, text="Login", command=partial(changeUser, userWindow, nameEntry))
    loginButton.pack()
    
    userWindow.mainloop()   #begin displaying user Login window
    
def dbAddBook(w, te, ae):   #adds book information to database
    title = te.get()    #gets title from text box entry
    author = ae.get()   #gets author from text box entry
    #print("title is " + title)
    #print("author is " + author)
    if(title == "" or author == ""):    #if title or author is blank, do not continue
        return
    cursor.execute("INSERT INTO books VALUES (NULL, '"+str(title)+"', '"+str(author)+"', 0)")   #insert book info to database
    connection.commit() #commit changes to database (may be unneccesary)
    #print("done adding book, closing window")
    w.destroy() #close the add book window

def doAddBook():    #Sets up window for adding book
    #print("adding book...")
    bookWindow = tk.Tk()
    bookWindow.title("Add Book")#initialize window default parameters
    bookWindow.minsize(400,100)
    bookWindow.configure(background="brown")

    tLabel = tk.Label(bookWindow, text="Title") #creates label for title entry text box
    tLabel.grid(row=0, column=0)
    aLabel = tk.Label(bookWindow, text="Author")#creates label for author entry text box
    aLabel.grid(row=1, column=0)

    bookWindow.rowconfigure(0, weight=1)    #configure window grid to stretch columns to size of window
    bookWindow.rowconfigure(1,weight=1)
    bookWindow.columnconfigure(0, weight=1)
    bookWindow.columnconfigure(1, weight=1)

    title = tk.Frame(bookWindow, bg="White")    #creates frame and entry box for book title
    title.grid(row=0, column=1)
    titleEntry = tk.Entry(title)
    titleEntry.pack()
    
    author = tk.Frame(bookWindow, bg="White")   #creates frame and entry box for author
    author.grid(row=1, column=1)
    authorEntry = tk.Entry(author)
    authorEntry.pack()

    finished = tk.Frame(bookWindow, bg="White") #creates button that will add the book info when pressed
    finished.grid(row=2,column=0)
    finishButton = tk.Button(finished, text="Add Book", command=partial(dbAddBook, bookWindow, titleEntry, authorEntry))
    finishButton.pack()
    
    bookWindow.mainloop()   #display book adding window
    

def doDisplayAll(r):    #Display Available Books
    r.delete(0, tk.END) #clear the list display box
    #print("displaying all books...")
    cursor.execute("SELECT * FROM books")   #select all books from database
    rows = cursor.fetchall()
    for row in rows:
        outputrow = [row[1],row[2],row[3]]  #omit the bookid value
        if(row[3] == 0):
            outputrow[2] = "Available"  #make availability status more readable
        else:
            outputrow[2] = "Unavailable"
        r.insert(tk.END, outputrow) #insert all books info into list display box
        #print(outputrow)
    
def dbMakeBorrowed(book):   #Make borrowed by User in both books and relations table
    #print(book[2])
    if(book[2]=="Unavailable"): #do not continue if book is already borrowed
        #print("here")
        return
    cursor.execute("SELECT * from books WHERE title='"+str(book[0])+"' AND status=0")#select all books that have the same title as
    rows = cursor.fetchall()                                                         #user selection and is available
    #for row in rows:
        #print(row)
    #print(rows[0])
    if(rows[0][3] == 0):    #if the status is available, continue (redundant?)
        bookid = str(rows[0][0]) #id number of our book
        dueDate = datetime.date.today() + datetime.timedelta(weeks=2) #sets duedate of book to 2 weeks from today
        cursor.execute("INSERT INTO relations VALUES (NULL, '"+str(activeUser)+"', '"+str(bookid)+"', '"+str(dueDate)+"')")
        #^ insert a new entry into relations table that links the users id to the books id
        cursor.execute("UPDATE books SET status = '1' WHERE id = '"+str(bookid)+"'")
        #^ update the book table to show the book as unavailable
        connection.commit()#commit changes to database
        doDisplayAll(resultsField)  #run display all function so the user can see the books availablity change
        
def doMakeBorrowed(r):  #make a book borrowed
    selection = r.curselection()
    if selection:   #if a user has selected a book, continue
        book = r.get(selection[0])
        #print(book)
        #print("Borrowing book...")
        dbMakeBorrowed(book)#makes the book borrowed (see above function)
    
def dbReturnBook(book):#Return book by updating database
    #print(book[0])
    cursor.execute("SELECT * from books WHERE title='"+str(book[0])+"' AND status='1'")
    #^ finds books with the selected title and is borrowed
    rows = cursor.fetchall()
    #for row in rows:
        #print(row)
        #print("here")
    returningBook = rows[0] #assign returning Book to the first unavailable book we have
    #print("returningBook= " + str(returningBook))
    cursor.execute("SELECT * from relations WHERE bookID='"+str(returningBook[0])+"' AND userID = '"+str(activeUser)+"'")
    #^ selects the relation between the book and the user
    rows = cursor.fetchall()
    relation = rows[0]
    
    #print(str(relation) + "here")
    bookid = str(returningBook[0])  #convert to strings 
    relationid = str(relation[0])
    cursor.execute("DELETE from relations where id='"+str(relationid)+"'")      #delete now irrelevant relations entry
    cursor.execute("UPDATE books SET status = '0' WHERE id = '"+str(bookid)+"'")#update the book status to available in database
    connection.commit()#commit changes to database
    doDisplayAll(resultsField) #display all books to show that an update has occured
    
def doReturnBook(r):    #returns book that user has selected
    selection = r.curselection()
    if selection:   #if the user has selected a book, continue
        book = r.get(selection[0])
        #print(book)
        if(book[2] == "Unavailable"):#if the user selection is a borrowed book, continue
            
            #print("Returning book...")
            dbReturnBook(book) #returns book and manages database relations (see above function)
    

def doSearchBook(s, r): #Search for book by title or author
    r.delete(0, tk.END) #clear the results box
    text=s.get()    #get serach term from search input box
    #print("searching books for " + text)

    cursor.execute("Select * from books WHERE title='"+str(text)+"' OR author='"+str(text)+"'")
    #^ select all books that have a title or author that is the same as the users search prompt
    rows = cursor.fetchall()
    for row in rows:
        outputrow = [row[1],row[2],row[3]]
        if(row[3] == 0):    #makes availability status more readable for user
            outputrow[2] = "Available"
        else:
            outputrow[2] = "Unavailable"
        r.insert(tk.END, outputrow) #insert search results into results box
        #print(outputrow)


#Make Buttons and assign functions
        
makeUser = tk.Button(buttons, text="Login", command=doMakeUser) #make Login button
#searchBook.grid(row=0, column=4)
makeUser.pack(fill="both", expand=True)

searchBook = tk.Button(buttons, text="Search", command=partial(doSearchBook,inputText,resultsField)) #Make search button
#searchBook.grid(row=0, column=0)
searchBook.pack(fill="both", expand=True)

addBook = tk.Button(buttons, text="Add Book", command=doAddBook) #make Add Book button
#addBook.grid(row=0, column=0)
addBook.pack(fill="both", expand=True)

displayAll = tk.Button(buttons, text="Display All Books", command=partial(doDisplayAll,resultsField)) #make Display All Books button
#displayAll.grid(row=0, column=1)
displayAll.pack(fill="both", expand=True)


makeBorrowed = tk.Button(buttons, text="Borrow Book", command=partial(doMakeBorrowed, resultsField)) #make Borrow Book button
#makeBorrowed.grid(row=0, column=2)
makeBorrowed.pack(fill="both", expand=True)


returnBook = tk.Button(buttons, text="Return Book", command=partial(doReturnBook, resultsField)) #make Return Book button
#returnBook.grid(row=0, column=3)
returnBook.pack(fill="both", expand=True)


# Start the event loop
doMakeUser()    #Opens login window on startup
window.mainloop() #opens main application window









    
