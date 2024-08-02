import logging
from sqlalchemy.orm import Session
from ..model.models import Product, Category

logger = logging.getLogger("Application")

def initialize_db(db: Session):
    products = [
        # Sanduíches
        {"name": "Sanduíche de Frango Grelhado", "description": "Grilled chicken sandwich with lettuce and tomato", "price": 15.00, "category_id": 1},
        {"name": "Cheeseburger Clássico", "description": "Classic cheeseburger with beef patty and cheese", "price": 12.00, "category_id": 1},
        {"name": "Sanduíche Vegano de Grão-de-Bico", "description": "Vegan sandwich with chickpea patty", "price": 14.00, "category_id": 1},
        
        # Pizzas
        {"name": "Pizza Margherita", "description": "Pizza with tomato sauce, mozzarella, and basil", "price": 25.00, "category_id": 2},
        {"name": "Pizza Pepperoni", "description": "Pizza with tomato sauce, mozzarella, and pepperoni", "price": 27.00, "category_id": 2},
        {"name": "Pizza Quatro Queijos", "description": "Pizza with four types of cheese", "price": 28.00, "category_id": 2},
        
        # Acompanhamentos
        {"name": "Batata Frita", "description": "Portion of crispy french fries", "price": 8.00, "category_id": 3},
        {"name": "Anéis de Cebola", "description": "Portion of breaded onion rings", "price": 9.00, "category_id": 3},
        {"name": "Salada Caesar", "description": "Caesar salad with lettuce, croutons, and parmesan cheese", "price": 10.00, "category_id": 3},
        
        # Bebidas
        {"name": "Coca-Cola", "description": "Cola soft drink", "price": 5.00, "category_id": 4},
        {"name": "Suco de Laranja", "description": "Natural orange juice", "price": 6.00, "category_id": 4},
        {"name": "Água Mineral", "description": "Still mineral water", "price": 4.00, "category_id": 4},
        
        # Sobremesas
        {"name": "Brownie de Chocolate", "description": "Chocolate brownie with walnuts", "price": 7.00, "category_id": 5},
        {"name": "Torta de Maçã", "description": "Apple pie with cinnamon", "price": 8.00, "category_id": 5},
        {"name": "Sorvete de Baunilha", "description": "Vanilla ice cream", "price": 6.00, "category_id": 5},
    ]

    existing_product_names = {product.name for product in db.query(Product.name).all()}
    
    for product in products:
        if product['name'] in existing_product_names:
            logger.info(f"Product already exists in the database: {product['name']} - Category: {product['category']}")
        else:
            db_product = Product(**product)
            db.add(db_product)
            logger.info(f"Product added: {db_product.name} - Category: {db_product.category}")
            
    categories = [
    {"name": "Sanduíches"},
    {"name": "Pizzas"},
    {"name": "Acompanhamentos"},
    {"name": "Bebidas"},
    {"name": "Sobremesas"},
]

    existing_categories_names = {category.name for category in db.query(Category.name).all()}

    for category in categories:
        if category['name'] in existing_categories_names:
            logger.info(f"Category already exists in the database: Category: {category['name']}")
        else:
            db_category = Category(**category)
            db.add(db_category)
            logger.info(f"Category added: {db_category.name}")

    db.commit()
    logger.info("Database initialization completed.")
