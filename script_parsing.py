import re

# class


def remove_b_tags(string):
    # Tout ce qui est de la forme <b> ... </b>
    # reg = re.compile("<b>[ \w0-9-\n]*</b>")
    # reg = re.compile("<b>[^\(</b>\)]*</b>")
    # reg = re.compile("<b>[^<]*</b>")
    reg = re.compile("<b>[^\(</b>\)]</b>")
    res = reg.finditer(string)
    for i in res:
        print("######")
        start, end = i.span()
        string = string[:start] + string[end+1:]
    return string

def remove_b_tags(string):
    # start = 0
    # end = 0
    # motDebut = "<b>"
    # debutOk = False
    # motFin = "</b>"
    # finOk = False
    # acc = ""
    # for c in string:
    #     if c == "<":
    #         acc += "<"
    #         if not(motDebut.startswith(acc)):


    # for c in 
    startString = "<b>"
    endString = "</b>"
    start = string.find(startString)
    end = string.find(endString)
    while start != -1:
        string = string[:start] + string[end+len(endString):]
        start = string.find(startString)
        end = string.find(endString)    

    return string

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
    word_list = [reg.search(word)[0].lower()  # [0] : tout ce qui a match
                 for word in remove_tags(script_str).split()
                 if reg.search(word) is not None]

    # Compte le nombre d'occurrences de chaque mot dans la liste
    occurrences = {word: word_list.count(word) for word in word_list}
    return occurrences


def main():
    script_str = "<b><i>Hello</i></b>, mister <i>villain</i>.\n<b>Welcome to my <i>kingdom</i>, my kingdom come.</b>"
    # print(remove_b_tags(script_str))
    # print(remove_tags(script_str))
    # print(parse_script(script_str))
    string = remove_b_tags(script_str)
    string = remove_tags(string)
    print(f"String de base: {script_str}", end="\n\n")
    print(f"Dico des mots: {parse_script(string)}")


if __name__ == '__main__':
    main()
