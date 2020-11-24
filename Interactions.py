# -*-coding:UTF-8-*

from constants import*


class Interactions:

    @staticmethod
    def authentication():

        user_name = input("Tapez votre nom d'utilisateur: ")
        password = input("Tapez votre mot de passe: ")

        if (user_name, password) == test:
            print("\nIdentification réussie\n")
        else:
            print("Echec de l'identification")
            return False

    @staticmethod
    def selection(name_of_search_field):

        stat = True

        while stat:
            try:
                numbr = int(input(f"\nTapez le numéro {name_of_search_field} que vous souhaitez explorer: "))
                return numbr
            except ValueError:
                print("\nentrez un nombre s'il vous plait!")
                continue

