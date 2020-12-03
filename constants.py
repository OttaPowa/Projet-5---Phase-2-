# -*-coding:UTF-8-*

import Category
import Product
import Brand
import Store

NAME_OF_TABLE = ["category", "product", 'store', "brand", "product_store", "product_brand", "product_category"]
COLUMN = ["name", "url", "picture_url", "nutriscore", "id", "id_category", "id_store", "id_brand", "id_product", "*"]
NAMES_IN_FRENCH = ["de la categorie", "du produit"]

INSERT_CATS = f"INSERT INTO category (name, url) VALUES (%s, %s)"
INSERT_STORES = f"INSERT INTO store (name) VALUES (%s)"
INSERT_BRANDS = f"INSERT INTO brand (name) VALUES (%s)"
INSERT_PRODUCTS = f"INSERT INTO product (name, url, picture_url, nutriscore) VALUES (%s, %s, %s, %s)"

DICT_OF_CLASSES = {'Store': Store.Store, 'Brand': Brand.Brand, 'Product': Product.Product,
                   'Category': Category.Category}

GREETING_MESSAGE = "\nCette application vous permet de rechercher un produit pour lequel vous souhaitez trouver un équivalent plus sain.\n" \
                   "Naviguez a travers les catégories pour trouver le produit que vous désirez.\n"

test = ("f", "t")