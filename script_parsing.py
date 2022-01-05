import re

class 

def remove_tags(string):
    """Enlève les balises de la chaîne passée en paramètre"""
    if "<" in string:
        start = string.index("<")
        end = string.index(">") + 1
        string = string[:start] + string[end:]
        return remove_tags(string)
    return string


def parse_script(script_str):
    reg = re.compile("\w+")
    # Des mots qui ne sont pas des balises, on récupère seulement les lettres
    word_list = [reg.search(word)[0].lower() # [0] : tout ce qui a match
                 for word in remove_tags(script_str).split()
                 if reg.search(word) is not None]

    # Compte le nombre d'occurrences de chaque mot dans la liste
    occurrences = { word: word_list.count(word) for word in word_list }
    return occurrences


def main():
    script_str = "<b><i>Hello</i></b>, mister <i>villain</i>.\n<b>Welcome to my <i>kingdom</i>, my kingdom come.</b>"
    print(remove_tags(script_str))
    print(parse_script(script_str))

if __name__ == '__main__':
    main()