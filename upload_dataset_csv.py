# import json
#
# import numpy as np
#
# from data_upload import load_csv_data
# from db import conn
# import singlestoredb as s2
#
# conn = s2.connect(
#     'DATABASE_URL'
# )
#
#
# # Check if the connection is open
# def check_connection():
#     with conn:
#         with conn.cursor() as cur:
#             flag = cur.is_connected()
#             print("Database Connected:", flag)
#
#
# cursor = conn.cursor()
#
# # Create table if it does not exist
# create_table_query = """
# CREATE TABLE IF NOT EXISTS appds_embeddings (
#     id INT AUTO_INCREMENT PRIMARY KEY,
#     EmailText TEXT,
#     EmailType VARCHAR(50),
#     Embedding JSON
# );
# """
#
# cursor.execute(create_table_query)  # Use cursor to execute SQL
#
# # Step 4: Insert data into the table
# insert_query = """
# INSERT INTO appds_embeddings (EmailText, EmailType, Embedding)
# VALUES (%s, %s, %s)
# """
#
# df = load_csv_data("./phishing-with-embeddings.csv")
#
# # Iterate over the DataFrame and insert each row into the table
# for _, row in df.iterrows():
#     embedding_array = row['embedding']
#
#     # Skip rows with NaN in the embedding array
#     if np.isnan(embedding_array).any():
#         print(f"Skipping row with NaN in Embedding: {row['Email Text'][:30]}...")  # Optional: log skipped rows
#         continue
#     # Convert embedding into a valid JSON array
#     # Ensure all values are valid by converting any remaining issues
#     embedding_array_clean = np.nan_to_num(embedding_array, nan=0.0)
#
#     # Convert to JSON
#     embedding_json = json.dumps(embedding_array_clean.tolist())
#
#     try:
#         # Execute insert query
#         cursor.execute(insert_query, (row['Email Text'], row['Email Type'], embedding_json))
#     except Exception as e:
#         print(f"Error inserting row: {e}")
#         continue
#
# # Commit the transaction and close the connection
# conn.commit()
# conn.close()
# conn.close()
#
# print("Data inserted successfully!")
