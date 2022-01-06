import re
# import imsdb_api


class Script:
    """
    Classe qui définit un script de film (str) et qui
    implémente des méthodes pour le traiter (ou "parse"),
    et stocker le résultat.
    """

    @staticmethod
    def _remove_b_tags(string):
        """
            Fonction qui enlève les balises <b> ainsi que leur contenu
        """
        string = re.sub("<b>.*?</b>", "", string)
        return string

    @staticmethod
    def _remove_tags(string):
        """Enlève les balises de la chaîne passée en paramètre"""
        string = re.sub("<.+?>|</.+?>", "", string)
        return string

    @property
    def parsed_script(self):
        if self._parsed_script is None:
            self.parse()
        return self._parsed_script

    @property
    def script(self):
        return self._script

    @script.setter
    def script(self, raw_script):
        """Utiliser script = … pour définir l'attribut _script"""
        # raw_script = imsdb_api.getScript(self._movie_url)
        # On enlève le contenu des balises <b>, et
        # toutes les autres balises sont supprimées
        self._script = self._remove_tags(self._remove_b_tags(raw_script))

    def __init__(self, movie_url):
        self._movie_url = movie_url
        self._script = None # str
        self._parsed_script = None # dict

    # def download(self):
    #     raw_script = imsdb_api.getScript(self._movie_url)
    #     # On enlève le contenu des balises <b>, et
    #     # toutes les autres balises sont supprimées
    #     self._script = self._remove_tags(self._remove_b_tags(raw_script))

    def parse(self):
        """
        Transforme le script en un dictionnaire
        associant les mots et leurs occurrences
        """
        if self._script is None:
            self.download()
        reg = re.compile("\w+")
        # Liste de tous les mots convertis en minuscules
        word_list = [reg.search(word)[0].lower() # [0] : tout ce qui a match
                     for word in self._script.split()
                     if reg.search(word) is not None]

        # Compte le nombre d'occurrences de chaque mot dans la liste
        self._parsed_script = {word: word_list.count(word) for word in word_list}


def main():
    # TODO : refaire les tests
    """
    script_str = "<b><i>Hello</i></b>, mister <i>villain</i>.\n<b>Welcome to my <i>kingdom</i>, my kingdom come.</b>"
    print(f"Base string: {script_str}\n")
    string = _remove_b_tags(script_str)
    print(f"After b tags removal : {string}")
    string = _remove_tags(string)
    print(f"After all tags removal : {string}")
    print(f"Occurrences: {parse_script(string)}")
    """


if __name__ == '__main__':
    main()
