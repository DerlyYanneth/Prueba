from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from transformers import pipeline
from jinja2 import Template
import tensorflow as tf

clasificador = pipeline("text-classification", model="nlptown/bert-base-multilingual-uncased-sentiment")
texto ="Hoy esta haciendo sol, podemos ir a jugar futbol "
resultado = clasificador(texto)
label = resultado[0]['label']
print(label)