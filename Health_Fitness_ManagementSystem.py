# Health and Fitness Management System
# Insert postGres password where postGresPassword = "12345" is below
# Create a databse in pgAdmin named "HFClubDB"

global postGresPassword
postGresPassword = "12345"

import psycopg2
import tkinter as tk
from tkinter import messagebox

# Login page code
def create_login_page():
   window = tk.Tk()
   window.title("Health and Fitness Management System Login")
   window.geometry("500x200")

   username_label = tk.Label(window, text="Username")
   username_label.pack()

   username_entry = tk.Entry(window)
   username_entry.pack()

   password_label = tk.Label(window, text="Password")
   password_label.pack()

   password_entry = tk.Entry(window)
   password_entry.pack()

   login_button = tk.Button(window, text="Login", command=lambda: login(username_entry.get(), password_entry.get(), window))
   login_button.pack()

   window.mainloop()

# Login button pressed
def login(username, password, window):
   global login_result
   conn = psycopg2.connect(dbname="HFClubDB", user="postgres", password=postGresPassword)
   cur = conn.cursor()
   cur.execute("SELECT * FROM \"Users\" WHERE username = %s AND password = %s", (username, password))
   result = cur.fetchone()
   if result is not None:
       login_result = result
       window.destroy()
   else:
       messagebox.showerror("Error", "Invalid username or password")
   cur.close()
   conn.close()

# Admin page
def create_admin_page():
   window = tk.Tk()
   window.title("Admin Page")
   window.geometry("950x650")
   conn = psycopg2.connect(dbname="HFClubDB", user="postgres", password=postGresPassword)
   cur = conn.cursor()
   global rooms_listbox
   global equipment_status_entry
   global room
   global events_listbox
   global event_name_entry
   global event_date_entry
   global event_description_entry
   global event_trainer_entry
   global event_room_entry

   logout_button = tk.Button(window, text="Logout", command=lambda: (window.destroy()))
   logout_button.grid(row=10, column=0)

   # Create event form
   event_form = tk.LabelFrame(window, text="Create Event")
   event_form.grid(row=0, column=0)

   event_name_label = tk.Label(event_form, text="Event Name")
   event_name_label.grid(row=0, column=0)

   event_name_entry = tk.Entry(event_form)
   event_name_entry.grid(row=0, column=1)

   event_date_label = tk.Label(event_form, text="Event Date")
   event_date_label.grid(row=1, column=0)

   event_date_entry = tk.Entry(event_form)
   event_date_entry.grid(row=1, column=1)

   event_description_label = tk.Label(event_form, text="Event Description")
   event_description_label.grid(row=2, column=0)

   event_description_entry = tk.Entry(event_form)
   event_description_entry.grid(row=2, column=1)

   event_trainer_label = tk.Label(event_form, text="Trainer ID")
   event_trainer_label.grid(row=3, column=0)

   event_trainer_entry = tk.Entry(event_form)
   event_trainer_entry.grid(row=3, column=1)

   event_room_label = tk.Label(event_form, text="Room ID")
   event_room_label.grid(row=4, column=0)

   event_room_entry = tk.Entry(event_form)
   event_room_entry.grid(row=4, column=1)

   create_event_button = tk.Button(event_form, text="Create Event", command=create_event)
   create_event_button.grid(row=5, column=0, columnspan=2)
   
   create_event_button = tk.Button(event_form, text="Delete Event", command=delete_event)
   create_event_button.grid(row=6, column=0, columnspan=2)

   # Fetch events from the database
   cur.execute("SELECT * FROM \"GroupEvents\"")
   events = cur.fetchall()

   # Display the list of events
   events_label = tk.Label(window, text="Events")
   events_label.grid(row=3, column=0)

   events_listbox = tk.Listbox(window, width=90)
   for event in events:
        
        # Fetch the trainer name and room name using the trainer ID and room ID
        cur.execute("SELECT username FROM \"Users\" WHERE user_id = (SELECT user_id FROM \"Trainers\" WHERE trainer_id = %s)", (event[4],))
        trainer_name = cur.fetchone()[0]
        cur.execute("SELECT name FROM \"Rooms\" WHERE room_id = %s", (event[5],))
        room_name = cur.fetchone()[0]

        # Count the number of members attending the event
        cur.execute("SELECT COUNT(*) FROM \"MemberGroupEvent\" WHERE event_id = %s", (event[0],))
        member_count = cur.fetchone()[0]

        events_listbox.insert(tk.END, f"{event[0]}: {event[1]}, held by {trainer_name} in room {room_name}. Date: {event[2]}. {member_count} members attending.")

   events_listbox.grid(row=4, column=0)

   # List of rooms and equipment status
   rooms_label = tk.Label(window, text="Rooms")
   rooms_label.grid(row=5, column=3)

   rooms_listbox = tk.Listbox(window, width=60)
   rooms_listbox.grid(row=6, column=3)

   # Fetch room data from the database and insert it into the listbox
   cur.execute("SELECT * FROM \"Rooms\"")
   rooms = cur.fetchall()
   for room in rooms:
       rooms_listbox.insert(tk.END, f"{room[0]}: {room[1]}, Status: {room[2]}")

   equipment_status_entry = tk.Entry(window)
   equipment_status_entry.grid(row=7, column=3)

   set_status_button = tk.Button(window, text="Set Equipment Status", command=set_status)
   set_status_button.grid(row=8, column=3)

   cur.close()
   conn.close()
   window.mainloop()

