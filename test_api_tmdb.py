import requests
import json

API_KEY = "dd6b80f1beb24a174bc0574dbfbd08fa"

def print_dico(dico):
	print(json.dumps(dico, indent=4))

def format_search_query(query):
	return "+".join(query.split(" "))

def get_movie_by_id(id):
	return requests.get(f"https://api.themoviedb.org/3/movie/{id}?api_key={API_KEY}").json()

def search_movie(query):
	return requests.get(f"https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&query={format_search_query(query)}").json()

def get_genres(dico):
	"""A faire avec un objet Movie"""
	return [genre["name"] for genre in dico["genres"]]

# r = requests.get(f"https://api.themoviedb.org/3/movie/550?api_key={API_KEY}")

# print_dico(r)

# query = "Jack reacher"
# r = requests.get(f"https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&query={format_search_query(query)}")

# print_dico(r)

# r = get_movie_by_id(75780)
# print_dico(r)

# r = search_movie("Collateral Damage")
# print_dico(r)

dico = get_movie_by_id(9884)
print_dico(dico)

genres = get_genres(dico)
print("genres :", genres)