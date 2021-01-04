# -*-coding:UTF-8-*

import Category
import Product
import Brand
import Store
import User
import Saving

NAME_OF_TABLE = ["category", "product", 'store', "brand", "product_store", "product_brand", "product_category"]
COLUMN = ["name", "url", "picture_url", "nutriscore", "id", "id_category", "id_store", "id_brand", "id_product", "*"]
NAMES_IN_FRENCH = ["de la catégorie", "du produit"]

INSERT_CATS = "INSERT INTO category (name, url) VALUES (%s, %s)"
INSERT_STORES = "INSERT INTO store (name) VALUES (%s)"
INSERT_BRANDS = "INSERT INTO brand (name) VALUES (%s)"
INSERT_PRODUCTS = "INSERT INTO product (name, url, picture_url, nutriscore) VALUES (%s, %s, %s, %s)"
INSERT_LOGS = "INSERT INTO user (user_name, password) VALUES (%s, %s)"
INSERT_SAVINGS = "INSERT INTO saving (bas_product_id, alternative_product_id) VALUES (%s, %s)"

DICT_OF_CLASSES = {'Store': Store.Store, 'Brand': Brand.Brand, 'Product': Product.Product,
                   'Category': Category.Category, 'User': User.User, 'Saving': Saving.Saving}

GREETING_MESSAGE = "\nCette application vous permet de rechercher un produit pour lequel vous souhaitez trouver " \
                   "un équivalent plus sain.\nNaviguez a travers les catégories pour trouver le produit que vous " \
                   "désirez.\n"
test = ("f", "t")
