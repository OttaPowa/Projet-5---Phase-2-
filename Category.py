# -*-coding:UTF-8-*


class Category:
    instantiated_categories = []

    def __init__(self,
                 args):
        """
            Constructor
            :param arg1: name of the category
            :type arg1: string
            :param arg2: url of the category
            :type arg2: string
        """

        self.name = args[0].replace("'", "''")
        self.url = args[1]
        self.instantiated_categories.append(self)
