from ....product.models import Product
import json
from decimal import Decimal

def test_product_by_id(db, client_query):
    product = Product.objects.create(
        name = "Test Product",
        description = "Product test desc",
        price = Decimal("49.99"),
        quantity=5.00
    )

    response = client_query(
        """
        query myproduct($id: ID!) {
            product(id: $id){
                price
                id
                name
                description
                quantity
            }
        }
        """,
        variables={'id':1}
    )
    content = json.loads(response.content)


    product_response = content['data']['product']

    assert product_response['id'] == str(product.id)
    assert product_response['description'] == product.description
    assert product_response['quantity'] == product.quantity
    assert product_response['price'] == str(product.price)