# Create an event in the admin page
def create_event():
    conn = psycopg2.connect(dbname="HFClubDB", user="postgres", password=postGresPassword)
    cur = conn.cursor()

    event_name = event_name_entry.get()
    event_date = event_date_entry.get()
    event_description = event_description_entry.get()
    event_trainer = event_trainer_entry.get()
    event_room = event_room_entry.get()

    cur.execute("INSERT INTO \"GroupEvents\" (event_name, event_date, event_description, trainer_id, room_id) VALUES (%s, %s, %s, %s, %s)",
                (event_name, event_date, event_description, event_trainer, event_room))

    conn.commit()

    # Update the status in the listbox
    cur.execute("SELECT * FROM \"GroupEvents\"")
    events = cur.fetchall()
    events_listbox.delete(0, tk.END)
    for event in events:
       # Fetch the trainer name and room name using the trainer ID and room ID
        cur.execute("SELECT username FROM \"Users\" WHERE user_id = (SELECT user_id FROM \"Trainers\" WHERE trainer_id = %s)", (event[4],))
        trainer_name = cur.fetchone()[0]
        cur.execute("SELECT name FROM \"Rooms\" WHERE room_id = %s", (event[5],))
        room_name = cur.fetchone()[0]
        
        # Count the number of members attending the event
        cur.execute("SELECT COUNT(*) FROM \"MemberGroupEvent\" WHERE event_id = %s", (event[0],))
        member_count = cur.fetchone()[0]

        events_listbox.insert(tk.END, f"{event[0]}: {event[1]}, held by {trainer_name} in room {room_name}. Date: {event[2]}. {member_count} members attending.")

    cur.close()
    conn.close()

# Delete an event in the admin page
def delete_event():
    conn = psycopg2.connect(dbname="HFClubDB", user="postgres", password=postGresPassword)
    cur = conn.cursor()

    selected_event_index = events_listbox.curselection()
    if len(selected_event_index) == 0:
        messagebox.showerror("Error", "No event selected")
        return

    # Get the selected event
    selected_event_id = events_listbox.get(selected_event_index)[0]

    # Delete the selected event from the database
    cur.execute("DELETE FROM \"GroupEvents\" WHERE event_id = %s", (selected_event_id,))

    # Commit the changes
    conn.commit()

    # Update the status in the listbox
    cur.execute("SELECT * FROM \"GroupEvents\"")
    events = cur.fetchall()
    events_listbox.delete(0, tk.END)
    for event in events:
       # Fetch the trainer name and room name using the trainer ID and room ID
        cur.execute("SELECT username FROM \"Users\" WHERE user_id = (SELECT user_id FROM \"Trainers\" WHERE trainer_id = %s)", (event[4],))
        trainer_name = cur.fetchone()[0]
        cur.execute("SELECT name FROM \"Rooms\" WHERE room_id = %s", (event[5],))
        room_name = cur.fetchone()[0]

        # Count the number of members attending the event
        cur.execute("SELECT COUNT(*) FROM \"MemberGroupEvent\" WHERE event_id = %s", (event[0],))
        member_count = cur.fetchone()[0]

        events_listbox.insert(tk.END, f"{event[0]}: {event[1]}, held by {trainer_name} in room {room_name}. Date: {event[2]}. {member_count} members attending.")

    cur.close()
    conn.close()

