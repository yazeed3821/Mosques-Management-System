import tkinter as tk
from tkinter import messagebox
import sqlite3

class Mosque:
    def __init__(self, ID, name, m_type, address, coordinates, imam_name):
       
        self.id = ID
        self.name = name
        self.m_type = m_type
        self.address = address
        self.coordinates = coordinates
        self.imam_name = imam_name

class Database:
    def __init__(self):
        self.conn = sqlite3.connect("mosques.db")
        self.cur = self.conn.cursor()
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS Mosq (
                ID INTEGER PRIMARY KEY,
                Name TEXT,
                Type TEXT,
                Address TEXT,
                Coordinates TEXT,
                Imam_name TEXT
            )
        """)
        self.conn.commit()

    def Display(self):
        self.cur.execute("SELECT * FROM Mosq")
        return self.cur.fetchall()

    def Search(self, name):
        self.cur.execute("SELECT * FROM Mosq WHERE Name=?", (name,))
        return self.cur.fetchone()

    def Insert(self, ID, name, m_type, address, coordinates, Imam_name):
        self.cur.execute("INSERT INTO Mosq VALUES (?,?,?,?,?,?)", 
                         (ID, name, m_type, address, coordinates, Imam_name))
        self.conn.commit()

    def Delete(self, ID):
        self.cur.execute("DELETE FROM Mosq WHERE ID=?", (ID,))
        self.conn.commit()

    def __del__(self):
        self.conn.close()

class MosqueSystem:
    def __init__(self, root):
        self.db = Database()
        self.root = root
        self.root.title("Mosques Management System")

        
        tk.Label(root, text="ID").grid(row=0, column=0)
        self.id_var = tk.StringVar()
        tk.Entry(root, textvariable=self.id_var).grid(row=0, column=1)

        tk.Label(root, text="Name").grid(row=0, column=2)
        self.name_var = tk.StringVar()
        tk.Entry(root, textvariable=self.name_var).grid(row=0, column=3)

        tk.Label(root, text="Type").grid(row=1, column=0)
        self.type_var = tk.StringVar()
        self.type_var.set("Local Mosque")
        tk.OptionMenu(root, self.type_var, "Grand Mosque", "Local Mosque", "Eid Musalla").grid(row=1, column=1, sticky="ew")

        tk.Label(root, text="Address").grid(row=1, column=2)
        self.addr_var = tk.StringVar()
        tk.Entry(root, textvariable=self.addr_var).grid(row=1, column=3)

        tk.Label(root, text="Coordinates").grid(row=2, column=0)
        self.coord_var = tk.StringVar()
        tk.Entry(root, textvariable=self.coord_var).grid(row=2, column=1)

        tk.Label(root, text="Imam_name").grid(row=2, column=2)
        self.imam_var = tk.StringVar()
        tk.Entry(root, textvariable=self.imam_var).grid(row=2, column=3)

        
        self.list_box = tk.Listbox(root, height=10, width=50)
        self.list_box.grid(row=0, column=4, rowspan=6, padx=10, pady=10)

        
        tk.Button(root, text="Display All", width=15, command=self.display_all).grid(row=3, column=1)
        tk.Button(root, text="Search By Name", width=15, command=self.search_entry).grid(row=3, column=2)
        tk.Button(root, text="Add Entry", width=15, command=self.add_entry).grid(row=4, column=1)
        tk.Button(root, text="Delete entry", width=15, command=self.delete_entry).grid(row=4, column=2)

    def display_all(self):
        self.list_box.delete(0, tk.END)
        for row in self.db.Display():
            self.list_box.insert(tk.END, row)

    def search_entry(self):
        self.list_box.delete(0, tk.END)
        row = self.db.Search(self.name_var.get())
        if row:
            self.list_box.insert(tk.END, row)
        else:
            messagebox.showwarning("Error", "Mosque name not found")

    def add_entry(self):
        try:
            
            new_mosque = Mosque(
                self.id_var.get(),
                self.name_var.get(),
                self.type_var.get(),
                self.addr_var.get(),
                self.coord_var.get(),
                self.imam_var.get()
            )

            
            self.db.Insert(
                new_mosque.id, 
                new_mosque.name, 
                new_mosque.m_type,
                new_mosque.address, 
                new_mosque.coordinates, 
                new_mosque.imam_name
            )
            self.display_all()
            messagebox.showinfo("Success", "Entry added successfully")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add entry: {e}")

    def delete_entry(self):
        self.db.Delete(self.id_var.get())
        self.display_all()

if __name__ == "__main__":
    main_root = tk.Tk()
    app = MosqueSystem(main_root)
    main_root.mainloop()