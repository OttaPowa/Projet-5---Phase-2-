# -*-coding:UTF-8-*

import mysql.connector

from PrepareData import PrepareData
from User import User
from Saving import Saving


class ManageDb:
    """
        This class manage the interactions with the database
    """

    # MySQL variables
    connexion = ""
    cursor = ""

    # user logs
    my_current_user_name = ""  # store the current user_name
    user_id = []  # store the current user_id
    list_of_user_id = []  # list of the ids of all the users (to verify if the current user already exists)

    # main variables used by all the program
    glob = ""  # variable to locate where we are in the process of application
    action = ""  # input of the user

    # variables used in different methods
    list_of_id = []  # list of the product ids (used to check if the tipped id is inside the current category
    my_category_id = ""  # get the current category id
    current_product = []  # current selected product

    # variables used for the instantiation leading to saving
    base_product = ""  # id of the original product chosen by the user
    alternative_product = ""  # id of the final product chosen by the user
    original_and_alternative_prod_ids = []  # list of the ids of the base product and the final product

    @staticmethod
    def verify_prerequisite():
        """
            verify if MySQL is installed on the client computer. if not print a message with à link to DL it.
        """

        print("\nBonjour, MySQL est nécéssaire pour faire fonctionner l'application."
              "\nVous pouvez l'installer en suivant ce lien: https://dev.mysql.com/downloads/mysql/#downloads\n")

        user_input = input("Si vous possèdez un compte tapez 'Y' "
                           "sinon tapez une touche pour quitter: ")

        if user_input == "Y" or user_input == "y":
            pass
        else:
            quit()

    @classmethod
    def mysql_connection(cls):

        user_name = input("MySql user name: ")
        password = input("Mysql password: ")
        my_logs = [(user_name, password)]

        try:
            cls.connexion = mysql.connector.connect(user=user_name, password=password)
            cls.cursor = cls.connexion.cursor()

            # instantiate logs into class User
            PrepareData.instantiate(User, my_logs)
            cls.my_current_user_name = user_name
            return True

        except mysql.connector.errors.ProgrammingError:
            print("\nEchec de l'authentification auprès de MySql")
            return False

    @classmethod
    def ask_to_update_database(cls):
        """
            ask the user if they want to use the old database
        """

        question = input("\nVoulez mettre à jour la base de donnée? ATTENTION: ceci supprimera vos sauvegardes!\n"
                         "(Y): oui, (N): non: ")

        if question == "Y" or question == "y":
            cls.cursor.execute("USE projet5")
            return True
        elif question == "N" or question == "n":
            cls.cursor.execute("USE projet5")
            return False

    @ classmethod
    def access_to_stored_data(cls):
        """
            allow the user to access their previous saves data if exists
        """

        user_id = cls.user_id[0][0]
        question = input("\nVoir vos recherches sauvegardées?\n (Y): oui, (N): non: ")

        if question == "Y" or question == "y":
            base_prod = f"saving " \
                        f"INNER JOIN product AS product1 ON product1.id = saving.base_product_id " \
                        f"INNER JOIN product AS product2 ON product2.id = saving.alternative_product_id " \
                        f"WHERE saving.user_id = {user_id}"
            result_bp = cls.select(("product1.id", "product1.name", "product1.nutriscore",
                                    "product2.id", "product2.name", "product2.nutriscore"), base_prod)

            if result_bp == []:
                print("Aucune donnée sauvegardé n'a été trouvé pour votre utilisateur")
            else:
                print("Vous aviez trouvé :")
                for index, result in enumerate(result_bp):
                    print(f"    {index + 1}) {result[1]} au nutriscore de {result[2].capitalize()} "
                          f"comme alternative à {result[4]} et son nutriscore de {result[5].capitalize()}")
                input("Tapez une touche pour continuer")

        elif question == "N" or question == "n":
            pass

    @classmethod
    def build(cls):
        """
            build the MySQL tables
        """

        print("Contruction de la base de données...")

        data_base_sql = """
                        
                        DROP TABLE IF EXISTS product_store;
                        DROP TABLE IF EXISTS product_brand;
                        DROP TABLE IF EXISTS product_category;
                        DROP TABLE IF EXISTS category;
                        DROP TABLE IF EXISTS saving;
                        DROP TABLE IF EXISTS product;
                        DROP TABLE IF EXISTS store;
                        DROP TABLE IF EXISTS brand;
                        DROP TABLE IF EXISTS user;
                        DROP DATABASE IF EXISTS projet5;
                        
                        CREATE DATABASE projet5;
                        USE projet5;
                        
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
                            
                        CREATE TABLE user (
                            id int NOT NULL AUTO_INCREMENT,
                            user_name varchar(200) DEFAULT NULL,
                            password varchar(200) DEFAULT NULL,
                            PRIMARY KEY(id))
                            ENGINE=InnoDB;
                            
                        CREATE TABLE saving (
                            id int NOT NULL AUTO_INCREMENT,
                            base_product_id int DEFAULT NULL,
                            alternative_product_id int DEFAULT NULL,
                            user_id int DEFAULT NULL,
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
                            
                        CREATE UNIQUE INDEX user_logs_UI
                            ON user (user_name, password);
                            
                        ALTER TABLE product_category ADD CONSTRAINT product_category_FK 
                            FOREIGN KEY (id_product) REFERENCES product(id);
                            
                        ALTER TABLE product_category ADD CONSTRAINT product_category_FK_1 
                            FOREIGN KEY (id_category) REFERENCES category(id);    
                            
                        ALTER TABLE product_brand ADD CONSTRAINT product_brand_FK 
                            FOREIGN KEY (id_brand) REFERENCES brand(id);
                            
                        ALTER TABLE product_brand ADD CONSTRAINT product_brand_FK_1 
                            FOREIGN KEY (id_product) REFERENCES product(id);
                            
                        ALTER TABLE product_store ADD CONSTRAINT product_store_FK 
                            FOREIGN KEY (id_store) REFERENCES store(id);
                            
                        ALTER TABLE product_store ADD CONSTRAINT product_store_FK_1 
                            FOREIGN KEY (id_product) REFERENCES product(id);
                            
                        ALTER TABLE saving ADD CONSTRAINT saving_FK 
                            FOREIGN KEY (user_id) REFERENCES user(id);
                            
                        ALTER TABLE saving ADD CONSTRAINT saving_FK_1
                            FOREIGN KEY (base_product_id) REFERENCES product(id);
                            
                        ALTER TABLE saving ADD CONSTRAINT saving_FK_2
                            FOREIGN KEY (alternative_product_id) REFERENCES product(id);
                                
                        """

        # apply multi true to execute sql actions in chain
        for result in cls.cursor.execute(data_base_sql, multi=True):
            pass

        cls.connexion.commit()
        print("La base de données à été crée.")

    @classmethod
    def insert_logs_and_get_id(cls):
        """
            insert the user logs in the user table and get the id generated
        """

        # insert instantiated logs into the user table
        for item in User.instantiated_logs:
            cls.cursor.execute("INSERT IGNORE INTO user (user_name, password) VALUES (%s, %s)",
                               (item.user_name, item.password))
        # get the id
        cls.user_id = cls.select(("id",), f'user WHERE user_name = "{cls.my_current_user_name}"')
        cls.list_of_user_id = cls.select(("id",), 'user')

        cls.connexion.commit()

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

        result = cls.select(("id", "name"), "category ORDER BY name")
        cls.print_result(result)

    @classmethod
    def display_products(cls, my_category):
        """
            display the products names and ids of the category chosen before
        """

        # get the product id, name and nutriscore depending of the category id
        my_products_query = f"product INNER JOIN product_category ON product.id = product_category.id_product " \
                            f"INNER JOIN category ON category.id = product_category.id_category " \
                            f"WHERE category.id = {my_category}"
        prods_id_name_nutriscore = cls.select(("product.id", "product.name", "product.nutriscore"), my_products_query)

        # get the category name
        cat_name = cls.select(("category.name",), f"category WHERE category.id = {my_category}")
        print(f"\nVoici les produits de la catégorie {cat_name[0][0].capitalize()}:\n")

        # print the list of products using the class method
        cls.print_result(prods_id_name_nutriscore)

        # set the current category id
        cls.my_category_id = my_category

        # set the ids of the products to compare with user interactions
        list_of_id = [prod_id[0] for prod_id in prods_id_name_nutriscore]
        cls.list_of_id = list_of_id

    @classmethod
    def display_nutriscore(cls, user_action):
        """
            display the nutriscore of the chosen product
        """

        # verify that the id product tipped by the user is in list_of_id
        if int(user_action) in cls.list_of_id:
            # select every data of the current product for incoming usages
            result = cls.select("*", f"product WHERE id = {user_action}")

            # display the name and the nutriscore of the selected product
            for my_product in result:
                cls.current_product.append(my_product)
                print(f'\nLe nutriscore de {my_product[1]} est {my_product[4].capitalize()}')
        else:
            print("Ce chiffre ne correspond pas a un produit de la catégorie que vous avez choisis")

    @classmethod
    def compare_product_in_current_category(cls):
        """
            compare the product with others from his category, display those that have the higher nutriscore
        """

        current_nutriscore = cls.current_product[0][4].capitalize()  # set the current nutriscore
        current_id = cls.current_product[0][0]  # set the current id

        if current_nutriscore == "A" or current_nutriscore == "a":
            print('\nVous avez déjà un produit qui a un nutriscore de A, impossible de vous proposer quelque-chose de '
                  'mieux!')

        else:
            # get the products id, name and nutriscore in the current category
            query = f"product INNER JOIN product_category ON product.id = product_category.id_product " \
                   f"INNER JOIN category on product_category.id_category = category.id " \
                   f"WHERE category.id = {cls.my_category_id} ORDER BY nutriscore"
            prods_from_mother_cat = cls.select(("product.id", "product.name", "product.nutriscore"), query)

            # display the product with the higher nutriscore til reach the nutriscore of the current product
            for my_product in prods_from_mother_cat:
                if my_product[2].capitalize() < current_nutriscore and my_product[0] != current_id:
                    print(f"\nNous vous proposons {my_product[1].capitalize()} comme produit de substitution avec son "
                          f"Nutriscore de {my_product[2].capitalize()}.")

                    # query the user. invoke the next method in line and break the loop
                    choice = input("\nVoulez vous voir les détails de ce produit?\n(Y): Oui, (N): Non: ")
                    if choice == "y" or choice == "Y":
                        cls.show_final_product_details(my_product[0])
                        break
                    else:
                        pass
                else:
                    pass

    @classmethod
    def compare_product_in_affiliated_categories(cls, product_id):
        """
            get and display the products with a nutriscore of A in affiliated categories of the chosen product
        """

        print("\nNous allons maintenant rechercher un produit dans les catégories affiliées au produit...")

        # get the categories ids affiliated to the product_id
        query_cat_id_and_name = f"category INNER JOIN product_category ON category.id = product_category.id_category " \
                                f"WHERE product_category.id_product = {product_id}"
        categories_ids = cls.select(("category.id",), query_cat_id_and_name)

        # display products in each affiliated categories
        for my_cat_id in categories_ids:
            cls.display_products(my_cat_id[0])

            choose_prod = input("\nVoulez vous explorer un produit de cette liste?\n"
                                "(Oui: tapez le numéro du produit), (Entrée: Continuer vers une autre catégorie)"
                                ", (Q: Quitter): ")

            # break the loop and launch class method display_nutriscore if the user enter a product number
            if choose_prod.isdigit():
                cls.display_nutriscore(choose_prod)
                break
            elif choose_prod == "Q" or choose_prod == "q":
                quit()
            else:
                pass

        print("\nDésolé mais vous avez épuisé tous les produits de toutes les  catégories affiliées...\n")

    @classmethod
    def show_final_product_details(cls, product_id):
        """
            show the details of the chosen alternative product
        """

        # get and display the Open Food Facts url of the product
        product_details = cls.select("*", f'product WHERE id = {product_id}')
        print(f"\nVous trouverez une fiche détaillée sur {product_details[0][1].capitalize()} en suivant le lien:\n"
              f"  - {product_details[0][2]}")

        # get the stores of the product
        query_store = f"store INNER JOIN product_store ON store.id = product_store.id_store " \
                      f"INNER JOIN product ON product.id = product_store.id_product " \
                      f"WHERE product.id = {product_id}"
        stores = cls.select(("store.name",), query_store)

        # display the stores name
        print("\nVous trouverez ce produit chez:")
        for store in stores:
            print(f"  - {store[0].capitalize()}")

        # get the brands of the product
        query_brand = f"brand INNER JOIN product_brand ON brand.id = product_brand.id_brand " \
                      f"INNER JOIN product ON product.id = product_brand.id_product " \
                      f"WHERE product.id = {product_id}"
        brands = cls.select(("brand.name",), query_brand)

        # display the brands name
        print("\nCe produit est vendu sous la(les) marque(s):")
        for brand in brands:
            print(f"  - {brand[0].capitalize()}")

        cls.alternative_product = product_details[0][0]
        cls.glob = "save search"

    @classmethod
    def ask_to_save_result(cls):
        """
            asks the user if they want to save the current product
        """

        if cls.glob != "save search":
            choice = input("\nVoulez vous enregister ce résultat de recherche?\n"
                           "(Y): oui, (Entrée): afficher le prochain produit, (Q): quitter:  ")

            # store the base product id and the final product id to instantiate later
            if choice == "Y" or choice == "y":
                cls.original_and_alternative_prod_ids = [(cls.base_product, cls.alternative_product)]
                cls.save_search()
            elif choice == "Q" or choice == "q":
                quit()
            else:
                pass
        else:
            cls.original_and_alternative_prod_ids = [(cls.base_product, cls.alternative_product)]
            cls.save_search()

    @classmethod
    def save_search(cls):
        """
            save the base product id and the alternative product id into the table saving.
            Then link tables user and saving into user_saving to associate user and data.
        """

        print("Sauvegarde de votre recherche...")

        # instantiate base_product_id and alternative_product_id into class Saving
        PrepareData.instantiate(Saving, cls.original_and_alternative_prod_ids)

        # insert instantiated data into the saving table
        for item in Saving.instantiated_saving:
            cls.cursor.execute("INSERT INTO saving (base_product_id, alternative_product_id, user_id) "
                               "VALUES (%s, %s, %s)", (item.base_product_id, item.alternative_product_id,
                                                       cls.user_id[0][0]))

        cls.connexion.commit()
        print("Vos produit ont bien été enregistrés.")

    @classmethod
    def selection(cls):
        """
            method that manage the user inputs
        """

        value = ""

        if cls.glob == "":
            value = "Tapez (C) pour afficher les catégories: "
        elif cls.glob == "display cat":
            value = "Tapez le numéro de la catégorie que vous souhaitez explorer vous pouvez quitter en tapant (Q): "
        elif cls.glob == "display prod":
            value = "Tapez le numéro du produit que vous souhaitez explorer\n" \
                    "vous pouvez quitter en tapant (Q) et revenir aux catégories en tapant (C): "
        elif cls.glob == "compare prod":
            value = "Voulez-vous chercher un produit similaire avec un meilleur nutriscore?\n" \
                    "(Y): oui, (C): retour aux catégories, (Q): quitter: "
        elif cls.glob == "alternative compare":
            value = "Il n'y a pas ou plus de produit au nutriscore supérieur dans la catégorie actuelle. " \
                    "Chercher dans d'autres catégories?\n" \
                    "(Y): oui, (S): ce produit me convient, (C): retour aux catégories, (Q): quitter: "
        elif cls.glob == "show details":
            value = "Voulez vous voir les détail du produit?\n" \
                    "(tapez le numéro du produit): Oui, (C): retour aux catégories (Q): Quitter: "
        elif cls.glob == "save search":
            value = "Voulez vous sauvegarder ce produit et les données s'y rapportant?\n" \
                    "(Y): Oui, (C): retour aux catégories, (Q): quitter: "
        elif cls.glob == "end cycle":
            value = "(C): revenir aux catégories ou (Q): quitter: "

        number = input(f"\n{value}")
        return number
