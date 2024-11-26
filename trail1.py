def fetch_filtered_buses(state, route, bus_name, bus_type, start_time, total_duration, price):
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="12345689",  # Update with your MySQL password
            database="red_bus_details"
        )
        cursor = conn.cursor()

        # Construct SQL query with filters
        query = "SELECT * FROM bus_details WHERE 1=1"
        params = []

        if state:
            query += " AND Route_name LIKE %s"
            params.append(f"{state}%")  # Assuming "state" is part of "Route_name"
        if route:
            query += " AND Route_name = %s"
            params.append(route)
        if bus_name:
            query += " AND Bus_name = %s"
            params.append(bus_name)
        if bus_type:
            query += " AND Bus_Type = %s"
            params.append(bus_type)
        if start_time:
            query += " AND Start_time = %s"
            params.append(start_time)
        if total_duration:
            query += " AND Total_duration = %s"
            params.append(total_duration)
        if price:
            query += " AND Price = %s"
            params.append(price)

        query += " ORDER BY Start_time"
        cursor.execute(query, tuple(params))
        result = cursor.fetchall()

        # Define column names for the bus details table
        columns = [
            "Bus_name", "Bus_Type", "Start_time", "End_time", "Total_duration",
            "Price", "Seats_Available", "Ratings", "Route_link", "Route_name"
        ]
        df = pd.DataFrame(result, columns=columns) if result else pd.DataFrame()

        conn.close()
        return df
    except mysql.connector.Error as err:
        st.error(f"Database error: {err}")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return pd.DataFrame()