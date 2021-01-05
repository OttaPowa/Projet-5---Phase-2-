# -*-coding:UTF-8-*

class Brand:
    instantiated_brands = []

    def __init__(self,
                 args):
        """
            Constructor
            :param args[0]: name of the product
            :type args[0]: string
        """

        self.name = args[0]
        self.instantiated_brands.append(self)
