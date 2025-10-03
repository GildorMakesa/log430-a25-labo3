"""
Tests for orders manager
SPDX - License - Identifier: LGPL - 3.0 - or -later
Auteurs : Gabriel C. Ullmann, Fabio Petrillo, 2025
"""

import json
import pytest
from store_manager import app
from uuid import uuid4

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_health(client):
    result = client.get('/health-check')
    assert result.status_code == 200
    assert result.get_json() == {'status':'ok'}

import json

def test_stock_flow(client):

    # 0. Créez un utilisateur (POST /users)
    user_email = f"test_{uuid4().hex[:8]}@example.com"
    user_data = {"name": "Test User", "email": user_email}
    response = client.post(
        "/users",
        data=json.dumps(user_data),
        content_type="application/json"
    )
    assert response.status_code == 201
    user_id = response.get_json()["user_id"]
    
    # 1. Créez un article (POST /products)
    product_data = {"name": "Some Item", "sku": "12345", "price": 99.90}
    response = client.post(
        "/products",
        data=json.dumps(product_data),
        content_type="application/json"
    )
    assert response.status_code == 201
    data = response.get_json()
    product_id = data["product_id"]
    assert product_id > 0




    # 2. Ajoutez 5 unités au stock de cet article (POST /products_stocks)
    stock_data = {"product_id": product_id, "quantity": 5}
    response = client.post(
        "/stocks",
        data=json.dumps(stock_data),
        content_type="application/json"
    )
    # >>> DEBUG en cas d’échec
    if response.status_code != 201:
        print("BODY:", response.get_data(as_text=True))
    assert response.status_code == 201




    # 3. Vérifiez le stock → doit être 5 (GET /stocks/:id)
    response = client.get(f"/stocks/{product_id}")
    assert response.status_code == 201
    print("\nStock après ajout:", response.get_json())  # <-- visible avec pytest -s
    stock_info = response.get_json()
    assert stock_info["quantity"] == 5




    # 4. Créez une commande de 2 unités (POST /orders)
    order_data = {
        "user_id": 1,   # Assurez-vous qu’il existe un utilisateur avec ID=1
        "items": [{"product_id": product_id, "quantity": 2}]
    }
    response = client.post(
        "/orders",
        data=json.dumps(order_data),
        content_type="application/json"
    )
    assert response.status_code == 201
    order_id = response.get_json()["order_id"]

    

    # 5. Vérifiez le stock encore une fois → doit être 3
    response = client.get(f"/stocks/{product_id}")
    assert response.status_code == 201
    stock_info = response.get_json()
    print("Stock final:", stock_info["quantity"])         # <-- visible avec pytest -s
    assert stock_info["quantity"] == 3

    # 6. Extra : supprimez la commande et vérifiez que le stock redevient 5
    response = client.delete(f"/orders/{order_id}")
    assert response.status_code == 200

    response = client.get(f"/stocks/{product_id}")
    assert response.status_code == 201
    stock_info = response.get_json()
    assert stock_info["quantity"] == 5
    #assert "Le test n'est pas encore là" == 1