# -*-coding:UTF-8-*


class Product:
    instantiated_products = []

    def __init__(self,
                 args):
        """
            Constructor
            :param arg1: name of the product
            :type arg1: string
            :param arg2: url of the product
            :type arg2: string
            :param arg3: url of the picture of the product
            :type arg3: string
            :param arg4: brand of the product
            :type arg4: string
            :param arg5: stores were the product can be bought
            :type arg5: string
            :param arg6: nutriscore of the product
            :type arg6: string
            :param arg7: categories of the product
            :type arg7: string
        """

        self.name = args[0]
        self.url = args[1]
        self.picture_url = args[2]
        self.brand = args[3]
        self.store = args[4]
        self.nutriscore = args[5]
        self.category = args[6]
        self.instantiated_products.append(self)
