from pathlib import Path
from tkinter import Tk, Canvas, Text, Entry, Button, PhotoImage, messagebox, Toplevel, ttk, simpledialog
import csv
import json
import pandas as pd # type: ignore

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\ishav\Documents\GitHub\Tkinter-Designer\build\assets\frame0")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

# Sample user data
users = {
    "admin": "admin",
    "user1": "admin"
}

def login():
    username = entry_1.get()
    password = entry_2.get()
    
    if username in users and users[username] == password:
        messagebox.showinfo("Login", "Login successful!")
        open_admin_home_page()
    else:
        messagebox.showerror("Login Failed", "Invalid username or password.")

def open_admin_home_page():
    def open_csv_window():
        # Create a new Toplevel window for displaying the CSV file
        csv_window = Toplevel()
        csv_window.title("Flight Details")
        csv_window.geometry("800x400")

        # Read the CSV file
        file_path = "flight_bookings_2024.csv"  # Replace with the path to your CSV file
        try:
            data = pd.read_csv(file_path)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to read CSV file: {e}")
            return

        # Create a Treeview widget
        tree = ttk.Treeview(csv_window, columns=list(data.columns), show="headings")
        for col in data.columns:
            tree.heading(col, text=col)
            tree.column(col, width=150, anchor='center')

        # Populate the Treeview with data
        for _, row in data.iterrows():
            tree.insert("", "end", values=list(row))

        tree.pack(fill="both", expand=True)

    window.destroy()  # Close the login window
    admin_home_window = Tk()
    admin_home_window.geometry("600x400")
    admin_home_window.configure(bg="#161632")
    
    canvas = Canvas(
        admin_home_window,
        bg="#161632",
        height=400,
        width=600,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )

    canvas.place(x=0, y=0)
    image_image_1 = PhotoImage(
        file=relative_to_assets("image_1.png"))
    image_1 = canvas.create_image(
        441.0,
        213.0,
        image=image_image_1
    )

    canvas.create_text(
        41.0,
        57.0,
        anchor="nw",
        text="ADMIN HOME",
        fill="#FFFFFF",
        font=("Roboto Bold", 32 * -1)
    )

    # Example buttons for the admin page

    book_flight_button_image = PhotoImage(
        file=relative_to_assets("book_flight_button.png"))  # This can be the "Add Flight Details" button image
    book_flight_button = Button(
        image=book_flight_button_image,
        borderwidth=0,
        highlightthickness=0,
        command=open_book_flight_window,
        relief="flat"
    )
    book_flight_button.place(
        x=49.0,
        y=185.0,
        width=197.0,
        height=29.0
    )

    cancel_flight_button_image = PhotoImage(
        file=relative_to_assets("cancel_flight_button.png"))  # Example for a third button
    cancel_flight_button = Button(
        image=cancel_flight_button_image,
        borderwidth=0,
        highlightthickness=0,
        command=cancel_flight,
        relief="flat"
    )
    cancel_flight_button.place(
        x=49.0,
        y=240.0,
        width=197.0,
        height=29.0
    )

    check_flight_button_image = PhotoImage(
        file=relative_to_assets("check_flight_button.png"))  # Example for a fourth button
    check_flight_button = Button(
        image=check_flight_button_image,
        borderwidth=0,
        highlightthickness=0,
        command=open_csv_window,  # Opens the new CSV window
        relief="flat"
    )
    check_flight_button.place(
        x=49.0,
        y=130.0,
        width=197.0,
        height=29.0
    )

    admin_home_window.resizable(False, False)
    admin_home_window.mainloop()

