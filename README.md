# Railway Reservation System

This is a Python-based Railway Reservation System built using Streamlit and SQLite. It provides a user-friendly interface for managing train information, booking tickets, canceling tickets, and viewing seat availability.

## Features

- **Add Train:** Add new trains to the system with their details (train number, name, start/end destinations).
- **Search Train:** Search for trains by their train number.
- **Delete Train:** Remove trains from the system.
- **Book Ticket:** Book tickets for specific trains, specifying passenger details (name, age, gender) and seat type.
- **Cancel Ticket:** Cancel existing bookings by train number and seat number.
- **View Seats:** View the seat availability and booking status for a given train.
- **View Trains:** View a list of all trains in the system.
- **User-Friendly Interface:** Built with Streamlit, providing a clean and interactive web application.
- **Data Persistence:** Uses SQLite for storing train and booking data.
- **Styling:** Custom CSS styling enhances the application's appearance.

## Prerequisites

Before running the application, ensure you have the following installed:

- **Python 3.x:** (Recommended: Python 3.7 or higher)
- **Streamlit:** `pip install streamlit`
- **SQLite:** (Usually comes pre-installed with Python)
- **Pandas:** `pip install pandas`

## Installation

1.  **Clone the Repository (Optional):** If you have the code in a repository, clone it to your local machine:

    ```bash
    git clone <repository_url>
    ```

2.  **Navigate to the Directory:** Change your current directory to the project folder:

    ```bash
    cd <project_directory>
    ```

3.  **Create the Database:** The application expects a database file named `railway.db`. If it doesn't exist, the code will create it. You may need to run the application at least once so that the database and the required tables are created.

## Running the Application

1.  **Run the Streamlit app:**

    ```bash
    streamlit run railway_reservation_system.py  # Replace with your file name if different
    ```

2.  **Access the Application:** Open your web browser and navigate to the URL provided by Streamlit (usually `http://localhost:8501`).

## Database Structure (`railway.db`)

The database consists of two main tables:

- **`trains`:**

  - `train_number` (TEXT, PRIMARY KEY)
  - `train_name` (TEXT)
  - `start_destination` (TEXT)
  - `end_destination` (TEXT)

- **`seats_<train_number>`:** (One table per train)
  - `seat_number` (INTEGER, PRIMARY KEY)
  - `seat_type` (TEXT) (e.g., "Window", "Aisle", "Middle")
  - `booked` (INTEGER) (0 for available, 1 for booked)
  - `passenger_name` (TEXT)
  - `passenger_age` (INTEGER)
  - `passenger_gender` (TEXT)

The `seats_<train_number>` tables are created dynamically when a new train is added. This structure allows for managing seats specific to each train. The application initially creates 50 seats for each train.

## Usage

1.  **Navigate using the Sidebar:** Use the sidebar menu to select different functionalities (Add Train, Search Train, Book Ticket, etc.).

2.  **Follow the Prompts:** The application will guide you through each process with clear instructions and input fields.

## Example

To add a train:

1.  Select "➕ Add Train" from the sidebar.
2.  Enter the train number, name, start destination, and end destination.
3.  Click "Add Train 🚂".

## Future Improvements

- **User Authentication:** Implement user login and registration.
- **Payment Integration:** Integrate with payment gateways for online ticket purchases.
- **More Advanced Search:** Allow searching for trains by route, date, etc.
- **Seat Selection:** Allow users to choose specific seats.
- **Admin Panel:** Create a separate admin panel for managing trains and users.
- **Error Handling:** Improve error handling and input validation.

## Contributing

Contributions are welcome! Feel free to submit pull requests or open issues.
