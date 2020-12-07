# -*-coding:UTF-8-*


class User:
    user_log_list = []

    def __init__(self,
                 user_name,
                 password):
        """
            :param: user_name: name of the user
            :type: user_name: str
            :param: password: password of the user
            :type: password: str
        """

        self.user_name = user_name
        self.password = password
