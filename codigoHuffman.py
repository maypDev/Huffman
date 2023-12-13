from flask import Flask, render_template, request
app = Flask(__name__)  # Crea una instancia de la aplicación Flask

class Node:  # Definición de la clase Node para representar nodos en el árbol de Huffman
    # Propiedades de los nodos
    probability = 0.0  # Probabilidad del símbolo
    symbol = ""  # Símbolo del nodo
    encoding = ""  # Codificación binaria del símbolo
    visited = False  # Indica si el nodo ha sido visitado durante la construcción del árbol
    parent = -1  # Índice del padre en la lista de nodos

class Huffman:  # Definición de la clase Huffman para la creación del árbol de Huffman
    Tree = None  # Árbol de Huffman resultante
    Root = None  # Raíz del árbol
    Nodes = []  # Lista de nodos en el árbol
    probs = {}  # Diccionario que almacena las probabilidades de los símbolos
    dictEncoder = {}  # Diccionario que almacena los códigos binarios de los símbolos

    # Métodos de la clase Huffman
    def __init__(self, symbols):
        # Inicializa la instancia de Huffman con la lista de símbolos y sus probabilidades
        self.initNodes(symbols)
        self.buildTree()
        self.buildDictionary()

    def initNodes(self, probs):
        # Inicializa los nodos del árbol con los símbolos y sus probabilidades
        for symbol in probs:
            node = Node()
            node.symbol = symbol
            node.probability = probs[symbol] * 0.1  # Ajusta la probabilidad para códigos más cortos
            node.visited = False
            self.Nodes.append(node)
            self.probs[symbol] = probs[symbol]

        # Asegura que el espacio esté incluido en el árbol de Huffman
        if ' ' not in self.probs:
            node = Node()
            node.symbol = ' '
            node.probability = 0.001  # Ajusta la probabilidad según sea necesario
            node.visited = False
            self.Nodes.append(node)
            self.probs[' '] = node.probability
    
    def buildTree(self):  # Realizamos las operaciones de acuerdo al reglamento para la construcción del árbol de Huffman
        indexMin1 = self.getNodeWithMinimumProb()  # Buscamos el menor número de la primera probabilidad
        indexMin2 = self.getNodeWithMinimumProb()  # Buscamos el menor número de la segunda probabilidad

        while indexMin1 != -1 and indexMin2 != -1:  # != evalúa como verdadero si 2 variables son diferentes
            node = Node()  # Inicializamos
            node.symbol = "."
            node.encoding = ""
            # Llamamos a las dos probabilidades mínimas
            prob1 = self.Nodes[indexMin1].probability
            prob2 = self.Nodes[indexMin2].probability
            node.probability = prob1 + prob2  # Sumamos las probabilidades
            node.visited = False  # False = 1
            node.parent = -1  # Restamos la probabilidad a -1
            self.Nodes.append(node)
            self.Nodes[indexMin1].parent = len(self.Nodes) - 1  # Lista o cadena que queremos medir
            self.Nodes[indexMin2].parent = len(self.Nodes) - 1

            # Regla: 0 a mayor probabilidad, 1 a menor probabilidad.
            if prob1 >= prob2:
                self.Nodes[indexMin1].encoding = "0"
                self.Nodes[indexMin2].encoding = "1"
            else:
                self.Nodes[indexMin1].encoding = "1"
                self.Nodes[indexMin2].encoding = "0"

            indexMin1 = self.getNodeWithMinimumProb()
            indexMin2 = self.getNodeWithMinimumProb()

    def getNodeWithMinimumProb(self):  # Realizamos una comparación para obtener el nodo de menor probabilidad
        minProb = 1.0  # La mínima probabilidad no puede ser mayor de 1
        indexMin = -1  # Índice para restar a la probabilidad

        for index in range(0, len(self.Nodes)):  # Index es el número de probabilidad
            if (self.Nodes[index].probability < minProb and
                    (not self.Nodes[index].visited)):
                minProb = self.Nodes[index].probability
                indexMin = index

        if indexMin != -1:
            self.Nodes[indexMin].visited = True

        return indexMin

    def showSymbolEncoding(self, symbol):
        found = False
        index = 0
        encoding = ""

        for i in range(0, len(self.Nodes)):
            if self.Nodes[i].symbol == symbol:
                found = True
                index = i
                break

        if found:
            while index != -1:
                encoding = "%s%s" % (self.Nodes[index].encoding, encoding)
                index = self.Nodes[index].parent
        else:
            encoding = "simbolo_desconocido"  # Ajusta según sea necesario

        return encoding

    def buildDictionary(self):  # Creamos un diccionario, guardamos todos los símbolos con sus respectivos códigos binarios
        # Resueltos por el árbol de Huffman
        for symbol in self.probs:
            encoding = self.showSymbolEncoding(symbol)
            self.dictEncoder[symbol] = encoding

    def encode(self, plain):  # Agrupa los códigos binarios codificados de acuerdo al mensaje escrito en consola
        encoded = ""
        for symbol in plain:
            encoded = "%s%s" % (encoded, self.dictEncoder[symbol])

        return encoded

    # INICIO DE LA DECODIFICACION ....................................................................................................................................................
    def decode(self, encoded):
        index = 0
        decoded = ""

        while index < len(encoded):
            found = False
            aux = encoded[index:]

            # Intenta encontrar un símbolo correspondiente para el código binario actual
            for symbol in self.probs:
                if aux.startswith(self.dictEncoder[symbol]):
                    decoded = "%s%s" % (decoded, symbol)
                    index = index + len(self.dictEncoder[symbol])
                    found = True
                    break

            # Si no se encuentra un símbolo correspondiente, agrega el carácter directamente
            if not found:
                decoded = "%s%s" % (decoded, aux[0])
                index += 1

        return decoded

    # FIN DE LA DECODIFICACION ..........................................................................................................................................................


