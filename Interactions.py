# -*-coding:UTF-8-*

from constants import*


class Interactions:

    @staticmethod
    def authentication():

        user_name = input("Tapez votre nom d'utilisateur: ")
        password = input("Tapez votre mot de passe: ")

        if (user_name, password) == test:
            print("\nIdentification réussie\n")
            return True
        else:
            print("Echec de l'identification")
            return False

    @staticmethod
    def selection(name_of_search_field):

        stat = True

        while stat:
            try:
                numbr = int(input(f"\nTapez le numéro {name_of_search_field} que vous souhaitez explorer: "))
                if numbr == 0:
                    return False
                else:
                    return numbr
            except ValueError:
                print("\nentrez un nombre s'il vous plait!")
                continue

    @staticmethod
    def quit_or_go_back():

        command = input()

        while command != 0 or 999:
            continue
        else:
            if command == 0:
                pass
                # ManageDb.display_category()
            elif command == 999:
                quit()
