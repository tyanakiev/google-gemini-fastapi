from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello, World!"}


def generate_large_response(num_tokens):
    # Generate a large string with the specified number of tokens
    # You can use any logic you want to generate the string
    # For example, you could use a simple repeating pattern:
    response = "This is a large response. " * (num_tokens // 27)
    return response


@app.get("/large-response")
async def large_response(num_tokens: int = 50000):
    response_text = generate_large_response(num_tokens)
    return {"response": response_text}
