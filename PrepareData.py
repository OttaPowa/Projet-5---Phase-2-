# -*-coding:UTF-8-*

import requests


class PrepareData:
    """
        this class prepare all the data to be exploited
    """

    # class instances
    cleaned_categories = []
    raw_products = []
    cleaned_products = []
    setted_items = []
    cleaned_cat_with_url = []

    # request to the OpenFoodFacts API to get the categories
    request = requests.get("https://fr.openfoodfacts.org/categories.json")
    result = request.json()

    @classmethod
    def get_categories(cls):
        """
            get the data by the API
        """
        cleaned_categories = []
        min_product = 200  # minimum number of product contained in the category
        max_product = 210  # maximum number of product contained in the category

        print("\nRécupération des catégories via l'API Open Food Fact...\n")

        # loop on the keys of the request
        for key in cls.result:
            if key == "count":
                print(f'Récupération terminée. {cls.result["count"]} catégories récupérées.\n')

        # loop on the categories to get those that contains only the number of product defined in the min/max_product
        for categories in cls.result["tags"]:
            if min_product <= categories["products"] <= max_product:
                cleaned_categories.append((categories["name"], categories["url"]))

        # set the local list to class instance
        cls.cleaned_categories = cleaned_categories
        print("veuillez patienter lors du tri des données, celui-ci peut prendre un peu de temps... ")

    @classmethod
    def get_and_sort_products(cls):
        """
            get the products by the API and clean the obtained data
        """

        position_in_cat_list = 0    # counter to change the url in the instantiated_categories
        page_nbr = 1    # counter to go forward in the pages of the products
        del_el = 0    # elements ignored because of a missing key corresponding to a needed data
        cat_nbr = 0    # counter to display the final number of products contained in each category
        uncleaned_products = []
        empty_slot = 0  # counter of dat containing an empty slot (these data are data are ignored)

        # loop on the list of categories
        for cat in cls.cleaned_categories:
            temp_prod = []  # temporary list of product for the current category
            https = cls.cleaned_categories[position_in_cat_list][1]  # url
            request = requests.get(f'{https}.json/{page_nbr}')  # request
            result = request.json()  # result of the request

            # switch pages in the json file
            if len(result["products"]) > 0:
                page_nbr += 1

                # append the product that contains all the needed data and ignore the rest
                for prod in result["products"]:
                    try:
                        temp_prod.append((prod["product_name_fr"], prod["url"], prod["image_url"], prod["brands"],
                                          prod["stores"], prod["nutrition_grades"], prod["categories"]))

                    # increment the deleted element counter
                    except KeyError:
                        del_el += 1
                        pass
            # reset the json file to page 1
            else:
                page_nbr = 1

            uncleaned_products.append(temp_prod)  # append the list with raw products
            position_in_cat_list += 1  # increment the counter the get the url

        # print the number of products got in the current category (the name of the category is the argument 0)
        for each in uncleaned_products:
            # increment the counter of categories
            cat_nbr += 1

        # add in the list the raw products that contains all the needed data and ignore the rest
        for my_list in uncleaned_products:
            for my_product in my_list:

                if my_product[0] == "" or my_product[1] == "" or my_product[2] == "" or my_product[3] == "" or \
                        my_product[4] == "" or my_product[5] == "" or my_product[6] == "":
                    empty_slot += 1
                    pass
                else:
                    cls.raw_products.append(my_product)

    @classmethod
    def calibrate(cls, list_of_data):
        """
             calibrate the data with lower case, strip and replace methods to make them ready to compare and eliminate
             multiple occurrences
        """
        temp_list = []

        # lower case the list
        lowercase_items = [(arg1.lower(), arg2.lower(), arg3.lower(), arg4.lower(), arg5.lower(), arg6.lower(),
                            arg7.lower()) for arg1, arg2, arg3, arg4, arg5, arg6, arg7 in list_of_data]

        # strip the lower cased list
        stripped_items = [(arg1.strip(), arg2.strip(), arg3.strip(), arg4.strip(), arg5.strip(), arg6.strip(),
                           arg7.strip()) for arg1, arg2, arg3, arg4, arg5, arg6, arg7 in lowercase_items]

        # replace dots in the striped list
        dot_replaced_items = [(arg1.replace(".", ""), arg2, arg3, arg4.replace(".", ""),
                               arg5.replace(".", ""), arg6.replace(".", ""), arg7.replace(".", ""))
                              for arg1, arg2, arg3, arg4, arg5, arg6, arg7 in stripped_items]

        # slip the quotation marks in the dot replaced list
        slip_quotation_marks = [(arg1.replace("'", "''"), arg2, arg3, arg4.replace("'", "''"),
                                 arg5.replace("'", "''"), arg6.replace("'", "''"), arg7.replace("'", "''"))
                                for arg1, arg2, arg3, arg4, arg5, arg6, arg7 in dot_replaced_items]

        # ignore the first empty item
        for i in slip_quotation_marks:
            if i != " ":
                temp_list.append(i)

        cls.cleaned_products = temp_list

    @classmethod
    def split_and_set(cls, items_list):
        """
            split and set the items regardless the len of the list
        """
        temp_all = []
        final_temp = []
        cls.setted_items = []

        # split item to get all the data
        for item in items_list:
            list_of_splited_items = item.split(",")
            for nbr in range(len(list_of_splited_items)):
                for data in list_of_splited_items:
                    temp = data.split(",")
                    temp_all.append(temp)

        # set the list to delete multiple occurrences
        for my_items in temp_all:
            for item in my_items:
                final_temp.append(item.strip())
        ready_to_append = list(set(final_temp))

        # append the cleaned items in the list
        for item in ready_to_append:
            cls.setted_items.append([item])

    @classmethod
    def get_url(cls, list_of_names):
        """
            make a request to get the url depending of the name
        """
        cap_list = []
        replaced_list = []

        # capitalize the str for a more accurate comparison
        for lone_list in list_of_names:
            for content in lone_list:
                cap_list.append(content.capitalize())

        # replace '' by ' for a more accurate comparison
        for i in cap_list:
            replaced_list.append(i.replace("''", "'"))

        # compare the names in replaced_list with the list of categories in the json file to get the corresponding url
        for name in replaced_list:
            for cat in cls.result["tags"]:
                if cat["name"] == name:
                    cls.cleaned_cat_with_url.append((name.lower(), cat["url"]))

    @classmethod
    def instantiate(cls, class_name, list_to_instantiate):
        """
            instantiate method used for all every instantiations
        """
        for item in list_to_instantiate:
            class_name(item)
