import tkinter
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import sqlite3
from PIL import Image, ImageTk

window=Tk()
#window config
window.title('Update new property')
window.geometry("1250x800")
window.state('zoomed')
window.config(bg="#142c14")

#image
img=Image.open("green3.jpg")
img_tk=ImageTk.PhotoImage(img)
Label(window ,text="image",image=img_tk).place(x=0,y=0)

#variables
anime_name=tkinter.StringVar()
anime_type=tkinter.StringVar() #combo
genre=tkinter.StringVar() #combo
season=tkinter.StringVar()
episode=tkinter.StringVar()
status=tkinter.StringVar() #combo
watch=tkinter.StringVar()
id=tkinter.StringVar() #search

#functions
def clear():
    anime_name.set("")
    anime_type.set("")
    genre.set("")
    season.set("")
    episode.set("")
    status.set("")
    watch.set("")
    id.set("")     
def add_anime():
    conn=sqlite3.connect('anime_list.db')
    cursor=conn.cursor()
    #cursor.execute('CREATE TABLE IF NOT EXISTS Anime (ID INT PRIMARY KEY AUTOINCREMENT, anime_name TEXT, anime_type TEXT, genre TEXT, season TEXT, episode INT, status TEXT,watch TEXT')
    if anime_name.get()=="" or anime_type.get()=="" or season.get()=="" or status.get()=="" or watch.get()=="" :
            messagebox.showerror("Error","   All fields are required!!   ") 
    else:
        cursor.execute("SELECT * FROM Anime WHERE anime_name=?",(anime_name.get(),))
        row=cursor.fetchone()
        print(row)
        if row!=None:
            messagebox.showerror("Error!","This anime already exist in the list.") 
        else:
            cursor.execute('INSERT INTO Anime (anime_name , anime_type , genre , season , episode ,status , watch) VALUES(?,?,?, ?,?,?,?)',
                           (anime_name.get() , anime_type.get() , genre.get() , season.get() , episode.get()  ,status.get() , watch.get()))  
            conn.commit()
            messagebox.showinfo(title="Anime added", message="You have successfully added new anime to the watchlist.")
            clear()
            view_anime()
    conn.close()
def search_anime():
    conn=sqlite3.connect('anime_list.db')
    cursor=conn.cursor()
    if id.get()=="":
        messagebox.showerror("Error!  ","   Please enter the Anime ID.   ") 
    else:
        cursor.execute("SELECT * FROM Anime WHERE id=?",(id.get(),))
        ani_row=cursor.fetchone()
        if ani_row==None:
            messagebox.showerror("Error!","  Anime ID does not exist.   ") 
        else:            
            anime_name.set(ani_row[1])
            anime_type.set(ani_row[2])
            genre.set(ani_row[3])
            season.set(ani_row[4])
            episode.set(ani_row[5])
            status.set(ani_row[6])
            watch.set(ani_row[7])
    conn.close()        
def update_anime():
    conn=sqlite3.connect('anime_list.db')
    cursor=conn.cursor()
    if anime_name.get()=="" or anime_type.get()=="" or season.get()=="" or status.get()=="" or watch.get()=="" :
            messagebox.showerror("Error","   All fields are required!!   ") 
    else:
        cursor.execute('UPDATE Anime SET anime_name=? , anime_type=? , genre=? , season=? , episode=? ,status=? , watch=? WHERE ID=?',
                        (anime_name.get() , anime_type.get() , genre.get() , season.get() , episode.get()  ,status.get() , watch.get(), id.get() ))  
        conn.commit()
        messagebox.showinfo(title="Anime added", message="You have successfully updated the anime watchlist.")
        clear() 
        view_anime()       
    conn.close()
def view_anime():
    conn=sqlite3.connect('anime_list.db')
    cursor=conn.cursor()
    cursor.execute("SELECT ID,anime_name, anime_type, status,watch,genre,season,episode FROM Anime ")
    rows=cursor.fetchall()
    if len(rows)!=0:
        animeTable.delete(*animeTable.get_children())
        for row in rows:
            animeTable.insert('',tkinter.END,values=row)
        conn.commit()    
    conn.close()       
    
# Create Frame widget
left_frame = Frame(window, width=600, height=600,relief=RAISED,borderwidth=5,bg='#2d5128')
left_frame.place(x=30,y=30)

right_frame = Frame(window, width=600, height=600,relief=RAISED,borderwidth=5,bg='#2d5128')
right_frame.place(x=660,y=30)

# view from database
view_frame = Frame(right_frame,  bd=5, relief=RIDGE,bg='#5e503f')
view_frame.place(x=15,y=70,width=560, height=500)

scrolly=Scrollbar(view_frame, orient=VERTICAL)
scrollx=Scrollbar(view_frame, orient=HORIZONTAL)

animeTable=ttk.Treeview(view_frame, columns=("ID","anime_name", "anime_type", "status","watch","genre","season","episode"),
                      xscrollcommand=scrollx.set, yscrollcommand=scrolly.set,padding=2,takefocus=5)

scrollx.pack(side=BOTTOM, fill=X)
scrolly.pack(side=RIGHT, fill=Y)

