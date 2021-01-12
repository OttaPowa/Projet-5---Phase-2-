# -*-coding:UTF-8-*

from Brand import Brand


class Store(Brand):
    instantiated_stores = []

    def __init__(self, args):

        """
            child class of Brand
        """
        Brand.__init__(self, args)
        self.instantiated_stores.append(self)
