


def ConnectDB():
    try:
        # Προσοχή: Εδώ θα βάλετε τα δικά σας στοιχεία της MySQL
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="eCar_db"
        )
        cursor = conn.cursor(dictionary=True)
        return cursor
    except mysql.connector.Error as err:
        print(f"Σφάλμα σύνδεσης με τη βάση: {err}")
        return None
    


