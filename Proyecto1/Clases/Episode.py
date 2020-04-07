import requests


class Episode():

    def __init__(self):

        self.name = ""
        self.air_date = ""
        self.episode = ""
        self.characters = []
        self.url = ""
        self.created = ""
        self.lista_personajes = []

    def cargar_episodio(self, dict_info):
        self.id = dict_info["id"]
        self.name = dict_info["name"]
        self.air_date = dict_info["air_date"]
        self.episode = dict_info["episode"]
        self.characters = dict_info["characters"]
        self.url = dict_info["url"]
        self.created = dict_info["created"]
        self.local_url = "../../episodio/"+str(self.id)+"/"

    def buscar_personajes(self):
        for p in self.characters:
            respuesta = requests.get(p).json()
            self.lista_personajes.append(
                ("../../personaje/"+str(respuesta["id"])+"/", respuesta["name"]))
