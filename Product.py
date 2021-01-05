# -*-coding:UTF-8-*

class Product:
    instantiated_products = []

    def __init__(self,
                 args):
        """
            Constructor
            :param args[0]: name of the product
            :type args[0]: string
            :param args[1]: url of the product
            :type args[1]: string
            :param args[2]: url of the picture of the product
            :type args[2]: string
            :param args[3]: brand of the product
            :type args[3]: string
            :param args[4]: stores were the product can be bought
            :type args[4]: string
            :param args[5]: nutriscore of the product
            :type args[5]: string
            :param args[6]: categories of the product
            :type args[6]: string
        """

        self.name = args[0]
        self.url = args[1]
        self.picture_url = args[2]
        self.brand = args[3]
        self.store = args[4]
        self.nutriscore = args[5]
        self.category = args[6]
        self.instantiated_products.append(self)
