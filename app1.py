import pandas as pd
import mysql.connector
import streamlit as slt
from streamlit_option_menu import option_menu

# Function to load state routes
@slt.cache_data
def load_state_routes():
    # Path to the CSV file
    file_path = r"C:/Users/PRIYA/OneDrive/Desktop/REDBUS_PROJECT/State_Files/FinalData.csv"
    df = pd.read_csv(file_path)

    # Extract states from Route_Names (assuming format "StateName - RouteName")
    df["State"] = df["Route_Names"].apply(lambda x: x.split(" - ")[0])
    
    # Group routes by state
    routes = {}
    for state in df["State"].unique():
        routes[state] = df[df["State"] == state]["Route_Names"].tolist()
    return routes

# Function to get bus details based on filters
def get_bus_details(route, seat_type, ac_type, rating_range, fare_range, start_time):
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="123456789",
        database="red_bus_details"
    )
    my_cursor = conn.cursor()

    # Seat Type Condition (e.g., Sleeper, Sitter)
    seat_condition = {
        "Sleeper": "Bus_type LIKE '%Sleeper%'",
        "Sitter": "Bus_type NOT LIKE '%Sleeper%'"
    }[seat_type]
    
    # AC Type Condition (AC or Non-AC)
    ac_condition = {
        "AC": "Bus_type LIKE '%A/c%'",
        "Non-AC": "Bus_type NOT LIKE '%A/c%'"
    }[ac_type]

    # Rating Range Condition
    min_rating, max_rating = {
        "1 to 2": (1, 2),
        "2 to 3": (2, 3),
        "3 to 4": (3, 4),
        "4 to 5": (4, 5)
    }[rating_range]
    rating_condition = f"Ratings BETWEEN {min_rating} AND {max_rating}"

    # Fare Range Condition
    fare_min, fare_max = {
        "50-1000": (50, 1000),
        "1000-2000": (1000, 2000),
        "2000 and above": (2000, 100000)
    }[fare_range]
    fare_condition = f"Price BETWEEN {fare_min} AND {fare_max}"

    # Start Time Condition
    time_condition = f"Start_time >= '{start_time}'" if start_time else "1=1"
    
    # Query with all the filters applied
    query = f'''
        SELECT * FROM bus_details 
        WHERE Route_Names = %s
        AND {seat_condition}
        AND {ac_condition}
        AND {rating_condition}
        AND {fare_condition}
        AND {time_condition}
        ORDER BY Price, Start_time
    '''
    
    my_cursor.execute(query, (route,))
    result = my_cursor.fetchall()
    conn.close()

    df = pd.DataFrame(result, columns=[
        "Bus_name", "Bus_type", "Start_time", "End_time", "Total_duration",
        "Price", "Seats_Available", "Ratings", "Route_Links", "Route_Names"
    ])
    return df

# Setting up Streamlit page
slt.set_page_config(layout="wide")

web = option_menu(menu_title="🚌 OnlineBus",
                  options=["📍States and Routes"],
                  icons=["info-circle"],
                  orientation="horizontal")

# States and Routes page
if web == "📍States and Routes":
    # Load state routes
    routes = load_state_routes()
    
    # State dropdown
    state = slt.selectbox("Select State", list(routes.keys()))

    # Route dropdown
    route = slt.selectbox("Select Route", routes[state])

    # Seat Type, AC Type dropdowns
    col1, col2, col3 = slt.columns(3)
    with col1:
        seat_type = slt.selectbox("Select Seat Type", ["Sleeper", "Sitter"])
    with col2:
        ac_type = slt.selectbox("Select AC Type", ["AC", "Non-AC"])

    # Rating dropdown, Start Time, Fare Range
    col4, col5, col6 = slt.columns(3)
    with col4:
        rating_range = slt.selectbox("Select Rating Range", ["1 to 2", "2 to 3", "3 to 4", "4 to 5"])
    with col5:
        start_time = slt.time_input("Select Starting Time", value=None)
    with col6:
        fare_range = slt.selectbox("Select Bus Fare Range", ["50-1000", "1000-2000", "2000 and above"])

    # Get bus details based on selected filters
    bus_details = get_bus_details(df['Bus_name'],df['Bus_type'],df['Start_time'],df['End_time'],df['Total_duration'],df['Price'],df['Seats_Available'],df['Ratings'],df['Route_Links'],df['Route_Names']) 

    # Display the results
    if bus_details.empty:
        slt.write("No buses found matching your criteria.")
    else:
        slt.dataframe(bus_details)
