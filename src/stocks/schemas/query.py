# src/stocks/schemas/query.py
import graphene
from graphene import ObjectType, Int
from db import get_redis_conn, get_sqlalchemy_session
from stocks.models.product import Product as ProductModel
from stocks.schemas.product import Product  # le type Graphene ci-dessus

class Query(ObjectType):
    product = graphene.Field(Product, id=Int(required=True))
    stock_level = Int(product_id=Int(required=True))
    
    def resolve_product(self, info, id):
        # Redis: quantité
        r = get_redis_conn()
        qty = r.hget(f"stock:{id}", "quantity")
        quantity = int(qty) if qty is not None else 0

        # MySQL: métadonnées produit
        session = get_sqlalchemy_session()
        try:
            p = session.query(ProductModel).filter(ProductModel.id == id).first()
            if not p:
                return None
            return Product(
                id=p.id,
                name=p.name,
                sku=p.sku,
                price=float(p.price) if p.price is not None else 0.0,
                quantity=quantity,
            )
        finally:
            session.close()

    def resolve_stock_level(self, info, product_id):
        r = get_redis_conn()
        qty = r.hget(f"stock:{product_id}", "quantity")
        return int(qty) if qty is not None else 0
    
    