def read_csv(file_path):
    data = {}
    with open(file_path, mode='r', newline='', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            if 'Flight Number' in row:
                data[row['Flight Number']] = row
    return data

# Load CSV data
csv_file_path = Path('flight_bookings_2024.csv')
csv_data = read_csv(csv_file_path)

def update_fields(event=None):
    flight_number = flight_number_entry.get("1.0", "end-1c").strip()
    if flight_number in csv_data:
        record = csv_data[flight_number]
        # Debugging output
        print(f"Record found: {record}")
        
        try:
            departure_date_entry.delete("1.0", "end")
            departure_date_entry.insert("1.0", record.get('Departure Date', ''))
            departure_time_entry.delete("1.0", "end")
            departure_time_entry.insert("1.0", record.get('Departure Time', ''))
            departure_city_entry.delete("1.0", "end")
            departure_city_entry.insert("1.0", record.get('Departure City', ''))
            arrival_date_entry.delete("1.0", "end")
            arrival_date_entry.insert("1.0", record.get('Arrival Date', ''))
            arrival_time_entry.delete("1.0", "end")
            arrival_time_entry.insert("1.0", record.get('Arrival Time', ''))
            arrival_city_entry.delete("1.0", "end")
            arrival_city_entry.insert("1.0", record.get('Arrival City', ''))
        except KeyError as e:
            print(f"Key error: {e}")
    else:
        print(f"Flight number {flight_number} not found in the CSV data")

def book_flight():
    flight_number = flight_number_entry.get("1.0", "end-1c").strip()
    departure_date = departure_date_entry.get("1.0", "end-1c").strip()
    departure_time = departure_time_entry.get("1.0", "end-1c").strip()
    departure_city = departure_city_entry.get("1.0", "end-1c").strip()
    arrival_date = arrival_date_entry.get("1.0", "end-1c").strip()
    arrival_time = arrival_time_entry.get("1.0", "end-1c").strip()
    arrival_city = arrival_city_entry.get("1.0", "end-1c").strip()
    flight_class = flight_class_combobox.get()
    flier_status = flier_status_combobox.get()
    meal_type = meal_type_combobox.get()
    flight_type = flight_type_combobox.get()

    if flight_number in csv_data:
        record = csv_data[flight_number]
        ticket_price = record.get("Ticket Price", "N/A")
        passenger_name = record.get("Passenger Name", "N/A")
        email = record.get("Email", "N/A")
        phone_number = record.get("Phone Number", "N/A")
        seat_number = record.get("Seat Number", "N/A")
        baggage_allowance = record.get("Baggage Allowance", "N/A")
        flight_duration = record.get("Flight Duration", "N/A")
        airline = record.get("Airline", "N/A")
    else:
        ticket_price = "N/A"
        passenger_name = "N/A"
        email = "N/A"
        phone_number = "N/A"
        seat_number = "N/A"
        baggage_allowance = "N/A"
        flight_duration = "N/A"
        airline = "N/A"

    ticket_info = {
        "Flight Number": flight_number,
        "Departure Date": departure_date,
        "Departure Time": departure_time,
        "Departure City": departure_city,
        "Arrival Date": arrival_date,
        "Arrival Time": arrival_time,
        "Arrival City": arrival_city,
        "Flight Class": flight_class,
        "Flier Status": flier_status,
        "Meal Type": meal_type,
        "Flight Type": flight_type,
        "Ticket Price": ticket_price,
        "Passenger Name": passenger_name,
        "Email": email,
        "Phone Number": phone_number,
        "Seat Number": seat_number,
        "Baggage Allowance": baggage_allowance,
        "Flight Duration": flight_duration,
        "Airline": airline
    }

    ticket_info_str = json.dumps(ticket_info, indent=4)
    messagebox.showinfo("Flight Ticket Information", ticket_info_str)

    output_format = simpledialog.askstring("Output Format", "Enter the desired output format (csv, json, txt):")

    if output_format == "csv":
        with open(f"{flight_number}_ticket.csv", mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=ticket_info.keys())
            writer.writeheader()
            writer.writerow(ticket_info)
    elif output_format == "json":
        with open(f"{flight_number}_ticket.json", mode='w') as file:
            json.dump(ticket_info, file, indent=4)
    elif output_format == "txt":
        with open(f"{flight_number}_ticket.txt", mode='w') as file:
            file.write(ticket_info_str)

    messagebox.showinfo("Success", f"Ticket saved as {flight_number}_ticket.{output_format}")

def cancel_flight():
    flight_number = simpledialog.askstring("Cancel Flight", "Enter Flight Number:")

    if flight_number in csv_data:
        record = csv_data[flight_number]
        flight_details = f"""
        Flight Number: {flight_number}
        Departure Date: {record.get('Departure Date', 'N/A')}
        Departure Time: {record.get('Departure Time', 'N/A')}
        Departure City: {record.get('Departure City', 'N/A')}
        Arrival Date: {record.get('Arrival Date', 'N/A')}
        Arrival Time: {record.get('Arrival Time', 'N/A')}
        Arrival City: {record.get('Arrival City', 'N/A')}
        Flight Class: {record.get('Flight Class', 'N/A')}
        Flier Status: {record.get('Flier Status', 'N/A')}
        Meal Type: {record.get('Meal Type', 'N/A')}
        Flight Type: {record.get('Flight Type', 'N/A')}
        Ticket Price: {record.get('Ticket Price', 'N/A')}
        Passenger Name: {record.get('Passenger Name', 'N/A')}
        Email: {record.get('Email', 'N/A')}
        Phone Number: {record.get('Phone Number', 'N/A')}
        Seat Number: {record.get('Seat Number', 'N/A')}
        Baggage Allowance: {record.get('Baggage Allowance', 'N/A')}
        Flight Duration: {record.get('Flight Duration', 'N/A')}
        Airline: {record.get('Airline', 'N/A')}
        """

        confirm_cancel = messagebox.askyesno("Confirm Cancellation", f"Flight details:\n{flight_details}\n\nAre you sure you want to cancel this flight?")

        if confirm_cancel:
            cancellation_ticket = {
                "Flight Number": flight_number,
                "Departure Date": record.get('Departure Date', 'N/A'),
                "Departure Time": record.get('Departure Time', 'N/A'),
                "Departure City": record.get('Departure City', 'N/A'),
                "Arrival Date": record.get('Arrival Date', 'N/A'),
                "Arrival Time": record.get('Arrival Time', 'N/A'),
                "Arrival City": record.get('Arrival City', 'N/A'),
                "Flight Class": record.get('Flight Class', 'N/A'),
                "Flier Status": record.get('Flier Status', 'N/A'),
                "Meal Type": record.get('Meal Type', 'N/A'),
                "Flight Type": record.get('Flight Type', 'N/A'),
                "Ticket Price": record.get('Ticket Price', 'N/A'),
                "Passenger Name": record.get('Passenger Name', 'N/A'),
                "Email": record.get('Email', 'N/A'),
                "Phone Number": record.get('Phone Number', 'N/A'),
                "Seat Number": record.get('Seat Number', 'N/A'),
                "Baggage Allowance": record.get('Baggage Allowance', 'N/A'),
                "Flight Duration": record.get('Flight Duration', 'N/A'),
                "Airline": record.get('Airline', 'N/A'),
                "Cancellation Status": "Confirmed"
            }

            output_format = simpledialog.askstring("Output Format", "Enter the desired output format (csv, json, txt):")

            if output_format == "csv":
                with open(f"{flight_number}_cancellation.csv", mode='w', newline='') as file:
                    writer = csv.DictWriter(file, fieldnames=cancellation_ticket.keys())
                    writer.writeheader()
                    writer.writerow(cancellation_ticket)
            elif output_format == "json":
                with open(f"{flight_number}_cancellation.json", mode='w') as file:
                    json.dump(cancellation_ticket, file, indent=4)
            elif output_format == "txt":
                with open(f"{flight_number}_cancellation.txt", mode='w') as file:
                    file.write(json.dumps(cancellation_ticket, indent=4))

            messagebox.showinfo("Success", f"Cancellation confirmed and saved as {flight_number}_cancellation.{output_format}")
    else:
        messagebox.showerror("Error", f"Flight number {flight_number} not found.")


def open_book_flight_window():
    book_flight_window = Toplevel()
    book_flight_window.geometry("600x400")
    book_flight_window.configure(bg="#161632")

    canvas = Canvas(
        book_flight_window,
        bg="#161632",
        height=400,
        width=600,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )
    canvas.place(x=0, y=0)
    canvas.create_text(
        191.0,
        33.0,
        anchor="nw",
        text="BOOK FLIGHT",
        fill="#FFFFFF",
        font=("Roboto Bold", 32 * -1)
    )

    canvas.create_text(
        14.0,
        168.0,
        anchor="nw",
        text="DEPARTURE TIME",
        fill="#FFFFFF",
        font=("Roboto Bold", 16 * -1)
    )

    canvas.create_text(
        13.0,
        123.0,
        anchor="nw",
        text="DEPARTURE DATE",
        fill="#FFFFFF",
        font=("Roboto Bold", 16 * -1)
    )

    canvas.create_text(
        221.0,
        82.0,
        anchor="nw",
        text="FLIGHT #",
        fill="#FFFFFF",
        font=("Roboto Bold", 16 * -1)
    )

    canvas.create_text(
        17.0,
        211.0,
        anchor="nw",
        text="DEPARTURE CITY",
        fill="#FFFFFF",
        font=("Roboto Bold", 16 * -1)
    )

    canvas.create_text(
        26.0,
        255.0,
        anchor="nw",
        text="FLIGHT CLASS",
        fill="#FFFFFF",
        font=("Roboto Bold", 16 * -1)
    )

    canvas.create_text(
        28.0,
        298.0,
        anchor="nw",
        text="FLIER STATUS",
        fill="#FFFFFF",
        font=("Roboto Bold", 16 * -1)
    )

    global departure_date_entry, flight_number_entry, departure_time_entry, departure_city_entry
    global flight_class_combobox, flier_status_combobox, meal_type_combobox, flight_type_combobox
    global arrival_date_entry, arrival_time_entry, arrival_city_entry

    departure_date_entry = Text(
        book_flight_window,
        bd=0,
        bg="#D9D9D9",
        fg="#000716",
        highlightthickness=0
    )
    departure_date_entry.place(
        x=164.0,
        y=123.0,
        width=134.0,
        height=18.0
    )

    flight_number_entry = Text(
        book_flight_window,
        bd=0,
        bg="#D9D9D9",
        fg="#000716",
        highlightthickness=0
    )
    flight_number_entry.place(
        x=300.0,
        y=81.0,
        width=74.0,
        height=18.0
    )
    flight_number_entry.bind("<KeyRelease>", update_fields)

    flight_class_combobox = ttk.Combobox(
        book_flight_window,
        values=["Economy", "Business", "First Class"]
    )
    flight_class_combobox.place(
        x=164.0,
        y=255.0,
        width=134.0,
        height=20.0
    )

    flier_status_combobox = ttk.Combobox(
        book_flight_window,
        values=["Bronze", "Silver", "Gold", "Platinum"]
    )
    flier_status_combobox.place(
        x=164.0,
        y=298.0,
        width=134.0,
        height=20.0
    )

    book_button_image = PhotoImage(
        file=relative_to_assets("book_button.png"))
    book_button = Button(
        book_flight_window,
        image=book_button_image,
        borderwidth=0,
        highlightthickness=0,
        command=book_flight,
        relief="flat"
    )
    book_button.place(
        x=233.0,
        y=357.0,
        width=133.0,
        height=29.0
    )

    departure_time_entry = Text(
        book_flight_window,
        bd=0,
        bg="#D9D9D9",
        fg="#000716",
        highlightthickness=0
    )
    departure_time_entry.place(
        x=164.0,
        y=167.0,
        width=134.0,
        height=18.0
    )

    departure_city_entry = Text(
        book_flight_window,
        bd=0,
        bg="#D9D9D9",
        fg="#000716",
        highlightthickness=0
    )
    departure_city_entry.place(
        x=164.0,
        y=211.0,
        width=134.0,
        height=18.0
    )

    canvas.create_text(
        325.0,
        167.0,
        anchor="nw",
        text="ARRIVAL TIME",
        fill="#FFFFFF",
        font=("Roboto Bold", 16 * -1)
    )

    canvas.create_text(
        324.0,
        124.0,
        anchor="nw",
        text="ARRIVAL DATE",
        fill="#FFFFFF",
        font=("Roboto Bold", 16 * -1)
    )

    canvas.create_text(
        327.0,
        210.0,
        anchor="nw",
        text="ARRIVAL CITY",
        fill="#FFFFFF",
        font=("Roboto Bold", 16 * -1)
    )

    canvas.create_text(
        335.0,
        256.0,
        anchor="nw",
        text="MEAL TYPE",
        fill="#FFFFFF",
        font=("Roboto Bold", 16 * -1)
    )

    canvas.create_text(
        329.0,
        302.0,
        anchor="nw",
        text="FLIGHT TYPE",
        fill="#FFFFFF",
        font=("Roboto Bold", 16 * -1)
    )

    arrival_date_entry = Text(
        book_flight_window,
        bd=0,
        bg="#D9D9D9",
        fg="#000716",
        highlightthickness=0
    )
    arrival_date_entry.place(
        x=454.0,
        y=123.0,
        width=134.0,
        height=18.0
    )

    meal_type_combobox = ttk.Combobox(
        book_flight_window,
        values=["Vegetarian", "Non-Vegetarian", "Vegan", "Gluten-Free"]
    )
    meal_type_combobox.place(
        x=454.0,
        y=255.0,
        width=134.0,
        height=20.0
    )

    flight_type_combobox = ttk.Combobox(
        book_flight_window,
        values=["One-Way", "Round-Trip"]
    )
    flight_type_combobox.place(
        x=454.0,
        y=298.0,
        width=134.0,
        height=20.0
    )

    arrival_time_entry = Text(
        book_flight_window,
        bd=0,
        bg="#D9D9D9",
        fg="#000716",
        highlightthickness=0
    )
    arrival_time_entry.place(
        x=454.0,
        y=167.0,
        width=134.0,
        height=18.0
    )

    arrival_city_entry = Text(
        book_flight_window,
        bd=0,
        bg="#D9D9D9",
        fg="#000716",
        highlightthickness=0
    )
    arrival_city_entry.place(
        x=454.0,
        y=211.0,
        width=134.0,
        height=18.0
    )

    book_flight_window.resizable(False, False)
    book_flight_window.mainloop()

# Main window (Login Page)
window = Tk()
window.geometry("600x400")
window.configure(bg="#161632")

canvas = Canvas(
    window,
    bg="#161632",
    height=400,
    width=600,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)

canvas.place(x=0, y=0)
image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    441.0,
    213.0,
    image=image_image_1
)

