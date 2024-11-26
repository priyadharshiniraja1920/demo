import pandas as pd
import mysql.connector
import streamlit as slt
from streamlit_option_menu import option_menu


# Path to the CSV file
#file_path = r"C:/Users/PRIYA/OneDrive/Desktop/REDBUS_PROJECT/State_Files/FinalData.csv"
df = pd.read_csv("FinalData.csv")

# Extract states from Route_Names (assuming format "StateName - RouteName")
df["State"] = df["Route_Names"].apply(lambda x: x.split(" - ")[0])
#print(df["State"])
#print("---------------")

# Group routes by state
routes = {}
for state in df["State"].unique():
    #print(state)
    routes[state] = df[df["State"] == state]["Route_Names"].tolist()
#print("**************")
#print(routes)
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="123456789",
    database="red_bus_details"
)
my_cursor = conn.cursor()
#print(my_cursor)
