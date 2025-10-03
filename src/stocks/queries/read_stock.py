"""
Product (read-only model)
SPDX - License - Identifier: LGPL - 3.0 - or -later
Auteurs : Gabriel C. Ullmann, Fabio Petrillo, 2025
"""

from db import get_sqlalchemy_session
from stocks.models.product import Product
from stocks.models.stock import Stock
from sqlalchemy import func



def get_stock_by_id(product_id):
    """Get stock by product ID """
    session = get_sqlalchemy_session()
    result = session.query(Stock).filter_by(product_id=product_id).all()
    if len(result):
        return {
            'product_id': result[0].product_id,
            'quantity': result[0].quantity,
        }
    else:
        return {}

# src/stocks/queries/read_stock.py

def get_stock_for_all_products():
    session = get_sqlalchemy_session()
    try:
        rows = (
            session.query(
                Product.id.label("product_id"),
                Product.name,
                Product.sku,
                Product.price,
                Stock.quantity
            )
            .join(Stock, Stock.product_id == Product.id)  # inner join
            .order_by(Product.id.asc())
            .all()
        )
        return [
            {
                "Article ID": row.product_id,
                "Nom de l'article": row.name,
                "Numéro SKU": row.sku,
                "Prix unitaire": float(row.price),
                "Unités en stock": int(row.quantity),
            }
            for row in rows
        ]
    finally:
        session.close()

