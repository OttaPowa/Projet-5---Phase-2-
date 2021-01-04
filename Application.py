# -*-coding:UTF-8-*

from ManageDb import*
from constants import*
from PrepareData import*
from Category import Category
from Product import Product
from Brand import Brand
from Store import Store


def main():
    # connexion and prerequisites:
    #ManageDb.verify_prerequisite()
    #authenticated = False
    #while not authenticated:
        #authenticated = ManageDb.mysql_connection()

    # get and clean the data:
    PrepareData.get_categories()

    PrepareData.get_and_sort_products()

    PrepareData.calibrate(PrepareData.raw_products)

    PrepareData.instantiate(DICT_OF_CLASSES["Product"], PrepareData.cleaned_products)

    stores = [store.store for store in Product.instantiated_products]
    brands = [brand.brand for brand in Product.instantiated_products]
    categories = [categories.category for categories in Product.instantiated_products]

    PrepareData.split_and_set(stores)
    PrepareData.instantiate(DICT_OF_CLASSES["Store"], PrepareData.setted_items)

    PrepareData.split_and_set(brands)
    PrepareData.instantiate(DICT_OF_CLASSES["Brand"], PrepareData.setted_items)

    PrepareData.split_and_set(categories)
    PrepareData.get_url(PrepareData.setted_items)
    PrepareData.instantiate(DICT_OF_CLASSES["Category"], PrepareData.cleaned_cat_with_url)

    # build and fill the data base:
    ManageDb.build()

    ManageDb.fill(INSERT_CATS, Category.instantiated_categories)
    ManageDb.fill(INSERT_STORES, Store.instantiated_stores)
    ManageDb.fill(INSERT_BRANDS, Brand.instantiated_brands)
    ManageDb.fill(INSERT_PRODUCTS, Product.instantiated_products)

    ManageDb.insert_n_n(Product.instantiated_products, NAME_OF_TABLE[1], NAME_OF_TABLE[2],
                        NAME_OF_TABLE[4], COLUMN[8], COLUMN[6])
    ManageDb.insert_n_n(Product.instantiated_products, NAME_OF_TABLE[1], NAME_OF_TABLE[3],
                        NAME_OF_TABLE[5], COLUMN[8], COLUMN[7])
    ManageDb.insert_n_n(Product.instantiated_products, NAME_OF_TABLE[1], NAME_OF_TABLE[0],
                        NAME_OF_TABLE[6], COLUMN[8], COLUMN[5])

    # application:
    print(GREETING_MESSAGE)

    while ManageDb.action != "Q":
        ManageDb.action = ManageDb.selection()

        if ManageDb.action == "C":
            ManageDb.glob = "display cat"
            ManageDb.display_categories()

        elif ManageDb.action.isdigit():
            if ManageDb.glob == "display cat":
                ManageDb.get_products_from_selected_category()
                ManageDb.display_products(ManageDb.prod_from_selected_cat)
                ManageDb.glob = "display prod"
            elif ManageDb.glob == "display prod":
                ManageDb.display_nutriscore(ManageDb.action)
                ManageDb.base_product = ManageDb.action
                ManageDb.glob = "compare prod"
            elif ManageDb.glob == "compare prod" and ManageDb.action == "999":
                ManageDb.compare_product_in_current_category()
                ManageDb.glob = "alternative compare"
            elif ManageDb.glob == "alternative compare" and ManageDb.action == "666":
                ManageDb.compare_product_in_affiliated_categories()
                ManageDb.glob = "show details"
            elif ManageDb.glob == "show details":
                ManageDb.show_final_product_details()
                ManageDb.glob = "save search"
            elif ManageDb.glob == "save search" and ManageDb.action == "000":
                ManageDb.ask_to_save_result()

        elif ManageDb.action != "Q":
            pass

    quit()

    # choix de stocker ses résultat dans la bd, de faire une nouvelle recherche et de quitter


if __name__ == '__main__':
    main()
else:
    pass
