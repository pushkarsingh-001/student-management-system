# Combined Student Management System - Enhanced Version
# Includes database creation and GUI application in one file

import sqlite3
import random
import os
from tkinter import Tk, StringVar, Label, Entry, Button, Frame, RIGHT, Y, BOTH, END, BOTTOM, X, LEFT
from tkinter import ttk, messagebox

# Database file path
DB_FILE = "students.db"

def create_database():
    """Create new database with sample students"""
    # Remove old database if exists
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)
    
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # Create Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS students(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        age TEXT,
        course TEXT,
        phone TEXT
    )
    """)
    
    # Sample Data
    names = [
        "Aarav Sharma", "Vivaan Singh", "Aditya Kumar", "Krishna Patel", "Arjun Verma",
        "Sai Raj", "Rohan Gupta", "Mohit Yadav", "Rahul Mishra", "Yash Tiwari",
        "Priya Sharma", "Ananya Singh", "Sneha Patel", "Kavya Verma", "Riya Gupta",
        "Neha Yadav", "Pooja Mishra", "Ishita Jain", "Simran Kaur", "Nikita Das",
        "Harsh Raj", "Manish Kumar", "Deepak Singh", "Nitin Sharma", "Aman Verma",
        "Sakshi Gupta", "Tanvi Jain", "Megha Singh", "Payal Patel", "Ritika Das",
        "Dev Kumar", "Shivam Yadav", "Ankit Mishra", "Rajat Tiwari", "Sumit Gupta",
        "Muskan Sharma", "Aditi Singh", "Komal Verma", "Preeti Yadav", "Nandini Jain",
        "Karan Patel", "Varun Kumar", "Ujjwal Singh", "Saurabh Gupta", "Abhishek Raj",
        "Jyoti Sharma", "Palak Verma", "Mansi Patel", "Tanya Singh", "Rohit Kumar"
    ]
    
    courses = ["BCA", "BBA", "B.Tech", "MBA", "MCA"]
    
    for i in range(50):
        name = names[i]
        age = str(random.randint(18, 25))
        course = random.choice(courses)
        phone = "9" + str(random.randint(100000000, 999999999))
        
        cursor.execute(
            "INSERT INTO students(name, age, course, phone) VALUES (?, ?, ?, ?)",
            (name, age, course, phone)
        )
    
    conn.commit()
    conn.close()

# ==================== GUI APPLICATION ====================

# Create fresh database on startup
create_database()

# Database connection
conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()

# Create table if not exists
cursor.execute("""
CREATE TABLE IF NOT EXISTS students(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    age TEXT,
    course TEXT,
    phone TEXT
)
""")
conn.commit()

# Window
root = Tk()
root.title("Student Management System")
root.geometry("900x600")
root.configure(bg="#f0f0f0")

# Variables
name_var = StringVar()
age_var = StringVar()
course_var = StringVar()
phone_var = StringVar()
search_var = StringVar()

# Style
style = ttk.Style()
style.theme_use("clam")
style.configure("Treeview", rowheight=25, font=("Arial", 10))
style.configure("Treeview.Heading", font=("Arial", 10, "bold"))
style.map("Treeview", background=[("selected", "#347CEC")])

# Functions
def show_message(title, message, msg_type="info"):
    """Display message box to user"""
    if msg_type == "info":
        messagebox.showinfo(title, message)
    elif msg_type == "warning":
        messagebox.showwarning(title, message)
    elif msg_type == "error":
        messagebox.showerror(title, message)

def validate_input():
    """Validate that all fields are filled"""
    if not name_var.get().strip():
        show_message("Validation Error", "Please enter student name!", "warning")
        return False
    if not age_var.get().strip():
        show_message("Validation Error", "Please enter student age!", "warning")
        return False
    if not course_var.get().strip():
        show_message("Validation Error", "Please enter course!", "warning")
        return False
    if not phone_var.get().strip():
        show_message("Validation Error", "Please enter phone number!", "warning")
        return False
    # Validate age is numeric
    try:
        age = int(age_var.get())
        if age < 1 or age > 100:
            show_message("Validation Error", "Age must be between 1 and 100!", "warning")
            return False
    except ValueError:
        show_message("Validation Error", "Age must be a valid number!", "warning")
        return False
    # Validate phone (10 digits starting with 9)
    phone = phone_var.get().strip()
    if len(phone) != 10 or not phone.isdigit():
        show_message("Validation Error", "Phone must be 10 digits!", "warning")
        return False
    return True

def get_student_count():
    """Get total number of students"""
    cursor.execute("SELECT COUNT(*) FROM students")
    return cursor.fetchone()[0]

def fetch_data(search_text=""):
    """Fetch all student data from database"""
    try:
        table.delete(*table.get_children())
        if search_text:
            cursor.execute("SELECT * FROM students WHERE name LIKE ? OR course LIKE ? OR phone LIKE ?",
                       (f"%{search_text}%", f"%{search_text}%", f"%{search_text}%"))
        else:
            cursor.execute("SELECT * FROM students")
        rows = cursor.fetchall()
        for row in rows:
            table.insert("", END, values=row)
        status_label.config(text=f"Total Students: {len(rows)}")
    except sqlite3.Error as e:
        show_message("Database Error", f"Error fetching data: {e}", "error")

def add_student():
    """Add a new student"""
    if not validate_input():
        return
    try:
        cursor.execute("INSERT INTO students(name, age, course, phone) VALUES (?, ?, ?, ?)",
                       (name_var.get().strip(), age_var.get().strip(), 
                        course_var.get().strip(), phone_var.get().strip()))
        conn.commit()
        fetch_data(search_var.get())
        clear()
        show_message("Success", "Student added successfully!")
    except sqlite3.Error as e:
        show_message("Database Error", f"Error adding student: {e}", "error")

def clear():
    """Clear all input fields"""
    name_var.set("")
    age_var.set("")
    course_var.set("")
    phone_var.set("")

def get_cursor(event):
    """Get selected row data"""
    row = table.focus()
    data = table.item(row)
    values = data["values"]

    if values:
        name_var.set(values[1])
        age_var.set(values[2])
        course_var.set(values[3])
        phone_var.set(values[4])

def update_student():
    """Update selected student"""
    row = table.focus()
    data = table.item(row)
    values = data["values"]
    
    if not values:
        show_message("Selection Error", "Please select a student to update!", "warning")
        return
    
    if not validate_input():
        return
    try:
        cursor.execute("""
        UPDATE students SET name=?, age=?, course=?, phone=? WHERE id=?
        """, (name_var.get().strip(), age_var.get().strip(), 
             course_var.get().strip(), phone_var.get().strip(), values[0]))
        conn.commit()
        fetch_data(search_var.get())
        clear()
        show_message("Success", "Student updated successfully!")
    except sqlite3.Error as e:
        show_message("Database Error", f"Error updating student: {e}", "error")

def delete_student():
    """Delete selected student"""
    row = table.focus()
    data = table.item(row)
    values = data["values"]
    
    if not values:
        show_message("Selection Error", "Please select a student to delete!", "warning")
        return
    
    confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this student?")
    if not confirm:
        return
    
    try:
        cursor.execute("DELETE FROM students WHERE id=?", (values[0],))
        conn.commit()
        fetch_data(search_var.get())
        clear()
        show_message("Success", "Student deleted successfully!")
    except sqlite3.Error as e:
        show_message("Database Error", f"Error deleting student: {e}", "error")

def search_student(event=None):
    """Search students"""
    search_text = search_var.get().strip()
    fetch_data(search_text)

def refresh_data():
    """Refresh data and clear search"""
    search_var.set("")
    fetch_data()
    show_message("Refresh", "Data refreshed successfully!")

def on_closing():
    """Close database connection and window"""
    conn.close()
    root.destroy()

# ==================== UI LAYOUT ====================

# Header
header_frame = Frame(root, bg="#347CEC", height=50)
header_frame.pack(fill=X)
Label(header_frame, text="Student Management System", font=("Arial", 18, "bold"), 
      bg="#347CEC", fg="white").pack(pady=10)

# Search Frame
search_frame = Frame(root, bg="#f0f0f0")
search_frame.pack(fill=X, padx=10, pady=5)
Label(search_frame, text="Search:", font=("Arial", 10, "bold"), bg="#f0f0f0").pack(side=LEFT)
Entry(search_frame, textvariable=search_var, font=("Arial", 10), width=30).pack(side=LEFT, padx=5)
Button(search_frame, text="🔍 Search", command=search_student, font=("Arial", 10)).pack(side=LEFT)
Button(search_frame, text="🔄 Refresh", command=refresh_data, font=("Arial", 10)).pack(side=LEFT, padx=5)

# Input Fields Frame
input_frame = Frame(root, bg="#f0f0f0")
input_frame.pack(fill=X, padx=10, pady=5)

Label(input_frame, text="Name:", font=("Arial", 10, "bold"), bg="#f0f0f0").grid(row=0, column=0, padx=5, pady=5)
Entry(input_frame, textvariable=name_var, font=("Arial", 10), width=20).grid(row=0, column=1, padx=5, pady=5)

Label(input_frame, text="Age:", font=("Arial", 10, "bold"), bg="#f0f0f0").grid(row=0, column=2, padx=5, pady=5)
Entry(input_frame, textvariable=age_var, font=("Arial", 10), width=10).grid(row=0, column=3, padx=5, pady=5)

Label(input_frame, text="Course:", font=("Arial", 10, "bold"), bg="#f0f0f0").grid(row=0, column=4, padx=5, pady=5)
Entry(input_frame, textvariable=course_var, font=("Arial", 10), width=20).grid(row=0, column=5, padx=5, pady=5)

Label(input_frame, text="Phone:", font=("Arial", 10, "bold"), bg="#f0f0f0").grid(row=1, column=0, padx=5, pady=5)
Entry(input_frame, textvariable=phone_var, font=("Arial", 10), width=20).grid(row=1, column=1, padx=5, pady=5)

# Buttons Frame
btn_frame = Frame(root, bg="#f0f0f0")
btn_frame.pack(fill=X, padx=10, pady=10)

Button(btn_frame, text="➕ Add", width=12, command=add_student, bg="#4CAF50", fg="white", 
       font=("Arial", 10, "bold")).pack(side=LEFT, padx=5)
Button(btn_frame, text="✏️ Update", width=12, command=update_student, bg="#2196F3", fg="white",
       font=("Arial", 10, "bold")).pack(side=LEFT, padx=5)
Button(btn_frame, text="🗑️ Delete", width=12, command=delete_student, bg="#f44336", fg="white",
       font=("Arial", 10, "bold")).pack(side=LEFT, padx=5)
Button(btn_frame, text=" Clear ", command=clear, bg="#9E9E9E", fg="white",
       font=("Arial", 10, "bold")).pack(side=LEFT, padx=5)

# Table Frame
table_frame = Frame(root, bg="#f0f0f0")
table_frame.pack(fill=BOTH, expand=True, padx=10, pady=5)

# Vertical scrollbar
yscroll = ttk.Scrollbar(table_frame, orient="vertical")
yscroll.pack(side=RIGHT, fill=Y)

# Horizontal scrollbar
xscroll = ttk.Scrollbar(table_frame, orient="horizontal")
xscroll.pack(side=BOTTOM, fill=X)

# Table
table = ttk.Treeview(table_frame, columns=("id", "name", "age", "course", "phone"), 
                   show="headings", yscrollcommand=yscroll.set, xscrollcommand=xscroll.set)

yscroll.config(command=table.yview)
xscroll.config(command=table.xview)

# Column headings
table.heading("id", text="ID", command=lambda: sort_column("id"))
table.heading("name", text="Name", command=lambda: sort_column("name"))
table.heading("age", text="Age", command=lambda: sort_column("age"))
table.heading("course", text="Course", command=lambda: sort_column("course"))
table.heading("phone", text="Phone", command=lambda: sort_column("phone"))

# Column widths
table.column("id", width=50, minwidth=50)
table.column("name", width=200, minwidth=150)
table.column("age", width=80, minwidth=80)
table.column("course", width=150, minwidth=100)
table.column("phone", width=150, minwidth=120)

table.pack(fill=BOTH, expand=True)
table.bind("<ButtonRelease-1>", get_cursor)

# Status Bar
status_frame = Frame(root, bg="#347CEC")
status_frame.pack(fill=X)
status_label = Label(status_frame, text="Total Students: 0", font=("Arial", 10), bg="#347CEC", fg="white")
status_label.pack(pady=5)

# Keyboard shortcuts
root.bind("<Control-f>", search_student)
root.bind("<Return>", lambda e: search_student())
root.bind("<Escape>", lambda e: clear())

# Close window handler
root.protocol("WM_DELETE_WINDOW", on_closing)

# Sort functionality
sort_column_col = None
sort_reverse = False

def sort_column(col):
    """Sort table by column"""
    global sort_column_col, sort_reverse
    
    if sort_column_col == col:
        sort_reverse = not sort_reverse
    else:
        sort_reverse = False
        sort_column_col = col
    
    try:
        table.delete(*table.get_children())
        cursor.execute(f"SELECT * FROM students ORDER BY {col} {'DESC' if sort_reverse else 'ASC'}")
        rows = cursor.fetchall()
        for row in rows:
            table.insert("", END, values=row)
    except sqlite3.Error as e:
        show_message("Database Error", f"Error sorting: {e}", "error")

# Fetch initial data
fetch_data()
root.mainloop()
