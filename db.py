import singlestoredb as s2
import numpy as np

# Create a connection to the database
conn = s2.connect(
    'DATABASE_URL'
)


# Check if the connection is open
def check_connection():
    """Check and print whether the database connection is active."""
    try:
        if conn.is_connected():
            print("Database Connected: True")
        else:
            print("Database Connected: False. Attempting to reconnect...")
            conn.ping(reconnect=True)
            print("Reconnected Successfully!")
    except Exception as e:
        print(f"Error checking connection: {e}")


# Fetch all embeddings from the database
def fetch_all_embeddings():
    """
    Fetch all embeddings from the appds_embeddings table.
    Reconnects if the connection is lost and handles potential exceptions.
    """
    try:
        # Ensure the connection is alive
        conn.ping(reconnect=True)

        with conn.cursor() as cursor:
            cursor.execute("SELECT id, EmailText, EmailType, Embedding FROM appds_embeddings")
            results = cursor.fetchmany(size=50)
        return results
    except Exception as e:
        print(f"Error fetching data: {e}")
        return []