# Set status in the admin page
def set_status():
    # Get the selected room ID
    selected_room_index = rooms_listbox.curselection()
    if len(selected_room_index) == 0:
        messagebox.showerror("Error", "No room selected")
        return
    selected_room_id = rooms_listbox.get(selected_room_index)[0] # Extract the room ID from the string

    # Get the new status
    new_status = equipment_status_entry.get()

    # Update the status of the selected room in the database
    conn = psycopg2.connect(dbname="HFClubDB", user="postgres", password=postGresPassword)
    cur = conn.cursor()
    cur.execute("UPDATE \"Rooms\" SET equipment_status = %s WHERE room_id = %s", (new_status, selected_room_id))
    conn.commit()

    # Update the status in the listbox
    cur.execute("SELECT * FROM \"Rooms\"")
    rooms = cur.fetchall()
    rooms_listbox.delete(0, tk.END)
    for room in rooms:
        rooms_listbox.insert(tk.END, f"{room[0]}: {room[1]}, Status: {room[2]}")
    cur.close()
    conn.close()

# Member page
def create_member_page(user_id):
    global events_listbox_member
    conn = psycopg2.connect(dbname="HFClubDB", user="postgres", password=postGresPassword)
    cur = conn.cursor()
    cur.execute("SELECT member_id FROM \"Members\" WHERE user_id = %s", (user_id,))
    member_id = cur.fetchone()[0]
    cur.execute("SELECT * FROM \"MemberDetails\" WHERE member_id = %s", (member_id,))
    member_details = cur.fetchone()
    cur.execute("SELECT s.session_id, s.trainer_id, d.session_date, d.session_time, d.session_status, u.username FROM \"Session\" s JOIN \"SessionDetails\" d ON s.session_id = d.session_id JOIN \"Users\" u ON s.trainer_id = u.user_id WHERE s.member_id = %s", (member_id,))
    sessions = cur.fetchall()
    sessions_listbox_items = [f"Date: {session[2]}, Time: {session[3]}, Trainer: {session[5]}, Status: {session[4]}" for session in sessions]

    window = tk.Tk()
    window.title("Member Page")
    window.geometry("800x600")


    # Member details
    member_details_label = tk.Label(window, text="Member Dashboard")
    member_details_label.pack()

    member_details_text = tk.Text(window, height = 8)
    member_details_text.insert(tk.END, f"Member ID: {member_details[0]}\n")
    member_details_text.insert(tk.END, f"Fitness Goals: {member_details[1]}\n")
    member_details_text.insert(tk.END, f"Health Metrics: {member_details[2]}\n")
    member_details_text.insert(tk.END, f"Exercise Routine: {member_details[3]}\n")
    member_details_text.insert(tk.END, f"Fitness Achievements: {member_details[4]}\n")
    member_details_text.insert(tk.END, f"Billing Info: {member_details[5]}\n")
    member_details_text.insert(tk.END, f"Loyalty Points: {member_details[6]}\n")
    member_details_text.pack()

    # List of sessions
    sessions_label = tk.Label(window, text="Sessions")
    sessions_label.pack()

    sessions_listbox = tk.Listbox(window, width=90, height=5)
    for item in sessions_listbox_items:
        sessions_listbox.insert(tk.END, item)
    sessions_listbox.pack()

    # List of events
    events_label = tk.Label(window, text="Events")
    events_label.pack()

    events_listbox_member = tk.Listbox(window, width=90, height=5)
    cur.execute("SELECT * FROM \"GroupEvents\"")
    events = cur.fetchall()
    for event in events:
       # Fetch the trainer name and room name using the trainer ID and room ID
        cur.execute("SELECT username FROM \"Users\" WHERE user_id = (SELECT user_id FROM \"Trainers\" WHERE trainer_id = %s)", (event[4],))
        trainer_name = cur.fetchone()[0]
        cur.execute("SELECT name FROM \"Rooms\" WHERE room_id = %s", (event[5],))
        room_name = cur.fetchone()[0]

        # Count the number of members attending the event
        cur.execute("SELECT COUNT(*) FROM \"MemberGroupEvent\" WHERE event_id = %s", (event[0],))
        member_count = cur.fetchone()[0]

        events_listbox_member.insert(tk.END, f"{event[0]}: {event[1]}, held by {trainer_name} in room {room_name}. Date: {event[2]}. {member_count} members attending.")

    events_listbox_member.pack()

    # Register for event button
    register_button = tk.Button(window, text="Register for Event", command=lambda: register_for_event(member_id, events_listbox_member.get(tk.ACTIVE)[0]))
    register_button.pack()

    logout_button = tk.Button(window, text="Logout", command=lambda: (window.destroy()))
    logout_button.pack()

    cur.close()
    conn.close()
    window.mainloop()

