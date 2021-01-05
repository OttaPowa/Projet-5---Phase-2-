# -*-coding:UTF-8-*

class Category:
    instantiated_categories = []

    def __init__(self,
                 args):
        """
            Constructor
            :param args[0]: name of the category
            :type args[0]: string
            :param args[1]: url of the category
            :type args[1]: string
        """

        self.name = args[0].replace("'", "''")
        self.url = args[1]
        self.instantiated_categories.append(self)
