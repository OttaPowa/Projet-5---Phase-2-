# -*-coding:UTF-8-*

import mysql.connector

from constants import*
from Interactions import Interactions


class ManageDb:
    """
        This class manage the interactions with the database
    """

    # class instances
    #connexion = ""  # methode definitive
    #cursor = ""

    # methode rapide pour test
    connexion = mysql.connector.connect(user="root", password="Donn1eDark0", database="projet5")
    cursor = connexion.cursor()

    list_of_prod_id = []

    prod_from_selected_cat = ()
    current_product = []
    list_of_id = []
    id_name_and_nutriscore_list = []

    @classmethod
    def verify_prerequisite(cls):
        """
            verify if MySQL is installed on the client computer. if not print a message with à link to DL it.
        """

        print("\nBonjour, MySQL est nécéssaire pour faire fonctionner l'application."
              "\nVous pouvez l'installer en suivant ce lien: https://dev.mysql.com/downloads/mysql/#downloads\n")

        user_input = input("Si vous possèdez un compte tapez 'Y' sinon tapez n'importe quelle autre touche: ")

        if user_input == "Y":
            pass
        else:
            quit()

    @classmethod
    def mysql_connection(cls):

        user_name = input("MySql user name: ")
        password = input("Mysql password: ")

        try:
            cls.connexion = mysql.connector.connect(user=user_name, password=password, database="projet5")
            cls.cursor = cls.connexion.cursor()
            return True
        except mysql.connector.errors.ProgrammingError:
            print("\nEchec de l'authentification auprès de MySql")
            return False


    @classmethod
    def build(cls):
        """
            build the MySQL tables
        """
        print("Contruction de la base de données...")

        data_base_sql = """
                        DROP TABLE IF EXISTS category;
                        DROP TABLE IF EXISTS product;
                        DROP TABLE IF EXISTS store;
                        DROP TABLE IF EXISTS brand;
                        DROP TABLE IF EXISTS product_store;
                        DROP TABLE IF EXISTS product_brand;
                        DROP TABLE IF EXISTS product_category;
                        
                        CREATE TABLE category(
                            id int NOT NULL AUTO_INCREMENT,
                            name varchar(200) DEFAULT NULL,
                            url varchar(300) DEFAULT NULL,
                            PRIMARY KEY(id))ENGINE=InnoDB;

                        CREATE TABLE product (
                            id int NOT NULL AUTO_INCREMENT,
                            name varchar(200) DEFAULT NULL,
                            url varchar(300) DEFAULT NULL,
                            picture_url varchar(300) DEFAULT NULL,
                            nutriscore varchar(5) DEFAULT NULL,
                            PRIMARY KEY(id))
                            ENGINE=InnoDB;

                        CREATE TABLE store (
                            id int NOT NULL AUTO_INCREMENT,
                            name varchar(200) DEFAULT NULL,
                            PRIMARY KEY(id))
                            ENGINE=InnoDB;

                        CREATE TABLE brand (
                            id int NOT NULL AUTO_INCREMENT,
                            name varchar(200) DEFAULT NULL,
                            PRIMARY KEY(id))
                            ENGINE=InnoDB;
                            
                        CREATE TABLE product_store (
                            id_product int DEFAULT NULL,
                            id_store int DEFAULT NULL)
                            ENGINE=InnoDB;
                            
                        CREATE TABLE product_brand (
                            id_product int DEFAULT NULL,
                            id_brand int DEFAULT NULL)
                            ENGINE=InnoDB;
                            
                        CREATE TABLE product_category (
                            id_product int DEFAULT NULL,
                            id_category int DEFAULT NULL)
                            ENGINE=InnoDB;
                        CREATE UNIQUE INDEX product_category_UI
                            ON product_category (id_product, id_category);
    
                        CREATE UNIQUE INDEX product_brand_UI
                            ON product_brand (id_product, id_brand);
    
                        CREATE UNIQUE INDEX product_store_UI
                            ON product_store (id_product, id_store);    
                        
                        """

        # apply multi true to execute sql actions in chain
        for result in cls.cursor.execute(data_base_sql, multi=True):
            pass

        cls.connexion.commit()
        print("La base de données à été crée.")

    @classmethod
    def delete(cls, what_to_drop, name):
        """
            delete database, table, line or column
        """
        cls.cursor.execute(f"DROP {what_to_drop} {name}")

    @classmethod
    def show_tables(cls):
        """
            show all tables of the database
        """
        cls.cursor.execute("SHOW TABLES")

        # display tables in a readable way
        for lines in cls.cursor:
            print(lines)

    @classmethod
    def select(cls, what_to_select, name_of_table):
        """
            select function in SQL
        """
        cls.list_of_prod_id = []  # clean the class instance

        fields = ", ".join(what_to_select)  # transform into a tuple

        sql_sentence = f"SELECT {fields} FROM {name_of_table}"

        cls.cursor.execute(sql_sentence)
        results = cls.cursor.fetchall()
        return results

    @classmethod
    def print_result(cls, results):
        """
            print the result of a SELECT
        """
        # loop on each rows, store the rows in a list and display them
        for items in results:
            cls.list_of_prod_id.append(items)
            print(items)

    @classmethod
    def fill(cls, insert_statement, list_of_items):
        """
            fill the database with the transformed API data
        """
        # try to raise AttributeError to select the right syntax
        for item in list_of_items:
            try:
                cls.cursor.execute(insert_statement, (item.name, item.url, item.picture_url, item.nutriscore))
            except AttributeError:
                try:
                    cls.cursor.execute(insert_statement, (item.name, item.url))

                except AttributeError:
                    cls.cursor.execute(insert_statement, (item.name,))

        cls.connexion.commit()

    @classmethod
    def insert_n_n(cls, instantiated_list, name_of_table1, name_of_table2, name_of_table3, column1, column2):
        """
            Prepare and insert data in the n_n tables
        """

        cat_unfounded = []  # categories not found in the french Api categories

        # loop on the instantiated products
        for product in instantiated_list:
            my_list_of_product_id = []  # renew the list in each lap
            my_product_id = ()  # renew the product id in each lap
            my_item_id = ()  # renew the item id in each lap

            # select the id of the product where the name is "product.name"
            query_product_id = f'SELECT id FROM {name_of_table1} WHERE name = "{product.name}"'
            cls.cursor.execute(query_product_id)

            # get the product id or ids
            for row in cls.cursor:
                my_product_id = row
                my_list_of_product_id.append(my_product_id)

            # do the associations of item id with all the product id of the list
            for my_prod_id in my_list_of_product_id:
                list_of_split_items = []

                if name_of_table2 == 'store':
                    list_of_split_stores = product.store.split(",")
                    list_of_split_items = list_of_split_stores
                elif name_of_table2 == 'brand':
                    list_of_split_brands = product.brand.split(",")
                    list_of_split_items = list_of_split_brands
                elif name_of_table2 == 'category':
                    list_of_split_categories = product.category.split(",")
                    list_of_split_items = list_of_split_categories
                else:
                    print("Erreur dans le nom de l'argument")

                split_items = []
                split_and_striped_item = []

                # clean the list of stores, brands or categories
                for my_length in range(len(list_of_split_items)):
                    for item in list_of_split_items:
                        temp = item.split(",")
                        split_items.append(temp)

                # prepare the data to be set
                for item_list in split_items:
                    for item in item_list:
                        split_and_striped_item.append(item.strip())

                # delete the doubloons
                cleaned_list_of_items = list(set(split_and_striped_item))

                # select the id of the store, brand or category where the name is the "item" value
                for item in cleaned_list_of_items:
                    query_item_id = f'SELECT id FROM {name_of_table2} WHERE name = "{item}"'
                    cls.cursor.execute(query_item_id)

                    # set the value of my_item_id
                    my_item_id = ()
                    for line in cls.cursor:
                        my_item_id = line

                    # some index error occurs when a name in another language is found (english or german mostly)
                    try:
                        query_insert = f"INSERT IGNORE INTO {name_of_table3} ({column1}, {column2}) VALUES (%s, %s)"
                        cls.cursor.execute(query_insert, (my_prod_id[0], my_item_id[0]))

                    except IndexError:
                        cat_unfounded.append(my_product_id)
                        continue

        cls.connexion.commit()

    @classmethod
    def display_categories(cls):
        """
            display the categories in screen and order them by name. Recover the number tipped by the user (category id)
            and get the corresponding products id
        """

        # select the categories and display it ordered by name
        result = cls.select((COLUMN[4], COLUMN[0]), f'{NAME_OF_TABLE[0]} ORDER BY name')
        cls.print_result(result)

        # get the number tipped by the user
        category_number = Interactions.selection(NAMES_IN_FRENCH[0])

        # recover the products id of the selected category
        cls.prod_from_selected_cat = cls.select((COLUMN[8], COLUMN[5]),
                                                f'{NAME_OF_TABLE[6]} WHERE {COLUMN[5]} = "{category_number}"')

    @classmethod
    def display_products(cls, list_of_products):
        """
            display the products names and ids of the category chosen before
        """

        list_of_id = []
        cls.current_product = []

        print('\nVoici les produits faisant partis de cette catégorie:\n')

        # display product name and id depending of the category id
        for my_product in list_of_products:
            result = cls.select((COLUMN[4], COLUMN[0]), f"{NAME_OF_TABLE[1]} WHERE {COLUMN[4]} = {my_product[0]}")

            # store the ids in a list so the list contains all the id product of the chosen category
            for my_id in result:
                list_of_id.append(my_id[0])
            cls.print_result(result)
        # il ya vait ici print("vous pouvez retiurner ux cat en tappant 0")
        product_number = Interactions.selection(NAMES_IN_FRENCH[1])

        cls.list_of_id = list_of_id
        # verify that the id product tipped by the user is in list_of_id
        if product_number in list_of_id:
            second_result = cls.select(COLUMN[9], f"{NAME_OF_TABLE[1]} WHERE {COLUMN[4]} = {product_number}")

            # display the name and the nutriscore of the selected product
            for my_product in second_result:
                cls.current_product.append(my_product)
                print(f'\nLe nutriscore de {my_product[1]} est {my_product[4].capitalize()}\n')
            return True
            # il y avait ici un elif pord numbr = 0: cls.display_cat
        else:
            print("Ce chiffre ne correspond pas a un produit de la catégorie que vous avez choisis")
            return False

    @classmethod
    def ready_to_compare(cls):
        res = input("Voulez-vous chercher un produit similaire meilleur pour votre santé?\n"
                    "(Y: oui), (N: retour aux catégories), (Q: quitter): ")

        if res == "Y":
            return True
        elif res == "N":
            return True
        elif res == "Q":
            print("Au revoir!")
            quit()
        else:
            input("Erreur! Touche non valide!")
            return False

    @classmethod
    def compare_product_in_current_category(cls):

        cls.id_name_and_nutriscore_list = []
        my_nutriscore = cls.current_product[0][4].capitalize()

        if my_nutriscore == "A":
            print('\nVous avez déjà un produit qui a un nutriscore de A, impossible de vous proposer quelque-chose de '
                  'mieux!')
            user_choice = input("\n(N: retour aux catégories), (Q: quitter): ")
            if user_choice == "Q":
                quit()
            if user_choice == "N":
                pass
                cls.display_categories()
                # NON FONCTIONNEL (ne reviens pas au debut affiche les cat et se stop une fois la cat selectionnée)

        else:
            for my_product in cls.prod_from_selected_cat:
                result = cls.select((COLUMN[4], COLUMN[0], COLUMN[3]),
                                    f"{NAME_OF_TABLE[1]} WHERE {COLUMN[4]} = {my_product[0]}")
                cls.id_name_and_nutriscore_list.append(result)

            for item in cls.id_name_and_nutriscore_list:
                if item[0][2] == "a":
                    print(f"\nNous vous proposons {item[0][1].capitalize()} comme produit de substitution avec son "
                          f"Nutriscore de {item[0][2].capitalize()}")
                    input("Tapez une touche pour afficher une autre proposition")
                else:
                    print("nous n'avons pas trouvés de résultat satisfaisant dans la catégorie")
                    cls.compare_product_in_affiliated_categories()

    @classmethod
    def compare_product_in_affiliated_categories(cls):  # EN TEST
        # get the products in affiliated categories of the chosen product

        my_id = cls.current_product[0][0]

        print("\nNous allons maintenant rechercher un produit dans les catégories affiliées au produit")

        # search the categories belonging to the product
        prod_and_cat_ids = cls.select((COLUMN[5], COLUMN[8]), f"{NAME_OF_TABLE[6]} WHERE {COLUMN[8]} = {my_id}")

        # clean to keep only the ids of the categories
        affiliated_categories_id = [cat_id[0] for cat_id in prod_and_cat_ids]

        for my_cat_id in affiliated_categories_id:
            prod_from_affiliated_cat = cls.select((COLUMN[8], COLUMN[5]),
                                                  f'{NAME_OF_TABLE[6]} WHERE {COLUMN[5]} = "{my_cat_id}"')
            print(prod_from_affiliated_cat)
            cls.display_products(prod_from_affiliated_cat)
            # essayer de n'afficher que ceux avec un  nutrisocre de A ?
            # abandonner cette methode et tester la recherhce nominative? combiner les deux?
            input("tapez une touche pour continuer")

            # fonctionne bien mais necessite de déplacer le choix de selction du numéro produit dans une methode dédié
            # sinon on est obligé de choisir un produit pour pouvoir ensuite passer a la suite de la boucle

    @classmethod
    def search_with_name(cls):
        # chercher par mot clé similaire
        pass

                # enregistrer automatiquement le résultat final d'une comparaison pour user
                # demander ensuite si la personne souhaite avoir toutes les infos disponibles sur ce produit
                # ou bien effectuer une nouvelle recherche ou quitter