# Register for event in member page
def register_for_event(member_id, event_id):
    conn = psycopg2.connect(dbname="HFClubDB", user="postgres", password=postGresPassword)
    cur = conn.cursor()
    cur.execute("INSERT INTO \"MemberGroupEvent\" (member_id, event_id) VALUES (%s, %s)", (member_id, event_id))
    conn.commit()

    #Update list by reloading contents
    cur.execute("SELECT * FROM \"GroupEvents\"")
    events = cur.fetchall()
    events_listbox_member.delete(0, tk.END)
    for event in events:
        # Fetch the trainer name and room name using the trainer ID and room ID
        cur.execute("SELECT username FROM \"Users\" WHERE user_id = (SELECT user_id FROM \"Trainers\" WHERE trainer_id = %s)", (event[4],))
        trainer_name = cur.fetchone()[0]
        cur.execute("SELECT name FROM \"Rooms\" WHERE room_id = %s", (event[5],))
        room_name = cur.fetchone()[0]

        # Count the number of members attending the event
        cur.execute("SELECT COUNT(*) FROM \"MemberGroupEvent\" WHERE event_id = %s", (event[0],))
        member_count = cur.fetchone()[0]

        events_listbox_member.insert(tk.END, f"{event[0]}: {event[1]}, held by {trainer_name} in room {room_name}. Date: {event[2]}. {member_count} members attending.")

    cur.close()
    conn.close()


# Setting up the database
def setupDB():
    import psycopg2

    # Connect to the default postgres database
    conn = psycopg2.connect(dbname="HFClubDB", user="postgres", password=postGresPassword)

    # Open a cursor to perform database operations
    cur = conn.cursor()

    # Open the SQL file
    with open('HFClubDB.sql', 'r') as f:
        sql_file = f.read()

    # Execute the SQL file
    cur.execute(sql_file)

    # Commit and close
    cur.close()
    conn.commit()
    conn.close()

# Populating the database
def populateDB():
    import psycopg2

    # Connect to the default postgres database
    conn = psycopg2.connect(dbname="HFClubDB", user="postgres", password=postGresPassword)

    # Open a cursor to perform database operations
    cur = conn.cursor()

    # Open the SQL file
    with open('populateDB.sql', 'r') as f:
        sql_file = f.read()

    # Execute the SQL file
    cur.execute(sql_file)

    # Close communication with the default postgres database
    cur.close()
    conn.commit()
    conn.close()


def main():
    #sets up tables by loading in .sql file
    setupDB()
    populateDB()

    while (True):
        #Login page
        create_login_page()
        user_id = login_result[0]
        user_type = login_result[4]
    
        if (user_type == "admin"):
            print("admin login")
            create_admin_page()
        elif (user_type == "member"):
            print("member login")
            create_member_page(user_id)
        elif (user_type == "trainer"):
            print("trainer login (not implemented)")




if __name__ == "__main__":
   main()
