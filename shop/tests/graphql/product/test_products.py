from ....product.models import Product
import json
from decimal import Decimal

def test_products(db, client_query):
    products = [
    Product.objects.create(
        name = "Test Products1",
        description = "Products1 test desc",
        price = Decimal("9.99"),
        quantity=5.00
    ),
    Product.objects.create(
        name = "Test Products2",
        description = "Tatata",
        price = Decimal("4.99"),
        quantity=12.00
    ),
    Product.objects.create(
        name = "Test wd1243123212",
        description = "xDD222",
        price = Decimal("5.99"),
        quantity=52.00
    ),
    Product.objects.create(
        name = "11111",
        description = "Super Product",
        price = Decimal("666.99"),
        quantity=92.00
    )
    ]

    
    response = client_query(
        """
      query myproducts {
             products{
                price
                id
                name
                description
                quantity
            }
        }
        """
    )
    
    content = json.loads(response.content)
    product_response = content['data']['products']

    # Asserting by range of all responsed products
    for cp_index in range(0, len(product_response)):
        assert product_response[cp_index]['id'] == str(products[cp_index].id)
        assert product_response[cp_index]['description'] == products[cp_index].description
        assert product_response[cp_index]['quantity'] == products[cp_index].quantity
        assert product_response[cp_index]['price'] == str(products[cp_index].price)