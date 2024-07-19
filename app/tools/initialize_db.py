import logging
from sqlalchemy.orm import Session
from ..model.models import Product

logger = logging.getLogger("Application")

def initialize_db(db: Session):
    products = [
        # Sanduíches
        {"name": "Sanduíche de Frango Grelhado", "description": "Grilled chicken sandwich with lettuce and tomato", "price": 15.00, "category": "Sanduíches"},
        {"name": "Cheeseburger Clássico", "description": "Classic cheeseburger with beef patty and cheese", "price": 12.00, "category": "Sanduíches"},
        {"name": "Sanduíche Vegano de Grão-de-Bico", "description": "Vegan sandwich with chickpea patty", "price": 14.00, "category": "Sanduíches"},
        
        # Pizzas
        {"name": "Pizza Margherita", "description": "Pizza with tomato sauce, mozzarella, and basil", "price": 25.00, "category": "Pizzas"},
        {"name": "Pizza Pepperoni", "description": "Pizza with tomato sauce, mozzarella, and pepperoni", "price": 27.00, "category": "Pizzas"},
        {"name": "Pizza Quatro Queijos", "description": "Pizza with four types of cheese", "price": 28.00, "category": "Pizzas"},
        
        # Acompanhamentos
        {"name": "Batata Frita", "description": "Portion of crispy french fries", "price": 8.00, "category": "Acompanhamentos"},
        {"name": "Anéis de Cebola", "description": "Portion of breaded onion rings", "price": 9.00, "category": "Acompanhamentos"},
        {"name": "Salada Caesar", "description": "Caesar salad with lettuce, croutons, and parmesan cheese", "price": 10.00, "category": "Acompanhamentos"},
        
        # Bebidas
        {"name": "Coca-Cola", "description": "Cola soft drink", "price": 5.00, "category": "Bebidas"},
        {"name": "Suco de Laranja", "description": "Natural orange juice", "price": 6.00, "category": "Bebidas"},
        {"name": "Água Mineral", "description": "Still mineral water", "price": 4.00, "category": "Bebidas"},
        
        # Sobremesas
        {"name": "Brownie de Chocolate", "description": "Chocolate brownie with walnuts", "price": 7.00, "category": "Sobremesas"},
        {"name": "Torta de Maçã", "description": "Apple pie with cinnamon", "price": 8.00, "category": "Sobremesas"},
        {"name": "Sorvete de Baunilha", "description": "Vanilla ice cream", "price": 6.00, "category": "Sobremesas"},
    ]

    existing_product_names = {product.name for product in db.query(Product.name).all()}
    
    for product in products:
        if product['name'] in existing_product_names:
            logger.info(f"Product already exists in the database: {product['name']} - Category: {product['category']}")
        else:
            db_product = Product(**product)
            db.add(db_product)
            logger.info(f"Product added: {db_product.name} - Category: {db_product.category}")
    
    db.commit()
    logger.info("Database initialization completed.")
