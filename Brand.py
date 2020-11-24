# -*-coding:UTF-8-*


class Brand:
    instantiated_brands = []

    def __init__(self,
                 args):
        """
            Constructor
            :param arg1: name of the product
            :type arg1: string
        """

        self.name = args[0]
        self.instantiated_brands.append(self)