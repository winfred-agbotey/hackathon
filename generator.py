# Function to generate a response using Google GenAI
import numpy as np
from flask import jsonify
import requests
import pandas as pd

from data_upload import load_csv_data
from db import get_embeddings_from_db
from get_embedding import get_embedding
from helper import find_closest_embeddings
import google.generativeai as genai

genai.configure(api_key="gemini")


# Function to calculate distance between two embeddings
def calculate_distance(embedding1, embedding2):
    return np.linalg.norm(np.array(embedding1) - np.array(embedding2))


# Get embeddings from the database
# emails_with_embeddings = get_embeddings_from_db()


# Calculate the distance between the question and each email embedding
data = load_csv_data("./phishing-with-embeddings.csv")
# print(data)


# Retrieve the question embedding
question = """"""
question_embedding = get_embedding(question)

# question_embedding = np.random.rand(768)  # Replace with actual question embedding

# distances = []
# for _, row in data.iterrows():
#     email_text = row['Email Text']  # Assuming 'Email Text' is the column name in the CSV
#     embedding = row['embedding']
#     distance = calculate_distance(question_embedding, embedding)
#     distances.append((email_text, distance))


# Sort emails by distance (closest match first)
# distances.sort(key=lambda x: x[1])

reference_embedding = np.zeros(768)
data['distance'] = data['embedding'].apply(lambda x: calculate_distance(x, question_embedding))

data.sort_values('distance', ascending=False, inplace=True)
# Get the top 5 closest emails
data.head()

# Construct the context from the 'Email Text' column
context = data['Email Text'].iloc[1] + "\n" + data['Email Text'].iloc[2] + data['Email Text'].iloc[3] + \
          data['Email Text'].iloc[
              4]
print("Context for generation:")


# print(context)


#
# def get_response():
#     question = (
#         "Dear Valued Customer, We are reaching out to inform you of a recent security update regarding your account..."
#     )
#
#     # Generate embedding for the question
#     question_embedding = get_embedding(question)
#
#     # Retrieve the closest stored emails from the database
#     closest_emails = find_closest_embeddings(question_embedding)
#
#     # Combine the closest email texts as context
#     context = "\n".join([email[0] for email in closest_emails])
#
#     # Prepare the prompt for the generative model
#     prompt = f"Context: {context}\nQuestion: {question}"
#
#     model = genai.GenerativeModel('gemini-1.5-flash')
#     response = model.generate_content(prompt)
#
#     return response.generations[0].text


def get_analysis(email_text):
    retrieved_context = f"Use this information about Phishing as context to answer the user's question accurately: {context}. stick to this context when answering the question."

    prompt = f"Context: {retrieved_context}\n Question: {email_text}"

    # model = genai.GenerativeModel('gemini-1.5-flash')
    # response = model.generate_content(prompt)

    external_api_url = "https://ai-api.amalitech.org/api/v1/public/chat"  # Replace with actual URL
    payload = {
        "prompt": prompt,
        "stream": False
    }

    headers = {"X-Api-Key": "key"}

    # Send the POST request to the external API
    external_response = requests.post(external_api_url, json=payload, headers=headers)

    if external_response.status_code == 200:
        external_data = external_response.json()  # Assuming the external API returns JSON
        print(external_data)
        return jsonify({"response": "", "external_response": external_data})
    else:
        return jsonify({
            "response": "",
            "external_error": "Failed to reach the external API",
            "status_code": external_response.status_code
        })
