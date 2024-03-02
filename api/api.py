import csv
import io
import pandas as pd
import matplotlib.pyplot as plt
from flask import Flask, jsonify, send_file
from tabulate import tabulate


df = pd.read_csv("dataset/datasetcleaned.csv", encoding="latin1")

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

@app.route('/question1.1', methods=['GET'])
def handed_analysis():
    handed_counts = df['Handed'].value_counts()
    handed_counts_df = handed_counts.to_frame().reset_index()
    handed_counts_df.columns = ['Laterality', 'Quantity']

    plt.figure(figsize=(8, 6))
    ax = handed_counts.plot(kind='bar', color=['blue', 'orange', 'green'])
    for p in ax.patches:
        ax.annotate(str(p.get_height()), (p.get_x() + p.get_width() / 2., p.get_height()), ha='center', va='bottom')
    plt.title('Number of students by type of laterality:')
    plt.xlabel('Laterality')
    plt.ylabel('Number of students')
    plt.xticks(rotation=0)

    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format='png')
    img_buffer.seek(0)
    plt.close()

    return send_file(img_buffer, mimetype='image/png')

@app.route('/question1.2', methods=['GET'])
def handed_analysis_byregion():

    foot_length_by_region = df.groupby(['Region', 'Longer_foot']).size().unstack(fill_value=0)

    plt.figure(figsize=(10, 6))
    ax = foot_length_by_region.plot(kind='bar', stacked=True)

    plt.title('Number of students by type of foot length and region:')
    plt.xlabel('Region')
    plt.ylabel('Number of students')
    plt.xticks(rotation=45, ha='right')
    plt.legend(title='Foot Length')
    plt.tight_layout()

    for p in ax.patches:
        width = p.get_width()
        height = p.get_height()
        x, y = p.get_xy()
        ax.annotate(f'{height}', (x + width / 2, y + height / 2), ha='center', va='center')


    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format='png')
    img_buffer.seek(0)
    plt.close()

    return send_file(img_buffer, mimetype='image/png') 

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
