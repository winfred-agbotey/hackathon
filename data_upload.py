# generator.py
import ast
import pickle
import numpy as np
import pandas as pd

import db  # Import the db.py module


# Function to load the pickle file
def load_csv_data(file_path):
    df = pd.read_csv(file_path)
    df['embedding'] = df['embedding'].apply(lambda x: np.array(ast.literal_eval(x)))
    return df


# Function to save embeddings from pickle file to the database
def save_embeddings_from_pickle(file_path):
    # Load data from the pickle file
    data = load_csv_data(file_path)

    # Iterate over the email texts and embeddings and save to the database
    # print(data)
    for _, row in data.iterrows():
        email_text = row['Email Text']  # Assuming 'Email Text' is the column name in the CSV
        embedding = np.array(eval(row['embedding']))  # Assuming embeddings are stored as stringified lists

        # Save each email text and its corresponding embedding to the database
        db.store_embedding(email_text, np.array(embedding))


# Example of usage: Save the embeddings from the pickle file to the database
# save_embeddings_from_pickle("./phishing-with-embeddings.pkl")

if __name__ == '__main__':
    save_embeddings_from_pickle("./phishing-with-embeddings.csv")
