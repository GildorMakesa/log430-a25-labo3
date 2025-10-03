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
    """Get stock quantity and product details for all products"""
    session = get_sqlalchemy_session()
    try:
        rows = (
            session.query(
                Product.id.label("product_id"),
                Product.name.label("name"),
                Product.sku.label("sku"),
                Product.price.label("price"),
                func.coalesce(func.sum(Stock.quantity), 0).label("quantity"),
            )
            .outerjoin(Stock, Stock.product_id == Product.id)  # inclut aussi les produits sans stock
            .group_by(Product.id, Product.name, Product.sku, Product.price)
            .order_by(Product.id.asc())
            .all()
        )

        return [
            {
                "Article": row.product_id,
                "Numéro SKU": row.sku or "",
                "Prix unitaire": float(row.price) if row.price is not None else 0.0,
                "Unités en stock": int(row.quantity or 0),
            }
            for row in rows
        ]
    finally:
        session.close()


