# google-gemini-fastapi

Welcome to google-gemini-fastapi, a project designed to integrate two Gemini models using FastAPI. This project leverages the power of AI to analyze prompts, determine the necessary API calls, and process the responses to generate meaningful outputs.
Overview

### The google-gemini-fastapi repository aims to provide a seamless integration of two Gemini models. The workflow is as follows:

    Model 1 analyzes the incoming prompt to determine which API needs to be called.
    The identified API is called to fetch the relevant data.
    The prompt is merged with the fetched data.
    Model 2 processes the combined prompt and data to generate a final response.

### Features

    Prompt Analysis: The first Gemini model intelligently analyzes the prompt to determine the appropriate API call.
    Dynamic API Integration: The system dynamically calls the necessary API based on the analysis.
    Data Merging: Combines the original prompt with the fetched data.
    Response Generation: The second Gemini model processes the merged data to produce a coherent and contextually relevant response.
    FastAPI Framework: Utilizes the FastAPI framework for building the API endpoints, ensuring high performance and easy deployment.

## Getting Started
### Prerequisites

Ensure you have the following installed:

    Python 3.8+
    FastAPI
    uvicorn
    Required dependencies listed in requirements.txt

## Installation

### Clone the repository:


    git clone https://github.com/yourusername/google-gemini-fastapi.git
    cd google-gemini-fastapi

Install the required dependencies:

bash

    pip install -r requirements.txt

Running the Application

    Set your Google API key in the `.env` file:

### Start the FastAPI application using uvicorn:

bash

    uvicorn main:app --reload


The application will be accessible at http://127.0.0.1:8000.
## Usage
### Endpoints

    POST http://localhost:8000/process-prompt Content-Type: application/json
    GET http://localhost:8000/get_orders
    GET http://localhost:8000/get_order_lines

### Example Workflow

    Send a prompt to the /process-prompt endpoint.
    The system will analyze the prompt and determine the necessary API call.
    The relevant data will be fetched and merged with the original prompt.
    The combined data will be processed to generate a final response, which will be returned to the user.

## Contributing

### Contributions are welcome! Please follow these steps:

    Fork the repository.
    Create a new branch (git checkout -b feature-branch).
    Make your changes.
    Commit your changes (git commit -m 'Add some feature').
    Push to the branch (git push origin feature-branch).
    Open a pull request.

## License

This project is licensed under the MIT License. See the LICENSE file for details.
Contact

For any questions or inquiries, please open an issue on GitHub.
