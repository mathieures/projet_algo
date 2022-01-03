from bs4 import BeautifulSoup, SoupStrainer
import threading
import concurrent.futures
import requests
from Movie import PartialMovie


# req2 = requests.get(lien)
# soup2 = BeautifulSoup(req2.text, "html.parser")

# soup2.find(class_="script-details")
# soup2.find_all("tr")[1]
# soup2.find_all("td")[1]
# lienScript = soup2.find_all("a")[-1]

SITE = "https://imsdb.com/"
SESSION = requests.Session()  # Garde la même session pour les requêtes (+ rapide)


def getName():
    """
    Renvoie un dictionnaire qui associe le nom d'un film
    (str) à un dict { url: str, genres: list }
    """
    # TODO : Renommer suivant PEP 8 ;)
    # TODO : Renommer les variables en anglais

    def parse_tag_in_thread(tag):
        """
        Traite le script du film dont l'url
        est passé en paramètre dans un thread
        """
        movie_title = tag.a["title"]
        movie_url = SITE + tag.a["href"][1:]  # Le href commence par un slash

        script_url = movie_url # test pour voir si c'est bcp plus rapide sans cette requête => OUI
        # script_url = get_script_url(movie_url)
        # Si le script est accessible
        if script_url is not None: # test pour voir si c'est bcp plus rapide sans tester => PAS TANT
        # if script_url is not None and is_valid_url(script_url):
            # Pour enlever le " Script" a la fin du nom du film
            if movie_title.endswith(" Script"):
                movie_title = movie_title[:-7]
            # " ".join(movie_title.split(" ")[:-1])

            # TODO : Récupérer les genres
            genres = ["Test_genre_1", "Test_genre_2"]

            print(f"{movie_title} ✅ ({script_url})")
            # pass
            data[movie_title] = {"url": script_url, "genres": genres}
        else:
            print(f"{movie_title} ❌")
            # pass

    url = SITE + "all-scripts.html"

    req = SESSION.get(url)
    # Contient le code HTML
    # soup = BeautifulSoup(req.text, "html.parser")

    # TODO : Demander à Thomas à quoi servent ces lignes
    # soup.find(id="maindoby")
    # soup.find_all("table")[1]
    # soup.tbody
    # soup.tr
    only_p_tags = SoupStrainer("p")
    tags = BeautifulSoup(req.text, "html.parser", parse_only=only_p_tags)
    # tags = soup.find_all("p")

    data = {}
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Mappe chaque tag à parse_tag_in_thread
        executor.map(parse_tag_in_thread, tags)

    return data


def get_script_url(movie_url):
    """Retourne l'url du script grâce à la page du film"""
    req = SESSION.get(movie_url)
    soup = BeautifulSoup(req.text, "html.parser")

    tag = soup.find(class_="script-details")
    # print("tag :", tag)
    if tag is not None and tag != "":
        # tag.tbody
        # tag.find_all("tr")[1]
        # tag.find_all("td")[1]
        a = tag.find_all("a")[-1]

        return SITE + a["href"]  # L'url est un chemin relatif sur le site
    else:
        return None


def is_valid_url(url):
    """Retourne True si l'url est accessible, False sinon"""
    return True if SESSION.head(url).status_code == 200 else False


def getScript(movie_url):
    """
    Prend en paramètre l'url du film et retourne le script associé à ce film
    """
    script_url = get_script_url(movie_url)
    if script_url is not None:
        # On demande le contenu de la page
        req = SESSION.get(script_url)

        # Si la requête a bien abouti
        if req.status_code == 200:
            soup = BeautifulSoup(req.text, "html.parser")

            tag = soup.find(class_="scrtext")
            script = tag.pre

            return PartialMovie(script=script)
    return None


def main():
    data = getName()
    print(len(data))
    print(data)

    title = "30 Minutes or Less"
    movie = getScript(data[title]["url"])
    # print(movie.script)


if __name__ == "__main__":
    main()
