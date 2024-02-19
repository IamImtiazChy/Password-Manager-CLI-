import mysql.connector


def dbconfig():
    try:
        db = mysql.connector.connect(
            host="localhost", port="3306", user="root", password=""
        )
        # print("Connected to the database successfully.")
        return db
    except mysql.connector.Error as e:
        print("Unable to connect to the database.")
        print(f"Error details: {e}")
        return None


# dbconfig()
