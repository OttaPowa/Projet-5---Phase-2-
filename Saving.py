# -*-coding:UTF-8-*

class Saving:
    instantiated_saving = []

    def __init__(self,
                 args):
        """
            :param: base_product_id: id of the base product
            :type: base_product_id: int
            :param: alternative_product_id: id of the final alternative chosen by the user
            :type: alternative_product_id: int
        """

        self.base_product_id = args[0]
        self.alternative_product_id = args[1]
        self.instantiated_saving.append(self)
