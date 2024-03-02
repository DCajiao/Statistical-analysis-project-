import csv
import io
import matplotlib.pyplot as plt
from flask import Flask, jsonify, send_file

app = Flask(__name__)

@app.route('/')
def mainpage():
    try:
        with open('welcometext.txt', 'r') as file:
            texto = file.read()  
        return f'<pre>{texto}</pre>'
    except FileNotFoundError:
        return jsonify({'error': 'El archivo welcometext.txt no se encontró.'})
    except Exception as e:
        return jsonify({'error': str(e)})

def cargar_datos(archivo):
    try:
        with open(archivo, 'r', encoding='latin1') as file:
            reader = csv.DictReader(file)
            datos = [row for row in reader]
        return jsonify(datos)
    except FileNotFoundError:
        return jsonify({'error': f'El archivo {archivo} no se encontró.'})
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/DATASET')
def obtener_datos():
    return cargar_datos('dataset/datasetcleaned.csv')

@app.route('/DATASET/CA')
def obtener_datos_CA():
    return cargar_datos('dataset/USA_CA.csv')


@app.route('/DATASET/TX')
def obtener_datos_TX():
    return cargar_datos('dataset/USA_TX.csv')

@app.route('/DATASET/PA')
def obtener_datos_PA():
    return cargar_datos('dataset/USA_PA.csv')

@app.route('/grafico')
def obtener_grafico():
    categorias = ['A', 'B', 'C', 'D']
    valores = [23, 45, 56, 78]

    plt.bar(categorias, valores)
    plt.xlabel('Categorías')
    plt.ylabel('Valores')
    plt.title('Gráfico de Barras')

    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format='png')
    img_buffer.seek(0)

    plt.clf()

    return send_file(img_buffer, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
