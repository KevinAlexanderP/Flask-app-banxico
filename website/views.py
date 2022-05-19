from crypt import methods
from statistics import mean
from flask import Blueprint, render_template, request,redirect, url_for
import urllib.request, json
import os

views = Blueprint('views', __name__)

@views.route("/api/usd/<begin_date>/<end_date>",methods=["POST","GET"])
def get_moneys(begin_date,end_date):
        if request.method == "POST":
            fecha_inicio = request.form["fecha_inicio"]
            fecha_final = request.form["fecha_final"]
            return redirect(url_for("views.get_moneys", begin_date=fecha_inicio,end_date=fecha_final))
        token = "90fb8e5aa818ca5fae557685cc4f3aadca77c195764771960799ba80a66b29a8"
        url = 'https://www.banxico.org.mx/SieAPIRest/service/v1/series/SF43718/datos/{}/{}?token={}'.format(begin_date,end_date,token)
        udis_url = 'https://www.banxico.org.mx/SieAPIRest/service/v1/series/SP68257/datos/{}/{}?token={}'.format(begin_date,end_date)
        response = urllib.request.urlopen(url)
        response_ud =  json.loads(urllib.request.urlopen(udis_url).read())
        data_udis = response_ud['bmx']['series'][0]['datos']
        data = response.read()
        dict = json.loads(data)
        dataset= dict['bmx']['series'][0]['datos']
        sumatoryUDIS = mean([int(float(x['dato'])) for x in data_udis])
        maximoUDIS = max([x['dato'] for x in data_udis])
        minimoUDIS = min([x['dato'] for x in data_udis])
        sumatory = mean([int(float(x['dato'])) for x in dataset])
        maximo = max([x['dato'] for x in dataset])
        minimo = min([x['dato'] for x in dataset])
        print(minimo)
        return render_template ("dollar.html",datosUS=dataset, sumatory=sumatory, maximo=maximo, minimo=minimo,udis= data_udis, sumUDI = sumatoryUDIS, maxUDI = maximoUDIS, minUDI =  minimoUDIS )

@views.route("/api/home", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        fecha_inicio = request.form["fecha_inicio"]
        fecha_final = request.form["fecha_final"]
        return redirect(url_for("views.get_moneys", begin_date=fecha_inicio,end_date=fecha_final))
    else:
	    return render_template("login.html")

@views.route("/api/info-serie-SF43718")
def serie_usd():
	    return render_template("serie.html")

@views.route("/api/info-dev")
def dev():
	    return render_template("dev.html")