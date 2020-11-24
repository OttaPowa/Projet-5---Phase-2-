# -*-coding:UTF-8-*

import Category
import Product
import Brand
import Store

NAME_OF_TABLE = ["category", "product", 'store', "brand", "product_store", "product_brand", "product_category"]
COLUMN = ["name", "url", "picture_url", "nutriscore", "id", "id_category", "id_store", "id_brand", "id_product", "*"]
NAMES_IN_FRENCH = ["de la categorie", "du produit"]

INSERT_CATS = f"INSERT INTO {NAME_OF_TABLE[0]} ({COLUMN[0]}, {COLUMN[1]}) VALUES (%s, %s)"
INSERT_STORES = f"INSERT INTO {NAME_OF_TABLE[2]} ({COLUMN[0]}) VALUES (%s)"
INSERT_BRANDS = f"INSERT INTO {NAME_OF_TABLE[3]} ({COLUMN[0]}) VALUES (%s)"
INSERT_PRODUCTS = f"INSERT INTO {NAME_OF_TABLE[1]} ({COLUMN[0]}, {COLUMN[1]}, {COLUMN[2]}, {COLUMN[3]}) VALUES (%s, %s, %s, %s)"

DICT_OF_CLASSES = {'Store': Store.Store, 'Brand': Brand.Brand, 'Product': Product.Product,
                   'Category': Category.Category}

GREETING_MESSAGE = "\nCette application vous permet de rechercher un produit pour lequel vous souhaitez trouver un équivalent plus sain.\n" \
                   "Naviguez a travers les catégories pour trouver le produit que vous désirez.\n"

test = ("f", "t")