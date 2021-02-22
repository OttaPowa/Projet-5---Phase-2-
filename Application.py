# -*-coding:UTF-8-*

from ManageDb import *
from PrepareData import *

from Category import Category
from Product import Product
from Brand import Brand
from Store import Store


def main():
    # connexion and prerequisites:
    ManageDb.verify_prerequisite()
    authenticated = False
    while not authenticated:
        authenticated = ManageDb.mysql_connection()

    # get and clean the data:
    update = ManageDb.ask_to_update_database()

    if update:
        PrepareData.get_categories()

        PrepareData.get_and_sort_products()

        PrepareData.calibrate(PrepareData.raw_products)

        PrepareData.instantiate(Product, PrepareData.cleaned_products)

        stores = [store.store for store in Product.instantiated_products]
        brands = [brand.brand for brand in Product.instantiated_products]
        categories = [categories.category for categories
                      in Product.instantiated_products]

        PrepareData.split_and_set(stores)
        PrepareData.instantiate(Store, PrepareData.setted_items)

        PrepareData.split_and_set(brands)
        PrepareData.instantiate(Brand, PrepareData.setted_items)

        PrepareData.split_and_set(categories)
        PrepareData.get_url(PrepareData.setted_items)
        PrepareData.instantiate(Category, PrepareData.cleaned_cat_with_url)

        # build and fill the data base:
        ManageDb.build()

        ManageDb.fill("INSERT INTO category (name, url) VALUES (%s, %s)",
                      Category.instantiated_categories)
        ManageDb.fill("INSERT INTO store (name) VALUES (%s)",
                      Store.instantiated_stores)
        ManageDb.fill("INSERT INTO brand (name) VALUES (%s)",
                      Brand.instantiated_brands)
        ManageDb.fill("INSERT INTO product (name, url, picture_url,"
                      " nutriscore) VALUES (%s, %s, %s, %s)",
                      Product.instantiated_products)

        ManageDb.insert_n_n(Product.instantiated_products, "product", "store",
                            "product_store", "id_product", "id_store")
        ManageDb.insert_n_n(Product.instantiated_products, "product", "brand",
                            "product_brand", "id_product", "id_brand")
        ManageDb.insert_n_n(Product.instantiated_products, "product",
                            "category", "product_category", "id_product",
                            "id_category")
    else:
        pass

    # application:
    ManageDb.insert_logs_and_get_id()

    if ManageDb.user_id[0] in ManageDb.list_of_user_id:
        ManageDb.access_to_stored_data()
    else:
        pass

    print("\nCette application vous permet de rechercher un produit pour "
          "lequel vous souhaitez trouver un équivalent plus sain.\n"
          "Naviguez a travers les catégories pour trouver le produit "
          "que vous désirez.")

    while ManageDb.action != "Q" or ManageDb.action != "q":
        ManageDb.action = ManageDb.selection()

        if ManageDb.action == "C" or ManageDb.action == "c":
            ManageDb.glob = "display cat"
            ManageDb.display_categories()

        elif ManageDb.action == "S" or ManageDb.action == "s":
            ManageDb.ask_to_save_result()
            ManageDb.glob = "end cycle"

        elif ManageDb.action == "Q" or ManageDb.action == "q":
            quit()

        elif ManageDb.action.isdigit() or ManageDb.action == "Y" \
                or ManageDb.action == "y":
            if ManageDb.glob == "display cat":
                ManageDb.display_products(ManageDb.action)
                ManageDb.glob = "display prod"
            elif ManageDb.glob == "display prod":
                ManageDb.display_nutriscore(ManageDb.action)
                ManageDb.base_product = ManageDb.action
                ManageDb.glob = "compare prod"
            elif ManageDb.glob == "compare prod" \
                    and (ManageDb.action == "Y"
                         or ManageDb.action == "y"):
                ManageDb.compare_product_in_current_category()
                ManageDb.glob = "alternative compare"
            elif ManageDb.glob == "alternative compare" \
                    and (ManageDb.action == "Y"
                         or ManageDb.action == "y"):
                ManageDb.compare_product_in_affiliated_categories(
                    ManageDb.current_product[0][0])
                ManageDb.glob = "show details"
            elif ManageDb.glob == "show details":
                ManageDb.show_final_product_details(ManageDb.action)
                ManageDb.glob = "save search"
            elif ManageDb.glob == "save search" \
                    and (ManageDb.action == "Y"
                         or ManageDb.action == "y"):
                ManageDb.ask_to_save_result()
                ManageDb.glob = "end cycle"

        elif ManageDb.action != "Q" or ManageDb.action != "q":
            pass

    quit()


if __name__ == '__main__':
    main()
else:
    pass
