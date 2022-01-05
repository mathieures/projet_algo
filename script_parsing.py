import re

# class


def remove_b_tags(string):
    """
        Fonction qui enlève les balises <b> ainsi que leur contenu
    """
    string = re.sub("<b>.*?</b>", "", string)
    return string


def remove_tags(string):
    """Enlève les balises de la chaîne passée en paramètre"""
    string = re.sub("<.+?>|</.+?>", "", string)
    return string


def parse_script(script_str):
    reg = re.compile("\w+")
    # Des mots qui ne sont pas des balises, on récupère seulement les lettres
    word_list = [reg.search(word)[0].lower()  # [0] : tout ce qui a match
                 for word in remove_tags(script_str).split()
                 if reg.search(word) is not None]

    # Compte le nombre d'occurrences de chaque mot dans la liste
    occurrences = {word: word_list.count(word) for word in word_list}
    return occurrences


def main():
    script_str = "<b><i>Hello</i></b>, mister <i>villain</i>.\n<b>Welcome to my <i>kingdom</i>, my kingdom come.</b>"
    print(f"Base string: {script_str}\n")
    string = remove_b_tags(script_str)
    print(f"After b tags removal : {string}")
    string = remove_tags(string)
    print(f"After all tags removal : {string}")
    print(f"Occurrences: {parse_script(string)}")


if __name__ == '__main__':
    main()
