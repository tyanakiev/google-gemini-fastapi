import os
import re
import logging
import json
from pathlib import Path
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
from typing import Optional, Dict, Any
import google.generativeai as genai
import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('orders.db')
c = conn.cursor()

# Configure logging
logging.basicConfig(filename='app.log', level=logging.DEBUG)

app = FastAPI()

# Load environment variables
load_dotenv()

# Configure generative models
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

# Load the OpenAPI documentation
openapi_path = Path(__file__).parent / "openapi.json"
with open(openapi_path, "r") as f:
    openapi_doc = json.load(f)

# Extract available API endpoints
available_apis = [path for path in openapi_doc["paths"].keys() if path.startswith("/")]

# Load the fine-tuned model

model_analyze = genai.GenerativeModel('gemini-1.5-pro-latest')  # Model 1 for analyzing prompt
model_generate = genai.GenerativeModel('gemini-1.5-pro-latest')  # Model 2 for generating response


# Request model with prompt
class AnalyzeRequest(BaseModel):
    prompt: str


# Response model
class Response(BaseModel):
    response: str




@app.post("/process-prompt", response_model=Response)
async def process_prompt(prompt: str, params: Optional[Dict[str, Any]] = None):
    try:
        logging.info(f"Received prompt: {prompt}")

        # Use the first model to predict the API label
        predicted_api = predict_api(prompt)
        logging.info(f"Predicted API: {predicted_api}")

        # Make API call and fetch data
        if params:
            data = call_api(predicted_api, **params)
        else:
            data = call_api(predicted_api)
        logging.info(f"Data retrieved: {data}")

        # Combine prompt and data, and generate response using the second model
        combined_prompt = f"{prompt}\n\nData:\n{data}"
        response = generate_response(combined_prompt)
        logging.info(f"Generated response: {response}")

        return Response(response=response)
    except Exception as e:
        logging.error("Error occurred: ", exc_info=True)



def call_api(api_to_call, **kwargs):
    # Extract header_id from api_to_call
    api_to_call = api_to_call.strip('*')
    api_to_call = api_to_call.strip('`')
    api_to_call = api_to_call.strip('')
    match = re.search(r'/get_order_line/(\d+)', api_to_call)
    header_id = int(match.group(1)) if match else None
    logging.info(f"api_to_call: '{api_to_call}', length: {len(api_to_call)}")
    if api_to_call.startswith("/get_orders"):
        orders = get_orders()
        return "\n".join([str(order) for order in orders])
    elif api_to_call.startswith("/get_order_lines"):
        logging.info("Calling get_order_lines")
        order_lines = get_order_lines()
        return "\n".join([str(order_line) for order_line in order_lines])
    elif api_to_call.startswith("/get_order_line/"):
        if header_id is None:
            raise HTTPException(status_code=400, detail="header_id is required for get_order_line")
        order_line = get_order_line(header_id)
        return str(order_line)
    else:
        raise HTTPException(status_code=404, detail="API not found")

def predict_api(prompt):
    # Use the first model to predict the API to call
    logging.info(available_apis)
    combined_input = (f"{prompt} here are all available APIs: {', '.join(available_apis)} "
                      f"Return just the API that is related to this question. "
                      f"Please insert any variables needed for the API call. Variables are in curly braces. "
                      f"For example if we have /get_order_line/{'header_id'} and the user wants to get order line for header_id 1, "
                      f"the user should input /get_order_line/1. "
                      f"Please ensure to include the header_id in the API call if it is required.")
    output = model_analyze.generate_content(combined_input)
    predicted_api = output.text.strip()
    logging.info(f"Predicted API: {predicted_api}")
    return predicted_api

def generate_response(combined_prompt):
    # Use the second model to generate a response
    response_result = model_generate.generate_content(combined_prompt)
    return response_result.text

@app.get("/get_orders")
def get_orders():
    """
    Retrieve all orders from the database.
    """
    c.execute("SELECT * FROM Orders")
    return c.fetchall()


@app.get("/get_order_lines")
def get_order_lines():
    """
    Retrieve all order lines
    """
    c.execute("SELECT * FROM OrderLines")
    return c.fetchall()

@app.get("/get_order_line/{header_id}")
def get_order_line(header_id: int):
    """
    Retrieve order lines for a specific order.
    """
    c.execute("SELECT * FROM OrderLines WHERE HEADER_ID=?", (header_id,))
    return c.fetchall()
