# Store embeddings in the database

import google.generativeai as genai
import numpy as np
import pandas as pd

from db import fetch_all_embeddings

genai.configure(api_key="AIzaSyDqNSlN0jbyMB7xQlor8w_5CqxAh9xRVBA")

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


# Find the closest embeddings to the query
def find_closest_embeddings(query_embedding, top_n=5):
    results = fetch_all_embeddings()
    distances = []

    for row in results:
        email_id, email_text, stored_embedding = row
        stored_embedding = np.array(eval(stored_embedding))  # Convert JSON string back to NumPy array
        distance = calculate_distance(query_embedding, stored_embedding)
        distances.append((email_text, distance))

    # Sort by distance and get top N closest matches
    distances.sort(key=lambda x: x[1])
    return distances[:top_n]
