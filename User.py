# -*-coding:UTF-8-*


class User:
    user_log_list = []

    def __init__(self,
                 user_name,
                 password):
        """
            :param: name of the user
            :type: str
            :param: password of the user
            :type: str
        """

        self.user_name = user_name
        self.password = password
