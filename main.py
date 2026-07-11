from fastapi import FastAPI

# defining an object
app = FastAPI()


@app.get("/")
def greet():
    return "Welcome to the AI world"


@app.get("/products")
def get_all_products():
    return "All Products"
