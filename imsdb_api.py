from bs4 import BeautifulSoup, SoupStrainer
import concurrent.futures
import requests
from Movie import PartialMovie


# req2 = requests.get(lien)
# soup2 = BeautifulSoup(req2.text, "html.parser")

# soup2.find(class_="script-details")
# soup2.find_all("tr")[1]
# soup2.find_all("td")[1]
# script_url = soup2.find_all("a")[-1]

SITE = "https://imsdb.com/"
SESSION = requests.Session()  # Garde la même session pour les requêtes (+ rapide)


def getName():
    """
    Renvoie un dictionnaire de dictionnaires de la forme :
    {
        "genre_1": {
            "film_1": "url_script_1",
            "film_2": "url_script_2"
        },
        "genre_2": {
            "film_2": "url_script_2",
            "film_3": "url_script_3"
        },
        …
    }
    """

    def parse_genre_in_thread(genre):
        """
        Traite le genre passé en paramètre dans un thread
        """
        genre_url = SITE + "genre/" + genre

        req = requests.get(genre_url)
        # On ne traite que les balises <p>
        only_p_tags = SoupStrainer("p")
        movies_tags = BeautifulSoup(req.text, "html.parser", parse_only=only_p_tags)

        current_genre = {}
        for movie_tag in movies_tags:
            movie_title = movie_tag.a["title"]
            movie_url = SITE + movie_tag.a["href"][1:] # Le href commence par un slash

            # Pour enlever le " Script" a la fin du nom du film
            if movie_title.endswith(" Script"):
                movie_title = movie_title[:-7]
            # movie_title = " ".join(movie_title.split(" ")[:-1])

            current_genre[movie_title] = movie_url
        
        result[genre] = current_genre


    # Récupération du nom des genres :
    req = requests.get(SITE)

    only_table_tags = SoupStrainer("table")
    soup = BeautifulSoup(req.text, "html.parser", parse_only=only_table_tags)

    genres_table = soup.find_all("table")[4] # Les genres se trouve sur la 5ième table de la page
    a_tags = genres_table.find_all("a")

    all_genres = [a.string for a in a_tags]

    result = {}
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Mappe chaque genre à parse_genre_in_thread
        executor.map(parse_genre_in_thread, all_genres)        

    return result


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

        return SITE + a["href"][1:] # L'url est un chemin relatif sur le site
    else:
        return None


# def is_valid_url(url):
#     """Retourne True si l'url est accessible, False sinon"""
#     return True if SESSION.head(url).status_code == 200 else False


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
    print(f"Nombre de genres : {len(data)}")
    # print(data)

    genre = "Action"
    first_movie_title = list(data[genre])[0]
    first_movie_url = data[genre][first_movie_title]
    print(f"Titre du premier film du genre '{genre}' : '{first_movie_title}'")
    print(f"URL de sa page : {first_movie_url}")
    print(f"URL de son script : {get_script_url(first_movie_url)}")


if __name__ == "__main__":
    main()
