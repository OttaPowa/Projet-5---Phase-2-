# -*-coding:UTF-8-*

from constants import*


class Interactions:
    """
        this class manage the interactions with the user
    """

    @staticmethod
    def authentication():

        user_name = input("Tapez votre nom d'utilisateur: ")
        password = input("Tapez votre mot de passe: ")

        if (user_name, password) == test:
            print("\nIdentification réussie\n")
            input("tapez sur une touche pour continuer et afficher les catégories")
            return True
        else:
            print("Echec de l'identification")
            return False

    @staticmethod
    def selection(name_of_search_field):

        stat = True

        while stat:
            try:
                number = int(input(f"\nTapez le numéro {name_of_search_field} que vous souhaitez explorer: "))
                if number == 0:
                    return False
                else:
                    return number
            except ValueError:
                print("\nentrez un nombre s'il vous plait!")
                continue

    @staticmethod  # pas utile pour le moment
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
