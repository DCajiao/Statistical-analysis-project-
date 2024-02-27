import csv
from flask import Flask, jsonify, send_file
import matplotlib.pyplot as plt
import io
import json

app = Flask(__name__)

@app.route('/')
def mainpage():
    try:
        with open('welcometext.txt', 'r') as file:
            texto = file.read()  # O file.readlines() si prefieres una lista de líneas
        return f'<pre>{texto}</pre>'
    except FileNotFoundError:
        return jsonify({'error': 'El archivo archivo.txt no se encontró.'})
    except Exception as e:
        return jsonify({'error': str(e)})
@app.route('/grafico')
def obtener_grafico():
    # Generar datos de ejemplo
    categorias = ['A', 'B', 'C', 'D']
    valores = [23, 45, 56, 78]

    # Crear el gráfico de barras
    plt.bar(categorias, valores)
    plt.xlabel('Categorías')
    plt.ylabel('Valores')
    plt.title('Gráfico de Barras')

    # Guardar el gráfico en un buffer
    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format='png')
    img_buffer.seek(0)

    # Limpiar la figura
    plt.clf()

    # Devolver la imagen como respuesta
    return send_file(img_buffer, mimetype='image/png')

@app.route('/CA')
def obtener_datos_CA():
    # Intentar cargar datos desde el archivo CSV y convertirlos a JSON
    try:
        with open('dataset/USA_CA.csv', 'r') as file:
            reader = csv.DictReader(file)
            datos = [row for row in reader]
        return jsonify(datos)
    except FileNotFoundError:
        return jsonify({'error': 'El archivo USA_CA.csv no se encontró.'})
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/TX')
def obtener_datos_TX():
    # Intentar cargar datos desde el archivo CSV y convertirlos a JSON
    try:
        with open('dataset/USA_TX.csv', 'r') as file:
            reader = csv.DictReader(file)
            datos = [row for row in reader]
        return jsonify(datos)
    except FileNotFoundError:
        return jsonify({'error': 'El archivo USA_TX.csv no se encontró.'})
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True, port=3000)
