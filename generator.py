import json

from flask import jsonify

import requests
import google.generativeai as genai

from get_embedding import get_embedding
from helper import find_closest_embeddings_from_db
import os

from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


# def get_analysis(email_text):
#     # Generate embedding for the question
#     email_text_embedding = get_embedding(email_text)
#
#     # Retrieve the closest stored emails from the database
#     closest_emails = find_closest_embeddings_from_db(email_text_embedding)
#
#     # Combine the closest email texts as context
#     context = "\n".join([email[0] for email in closest_emails])
#     retrieved_context = f"Use this information about Phishing as context to answer the user's question accurately: {context}. stick to this context when answering the question."
#
#     # Prepare the prompt for the generative model
#     prompt = f"Context: {retrieved_context}\nQuestion: {email_text}"
#
#     model = genai.GenerativeModel('gemini-1.5-flash')
#     response = model.generate_content(prompt)
#
#     return response.text

def get_analysis(email_text):
    # Generate embedding for the question
    email_text_embedding = get_embedding(email_text)

    # Retrieve the closest stored emails from the database
    closest_emails = find_closest_embeddings_from_db(email_text_embedding)
    # Combine the closest email texts as context
    context = "\n".join(closest_emails["EmailText"].tolist())

    retrieved_context = f"""1. Use this information about Phishing as context to analyze this email content accurately: {context}. 
                            2. Stick to this context when analyzing the email content. If is a phishing attempt make it clear and concise.
                            3. The outcome, denoted by a status label, should be either SAFE(meaning the email is safe to engage), THREAT(meaning the email is a phishing mail and with critical threat), RISK(meaning the email contains some traits of phishing, but with less severe threats)
                            4. The response should be in json format(example: {{'status':'','description':''}}) """

    # Prepare the prompt for the generative model
    prompt = f"Context: {retrieved_context}\nQuestion: {email_text}"

    external_api_url = "https://ai-api.amalitech.org/api/v1/public/chat"  # Replace with actual URL
    payload = {
        "prompt": prompt,
        "modelId": os.getenv("MODEL_ID"),
        "stream": False
    }
    #     #
    headers = {"X-Api-Key": os.getenv("KEY")}

    # Send the POST request to the external API
    external_response = requests.post(external_api_url, json=payload, headers=headers)

    if external_response.status_code == 200:
        response_content = external_response.json()["data"]["content"]
        if isinstance(response_content, str):
            response_content = json.loads(response_content)

        return jsonify({"data": response_content})
    else:
        return jsonify({
            "response": "",
            "external_error": "Failed to reach the external API",
            "status_code": external_response.status_code
        })
