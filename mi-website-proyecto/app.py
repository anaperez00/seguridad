import matplotlib.pyplot as plt
import io
import base64
import unicodedata

from flask import Flask, render_template, request

app = Flask(__name__)

def validar_texto(texto):
    valid_chars = "ABCDEFGHIJKLMNÑOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz "
    return all(c in valid_chars for c in texto) and len(texto) >= 90



valor_letra = {
    'A': 0, 
    'B': 1, 
    'C': 2, 
    'D': 3, 
    'E': 4,
    'F': 5, 
    'G': 6, 
    'H': 7, 
    'I': 8, 
    'J': 9,
    'K': 10, 
    'L': 11, 
    'M': 12, 
    'N': 13, 
    'Ñ': 14,
    'O': 15, 
    'P': 16,   
    'Q': 17, 
    'R': 18, 
    'S': 19,
    'T': 20,   
    'U': 21, 
    'V': 22, 
    'W': 23, 
    'X': 24,
    'Y': 25, 
    'Z': 26
}

valor_letraCifrado = {
    'A': 0, 
    'B': 1, 
    'C': 2, 
    'D': 3, 
    'E': 4,
    'F': 5, 
    'G': 6, 
    'H': 7, 
    'I': 8, 
    'J': 9,
    'K': 10, 
    'L': 11, 
    'M': 12, 
    'N': 13, 
    'Ñ': 14,
    'O': 15, 
    'P': 16,   
    'Q': 17, 
    'R': 18, 
    'S': 19,
    'T': 20,   
    'U': 21, 
    'V': 22, 
    'W': 23, 
    'X': 24,
    'Y': 25, 
    'Z': 26,
    ' ': 27
}

def asignar_valores(texto):
    valores = [valor_letra[char] for char in texto]
    return valores

def asignar_valoresCifrado(texto):
    # Diccionario para asignar valores a letras
    valor_letra = {
        'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6, 'H': 7, 'I': 8, 'J': 9,
        'K': 10, 'L': 11, 'M': 12, 'N': 13, 'Ñ': 14, 'O': 15, 'P': 16, 'Q': 17, 'R': 18, 'S': 19,
        'T': 20, 'U': 21, 'V': 22, 'W': 23, 'X': 24, 'Y': 25, 'Z': 26, ' ': 27  # Espacio se mapea a sí mismo
    }
    
    valores = [valor_letra[char] for char in texto]
    return valores

def contar_caracteres(texto):
    contador = {}
    total_caracteres = len(texto)

    for char in texto:
        if char in contador:
            contador[char] += 1
        else:
            contador[char] = 1

    return contador

def calcular_inversa_modulo27(valor):
    for inversa in range(27):
        if (valor * inversa) % 27 == 1:
            return inversa
    return None

def limpiar_texto(texto):
    # Remover caracteres de retorno de carro y salto de línea
    texto = texto.replace('\r', '').replace('\n', '')
    
    # Remover caracteres especiales y números, excepto la 'Ñ'
    caracteres_especiales = '''!"#$%&'()*+,-./0123456789:;<=>?@[\]^_`{|}~'''
    caracteres_no_remover = ['ñ']  # Lista de caracteres que no se eliminarán
    texto_limpio = ''.join([char for char in texto if char not in caracteres_especiales or char in caracteres_no_remover])
    
    return texto_limpio.upper() 
def asignar_letra(valor):
    for letra, val in valor_letra.items():
        if val == valor:
            return letra
    return ''

@app.route("/")
def index():
    return render_template('index.html', caracteres_asociados="", grafico="")

@app.route("/cifrar", methods=['POST','GET'])
def cifrar():
    texto_claro = request.form['textoclaro']
    texto_procesado = limpiar_texto(texto_claro)
    decimacionA = int(request.form['decimacionA'])  # Convertir a entero
    desplazamientoB = int(request.form['desplazamientoB'])  # Convertir a entero
   
    texto_valores = asignar_valoresCifrado(texto_procesado)
    
    # Realizar la operación de multiplicación por decimacionA a los elementos numéricos de texto_valores
    texto_valores_procesados = []
    for valor in texto_valores:
        if isinstance(valor, int):  # Verificar si el valor es numérico
            if valor == 27:
                texto_valores_procesados.append(valor)
            else:
                valor_procesado = (valor * decimacionA) % 27
                texto_valores_procesados.append(valor_procesado)
    
    return render_template('index.html',texto_valores_procesados=texto_valores_procesados)




