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

genai.configure(api_key="GEMINI")


def get_analysis(question):
    # question = (
    #     "Dear Valued Customer, We are reaching out to inform you of a recent security update regarding your account..."
    # )

    # Generate embedding for the question
    question_embedding = get_embedding(question)

    # Retrieve the closest stored emails from the database
    closest_emails = find_closest_embeddings(question_embedding)

    # Combine the closest email texts as context
    context = "\n".join([email[0] for email in closest_emails])
    retrieved_context = f"Use this information about Phishing as context to answer the user's question accurately: {context}. stick to this context when answering the question."

    # Prepare the prompt for the generative model
    prompt = f"Context: {retrieved_context}\nQuestion: {question}"

    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content(prompt)

    return response.text

#
# def get_analysis(email_text):
#     retrieved_context = f"Use this information about Phishing as context to answer the user's question accurately: {context}. stick to this context when answering the question."
#
#     prompt = f"Context: {retrieved_context}\n Question: {email_text}"
#
#     model = genai.GenerativeModel('gemini-1.5-flash')
#     response = model.generate_content(prompt)
#
#     return response.text
#
#     # external_api_url = "https://ai-api.amalitech.org/api/v1/public/chat"  # Replace with actual URL
#     # payload = {
#     #     "prompt": prompt,
#     #     "stream": False
#     # }
#     #
#     # headers = {"X-Api-Key": "key"}
#     #
#     # # Send the POST request to the external API
#     # external_response = requests.post(external_api_url, json=payload, headers=headers)
#     #
#     # if external_response.status_code == 200:
#     #     external_data = external_response.json()  # Assuming the external API returns JSON
#     #     print(external_data)
#     #     return jsonify({"response": "", "external_response": external_data})
#     # else:
#     #     return jsonify({
#     #         "response": "",
#     #         "external_error": "Failed to reach the external API",
#     #         "status_code": external_response.status_code
#     #     })
