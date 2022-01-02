from bs4 import BeautifulSoup
import requests

class Movie:
    SITE = "https://imsdb.com/"
    """Classe décrivant un film"""

    def __init__(self, title, genres, lien):
        # TODO : Ajouter les attributs dont on a besoin au fur et à mesure
        self.title = title
        self.genres = genres
        self.lien = lien
        self.script = None
    
    def getScript(self):
        """
            Fonction qui renvoie le script sous forme de str et le créer s'il n'existe pas
        """

        if self.script == None:
            
            req = requests.get(self.lien)
            soup = BeautifulSoup(req.text, "html.parser")

            tag = soup.find(class_="script-details")
            tag.tbody
            tag.find_all("tr")[1]
            tag.find_all("td")[1]
            a = tag.find_all("a")[-1]

            urlScript = self.SITE + a["href"]

            # Seconde requete pour le texte du script cette fois
            req = requests.get(urlScript)
            soup = BeautifulSoup(req.text, "html.parser")

            tag = soup.find(class_="scrtext")
            self.script = tag.pre
        
        return self.script

    def __str__(self):
        return self.title