import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize
from transformers import pipeline
from statistics import mean

# Descargar recursos necesarios (solo la primera vez)
nltk.download("stopwords")
nltk.download("punkt")

# Cargar el modelo de sentimiento
modelo_sentimiento = pipeline("sentiment-analysis", model="nlptown/bert-base-multilingual-uncased-sentiment")

# Stopwords en español e inglés
stopwords_es = set(stopwords.words("spanish"))
stopwords_en = set(stopwords.words("english"))
stopwords_totales = stopwords_es.union(stopwords_en)

def limpiar_texto(texto):
    """
    Limpia el texto eliminando URLs, menciones, caracteres especiales y stopwords.
    """
    texto = texto.lower()  # Convertir a minúsculas
    texto = re.sub(r"http\S+|www\S+|@\S+|#\S+", "", texto)  # Eliminar URLs y menciones
    texto = re.sub(r"[^a-zA-ZáéíóúüñÁÉÍÓÚÜÑ\s]", "", texto)  # Eliminar caracteres especiales
    palabras = texto.split()
    palabras_limpias = [p for p in palabras if p not in stopwords_totales]
    return " ".join(palabras_limpias)

def analizar_sentimiento(texto):
    """
    Analiza el sentimiento del texto:
    - Limpia el texto.
    - Segmenta en oraciones (usando NLTK).
    - Para cada oración, obtiene la cantidad de estrellas del modelo.
    - Promedia los resultados y asigna una clasificación.
    Devuelve un diccionario con las claves: 'texto', 'sentimiento' y 'confianza'.
    """
    texto_limpio = limpiar_texto(texto)
    oraciones = sent_tokenize(texto_limpio)
    resultados = []

    for oracion in oraciones:
        try:
            res = modelo_sentimiento(oracion)
            # Verifica que el resultado tenga la clave 'label'
            if res and isinstance(res, list) and "label" in res[0]:
                estrellas = int(res[0]["label"][0])
                resultados.append(estrellas)
        except Exception as e:
            print(f"⚠️ Error al analizar la oración: '{oracion}'. Detalle: {e}")
            continue

    # Si no se obtuvo ningún resultado, devolver valores predeterminados
    if not resultados:
        return {
            "texto": texto_limpio,
            "sentimiento": "No detectado",
            "confianza": 0.0
        }

    promedio_estrellas = mean(resultados)

    # Mapear el promedio a una clasificación de sentimiento
    if promedio_estrellas <= 1.5:
        sent = "😢 Muy Negativo"
    elif promedio_estrellas <= 2.5:
        sent = "🙁 Negativo"
    elif promedio_estrellas <= 3.5:
        sent = "😐 Neutral"
    elif promedio_estrellas <= 4.5:
        sent = "🙂 Positivo"
    else:
        sent = "😃 Muy Positivo"

    return {
        "texto": texto_limpio,
        "sentimiento": sent,
        "confianza": round(promedio_estrellas / 5, 2)
    }
