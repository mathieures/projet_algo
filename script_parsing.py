import re


def _remove_b_tags(string):
    """
        Fonction qui enlève les balises <b> ainsi que leur contenu
    """
    string = re.sub("<b>.*?</b>", "", string)
    return string


def _remove_tags(string):
    """Enlève les balises de la chaîne passée en paramètre"""
    string = re.sub("<.+?>|</.+?>", "", string)
    return string


def parse_script(script_str):
    """Traite et transforme le script (str) passé en paramètre"""
    script = _remove_tags(_remove_b_tags(script_str))
    reg = re.compile("\w+")
    # Des mots qui ne sont pas des balises, on récupère seulement les lettres
    word_list = [reg.search(word)[0].lower()  # [0] : tout ce qui a match
                 for word in _remove_tags(script).split()
                 if reg.search(word) is not None]

    # Compte le nombre d'occurrences de chaque mot dans la liste
    parsed_script = {word: word_list.count(word) for word in word_list}
    return parsed_script


def main():

    # TODO : refaire les tests en important Movie etc.
    script_str = "<b><i>Hello</i></b>, mister <i>villain</i>.\n<b>Welcome to my <i>kingdom</i>, my kingdom come.</b>"
    print(f"Base string: {script_str}\n")
    string = _remove_b_tags(script_str)
    print(f"After b tags removal : {string}")
    string = _remove_tags(string)
    print(f"After all tags removal : {string}")
    print(f"Occurrences: {parse_script(string)}")


if __name__ == '__main__':
    main()
