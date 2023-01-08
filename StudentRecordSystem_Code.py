from tkinter import *
import tkinter.messagebox as mb
from tkinter.simpledialog import askstring
from tkinter import ttk, Scrollbar
import mysql.connector

print("\nDatabase Systems - CENG301 Fall 2022-2023 Project")
print("Marya Aktas 200444001\nMert Ornek 190444076\nCihan Balkir 190444053\n")
print("Wellcome to Student Management System!!\nIn this app, you can record or delete student records.")
print("You can see the GPA\'s of each student, you can see the grades and delete the database.")
print("\nIn \'Students\' database, there are 4 tables, which are:\nStudent\nDepartment\nCourses\nGrades\n")
print("The courses and the departments are previously specified and will be inserted in the database automatically.")
print("Each student can take many courses from different departments.")

db_connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="CuteKitten12.")

db_cursor = db_connection.cursor(buffered=True)


class StudentManage(Tk):
    def __init__(self):
        super().__init__()

        self.title('Student Record System')
        self.geometry('1200x800')

        self.FName = StringVar()
        self.LName = StringVar()
        self.ID = StringVar()
        self.grade = StringVar()
        self.course_id = StringVar()
        self.dept_id = StringVar()

        self.selected_id = StringVar()  # For selecting an ID and showing the courses

        Label(self, text="STUDENT RECORD SYSTEM", font=('Helvetica', 15), bg="#57356A", fg="white", pady=5).pack(
            side=TOP, fill=X)
        self.top_frame = Frame(self, bg="#AE9CC2")
        self.top_frame.place(x=0, y=30, height=400, width=1200)
        self.bottom_frame = Frame(self, bg="#AA98B5")
        self.bottom_frame.place(x=0, y=400, height=410, width=1200)

        self.LABEL_LIST = ["First Name:", "Last Name:", "Student ID:", "Grade:", "Department Code:", "Course Code:"]
        self.ENTRY_LIST = [self.FName, self.LName, self.ID, self.grade, self.dept_id, self.course_id]

        for i in range(len(self.ENTRY_LIST)-2):
            Label(self.top_frame, text=self.LABEL_LIST[i], font=('Helvetica', 14), padx=7, bg="#856AA2", fg="white",
                  width=15).place(x=30, y=(i+1) * 50)
            Entry(self.top_frame, width=30, textvariable=self.ENTRY_LIST[i], font=('Helvetica', 14), fg="#5C4773",
                  borderwidth=3).place(x=220, y=(i+1) * 50)

        Label(self.top_frame, text=self.LABEL_LIST[-2], font=('Helvetica', 14), padx=7, bg="#856AA2", fg="white",
              width=15).place(x=30, y=250)  # Label of radiobutton 'Department Code'
        Label(self.top_frame, text=self.LABEL_LIST[-1], font=('Helvetica', 14), padx=7, bg="#856AA2", fg="white",
              width=15).place(x=30, y=300)  # Label of radiobutton 'Course  Code'

        self.DEPT_CODE = ["EEE", "AEE", "CENG"]  # Text of the radiobuttons
        self.DEPT_NAME = ["Electrical and Electronics Engineering", "Aeronautical Engineering", "Computer Engineering"]
        self.dept_id.set(self.DEPT_CODE[0])
        for i in range(len(self.DEPT_CODE)):
            Radiobutton(self.top_frame, text=self.DEPT_CODE[i], variable=self.dept_id, value=self.DEPT_CODE[i],
                        command=self.change_dept, padx=5, bg="white", fg="#8B6914").place(x=220 + i*70, y=250)

        self.BUTTON_TEXT = ["Add Record or Update Grade", "Show Students", "Show Grades", "Show Courses",
                            "Calculate GPA\'s", "Show Courses of a Student", "Delete Student", "Clear Entries",
                            "Remove Database", "Exit"]
        self.BUTTON_COMMANDS = [self.add_record, self.show_students, self.show_grades, self.show_all_courses,
                                self.show_gpa, self.show_student_courses, self.remove_record, self.reset_fields,
                                self.remove_database, self.exit]

        for i in range(0, 5):
            Button(self.top_frame, text=self.BUTTON_TEXT[i], font=('Helvetica', 14), relief=RAISED, bg="#E4DEEA",
                   fg="#371C4B", command=self.BUTTON_COMMANDS[i], width=22, height=2).place(x=600, y=60*i + 13)
            Button(self.top_frame, text=self.BUTTON_TEXT[i + 5], font=('Helvetica', 14), relief=RAISED, bg="#E4DEEA",
                   fg="#371C4B", command=self.BUTTON_COMMANDS[i + 5], width=22, height=2).place(x=900, y=60 * i + 13)

        self.tree_header = Label(self.bottom_frame, text='Student Records', font=('Helvetica', 13), relief=RAISED,
                                 bg='#5C4773', fg='#F4F2F7', pady=5)
        self.tree_header.pack(side=TOP, fill=BOTH)

        # For arranging the colors of the treeview
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("Treeview", background="white", foreground="black")
        style.configure("Treeview.Heading", background="#897098", foreground="white")

        # Creating the treeview for showing the database
        self.CENG_COURSE_CODE = ["CENG205", "CENG476", "CENG208"]
        self.CENG_COURSE_NAME = ["Logic Design", "Microprocessors", "Deep Learning"]
        self.EEE_COURSE_CODE = ["EEE202", "EEE301", "EEE414"]
        self.EEE_COURSE_NAME = ["Electronic Circuits", "Signals and Systems", "Fuzzy Logic"]
        self.AEE_COURSE_CODE = ["AEE172", "AEE451", "AEE361"]
        self.AEE_COURSE_NAME = ["Aircraft Performance", "Applied Elasticity", "Aircraft Design"]

        self.create_tables()  # Creating the database
        self.show_students()  # Showing the students

    def change_dept(self):
        if self.dept_id.get() == "CENG":
            self.course_id.set(self.CENG_COURSE_CODE[0])
            for i in range(len(self.CENG_COURSE_CODE)):
                Radiobutton(self.top_frame, text=self.CENG_COURSE_CODE[i], variable=self.course_id,
                            value=self.CENG_COURSE_CODE[i], bg="white", fg="#8B2500", padx=4).place(x=220+i*100, y=300)
        elif self.dept_id.get() == "EEE":
            self.course_id.set(self.EEE_COURSE_CODE[0])
            for i in range(len(self.EEE_COURSE_CODE)):
                Radiobutton(self.top_frame, text=self.EEE_COURSE_CODE[i], variable=self.course_id,
                            value=self.EEE_COURSE_CODE[i], bg="white", fg="#8B2500", padx=10).place(x=220+i*100, y=300)
        elif self.dept_id.get() == "AEE":
            self.course_id.set(self.AEE_COURSE_CODE[0])
            for i in range(len(self.AEE_COURSE_CODE)):
                Radiobutton(self.top_frame, text=self.AEE_COURSE_CODE[i], variable=self.course_id,
                            value=self.AEE_COURSE_CODE[i], bg="white", fg="#8B2500", padx=10).place(x=220+i*100, y=300)

    def reset_fields(self):
        for i in range(len(self.ENTRY_LIST)-2):
            self.ENTRY_LIST[i].set('')

        self.dept_id.set('EEE')

    def exit(self):
        msgbox = mb.askquestion('Exit The System', 'Are you sure you want to exit the application?', icon='warning')
        if msgbox == 'yes':
            self.destroy()

    def remove_database(self):
        msgbox = mb.askquestion('Delete Database', 'Are you sure you want to delete the WHOLE database?', icon='warning')
        if msgbox == 'yes':
            if not db_connection.is_connected():
                db_connection.connect()
            db_cursor.execute('drop database Students')
            self.destroy()

    def create_tables(self):
        if not db_connection.is_connected():
            db_connection.connect()
            # executing cursor with execute method and pass SQL query
        db_cursor.execute("CREATE DATABASE IF NOT EXISTS Students")  # Create a Database Named Students
        db_cursor.execute("use Students")  # Interact with Students Database
        # creating required tables
        db_cursor.execute("create table if not exists Department(Dept_Code VARCHAR(10), Dept_Name VARCHAR(50) UNIQUE," +
                          " PRIMARY KEY(Dept_Code))")
        db_cursor.execute("create table if not exists Courses(Course_Code VARCHAR(10), Course_Name VARCHAR(50) " +
                          "UNIQUE, Dept_Code VARCHAR(10), FOREIGN KEY(Dept_Code) REFERENCES Department(Dept_Code)" +
                          " ON DELETE CASCADE, PRIMARY KEY(Course_Code, Dept_Code))")
        db_cursor.execute("create table if not exists Student(ID INT NOT NULL, FName VARCHAR(30), LName VARCHAR(30), " +
                          "PRIMARY KEY(ID))")
        db_cursor.execute("create table if not exists Grades(st_id INT NOT NULL, Course_Code VARCHAR(10), grade " +
                          "INT CHECK (grade<101 AND grade>-1), Dept_Code VARCHAR(10), FOREIGN KEY(st_id) REFERENCES " +
                          "Student(ID) ON DELETE CASCADE ON UPDATE CASCADE, FOREIGN KEY(Course_Code, Dept_Code) " +
                          "REFERENCES Courses(Course_Code, Dept_Code) ON DELETE CASCADE, UNIQUE(st_id, Course_Code))")
        for i in range(len(self.DEPT_CODE)):
            db_cursor.execute("INSERT IGNORE INTO Department (Dept_Code, Dept_Name) VALUES ('%s','%s')" %
                              (self.DEPT_CODE[i], self.DEPT_NAME[i]))
        for i in range(len(self.AEE_COURSE_CODE)):
            db_cursor.execute("INSERT IGNORE INTO Courses (Course_Code, Course_Name, Dept_Code) VALUES ('%s','%s','%s')"
                              % (self.AEE_COURSE_CODE[i], self.AEE_COURSE_NAME[i], "AEE"))
        for i in range(len(self.CENG_COURSE_CODE)):
            db_cursor.execute("INSERT IGNORE INTO Courses (Course_Code, Course_Name, Dept_Code) VALUES ('%s','%s','%s')"
                              % (self.CENG_COURSE_CODE[i], self.CENG_COURSE_NAME[i], "CENG"))
        for i in range(len(self.EEE_COURSE_CODE)):
            db_cursor.execute("INSERT IGNORE INTO Courses (Course_Code, Course_Name, Dept_Code) VALUES ('%s','%s','%s')"
                              % (self.EEE_COURSE_CODE[i], self.EEE_COURSE_NAME[i], "EEE"))
        db_connection.commit()

    def add_record(self):
        if not db_connection.is_connected():
            db_connection.connect()
        firstname = self.FName.get()  # Retrieving entered first name
        lastname = self.LName.get()  # Retrieving entered last name
        st_id = self.ID.get()  # Retrieving entered contact number
        dept = self.dept_id.get()  # Retrieving entered city name
        course = self.course_id.get()  # Retrieving entered state name
        grade = self.grade.get()  # Retrieving chosen date

        list1 = [firstname, lastname, st_id, grade, dept, course]
        list2 = ["firstname", "lastname", "student ID", "grade", "course code", "department code"]
        # validating Entry Widgets
        for i in range(len(list1)):
            if list1[i] == "":
                mb.showinfo('Information', "Please enter the {}!".format(list2[i]))
                return
        try:
            query = "INSERT IGNORE INTO Student(ID, FName, LName) VALUES('%s','%s','%s')" % (st_id, firstname, lastname)
            db_cursor.execute(query)
            query = "REPLACE INTO Grades(st_id, Dept_Code, Course_Code, grade) VALUES('%s','%s','%s','%s')" \
                    % (st_id, dept, course, grade)
            db_cursor.execute(query)
            mb.showinfo('Information', "Student Registered / Grade Updated Successfully!")
            db_connection.commit()
        except mysql.connector.Error:
            db_connection.rollback()
            mb.showinfo('Information', "Student Registration Failed!\nThe error is:\n\n%s!" % mysql.connector.Error)
        finally:
            db_connection.close()
        self.show_students()

    def show_students(self):
        self.place_records()
        if not db_connection.is_connected():
            db_connection.connect()
        self.display.delete(*self.display.get_children())  # clears the treeview tvStudent
        db_cursor.execute("use Students")
        db_cursor.execute('SELECT DISTINCT ID, FName, LName, Dept_Code FROM Student, Grades WHERE st_id=ID ORDER BY ID')
        tuples = db_cursor.fetchall()
        for row in tuples:
            self.display.insert("", 'end', values=row)

    def show_gpa(self):
        self.place_gpa()
        if not db_connection.is_connected():
            db_connection.connect()
        self.display.delete(*self.display.get_children())  # clears the treeview tvStudent
        db_cursor.execute("use Students")
        db_cursor.execute('SELECT ID, AVG(grade) FROM Student, Grades, Courses WHERE ID=st_id AND ' +
                          'Courses.Course_Code=Grades.Course_Code GROUP BY ID ORDER BY AVG(grade) DESC')
        tuples = db_cursor.fetchall()
        for row in tuples:
            self.display.insert("", 'end', values=row)

    def show_grades(self):
        self.place_grades()
        if not db_connection.is_connected():
            db_connection.connect()
        self.display.delete(*self.display.get_children())  # clears the treeview tvStudent
        db_cursor.execute("use Students")
        db_cursor.execute('SELECT DISTINCT ID, Courses.Course_Code, Course_Name, FName, LName, grade FROM Student, ' +
                          'Grades, Courses WHERE ID=st_id AND Courses.Course_Code=Grades.Course_Code ORDER BY ID')
        tuples = db_cursor.fetchall()
        for row in tuples:
            self.display.insert("", 'end', values=row)

    def show_student_courses(self):
        string = askstring('Select ID', 'What is the id of the student that you want see the courses of?')
        self.selected_id.set(string)
        if string == "" or self.selected_id.get() == None:
            mb.showinfo('Information', "Please Enter an ID!")
            return
        self.place_courses()
        if not db_connection.is_connected():
            db_connection.connect()
        self.display.delete(*self.display.get_children())  # clears the treeview tvStudent
        db_cursor.execute("use Students")
        db_cursor.execute("SELECT DISTINCT Grades.Course_Code, Course_Name, Dept_Name FROM Student, Grades, " +
                          "Department, Courses WHERE ID=st_id AND Courses.Dept_Code=Department.Dept_Code AND " +
                          "Grades.Course_Code=Courses.Course_Code AND ID='%s'" % self.selected_id.get())
        tuples = db_cursor.fetchall()
        for row in tuples:
            self.display.insert("", 'end', values=row)

    def show_all_courses(self):
        self.place_courses()
        self.tree_header.config(text="All Courses in the Database")
        if not db_connection.is_connected():
            db_connection.connect()
        self.display.delete(*self.display.get_children())  # clears the treeview tvStudent
        db_cursor.execute("use Students")
        db_cursor.execute("SELECT Course_Code, Course_Name, Dept_Name FROM Courses, Department WHERE " +
                          "Courses.Dept_Code=Department.Dept_Code")
        tuples = db_cursor.fetchall()
        for row in tuples:
            self.display.insert("", 'end', values=row)

    def remove_record(self):
        if not self.display.selection():
            mb.showerror('Removing Failed!', 'Please select a student from the database!')
        else:
            values = self.display.item(self.display.focus())
            selection = values["values"]
            if not type(selection[0]) == int:
                if self.tree_header.cget("text") == "All Courses in the Database":
                    mb.showerror('Removing Failed!', 'Please select a student from the database!')
                    return
                else:
                    sel_id = self.selected_id.get()  # selected id for deleting
            elif type(selection[0]) == int:
                sel_id = selection[0]  # selected id for deleting
            warning = 'Are you sure? Do you want to delete the student with id "%s" from the records?' % sel_id
            msgbox = mb.askquestion('Delete Record', warning, icon='warning')
            if msgbox == 'yes':
                if not db_connection.is_connected():
                    db_connection.connect()
                db_cursor.execute("use Students")  # Interact with Student Database
                db_cursor.execute('DELETE FROM Student WHERE ID=%s' % sel_id)
                db_connection.commit()
                mb.showinfo("Information", "Student Record Deleted Successfully!")
                self.show_students()
                self.reset_fields()

    def place_records(self):
        self.tree_header.config(text="Student Records")
        self.display = ttk.Treeview(self.bottom_frame, height=100, selectmode=BROWSE,
                                    columns=("Student ID", "First Name", "Last Name", "Takes Courses"))
        self.X_scroller = Scrollbar(self.display, orient=HORIZONTAL, command=self.display.xview)
        self.Y_scroller = Scrollbar(self.display, orient=VERTICAL, command=self.display.yview)
        self.X_scroller.pack(side=BOTTOM, fill=X)
        self.Y_scroller.pack(side=RIGHT, fill=Y)
        self.display.config(yscrollcommand=self.Y_scroller.set, xscrollcommand=self.X_scroller.set)
        headings = ['Student ID', 'First Name', 'Last Name', 'Takes Courses From']
        self.display.column('#0', width=0, stretch=NO)
        for i in range(len(headings)):
            number = '#' + str(i+1)
            self.display.heading(number, text=headings[i], anchor=CENTER)
            self.display.column(number, width=300, stretch=NO)
        self.display.place(y=30, relwidth=1, relheight=0.9, relx=0)

    def place_grades(self):
        self.tree_header.config(text="Grades")
        self.display = ttk.Treeview(self.bottom_frame, height=100, selectmode=BROWSE, columns=('Student ID',
                                                                                               'Course Code',
                                                                                               "First Name",
                                                                                               "Last Name",
                                                                                               "Course Name",
                                                                                               "Grade"))
        self.X_scroller = Scrollbar(self.display, orient=HORIZONTAL, command=self.display.xview)
        self.Y_scroller = Scrollbar(self.display, orient=VERTICAL, command=self.display.yview)
        self.X_scroller.pack(side=BOTTOM, fill=X)
        self.Y_scroller.pack(side=RIGHT, fill=Y)

        self.display.config(yscrollcommand=self.Y_scroller.set, xscrollcommand=self.X_scroller.set)

        headings = ['Student ID', 'Course Code', 'Course Name', 'First Name', 'Last Name', 'Grade']
        self.display.column('#0', width=0, stretch=NO)
        for i in range(len(headings)):
            number = '#' + str(i + 1)
            self.display.heading(number, text=headings[i], anchor=CENTER)
            self.display.column(number, width=200, stretch=NO)
        self.display.place(y=30, relwidth=1, relheight=0.9, relx=0)

    def place_gpa(self):
        self.tree_header.config(text="GPA\'s of Each Student")
        self.display = ttk.Treeview(self.bottom_frame, height=100, selectmode=BROWSE,
                                    columns=('Student ID', "GPA"))
        self.X_scroller = Scrollbar(self.display, orient=HORIZONTAL, command=self.display.xview)
        self.Y_scroller = Scrollbar(self.display, orient=VERTICAL, command=self.display.yview)
        self.X_scroller.pack(side=BOTTOM, fill=X)
        self.Y_scroller.pack(side=RIGHT, fill=Y)

        self.display.config(yscrollcommand=self.Y_scroller.set, xscrollcommand=self.X_scroller.set)

        headings = ['Student ID', 'GPA']
        self.display.column('#0', width=0, stretch=NO)
        for i in range(len(headings)):
            number = '#' + str(i + 1)
            self.display.heading(number, text=headings[i], anchor=CENTER)
            self.display.column(number, width=600, stretch=NO)
        self.display.place(y=30, relwidth=1, relheight=0.9, relx=0)

    def place_courses(self):
        self.tree_header.config(text="The Courses of the Student with ID \'%s\'" % self.selected_id.get())
        self.display = ttk.Treeview(self.bottom_frame, height=100, selectmode=BROWSE,
                                    columns=("Course Code", "Course Name", "Department Name"))
        self.X_scroller = Scrollbar(self.display, orient=HORIZONTAL, command=self.display.xview)
        self.Y_scroller = Scrollbar(self.display, orient=VERTICAL, command=self.display.yview)
        self.X_scroller.pack(side=BOTTOM, fill=X)
        self.Y_scroller.pack(side=RIGHT, fill=Y)
        self.display.config(yscrollcommand=self.Y_scroller.set, xscrollcommand=self.X_scroller.set)
        headings = ['Course Code', 'Course Name', 'Course\'s Department Name']
        self.display.column('#0', width=0, stretch=NO)
        for i in range(len(headings)):
            number = '#' + str(i + 1)
            self.display.heading(number, text=headings[i], anchor=CENTER)
            self.display.column(number, width=400, stretch=NO)
        self.display.place(y=30, relwidth=1, relheight=0.9, relx=0)


if __name__ == "__main__":
    app = StudentManage()
    app.mainloop()