def obtener_info_adicional(mensaje):
    return {
        'numero_caracteres': len(mensaje),
        'fichero_inicial': 'nombre_del_fichero_inicial.txt',  # Reemplaza con el nombre real del fichero
        'fichero_compreso': 'nombre_del_fichero_compreso.txt',  # Reemplaza con el nombre real del fichero
        'informacion_media': 'informacion_media.txt',  # Reemplaza con el nombre real del fichero
    }

def obtener_frecuencia_absoluta(mensaje):
    return {symbol: mensaje.count(symbol) for symbol in set(mensaje)}

def obtener_info_codificacion(simbolos, mensaje):
    simbolos = ''
    probabilidad = []
    msm = mensaje
    d = 0

    for i in mensaje:
        if i in msm:
            simbolos += i
            probabilidad.append(float(msm.count(i) / len(mensaje)))
            msm = msm.replace(i, '')
            d += 1

    symbols = dict(zip(simbolos, probabilidad))
    huffman = Huffman(symbols)
    encoded = huffman.encode(mensaje)

    # Ordena el diccionario por frecuencia absoluta de mayor a menor
    frecuencia_absoluta = obtener_frecuencia_absoluta(mensaje)
    frecuencia_ordenada = dict(sorted(frecuencia_absoluta.items(), key=lambda item: item[1], reverse=True))

    return {
        'encoded': encoded,
        'symbols': symbols,
        'dictEncoder': huffman.dictEncoder,
        'frecuencia_absoluta': frecuencia_ordenada,
    }

@app.route('/')
def index():
    return render_template('huffman.html')


@app.route('/encode', methods=['POST'])
def encode():
    mensaje = request.form['mensaje']

    simbolos = ''
    probabilidad = []
    msm = mensaje
    d = 0

    for i in mensaje:
        if i in msm:
            simbolos += i
            probabilidad.append(float(msm.count(i) / len(mensaje)))
            msm = msm.replace(i, '')
            d += 1

    symbols = dict(zip(simbolos, probabilidad))

    huffman = Huffman(symbols)

    encoded = huffman.encode(mensaje)

    # Calcula la frecuencia absoluta
    frecuencia_absoluta = {symbol: mensaje.count(symbol) for symbol in set(mensaje)}

    # Ordena el diccionario por frecuencia absoluta de mayor a menor
    frecuencia_ordenada = dict(sorted(frecuencia_absoluta.items(), key=lambda item: item[1], reverse=True))

    # Información adicional
    info_adicional = {
        'numero_caracteres': len(mensaje),
        'fichero_inicial': len(mensaje)*8,  # Reemplaza con el nombre real del fichero
        'fichero_compreso': len(frecuencia_absoluta)*8,  # Reemplaza con el nombre real del fichero
    }

    # Decodificar el mensaje
    decoded = huffman.decode(encoded)

    # Agrega información adicional y mensaje decodificado al contexto para la plantilla
    context = {
        'mensaje': mensaje,
        'encoded': encoded,
        'symbols': symbols,
        'dictEncoder': huffman.dictEncoder,
        'frecuencia_absoluta': frecuencia_ordenada,
        'info_adicional': info_adicional,
        'decoded': decoded,  # Agregamos el mensaje decodificado
    }
    return render_template('resultado.html', **context)

if __name__ == '__main__':
    app.run(debug=True)