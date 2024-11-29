# Store embeddings in the database
import json

import numpy as np
import pandas as pd

from data_upload import load_csv_data
from db import fetch_all_embeddings


# Calculate distance between two embeddings (Euclidean distance)
def calculate_distance(embedding1, embedding2):
    return np.linalg.norm(np.array(embedding1) - np.array(embedding2))


data = load_csv_data("./phishing-with-embeddings.csv")

"""
  Fetch embeddings from database csv file
   """
# def find_closest_embeddings(question_embedding, top_n=5):
#     stored_embeddings = data['embedding']
#     data['distance'] = stored_embeddings.apply(lambda x: calculate_distance(question_embedding, x))
#
#     # Filter out rows with NaN in 'Email Text'
#     filtered_data = data.dropna(subset=['Email Text'])
#
#     data_sorted = filtered_data.sort_values('distance', ascending=False)
#
#     return data_sorted.head(top_n)[['Email Text', 'distance']]


"""
  Fetch embeddings from database csv file
   """


def find_closest_embeddings_from_db(email_text_embedding, top_n=5):
    stored_data = fetch_all_embeddings()
    embedding_data = pd.DataFrame(stored_data, columns=["id", "EmailText", "EmailType", "Embedding"])

    # Get distance between the query embeddings and stored embeddings
    embedding_data['distance'] = embedding_data['Embedding'].apply(
        lambda x: calculate_distance(email_text_embedding, x))

    # Filter out rows with NaN in 'EmailText'
    filtered_data = embedding_data.dropna(subset=['EmailText'])

    # # Sort the data by distance in ascending order (closest first)
    data_sorted = filtered_data.sort_values('distance', ascending=False)

    # # Return the top_n closest embeddings, selecting only relevant columns
    return data_sorted.head(top_n)[['EmailText', 'distance']]
