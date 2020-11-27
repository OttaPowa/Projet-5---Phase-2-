# -*-coding:UTF-8-*

import mysql.connector

from constants import*
from Interactions import Interactions


class ManageDb:
    """
        This class manage the interactions with the database
    """

    connexion = mysql.connector.connect(user="root", password="Donn1eDark0", database="projet5")
    cursor = connexion.cursor()

    SQL_CAT_INSERT = """INSERT INTO category (name,url) VALUES (%(name)s, %(url)s)"""
    list_of_prod_id = []
    prod_from_selected_cat = ()

    @classmethod
    def verify_prerequisite(cls):
        """
            verify if MySQL is installed on the client computer. if not print a message with à link to DL it.
        """

    @classmethod
    def build(cls):
        """
            build the MySQL database
        """
        print("Contruction de la base de données...")

        DATA_BASE_SQL = """
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
                        """

        for result in cls.cursor.execute(DATA_BASE_SQL, multi=True):
            pass

        cls.connexion.commit()
        print("La base de données à été crée.")

    @classmethod
    def delete(cls, name_of_table):
        """
            delete database, table, line or column
        """
        cls.cursor.execute(f"DROP TABLE {name_of_table}")

    @classmethod
    def show_tables(cls):
        """
        update the database data...

        """
        cls.cursor.execute("SHOW TABLES")
        for lines in cls.cursor:
            print(lines)

    @classmethod
    def select(cls, what_to_select, name_of_table):
        """
            select function in SQL
        """
        #  a modifier!, codé en dur ne fonctione que pour une seule ou deux colones pas plus
        """for i in range(len(what_to_select)):
            j = i + 1"""
        """
        if what_to_select is tuple:
            for x in enumerate(len(what_to_select)):
                cls.cursor.execute(f"SELECT {what_to_select[0]},{what_to_select[1]} FROM {name_of_table}")"""
        cls.list_of_prod_id = []

        sql_sentence = ""

        try:
            sql_sentence = f"SELECT {what_to_select} FROM {name_of_table}"

        except:
            sql_sentence = f"SELECT {what_to_select[0]},{what_to_select[1]} FROM {name_of_table}"

        print(sql_sentence)
        cls.cursor.execute(sql_sentence)
        rows = cls.cursor.fetchall()
        return rows

    @classmethod
    def print_result(cls, results):

        for items in results:
            cls.list_of_prod_id.append(items)
            print(items)


    @classmethod
    def fill(cls, insert_statement, list_of_items):
        """
            fill the database with the transformed API data
        """

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
            Préparation et insertion des données dans les bases (n-n)
        """
        cat_unfounded = []

        for product in instantiated_list:

            my_list_of_product_id = []
            my_product_id = ()
            my_item_id = ()

            query_product_id = f'SELECT id FROM {name_of_table1} WHERE name = "{product.name}"'
            print(query_product_id)
            cls.cursor.execute(query_product_id)

            for row in cls.cursor:
                my_product_id = row
                my_list_of_product_id.append(my_product_id)

                print(my_product_id)


            for my_prod_id in my_list_of_product_id:

                list_of_splited_items = []

                if name_of_table2 == 'store':
                    list_of_splited_stores = product.store.split(",")
                    list_of_splited_items = list_of_splited_stores
                elif name_of_table2 == 'brand':
                    list_of_splited_brands = product.brand.split(",")
                    list_of_splited_items = list_of_splited_brands
                elif name_of_table2 == 'category':
                    list_of_splited_categories = product.category.split(",")
                    list_of_splited_items = list_of_splited_categories
                else:
                    print("Erreur dans le nom de l'argument")

                splited_items = []
                splited_and_striped_item = []

                for my_length in range(len(list_of_splited_items)):
                    for item in list_of_splited_items:
                        temp = item.split(",")
                        splited_items.append(temp)

                for item_list in splited_items:
                    for item in item_list:
                        splited_and_striped_item.append(item.strip())
                cleaned_list_of_items = list(set(splited_and_striped_item))
                print(cleaned_list_of_items)

                for item in cleaned_list_of_items: # cleaned list of stores, brands or categories

                    query_item_id = f'SELECT id FROM {name_of_table2} WHERE name = "{item}"'
                    print(query_item_id)
                    cls.cursor.execute(query_item_id)
                    my_item_id = () # actualise la variable pour éviter d'injecter les catégories non trouvé par l'API qui étient remplacé par es données précede,tes

                    for line in cls.cursor:
                        my_item_id = line
                        print(my_item_id)

                    try:
                        query_insert = f"INSERT INTO {name_of_table3} ({column1}, {column2}) VALUES (%s, %s)"
                        print(query_insert)
                        print(my_prod_id[0], my_item_id[0])
                        cls.cursor.execute(query_insert, (my_prod_id[0], my_item_id[0]))

                    except IndexError:  # some indexerror occures when a name in another language is found (english or german mostly)
                        cat_unfounded.append(my_product_id)
                        continue

            print(cat_unfounded)
        cls.connexion.commit()

    @classmethod
    def display_categories(cls):

        result = cls.select((COLUMN[4], COLUMN[0]), f'{NAME_OF_TABLE[0]} ORDER BY name')
        cls.print_result(result)

        cat_nbr = Interactions.selection(NAMES_IN_FRENCH[0])
        cls.prod_from_selected_cat = cls.select((COLUMN[8], COLUMN[5]), f'{NAME_OF_TABLE[6]} WHERE {COLUMN[5]} = "{cat_nbr}"')


    @classmethod
    def display_products(cls):

        print('\nVoici les produits faisant partis de cette catégorie:\n'
              'Vous pouvez retourner aux catégories en tapant 0\n')

        for my_product in cls.prod_from_selected_cat:  # display product name and id depending of the category id
            result = cls.select((COLUMN[4], COLUMN[0]), f"{NAME_OF_TABLE[1]} WHERE {COLUMN[4]} = {my_product[0]}")
            cls.print_result(result)

        prod_nbr = Interactions.selection(NAMES_IN_FRENCH[1])

        if prod_nbr == 0:
            cls.display_categories()
        else:
            res = cls.select(COLUMN[9], f"{NAME_OF_TABLE[1]} WHERE {COLUMN[4]} = {prod_nbr}")

            for my_product in res:  # display the name and the nutriscore of the selected product
                print(f'\nLe nutriscore de {my_product[1]} est {my_product[4].capitalize()}')

        # EN TEST : condition pour ne pas pouvoir entrer un chiffre autre que ceux de la list_of_prod_id
        list_of_id = []
        for id in cls.list_of_prod_id:
            list_of_id.append(id[0])
            print("Ce chiffre ne correspond pas  a un produit de la catégorie que vous avez choisis")


    @classmethod
    def compare_products(cls):
        my_nutriscore = cls.list_of_prod_id[4]

        # recupérer la cat selectionner et les products pour effectuer la recherche (return? ou variable?)
        # mettre cat_nbr en cls pour utilser la catégorie pour effectuer les recherches de comparaison
        # faire pareil avec prod_nbr pour comparer a partir du nom de produit si aucun autre produit dans la cat selectionnée

        if my_nutriscore == "A" or "a":
            print('Vous avez déjà un produit qui a un nutriscore de A, impossible de vous proposer quelquechose de '
                  'mieux!')
        elif my_nutriscore == "B" or "b":
            pass
        elif my_nutriscore == "C" or "c":
            pass
        else:
            pass