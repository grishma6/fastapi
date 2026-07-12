from fastapi import Depends, FastAPI
from models import Product
from database import SessionLocal, engine
import database_model
from sqlalchemy.orm import Session

# defining an object
app = FastAPI()

# databse connection
database_model.Base.metadata.create_all(bind=engine)


@app.get("/")
def greet():
    return "Welcome to the AI world"


products = [
    Product(id=1, name="Phone", description="A smartphone",
            price=699.99, quantity=50),
    Product(id=2, name="Laptop", description="A powerful Laptop",
            price=999.99, quantity=30),
    Product(id=5, name="Pen", description="A blue ink pen",
            price=1.99, quantity=100),
    Product(id=6, name="Table", description="A wooden table",
            price=199.99, quantity=20),
]

def get_db():
    db = SessionLocal()
    #if something goes wrong with the usage so exception is used
    try:
        yield db #close after others have used it 
    finally:
        db.close()

# database, **->key value pairs, model_dump-->>dictonary,
def init_db():
    db = SessionLocal()

    count = db.query(database_model.Product).count
    if count == 0:
        for product in products:
            db.add(database_model.Product(**product.model_dump()))

    db.commit()

init_db()


@app.get("/products")
def get_all_products(db: Session = Depends(get_db)): #asking permission

    db_products = db.query(database_model.Product).all()
    return db_products


@app.get("/product/{id}")
def get_product_by_id(id: int, db: Session = Depends(get_db)):
    db_product = db.query(database_model.Product).filter(database_model.Product.id == id).first()
    if db_product:
        return db_product
    return "product not found"



@app.post("/product")
def add_product(product: Product, db: Session = Depends(get_db)):
    db.add(database_model.Product(**product.model_dump()))
    db.commit()
    return product


@app.put("/product")
def update_product(id: int, product: Product, db: Session = Depends(get_db)):
    db_product = db.query(database_model.Product).filter(database_model.Product.id == id).first()

    if db_product:
        db_product.name = product.name
        db_product.description = product.description
        db_product.price = product.price
        db_product.quantity = product.quantity
        db.commit()
        return "Product Updated"
    else:
        return "NO product found"
    


@app.delete("/product")
def delete_product(id: int, db: Session = Depends(get_db)):
    db_product = db.query(database_model.Product).filter(database_model.Product.id == id).first()
    if db_product:
            db.delete(db_product)
            db.commit()
            return "Product Deleted Successfully"
    else:
        return "No product deleted"
    