@app.route("/descifrar", methods=['POST'])
def descifrar():
    texto_cifrado = request.form['textocifrado'] 
   # correspondienteE = request.form['correspondienteE']
    #correspondienteA= request.form['correspondienteA']

    texto_cifrado = texto_cifrado.upper()
    resultados = []  # Lista para almacenar los resultados}
    resultados2 = []
    
    if validar_texto(texto_cifrado):
        texto_sin_espacios = texto_cifrado.replace(" ", "")
        valores = asignar_valores(texto_sin_espacios)
        valores2 = asignar_valores(texto_sin_espacios)
        conteo_caracteres = contar_caracteres(texto_sin_espacios)

        for char, count in conteo_caracteres.items():
            porcentaje = (count / len(texto_sin_espacios)) * 100
            valor = valores[ord(char) - ord('A')]
            resultados.append((char, count, porcentaje, valor))  
            # Agregar resultados a la lista

        resultados.sort(key=lambda x: x[1], reverse=False) # Ordenar en función de la cantidad de repeticiones en orden descendente

        variable_mejor = max(valores, key=valores.count)
        valores_sin_mejor = sorted(set(valores), key=valores.count, reverse=True)
        variable_b = valores_sin_mejor[1]
        consE = valor_letra["E"]
        consA = valor_letra["A"]
        valores_del_texto = valores
        resta = variable_mejor - variable_b
        inversa_consE = calcular_inversa_modulo27(consE)
        mul = resta * inversa_consE
        a = mul % 27
        inversaFinal = calcular_inversa_modulo27(a)
        
        variable_mejor2 = valores_sin_mejor[1]
        variable_b2 = max(valores, key=valores.count)
        resta2 = variable_mejor2-variable_b2
        valores_del_texto2 = valores2
        inversa_consE2= calcular_inversa_modulo27(consE)
        mul2 = resta2 * inversa_consE2
        a2= mul % 27
        inversaFinal2= calcular_inversa_modulo27(a2)


        for i in range(len(valores_del_texto)):
            valores_del_texto[i] = ((valores_del_texto[i] - variable_b) * calcular_inversa_modulo27(a)) % 27
            caracteres_asociados = [None] * len(valores_del_texto)

        for i in range(len(valores_del_texto2)):
                valores_del_texto2[i] = ((valores_del_texto2[i] - variable_b2) * calcular_inversa_modulo27(a2)) % 27
                caracteres_asociados2 = [None] * len(valores_del_texto2)

        for i, valor in enumerate(valores_del_texto):
            for char, val in valor_letra.items():
                if val == valor:
                    caracteres_asociados[i] = char
                    break

        for i, valor in enumerate(valores_del_texto2):
            for char, val in valor_letra.items():
                if val == valor:
                    caracteres_asociados2[i] = char
                    break

        resultado = {}
        output = f'el texto es valido{resultado}'
        constante = f'constantes y variables contanteE:{consE}, consA{consA}, variablemejor{variable_mejor}, variableb{variable_b}'
        etiquetas = [char for char, _, _, _ in resultados]
        # Crear una lista para las repeticiones de cada carácter
        repeticiones = [count for _, count, _, _ in resultados]

            # Generar el gráfico de barras
        plt.figure(figsize=(8, 6))
        plt.barh(etiquetas, repeticiones, color='skyblue')
        plt.xlabel('Repeticiones')
        plt.ylabel('Carácter')
        plt.title('Repeticiones de Caracteres en el Texto Cifrado')
        plt.tight_layout()

        # Convertir el gráfico a una imagen base64
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        imagen_base64 = base64.b64encode(buffer.read()).decode('utf-8')

    else: 
        output = "el texto es invalido"

    return render_template('index.html', resultado=f'el textoes impresionantemente largo {output}', resultados=resultados, constante=constante, caracteres_asociados="".join(caracteres_asociados), caracteres_asociados2="".join(caracteres_asociados2), grafico=imagen_base64)


if __name__ == "__main__":
    app.run(debug=True)