entry_image_1 = PhotoImage(
    file=relative_to_assets("entry_1.png"))
entry_bg_1 = canvas.create_image(
    134.5,
    179.5,
    image=entry_image_1
)
entry_1 = Entry(
    bd=0,
    bg="#D9D9D9",
    fg="#000716",
    highlightthickness=0
)
entry_1.place(
    x=36.0,
    y=165.0,
    width=197.0,
    height=27.0
)

# Login Button (only one button should be here)
login_button_image = PhotoImage(
    file=relative_to_assets("login_button.png"))  # Using the same button image for the login button
login_button = Button(
    image=login_button_image,  # Only the login button here
    borderwidth=0,
    highlightthickness=0,
    command=login,  # Ensure the login function is called when the button is pressed
    relief="flat"
)
login_button.place(
    x=68.0,
    y=309.0,
    width=133.0,
    height=29.0
)

entry_image_2 = PhotoImage(
    file=relative_to_assets("entry_2.png"))
entry_bg_2 = canvas.create_image(
    134.5,
    251.5,
    image=entry_image_2
)
entry_2 = Entry(
    bd=0,
    bg="#D9D9D9",
    fg="#000716",
    highlightthickness=0,
    show="*"
)
entry_2.place(
    x=36.0,
    y=237.0,
    width=197.0,
    height=27.0
)

canvas.create_text(
    36.0,
    142.0,
    anchor="nw",
    text="Username ",
    fill="#FFFFFF",
    font=("Roboto Bold", 20 * -1)
)

canvas.create_text(
    36.0,
    214.0,
    anchor="nw",
    text="Password",
    fill="#FFFFFF",
    font=("Roboto SemiBold", 20 * -1)
)

canvas.create_text(
    28.0,
    57.0,
    anchor="nw",
    text="ADMIN LOGIN ",
    fill="#FFFFFF",
    font=("Roboto Bold", 32 * -1)
)

window.resizable(False, False)
window.mainloop()