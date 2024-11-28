# Store embeddings in the database

import numpy as np

from data_upload import load_csv_data

# def store_embedding(email_text, embedding):
#     with conn.cursor() as cur:
#         sql = """
#         INSERT INTO email_embeddings (email_text, embedding)
#         VALUES (%s, %s)
#         """
#         cur.execute(sql, (email_text, embedding.tolist()))  # Convert embedding to list for storage
#     conn.commit()
#     print("Embedding stored successfully.")
#
#
# # Fetch all embeddings from the database
# def fetch_all_embeddings():
#     with conn.cursor() as cur:
#         cur.execute("SELECT id, email_text, embedding FROM email_embeddings")
#         results = cur.fetchall()
#         return results


# Calculate distance between two embeddings (Euclidean distance)
def calculate_distance(embedding1, embedding2):
    return np.linalg.norm(np.array(embedding1) - np.array(embedding2))


data = load_csv_data("./phishing-with-embeddings.csv")


def find_closest_embeddings(question_embedding, top_n=5):
    stored_embeddings = data['embedding']
    data['distance'] = stored_embeddings.apply(lambda x: calculate_distance(question_embedding, x))

    # Filter out rows with NaN in 'Email Text'
    filtered_data = data.dropna(subset=['Email Text'])

    data_sorted = filtered_data.sort_values('distance', ascending=False)

    return data_sorted.head(top_n)[['Email Text', 'distance']]
