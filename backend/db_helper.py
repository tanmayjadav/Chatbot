import mysql.connector
global connection
connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="pandeyji_eatery"
        )

def insert_order_tracking(order_id, status):
    cursor = connection.cursor()

    # Inserting the record into the order_tracking table
    insert_query = "INSERT INTO order_tracking (order_id, status) VALUES (%s, %s)"
    cursor.execute(insert_query, (order_id, status))

    # Committing the changes
    connection.commit()

    # Closing the cursor
    cursor.close()

def insert_order_item(food_item, number, order_id):
    try:
        cursor = connection.cursor()

        # Calling the stored procedure
        cursor.callproc('insert_order_item', (food_item, number, order_id))

        # Committing the changes
        connection.commit()

        # Closing the cursor
        cursor.close()

        print("Order item inserted successfully!")

        return 1

    except mysql.connector.Error as err:
        print(f"Error inserting order item: {err}")

        # Rollback changes if necessary
        connection.rollback()

        return -1

    except Exception as e:
        print(f"An error occurred: {e}")
        # Rollback changes if necessary
        connection.rollback()

        return -1
    
def get_total_order_price(order_id):
    cursor = connection.cursor()

    # Executing the SQL query to get the total order price
    query = f"SELECT get_total_order_price({order_id})"
    cursor.execute(query)

    # Fetching the result
    result = cursor.fetchone()[0]

    # Closing the cursor
    cursor.close()

    return result

# Function to read status for a given order ID
def read_status(order_id : int):
    try:
        # Create a cursor object to interact with the database
        cursor = connection.cursor()

        # Define the query to retrieve the status for the given order ID
        query = f"SELECT status FROM order_tracking WHERE order_id = {order_id}"

        # Execute the query with the order ID as a parameter
        cursor.execute(query)

        # Fetch the status
        status = cursor.fetchone()

        if status:
            return f"Status for Order ID {order_id}: {status[0]}"
        else:
            return f"Order ID {order_id} not found in the database."

    except mysql.connector.Error as error:
        print("Error:", error)
        return f"An error occurred while fetching the status for Order ID {order_id}."

    finally:
        # Close the cursor and the database connection
        if cursor:
            cursor.close()
    
def get_next_order_id():
    cursor = connection.cursor()

    # Executing the SQL query to get the next available order_id
    query = "SELECT MAX(order_id) FROM orders"
    cursor.execute(query)

    # Fetching the result
    result = cursor.fetchone()[0]

    # Closing the cursor
    cursor.close()

    # Returning the next available order_id
    if result is None:
        return 1
    else:
        return result + 1
    
if __name__ == "__main__":
    # print(get_total_order_price(56))
    # insert_order_item('Samosa', 3, 99)
    # insert_order_item('Pav Bhaji', 1, 99)
    # insert_order_tracking(99, "in progress")
    print(get_next_order_id())