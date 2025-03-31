from transformers import pipeline

# Cargar modelo multilingüe
modelo_sentimiento = pipeline("sentiment-analysis", model="nlptown/bert-base-multilingual-uncased-sentiment")

def analizar_sentimiento(texto):
    resultado = modelo_sentimiento(texto)[0]
    
    # Convertir la clasificación a un sentimiento
    estrellas = int(resultado['label'][0])  # Extrae el número de estrellas
    if estrellas == 1:
        sentimiento = "😢 Muy Negativo"
    elif estrellas == 2:
        sentimiento = "🙁 Negativo"
    elif estrellas == 3:
        sentimiento = "😐 Neutral"
    elif estrellas == 4:
        sentimiento = "🙂 Positivo"
    else:
        sentimiento = "😃 Muy Positivo"
    
    return {
        "texto": texto,
        "sentimiento": sentimiento,
        "confianza": resultado["score"]
    }
