# -*-coding:UTF-8-*

import mysql.connector

from constants import*


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
    glob = ""
    action = ""

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

    @staticmethod
    def authentication():
        """
            authentication of the user with they logs
        """

        user_name = input("Tapez votre nom d'utilisateur: ")
        password = input("Tapez votre mot de passe: ")

        if (user_name, password) == test:
            print("\nIdentification réussie")
            return True
        else:
            print("Echec de l'identification")
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
            result_string = f"{str(items[0]).rjust(6, ' ').capitalize()}"
            for index, item in enumerate(items):
                if index == 1:
                    result_string += f" - {str(item).capitalize()}"
                elif index > 1:
                    result_string += f" - {str(item).capitalize()}"
            print(result_string)

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
            display the categories in screen and order them by name.
        """

        result = cls.select((COLUMN[4], COLUMN[0]), f'{NAME_OF_TABLE[0]} ORDER BY name')
        cls.print_result(result)

    @classmethod
    def get_products_from_selected_category(cls):
        """
            get the products id of the selected category
        """
        cls.prod_from_selected_cat = cls.select((COLUMN[8], COLUMN[5]),
                                                f'{NAME_OF_TABLE[6]} WHERE {COLUMN[5]} = "{cls.action}"')

    @classmethod
    def display_products(cls, list_of_products):
        """
            display the products names and ids of the category chosen before
        """

        list_of_id = []
        cls.current_product = []

        cat_name = cls.select((COLUMN[0],), f"{NAME_OF_TABLE[0]} WHERE {COLUMN[4]} = {list_of_products[0][1]}")
        print(f"\nVoici les produits faisant partis de la catégorie {cat_name[0][0].replace(',','').capitalize()}:\n")

        # display product name and id depending of the category id
        for my_product in list_of_products:
            result = cls.select((COLUMN[4], COLUMN[0], COLUMN[3]), f"{NAME_OF_TABLE[1]} WHERE {COLUMN[4]} = {my_product[0]}")

            # store the ids in a list so the list contains all the id product of the chosen category
            for my_id in result:
                list_of_id.append(my_id[0])
            cls.print_result(result)

        cls.list_of_id = list_of_id

    @classmethod
    def display_nutriscore(cls, user_action):
        """
            display the nutriscore of the chosen product
        """

        # verify that the id product tipped by the user is in list_of_id
        if int(user_action) in cls.list_of_id:
            second_result = cls.select(COLUMN[9], f"{NAME_OF_TABLE[1]} WHERE {COLUMN[4]} = {user_action}")

            # display the name and the nutriscore of the selected product
            for my_product in second_result:
                cls.current_product.append(my_product)
                print(f'\nLe nutriscore de {my_product[1]} est {my_product[4].capitalize()}')
        else:
            print("Ce chiffre ne correspond pas a un produit de la catégorie que vous avez choisis")

    @classmethod
    def compare_product_in_current_category(cls):
        """
            compare the product with others from his category, display those that have a nutriscore of A
        """

        cls.id_name_and_nutriscore_list = []
        my_nutriscore = cls.current_product[0][4].capitalize()

        if my_nutriscore == "A":
            print('\nVous avez déjà un produit qui a un nutriscore de A, impossible de vous proposer quelque-chose de '
                  'mieux!')

        else:
            for my_product in cls.prod_from_selected_cat:
                result = cls.select((COLUMN[4], COLUMN[0], COLUMN[3]),
                                    f"{NAME_OF_TABLE[1]} WHERE {COLUMN[4]} = {my_product[0]}")
                cls.id_name_and_nutriscore_list.append(result)

            for item in cls.id_name_and_nutriscore_list:
                if item[0][2] == "a":
                    print(f"\nNous vous proposons {item[0][1].capitalize()} comme produit de substitution avec son "
                          f"Nutriscore de {item[0][2].capitalize()}")
                    cls.ask_to_save_result()

                elif item[0][2] == "b" and (my_nutriscore != "a" and my_nutriscore != "b"):
                    print(f"\nNous vous proposons {item[0][1].capitalize()} comme produit de substitution avec son "
                          f"Nutriscore de {item[0][2].capitalize()}")
                    cls.ask_to_save_result()

                else:
                    pass
            print("\nIl n'y a pas (ou plus) de produit au nutriscore satisfaisant dans cette catégorie.")




    @classmethod
    def compare_product_in_affiliated_categories(cls):
        """
            get and display the products with a nutriscore of A in affiliated categories of the chosen product
        """

        my_id = cls.current_product[0][0]

        print("\nNous allons maintenant rechercher un produit dans les catégories affiliées au produit")

        # search the categories belonging to the product
        prod_and_cat_ids = cls.select((COLUMN[5], COLUMN[8]), f"{NAME_OF_TABLE[6]} WHERE {COLUMN[8]} = {my_id}")

        # clean to keep only the ids of the categories
        affiliated_categories_id = [cat_id[0] for cat_id in prod_and_cat_ids]

        # display product in each affiliated categories
        for my_cat_id in affiliated_categories_id:
            prod_from_affiliated_cat = cls.select((COLUMN[8], COLUMN[5]),
                                                  f'{NAME_OF_TABLE[6]} WHERE {COLUMN[5]} = "{my_cat_id}"')

            cls.display_products(prod_from_affiliated_cat)

            choose_prod = input("\nVoulez vous explorer un produit de cette liste?\n"
                                "(Oui: tapez le numéro du produit), (Entrée: Continuer vers une autre catégorie)"
                                ", (Q: Quitter): ")

            if choose_prod.isdigit():
                cls.display_nutriscore(choose_prod)
                break
            elif choose_prod == "Q":
                quit()
            else:
                pass

    @classmethod
    def show_final_product_details(cls):

        product_details = cls.select((COLUMN[9]), f'{NAME_OF_TABLE[1]} WHERE {COLUMN[4]} = {cls.action}')
        print(f"\nVous trouverez une fiche détaillée sur {product_details[0][1].capitalize()} en suivant le liens:\n"
              f"{product_details[0][2]}")

        stores_id = cls.select((COLUMN[6],), f'{NAME_OF_TABLE[4]} WHERE {COLUMN[8]} = {product_details[0][0]}')

        print("\nLa/les boutiques ou vous trouverez ce produit sont:")
        for my_store_id in stores_id:
            stores_details = cls.select((COLUMN[0],), f'{NAME_OF_TABLE[2]} WHERE {COLUMN[4]} = {my_store_id[0]}')
            cls.print_result(stores_details)

        print("\nla/les marques qui vendent ce produit sont:")
        brands_id = cls.select((COLUMN[7],), f'{NAME_OF_TABLE[5]} WHERE {COLUMN[8]} = {product_details[0][0]}')
        for my_brand_id in brands_id:
            brands_details = cls.select((COLUMN[0],), f'{NAME_OF_TABLE[3]} WHERE {COLUMN[4]} = {my_brand_id[0]}')
            cls.print_result(brands_details)

    @classmethod
    def ask_to_save_result(cls):

        if cls.glob != "save search":

            choice = input("Voulez vous enregister ce résultat de recherche?\n"
                           "(555: oui), (Entrée: afficher le prochain produit)")
            if choice == "555":
                cls.save_search()

            else:
                pass
        else:
            cls.save_search()

    @classmethod
    def save_search(cls):
        print("Sauvegarde de votre recherche")
        "quit()"  # ou demander comme d'hab de quitter ou revenir aux cat
        pass

    @classmethod
    def selection(cls):
        """
            method that manage the user inputs
        """

        value = ""

        if cls.glob == "":
            value = " Tapez (C) pour afficher les catégories: "
        elif cls.glob == "display cat":
            value = " Tapez le numéro de la catégorie que vous souhaitez explorer vous pouvez quitter en tapant (Q): "
        elif cls.glob == "display prod":
            value = " Tapez le numéro du produit que vous souhaitez explorer\n" \
                    " vous pouvez quitter en tapant (Q) et revenir aux catégories en tapant (C): "
        elif cls.glob == "compare prod":
            value = "Voulez-vous chercher un produit similaire meilleur pour votre santé?\n" \
                    "(999: oui), (C: retour aux catégories), (Q: quitter): "
        elif cls.glob == "alternative compare":
            value = "Voulez vous continuer vos recherches dans les autres catégories affiliées au produit?\n" \
                    "(666: oui), (C: retour aux catégories), (Q: quitter): "
        elif cls.glob == "show details":
            value = "Voulez vous voir les détail du produit?\n" \
                    "(Oui: tapez le numéro du produit) (Q: Quitter)): "
        elif cls.glob == "save search":
            value = "Voulez vous sauvegarder ce produit et les données s'y rapportant?\n " \
                    "(000: Oui, (C: retour aux catégories), (Q: quitter): )"

        number = input(f"\n{value}")
        return number

    # enregistrer automatiquement le résultat final d'une comparaison pour user
    # demander ensuite si la personne souhaite avoir toutes les infos disponibles sur ce produit
    # ou bien effectuer une nouvelle recherche ou quitter