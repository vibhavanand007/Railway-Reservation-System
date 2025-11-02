import streamlit as st
import sqlite3
import pandas as pd

# -----------------------------
# Database Setup
# -----------------------------
conn = sqlite3.connect("railway.db", check_same_thread=False)
c = conn.cursor()

# Create trains table if not exists
c.execute("""
CREATE TABLE IF NOT EXISTS trains (
    train_number TEXT PRIMARY KEY,
    train_name TEXT NOT NULL,
    start_destination TEXT NOT NULL,
    end_destination TEXT NOT NULL
)
""")
conn.commit()

# -----------------------------
# Streamlit Page Config
# -----------------------------
st.set_page_config(
    page_title="Railway Reservation System",
    page_icon="🚆",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -----------------------------
# Custom Styling
# -----------------------------
st.markdown(
    """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap');
        * { font-family: 'Poppins', sans-serif; }
        [data-testid="stSidebar"] { background-color: #2B2B52; color: white; }
        h1, h2, h3, h4 { color: #2E86C1; }
        .stButton>button {
            background-color: #2E86C1; color: white;
            border-radius: 10px; border: none; padding: 10px;
        }
        .stDataFrame { border-radius: 10px; overflow: hidden; }
    </style>
    """,
    unsafe_allow_html=True,
)

# -----------------------------
# Sidebar Navigation
# -----------------------------
st.sidebar.markdown(
    """
    <div style="display: flex; align-items: center;">
        <img src="https://wallpapers.com/images/featured-full/indian-railway-pictures-24ambowp0ldn517f.jpg" 
             width="50" style="margin-right: 10px;">
        <h2 style="color: white;">Railway System</h2>
    </div>
    """,
    unsafe_allow_html=True
)
st.sidebar.markdown("---")

option = st.sidebar.radio(
    "Select an Option",
    [
        "🏠 Home",
        "➕ Add Train",
        "🔍 Search Train",
        "🗑 Delete Train",
        "🎟 Book Ticket",
        "❌ Cancel Ticket",
        "📊 View Seats",
        "🚂 View Trains",
    ]
)
st.sidebar.markdown("---")
st.sidebar.info("📌 A modern railway reservation system built with Streamlit.")

# -----------------------------
# Utility Function
# -----------------------------
def create_seats_table(train_number):
    """Create a seat table for a given train if not exists."""
    table_name = f"seats_{train_number}"
    c.execute(f"""
    CREATE TABLE IF NOT EXISTS {table_name} (
        seat_number INTEGER PRIMARY KEY AUTOINCREMENT,
        seat_type TEXT,
        booked INTEGER DEFAULT 0,
        passenger_name TEXT,
        passenger_age INTEGER,
        passenger_gender TEXT
    )
    """)
    conn.commit()

    # Initialize 10 seats if empty
    c.execute(f"SELECT COUNT(*) FROM {table_name}")
    if c.fetchone()[0] == 0:
        seat_types = ["Window", "Aisle", "Middle"]
        for i in range(10):
            c.execute(f"INSERT INTO {table_name} (seat_type) VALUES (?)", (seat_types[i % 3],))
        conn.commit()

# -----------------------------
# Add Train
# -----------------------------
def add_train():
    st.subheader("➕ Add a New Train")
    with st.form("train_form"):
        train_number = st.text_input("Train Number", help="Enter the unique train number")
        train_name = st.text_input("Train Name", help="Enter the train name")
        start_dest = st.text_input("Start Destination")
        end_dest = st.text_input("End Destination")
        submit = st.form_submit_button("Add Train 🚂")
    
    if submit:
        if not (train_number and train_name and start_dest and end_dest):
            st.error("❌ Please fill in all fields!")
            return

        try:
            c.execute(
                "INSERT INTO trains (train_number, train_name, start_destination, end_destination) VALUES (?, ?, ?, ?)",
                (train_number, train_name, start_dest, end_dest),
            )
            conn.commit()

            # Create seat table for this train
            create_seats_table(train_number)
            st.success(f"✅ Train '{train_name}' added successfully with seats initialized!")

        except sqlite3.IntegrityError:
            st.error(f"⚠ Train Number '{train_number}' already exists! Please use a unique one.")
        except sqlite3.Error as e:
            st.error(f"❌ Database error: {e}")

# -----------------------------
# View Trains
# -----------------------------
def view_trains():
    st.subheader("🚂 View All Trains")
    c.execute("SELECT * FROM trains")
    trains = c.fetchall()
    
    if trains:
        df = pd.DataFrame(trains, columns=["Train Number", "Train Name", "Start Destination", "End Destination"])
        st.dataframe(df.style.set_properties(**{"background-color": "#f4f4f4", "color": "#000"}))
    else:
        st.warning("⚠ No trains found!")

# -----------------------------
# Book Ticket
# -----------------------------
def book_ticket():
    st.subheader("🎟 Book a Ticket")
    train_number = st.text_input("Enter Train Number")
    passenger_name = st.text_input("Passenger Name")
    passenger_age = st.number_input("Passenger Age", min_value=1)
    passenger_gender = st.radio("Select Gender", ["Male", "Female"])
    seat_type = st.radio("Seat Type", ["Window", "Aisle", "Middle"])
    
    if st.button("Book Ticket 🎫"):
        if not train_number:
            st.error("❌ Please enter a valid train number.")
            return
        try:
            table_name = f"seats_{train_number}"
            c.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'")
            if not c.fetchone():
                st.error(f"❌ Train '{train_number}' does not exist or has no seats table.")
                return

            # Find available seat
            c.execute(
                f"SELECT seat_number FROM {table_name} WHERE booked=0 AND seat_type=? LIMIT 1",
                (seat_type,)
            )
            seat = c.fetchone()

            if seat:
                seat_number = seat[0]
                c.execute(
                    f"UPDATE {table_name} SET booked=1, passenger_name=?, passenger_age=?, passenger_gender=? WHERE seat_number=?",
                    (passenger_name, passenger_age, passenger_gender, seat_number),
                )
                conn.commit()
                st.success(f"✅ Ticket booked successfully! Seat Number: {seat_number}")
            else:
                st.error(f"❌ No available {seat_type} seats!")
        except sqlite3.Error as e:
            st.error(f"❌ Database error: {e}")

# -----------------------------
# Cancel Ticket
# -----------------------------
def cancel_ticket():
    st.subheader("❌ Cancel a Ticket")
    train_number = st.text_input("Enter Train Number")
    seat_number = st.number_input("Enter Seat Number", min_value=1)
    if st.button("Cancel Ticket ⛔"):
        try:
            table_name = f"seats_{train_number}"
            c.execute(f"UPDATE {table_name} SET booked=0, passenger_name='', passenger_age='', passenger_gender='' WHERE seat_number=?", (seat_number,))
            conn.commit()
            st.success("✅ Ticket canceled successfully!")
        except sqlite3.Error as e:
            st.error(f"❌ Database error: {e}")

# -----------------------------
# View Seats
# -----------------------------
def view_seats():
    st.subheader("📊 View Seats in a Train")
    train_number = st.text_input("Enter Train Number")

    if st.button("View Seats"):
        if not train_number:
            st.error("❌ Please enter a train number.")
            return

        table_name = f"seats_{train_number}"
        try:
            # Check and create if not exists
            c.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'")
            if not c.fetchone():
                st.warning(f"⚠ Seat data not found for Train {train_number}. Creating default seats...")
                create_seats_table(train_number)

            c.execute(f"SELECT * FROM {table_name}")
            seats = c.fetchall()

            if seats:
                df = pd.DataFrame(
                    seats,
                    columns=["Seat Number", "Seat Type", "Booked", "Passenger Name", "Passenger Age", "Passenger Gender"]
                )
                st.dataframe(df)
            else:
                st.error("⚠ No seat data found!")

        except sqlite3.Error as e:
            st.error(f"❌ Database error: {e}")

# -----------------------------
# Page Routing
# -----------------------------
if option == "🏠 Home":
    st.markdown(
        """
        <div style="display: flex; align-items: center;">
            <img src="https://wallpapers.com/images/featured-full/indian-railway-pictures-24ambowp0ldn517f.jpg" 
                 width="50" style="margin-right: 10px; border-radius: 5px;">
            <h1>Railway Reservation System</h1>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.markdown("### Welcome to the Railway Reservation System.")
    st.info("📌 Use the sidebar to navigate and manage train reservations.")
elif option == "➕ Add Train":
    add_train()
elif option == "🔍 Search Train":
    st.subheader("🔍 Search for a Train")
    train_number = st.text_input("Enter Train Number")
    if st.button("Search"):
        c.execute("SELECT * FROM trains WHERE train_number=?", (train_number,))
        train = c.fetchone()
        if train:
            st.success(f"🚆 Train Found: {train[1]} | Route: {train[2]} → {train[3]}")
        else:
            st.error("❌ Train not found!")
elif option == "🗑 Delete Train":
    st.subheader("🗑 Delete a Train")
    train_number = st.text_input("Enter Train Number")
    if st.button("Delete Train"):
        try:
            c.execute("DELETE FROM trains WHERE train_number=?", (train_number,))
            conn.commit()
            # Also drop corresponding seat table
            c.execute(f"DROP TABLE IF EXISTS seats_{train_number}")
            conn.commit()
            st.success(f"🗑 Train {train_number} deleted successfully!")
        except sqlite3.Error as e:
            st.error(f"❌ Database error: {e}")
elif option == "🎟 Book Ticket":
    book_ticket()
elif option == "❌ Cancel Ticket":
    cancel_ticket()
elif option == "📊 View Seats":
    view_seats()
elif option == "🚂 View Trains":
    view_trains()
