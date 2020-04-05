from django.http import HttpResponse
from django.template.loader import get_template
from django.shortcuts import render
import datetime
import requests
from Proyecto1.Clases.Episode import Episode
from Proyecto1.Clases.Character import Character
from Proyecto1.Clases.Location import Location


def saludo(request):
    return HttpResponse("holi")


def dameEdad(request, agno, edad):
    periodo = agno-2020
    edadFutura = "En año %s tendras %s años" % (agno, edad)
    return HttpResponse(edadFutura)


def homeView(request):
    doc_externo = get_template('index.html')
    respuesta = requests.get('https://rickandmortyapi.com/api/episode')
    r_episodios = respuesta.json()
    lista_episodios = r_episodios["results"]
    lista_clases = []
    for e in lista_episodios:
        episodio = Episode()
        episodio.cargar_episodio(e)
        lista_clases.append(episodio)
    documento = doc_externo.render(
        {"episodios": lista_clases})
    return HttpResponse(documento)


def characterView(request, id):
    doc_externo = get_template('character.html')
    respuesta = requests.get(
        'https://rickandmortyapi.com/api/character/'+str(id)).json()
    lista_episodios = []
    lista_lugares = []
    # buscar episodios
    for e in respuesta["episode"]:
        answer = requests.get(e).json()
        lista_episodios.append(
            {"url": "../../episodio/"+str(answer["id"])+"/", "name": answer["name"], "episode": answer["episode"]})
    # buscar origin
    origin_url = respuesta["origin"]["url"]
    answer_or = requests.get(origin_url).json()
    origin = {"url": "../../lugar/" +
              str(answer_or["id"])+"/", "name": answer_or["name"]}
    # buscar location
    location_url = respuesta["location"]["url"]
    answer_loc = requests.get(location_url).json()
    location = {"url": "../../lugar/" +
                str(answer_loc["id"])+"/", "name": answer_loc["name"]}

    documento = doc_externo.render(
        {"personaje": respuesta, "lista_episodios": lista_episodios, "location": location, "origin": origin})
    return HttpResponse(documento)


def episodeView(request, id):
    doc_externo = get_template('episode.html')
    respuesta = requests.get(
        'https://rickandmortyapi.com/api/episode/'+str(id))
    r_episodio = respuesta.json()
    lista_personajes = []
    for p in r_episodio["characters"]:
        answer = requests.get(p).json()
        lista_personajes.append(
            {"url": "../../personaje/"+str(answer["id"])+"/", "name": answer["name"], "image": answer["image"]})
    documento = doc_externo.render(
        {"episodio": r_episodio, "lista_personajes": lista_personajes})
    return HttpResponse(documento)


def placeView(request, id):
    doc_externo = get_template('location.html')
    respuesta = requests.get(
        'https://rickandmortyapi.com/api/location/'+str(id))
    r_lugar = respuesta.json()
    lista_personajes = []
    for p in r_lugar["residents"]:
        answer = requests.get(p).json()
        lista_personajes.append(
            {"url": "../../personaje/"+str(answer["id"])+"/", "name": answer["name"], "image": answer["image"]})

    documento = doc_externo.render({"lugar": r_lugar,"lista_residentes": lista_personajes})
    return HttpResponse(documento)
