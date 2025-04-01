import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize
from transformers import pipeline
from statistics import mean

# Descargar recursos necesarios
nltk.download("stopwords")
nltk.download("punkt")  # Para segmentación de oraciones

# Cargar modelo de sentimiento
modelo_sentimiento = pipeline("sentiment-analysis", model="nlptown/bert-base-multilingual-uncased-sentiment")

# Stopwords en español e inglés
stopwords_es = set(stopwords.words("spanish"))
stopwords_en = set(stopwords.words("english"))
stopwords_totales = stopwords_es.union(stopwords_en)

def limpiar_texto(texto):
    """
    Limpia el texto eliminando caracteres especiales, emojis y stopwords.
    """
    texto = texto.lower()  # Convertir a minúsculas
    texto = re.sub(r"http\S+|www\S+|@\S+|#\S+", "", texto)  # Eliminar URLs y menciones
    texto = re.sub(r"[^a-zA-ZáéíóúüñÁÉÍÓÚÜÑ\s]", "", texto)  # Eliminar caracteres especiales
    palabras = texto.split()
    palabras_limpias = [p for p in palabras if p not in stopwords_totales]  # Eliminar stopwords
    return " ".join(palabras_limpias)

def analizar_sentimiento(texto):
    """
    Analiza el sentimiento de un texto dividiéndolo en oraciones, limpiando y promediando los resultados.
    """
    texto = limpiar_texto(texto)  # Limpiar el texto antes del análisis
    oraciones = sent_tokenize(texto)  # Mejor segmentación de oraciones

    resultados = []
    for oracion in oraciones:
        try:
            resultado = modelo_sentimiento(oracion)
            print(f"🔍 Resultado del modelo: {resultado}")  # Depuración
            
            if resultado and isinstance(resultado, list) and "label" in resultado[0]:
                estrellas = int(resultado[0]["label"][0])
                resultados.append(estrellas)  # Extraer la cantidad de estrellas
        except Exception as e:
            print(f"⚠️ Error al analizar la oración: {oracion}. Detalle: {e}")
            continue  # Si hay un fallo, saltar a la siguiente oración

    if not resultados:
        resultado_final = {
            "texto": texto,
            "sentimiento": "No detectado",
            "confianza": 0.0
        }
    else:
        # Promediar resultados de todas las oraciones
        promedio_estrellas = mean(resultados)

        # Asignar sentimiento mejorado
        if promedio_estrellas <= 1.5:
            sentimiento = "😢 Muy Negativo"
        elif 1.5 < promedio_estrellas <= 2.5:
            sentimiento = "🙁 Negativo"
        elif 2.5 < promedio_estrellas <= 3.5:
            sentimiento = "😐 Neutral"
        elif 3.5 < promedio_estrellas <= 4.5:
            sentimiento = "🙂 Positivo"
        else:
            sentimiento = "😃 Muy Positivo"

        resultado_final = {
            "texto": texto,
            "sentimiento": sentimiento,
            "confianza": round(promedio_estrellas / 5, 2)  # Convertir a una escala de 0 a 1 con 2 decimales
        }

    print(f"📢 Resultado final antes de retornar: {resultado_final}")  # Depuración
    return resultado_final