scrollx.config(command=animeTable.xview)
scrolly.config(command=animeTable.yview)

animeTable.heading("ID", text=" ID ")
animeTable.heading("anime_name", text=" Anime Name ")
animeTable.heading("anime_type", text=" Type ")
animeTable.heading("status", text=" Status ")
animeTable.heading("watch", text=" Watching ")
animeTable.heading("genre", text=" Genre ")
animeTable.heading("season", text=" Season ")
animeTable.heading("episode", text=" Episode")

animeTable["show"] = 'headings'

animeTable.column("ID", width=30,anchor="center")
animeTable.column("anime_name", width=150,anchor="center")
animeTable.column("anime_type", width=100,anchor="center")
animeTable.column("status", width=150,anchor="center")
animeTable.column("watch", width=100,anchor="center")
animeTable.column("genre", width=100,anchor="center")
animeTable.column("season", width=100,anchor="center")
animeTable.column("episode", width=100,anchor="center")
animeTable.pack(fill=BOTH, expand=True)
view_anime()

#left frame Labels and entry 
Label(left_frame ,text="My Anime Watchlist",bg='#2d5128', fg="#FFFFFF", font=("Brush Script MT", 25)).place(x=180,y=0)

name_label = tkinter.Label(left_frame, text="Anime Name ", bg='#2d5128', fg="#8da750", font=("times new roman", 13, 'bold'))
type_label = tkinter.Label(left_frame, text="Type ", bg='#2d5128', fg="#8da750", font=("times new roman", 13, 'bold'))
genre_label = tkinter.Label(left_frame, text="Genre ", bg='#2d5128', fg="#8da750", font=("times new roman", 13, 'bold'))
season_label = tkinter.Label(left_frame, text="Season", bg='#2d5128', fg="#8da750", font=("times new roman", 13, 'bold'))
episode_label =tkinter.Label(left_frame, text="Episode", bg='#2d5128', fg="#8da750", font=("times new roman", 13, 'bold'))
status_label = tkinter.Label(left_frame, text="Status ", bg='#2d5128', fg="#8da750", font=("times new roman", 13, 'bold'))
watch_label=tkinter.Label(left_frame, text="Watching ", bg='#2d5128', fg="#8da750", font=("times new roman", 13, 'bold'))

name_entry = tkinter.Entry(left_frame,borderwidth=5,width=30, font=("times new roman", 13),textvariable=anime_name)
season_entry = tkinter.Entry(left_frame,borderwidth=5,width=30, font=("times new roman", 13),textvariable=season)
episode_entry= tkinter.Entry(left_frame,borderwidth=5,width=30, font=("times new roman", 13),textvariable=episode) 
watch_entry=tkinter.Entry(left_frame,borderwidth=5,width=30, font=("times new roman", 13),textvariable=watch)

type_entry  = ttk.Combobox(left_frame,width=29, font=("times new roman", 13),state='readonly', textvariable = anime_type) 
type_entry ['values'] = ('Anime Series','Anime Movie','Extra','Donghua')
genre_entry  = ttk.Combobox(left_frame,width=29, font=("times new roman", 13),state='readonly', textvariable = genre) 
genre_entry ['values'] = ('Action','Mystery','Dark','Isakai','Rom-com','Depression','Psycological','Shonen','BL')
status_entry  = ttk.Combobox(left_frame,width=29, font=("times new roman", 13),state='readonly', textvariable = status) 
status_entry ['values'] = ('Ongoing','Completed','New Season Coming','Finished Airing','Hiatus')

name_label.place(x=30,y=50)
type_label.place(x=30,y=120)
genre_label.place(x=30,y=190)
season_label.place(x=30,y=260)
episode_label.place(x=30,y=330)
status_label.place(x=30,y=400)
watch_label.place(x=30,y=470)

name_entry.place(x=160,y=50)
type_entry.place(x=160,y=120)
genre_entry.place(x=160,y=190)
season_entry.place(x=160,y=260)
episode_entry.place(x=160,y=330)
status_entry.place(x=160,y=400)
watch_entry.place(x=160,y=470)

#right frame
search_label=tkinter.Label(right_frame, text="Search", bg='#2d5128', fg="#8da750", font=("times new roman", 13, 'bold'))
search_entry=tkinter.Entry(right_frame,borderwidth=5,width=20, font=("times new roman", 13),textvariable=id)
search_label.place(x=30,y=20)
search_entry.place(x=100,y=20)


#buttons
add_button = Button(left_frame,text=" Add Anime ✨",relief=GROOVE, bg="#8da750", fg="#142c14", borderwidth=3,font=("times new roman", 14,),command= add_anime)
add_button.place(x=230,y=530)

search_button = Button(right_frame,text="Search Anime",relief=RAISED, bg="#8da750", fg="#142c14", borderwidth=3,font=("times new roman", 13),command= search_anime)
search_button.place(x=320,y=17)

update_button = Button(right_frame,text="Update Anime",relief=RAISED, bg="#142c14", fg="#8da750", borderwidth=3,font=("times new roman", 13),command= update_anime)
update_button.place(x=450,y=17)

window.mainloop()