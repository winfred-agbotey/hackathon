# db.py
import singlestoredb as s2
import numpy as np

# Create a connection to the database
conn = s2.connect(
    'DATABASE_URL'
)


# Check if the connection is open
def check_connection():
    with conn:
        with conn.cursor() as cur:
            flag = cur.is_connected()
            print("Database Connected:", flag)


# Function to retrieve embeddings from the database
def get_embeddings_from_db():
    query = "SELECT email_text, embedding FROM email_embeddings"
    with conn.cursor() as cur:
        cur.execute(query)
        result = cur.fetchall()
        # Convert embedding from bytes to numpy array
        data = [(email_text, np.frombuffer(embedding, dtype=np.float32)) for email_text, embedding in result]

        print("data from db: ", data)
    return data


# # Function to save the embeddings into the database
# def save_embedding_to_db(email_text, embedding):
#     query = "INSERT INTO phishing_emails (email_text, embedding) VALUES (%s, %s)"
#     with conn.cursor() as cur:
#         cur.execute(query, (email_text, embedding.tobytes()))
#         conn.commit()


def store_embedding(email_text, embedding):
    with conn.cursor() as cur:
        sql = """
        INSERT INTO email_embeddings (email_text, embedding)
        VALUES (%s, %s)
        """
        cur.execute(sql, (email_text, embedding.tolist()))  # Convert embedding to list for storage
    conn.commit()
    print("Embedding stored successfully.")


# Fetch all embeddings from the database
def fetch_all_embeddings():
    with conn.cursor() as cur:
        cur.execute("SELECT id, email_text, embedding FROM email_embeddings")
        results = cur.fetchall()
        return results
