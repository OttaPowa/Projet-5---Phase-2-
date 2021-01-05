# -*-coding:UTF-8-*

class User:
    instantiated_logs = []

    def __init__(self,
                 args):
        """
            :param: user_name: name of the user
            :type: user_name: str
            :param: password: password of the user
            :type: password: str
        """

        self.user_name = args[0]
        self.password = args[1]
        self.instantiated_logs.append(self)
