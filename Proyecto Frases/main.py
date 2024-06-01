from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from transformers import pipeline
from jinja2 import Template
import tensorflow as tf

app = FastAPI()
clasificador = pipeline("text-classification", model="nlptown/bert-base-multilingual-uncased-sentiment")

def obtener_mensaje_sentimiento(resultado):
    label = resultado[0]['label']
    print(label)
    if label == '1 star':
        return "Es triste"
    elif label == '2 stars':
        return "Es un poco triste"
    elif label == '3 stars':
        return "Es Neutro"
    elif label == '4 stars':
        return "Es un poco feliz"
    elif label == '5 stars':
        return "Es Feliz"
    else:
        return "No reconoce la emoción"

formulario_html = """
<!DOCTYPE html>
<html>
<head>
    <title>Analizar Sentimiento Textual</title>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
    <style>
        .resultado-container {
            display: {% if resultado %} block; {% else %} none; {% endif %};
        }
    </style>
</head>
<body>
    <div class="container">
        <center>
        <h2 class="mt-5">Analizar Sentimiento Textual</h2>
        </center>
        <form action="/analizar-sentimiento/" method="post" class="mt-3">
            <div class="form-group">
                <label for="texto">Texto:</label>
                <input type="text" id="texto" name="texto" class="form-control">
            </div>
            <button type="submit" class="btn btn-primary">Analizar</button>
        </form>
        <div class="resultado-container">
            {% if resultado %}
             <h2 class="mt-3">Resultado:</h2>
            <center>
            <h4>{{ mensaje_sentimiento }}</h4>
            </center>
            {% endif %}
        </div>
    </div>
</body>
</html>
"""

@app.get("/analizar-sentimiento/", response_class=HTMLResponse)
async def analizar_sentimiento_get(request: Request):
    return formulario_html

@app.post("/analizar-sentimiento/", response_class=HTMLResponse)
async def analizar_sentimiento_post(request: Request):
    form_data = await request.form()
    texto = form_data.get('texto', '')
    resultado = clasificador(texto)
    mensaje_sentimiento = obtener_mensaje_sentimiento(resultado)
    template = Template(formulario_html)
    return template.render(resultado=resultado, mensaje_sentimiento=mensaje_sentimiento)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
