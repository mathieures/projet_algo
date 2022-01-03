from bs4 import BeautifulSoup
import requests

# req2 = requests.get(lien)
# soup2 = BeautifulSoup(req2.text, "html.parser")

# soup2.find(class_="script-details")
# soup2.find_all("tr")[1]
# soup2.find_all("td")[1]
# lienScript = soup2.find_all("a")[-1]

SITE = "https://imsdb.com/"


def getName():
    """
    Renvoie un dico de dico. Forme: { genre1 : {nomFilm : lienScript} , genre2 : {nomFilm : lienScript} , ... }
    lienScript : un url permettant d'acceder a une page qui elle même possède l'url du script
    """

    listeGenre = ["Action", "Adventure", "Animation", "Comedy", "Crime", 
                  "Drama", "Family", "Fantasy", "Fiml-Noir", "Horror", 
                  "Musical", "Mystery", "Romance", "Sci-Fi", "Short", 
                  "Thriller", "War", "Western"]
    
    grandDico = {}

    for genre in listeGenre:

        url = SITE + "genre/" + genre

        req = requests.get(url)
        # soup contient le code HTML de url
        soup = BeautifulSoup(req.text, "html.parser")

        soup.find(id="maindoby")
        soup.find_all("table")[1]
        soup.tbody
        soup.tr
        tag = soup.find_all("p")

        dico = {}
        for t in tag:
            nomFilm = t.a["title"]
            lien = SITE + t.a["href"]

            # Pour enlever le "Script" a la fin du nom du film
            nomFilm = " ".join(nomFilm.split(" ")[:-1])

            dico[nomFilm] = SITE + lien
        
        grandDico[genre] = dico

    return grandDico


# def getScript(url):
#     """
#         Fonction qui prend en entrée le nom de l'url temporaire pour acceder au script
#         et qui renvoie le script sous forme de str
#     """
#     req = requests.get(url)
#     soup = BeautifulSoup(req.text, "html.parser")

#     tag = soup.find(class_="script-details")
#     tag.tbody
#     tag.find_all("tr")[1]
#     tag.find_all("td")[1]
#     a = tag.find_all("a")[-1]

#     urlScript = SITE + a["href"]

#     # Seconde requete pour le texte du script cette fois
#     req = requests.get(urlScript)
#     soup = BeautifulSoup(req.text, "html.parser")

#     tag = soup.find(class_="scrtext")
#     texte = tag.pre

#     return texte


def main():

    dico = getName()
    print(dico.keys())


if __name__ == "__main__":
    main()
