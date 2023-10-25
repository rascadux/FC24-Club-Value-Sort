import csv
import unicodedata

# FUnction to correct characters
def corregir_caracteres(texto):
    return ''.join(unicodedata.normalize('NFKD', texto).encode('utf-8', 'ignore').decode('utf-8'))

# Read the original CSV file
with open('club-analyzer.csv', mode='r', encoding='utf-8') as archivo_original:
    lector = csv.reader(archivo_original)
    datos_corregidos = []

    for fila in lector:
        fila_corregida = [corregir_caracteres(celda) for celda in fila]
        datos_corregidos.append(fila_corregida)

# Write the corrected data to a new CSV file
with open('my_club.csv', mode='w', newline='', encoding='utf-8') as archivo_corregido:
    escritor = csv.writer(archivo_corregido)
    escritor.writerows(datos_corregidos)