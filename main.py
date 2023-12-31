# Exam: Laboratorio di Algoritmi
# Description: Implementation of a B-Tree
# Autor: Federico Marra
# Matricola: 7025997

# I B-alberi (capitolo 18 libro di testo) sono strutture dati per memoria secondaria in cui ogni nodo può avere molti figli.
# ▶ Implementare B-alberi e confrontarli con la memorizzazione in alberi binari di ricerca
# ▶ in memoria secondaria gli algoritmi si confrontano sulla base degli accessi a disco (in questo caso possiamo considerare il numero di nodi letti o scritti)
# Per fare questo dovremo:
# Scrivere i programmi Python (no notebook) che:
# ▶ implementano quanto richiesto
# ▶ eseguono un insieme di test che ci permettano di comprendere
# vantaggi e svantaggi delle diverse implementazioni Svolgere ed analizzare opportuni esperimenti
# Scrivere una relazione (in LATEX) che descriva quanto fatto
# Nota: le strutture dati devono sempre essere implementate nel progetto; non si possono utilizzare librerie sviluppate da altri o copiare codice di altri


# randomizzazione dei valori degli array:
from random import randint as rand

# misurazione dei tempi di esecuzione
from timeit import default_timer as timer

# creazione delle tabelle
import os

# creazione delle tabelle
import numpy as np

# creazione dei grafici
from matplotlib import pyplot as plt

# creazione legende ai grafici:
from matplotlib import patches as mpatch


# Albero binario di ricerca:
class BinaryTreeNode:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.p = None

class BinaryTree:
    def __init__(self):
        self.node = BinaryTreeNode(0)
        self.node.left = None
        self.node.right = None
        self.root = self.node
        self.node_read = 0
        self.node_written = 0

    def get_node_read(self):
        return self.node_read

    def get_node_written(self):
        return self.node_written

    # ricerca
    def search(self, x, key):
        if x == None or key == x.key:
            self.node_read += 1
            return x
        if key < x.key:
            self.node_read += 1
            return self.search(x.left, key)
        else:
            self.node_read += 1
            return self.search(x.right, key)

    # insert
    def insert(self, z):
        y = None
        x = self.root
        while x is not None:
            self.node_read += 1
            y = x
            if z.key < x.key:
                x = x.left
            else:
                x = x.right
        z.p = y
        if y is None:
            self.root = z
        elif z.key < y.key:
            y.left = z
        else:
            y.right = z
        self.node_written += 1
        return z


# B-Albero:
class BTreeNode:
    def __init__(self, leaf=False):
        self.leaf = leaf
        self.keys = []
        self.child = []
        self.n = 0


class BTree:
    def __init__(self, t):
        self.root = BTreeNode(True)
        self.t = t
        self.node_read = 0
        self.node_written = 0

    def get_node_read(self):
        return self.node_read

    def get_node_written(self):
        return self.node_written

    def search(self, key):
        i = 0
        while i < len(self.root.keys) and key > self.root.keys[i]:
            i += 1
        if i < len(self.root.keys) and key == self.root.keys[i]:
            return self.root, i
        elif self.root.leaf:
            return None, 0  # key not found
        else:
            self.node_read += 1
            return self.root.child[i].search(key)

    def split_child(self, x, i):
        z = BTreeNode()
        y = x.child[i]
        z.leaf = y.leaf
        z.n = self.t - 1
        for j in range(0, self.t - 2):
            z.keys[j] = y.keys[j + self.t]
        if not y.leaf:
            for j in range(0, self.t - 1):
                z.child[j] = y.child[j + self.t]
        y.n = self.t - 1
        for j in range(x.n, i, - 1):
            x.child[j + 1] = x.child[j]
        x.child[i + 1] = z
        for j in range(x.n - 1, i - 1, -1):
            x.keys[j + 1] = x.keys[j]
        x.keys[i] = y.keys[self.t - 1]
        x.n = x.n + 1
        y.node_written += 1
        z.node_written += 1
        x.node_written += 1

    # Funzione per inserire una chiave in un albero
    def insert(self, key):
        r = self.root
        if r.n == (2 * self.t) - 1:
            s = BTreeNode()
            self.root = s
            s.leaf = False
            s.n = 0
            s.child[0] = r
            self.split_child(s, 0)
            self.insert_nonfull(s, key)
        else:
            self.insert_nonfull(r, key)

    # Funzione per inserire una chiave in un nodo non pieno
    def insert_nonfull(self, x, k):
        self.node_read += 1
        i = len(x.keys) - 1
        if x.leaf:
            x.keys.append(k)
            while i >= 0 and k < x.keys[i]:
                x.keys[i + 1] = x.keys[i]
                i -= 1
            x.keys[i + 1] = k
        else:
            while i >= 0 and k < x.keys[i]:
                i -= 1
            i += 1
            if len(x.child[i].keys) == (2 * self.t) - 1:
                self.split_child(x, i)
                if k > x.keys[i]:
                    i += 1
            self.insert_nonfull(x.child[i], k)


# Creazione di un array randomico di n elementi
def random_array(n):
    return [rand(1, n) for _ in range(n)]


def test_search(BinaryTree, BTree, array):
    print(f"\nRicerca di {len(array)} elementi:")

    timesBin = 0
    timesBT = 0
    for i in range(len(array)):
        start = timer()
        BinaryTree.search(BinaryTree.root, array[i])
        end = timer()
        timesBin += (end - start) * 1000

        start = timer()
        BTree.search(array[i])
        end = timer()
        timesBT += (end - start) * 1000

    readBin = BinaryTree.get_node_read()
    writtenBin = BinaryTree.get_node_written()
    readBT = BTree.get_node_read()
    writtenBT = BTree.get_node_written()

    print(f"Albero binario di ricerca: {timesBin} ms")
    print(f"B-albero: {timesBT} ms")
    print(f"Albero binario di ricerca: {readBin} letture, {writtenBin} scritture")
    print(f"B-albero: {readBT} letture, {writtenBT} scritture")

    return timesBin, timesBT, readBin, readBT, writtenBin, writtenBT


def test_insert(BinaryTree, BTree, array):
    print(f"\nInserimento di {len(array)} elementi:")
    timesBin = 0
    timesBT = 0
    for i in range(len(array)):
        start = timer()
        BinaryTree.insert(BinaryTreeNode(array[i]))
        end = timer()
        timesBin += (end - start) * 1000

        start = timer()
        BTree.insert(array[i])
        end = timer()
        timesBT += (end - start) * 1000

    readBin = BinaryTree.get_node_read()
    writtenBin = BinaryTree.get_node_written()
    readBT = BTree.get_node_read()
    writtenBT = BTree.get_node_written()

    print(f"Albero binario di ricerca: {timesBin} ms")
    print(f"B-albero: {timesBT} ms")
    print(f"Albero binario di ricerca: {readBin} letture, {writtenBin} scritture")
    print(f"B-albero: {readBT} letture, {writtenBT} scritture")

    return timesBin, timesBT, readBin, readBT, writtenBin, writtenBT


def draw_table(data, title, colorHead="orange", colorCell="yellow", filename = "table"):
    # Crea un nuovo grafico
    figSizeX = 8
    figSizeY = nTests / 3 + 1
    fig, ax = plt.subplots(figsize=(figSizeX, figSizeY))
    plt.title(title)

    # Unisci le liste di dati come colonne al fine di creare un array bidimensionale di dati: 'data'
    if len(data) == 3:
        data = np.column_stack((data[0], data[1], data[2]))
        headers = ("N° elementi", "Albero Binario di Ricerca", "B-Albero")
    elif len(data) == 5:
        data = np.column_stack((data[0], data[1], data[2], data[3], data[4]))
        headers = ("N° elementi", "Lettura ABR", "Lettura BA", "Scrittura ABR", "Scrittura BA")
    else:
        data = np.stack(tuple(data), axis=len(data))
        headers = ("N° elementi", "Albero Binario di Ricerca", "B-Albero")

    # Stile tabella
    ax.axis('off')
    table = ax.table(cellText=data, colLabels=headers, loc="center", cellLoc="center")
    table.auto_set_column_width(col=list(range(len(data))))
    table.scale(1, 1.5)

    # Colorazione delle celle
    cell_colors = {
        cell: (colorHead, {"weight": "bold"})
        if table[cell].get_text().get_text() in headers
        else (colorCell, {})
        for cell in table._cells
        if cell[0] % 2 == 0
    }

    # Imposta il colore delle celle
    for cell, (color, text_props) in cell_colors.items():
        # imposta il colore della cella
        table[cell].set_facecolor(color)
        # imposta le proprietà del testo della cella
        table[cell].set_text_props(**text_props)

    #plt.show()

    # Salvataggio del grafico
    fig.savefig(f"plots/tables/{filename}.png", bbox_inches='tight')


def draw_side_graphs(left_data, right_data, plot_title, filename):
    fig, (left, right) = plt.subplots(1, 2, figsize=(15, 5))

    # Insertion sort, grafico a sinistra
    left.plot(x_axis, left_data, color=color1)
    left.set_title(label1)
    left.set_xlabel(xlabel)
    left.set_ylabel(ylabel)
    #left.legend(handles=[legend1])

    # Quick sort, grafico a destra
    right.plot(x_axis, right_data, color=color2)
    right.set_title(label2)
    right.set_xlabel(xlabel)
    right.set_ylabel(ylabel)
    #right.legend(handles=[legend2])

    fig.suptitle(plot_title, fontsize=16)
    #plt.show()

    # salvataggio del grafico
    fig.savefig(f"./plots/side-graphs/{filename}.png", bbox_inches='tight')


def draw_comparison_graphs(data1, data2, title, filename):
    fig, plot = plt.subplots(1, 1, figsize=(15, 12))
    plot.plot(x_axis, data1, label=label1, color=color1)
    plot.plot(x_axis, data2, label=label2, color=color2)
    plot.set_title(title)
    plot.set_xlabel(xlabel)
    plot.set_ylabel(ylabel)
    plot.legend(handles=[legend1, legend2])

    #plt.show()

    # salvataggio del grafico
    fig.savefig(f"./plots/comparison-graphs/{filename}.png", bbox_inches='tight')


if __name__ == '__main__':

    step, nTests = 50, 20

    #step, nTests = 10, 100
    #step, nTests = 200, 50
    #step, nTests = 500, 20

    ts = [100, 250, 1000]

    # Creazione degli array randomici
    arrays = []
    for n in range(step, step * (nTests + 1), step):
        arrays.append(random_array(n))

    opname1, opname2 = "insert", "search"

    x_axis = [n for n in range(step, step * (nTests + 1), step)]
    label1, color1 = "Albero Binario di Ricerca", "black"
    label2, color2 = "B-Albero", "red"
    xlabel, ylabel = "Dimensione dell'array (n)", "Tempo di esecuzione [ms]"
    legend1, legend2 = mpatch.Patch(label=label1, color=color1), mpatch.Patch(label=label2, color=color2)

    # Creazione delle cartelle
    directory = ["plots", "plots/tables", "plots/side-graphs", "plots/comparison-graphs"]
    for dir in directory:
        if not os.path.exists(dir):
            os.makedirs(dir)

    # Test
    for i in range(len(ts)):
        #t = ts[i]
        t = 250
        print(f"\nTest {i + 1}: t = ", t)
        # Reset delle liste tempi per un certo t

        BinaryTrees, BTrees = [], []
        InsertTimesTitle, SearchTimesTitle = [], []
        InsertWRTitle, SearchWRTitle = [], []
        InsertTimesData, SearchTimesData = [], []
        InsertWRData, SearchWRData = [], []
        timesInsertBin, timesInsertBT = [], []
        timesSearchBin, timesSearchBT = [], []
        readInsertBin, readInsertBT, writtenInsertBin, writtenInsertBT = [], [], [], []
        readSearchBin, readSearchBT, writtenSearchBin, writtenSearchBT = [], [], [], []
        j = -1
        for a in arrays:
            j += 1
            # Inizializzazione alberi
            BinaryTrees.append(BinaryTree())
            BTrees.append(BTree(t))

            # Test inserimento
            tInsertBin, tInsertBT, rInsertBin, rInsertBT, wInsertBin, wInsertBT = test_insert(BinaryTrees[j], BTrees[j], a)
            timesInsertBin.append(tInsertBin)
            timesInsertBT.append(tInsertBT)
            readInsertBin.append(rInsertBin)
            readInsertBT.append(rInsertBT)
            writtenInsertBin.append(wInsertBin)
            writtenInsertBT.append(wInsertBT)

            # Test ricerca
            tSearchBin, tSearchBT, rSearchBin, rSearchBT, wSearchBin, wSearchBT = test_search(BinaryTrees[j], BTrees[j], a)
            timesSearchBin.append(tSearchBin)
            timesSearchBT.append(tSearchBT)
            readSearchBin.append(rSearchBin)
            readSearchBT.append(rSearchBT)
            writtenSearchBin.append(wSearchBin)
            writtenSearchBT.append(wSearchBT)

        # end ciclo su t in ts

        # Creazione dei dati per le tabelle
        InsertTimesData.append([
            [n for n in range(step, step * (nTests + 1), step)],
            ["{:.3e}".format(val) for val in timesInsertBin],
            ["{:.3e}".format(val) for val in timesInsertBT]
        ])
        InsertTimesTitle.append(f"Inserimento con t = {t}: tempi di esecuzione [ms]")

        InsertWRData.append([
            [n for n in range(step, step * (nTests + 1), step)],
            ["{:.3e}".format(val) for val in readInsertBin],
            ["{:.3e}".format(val) for val in readInsertBT],
            ["{:.3e}".format(val) for val in writtenInsertBin],
            ["{:.3e}".format(val) for val in writtenInsertBT]
        ])
        InsertWRTitle.append(f"Inserimento con t = {t}: letture e scritture")

        SearchTimesData.append([
            [n for n in range(step, step * (nTests + 1), step)],
            ["{:.3e}".format(val) for val in timesSearchBin],
            ["{:.3e}".format(val) for val in timesSearchBT]
        ])
        SearchTimesTitle.append(f"Ricerca con t = {t}: tempi di esecuzione [ms]")

        SearchWRData.append([
            [n for n in range(step, step * (nTests + 1), step)],
            ["{:.3e}".format(val) for val in readSearchBin],
            ["{:.3e}".format(val) for val in readSearchBT],
            ["{:.3e}".format(val) for val in writtenSearchBin],
            ["{:.3e}".format(val) for val in writtenSearchBT]
        ])
        SearchWRTitle.append(f"Ricerca con t = {t}: letture e scritture")

        filename1 = f"{opname1}-ms-t{t}"
        filename2 = f"{opname2}-ms-t{t}"
        filename3 = f"{opname1}-wr-t{t}"
        filename4 = f"{opname2}-wr-t{t}"

        # Creazione delle tabelle
        draw_table(InsertTimesData[i], InsertTimesTitle[i], "green", "lightgreen", filename1)
        draw_table(SearchTimesData[i], InsertTimesTitle[i], "purple", "pink", filename2)
        draw_table(InsertWRData[i], InsertWRTitle[i], "green", "lightgreen", filename3)
        draw_table(SearchWRData[i], SearchWRTitle[i], "purple", "pink", filename4)

        # Creazione dei grafici
        draw_side_graphs(timesInsertBin, timesInsertBT, "Inserimento", filename1)
        draw_side_graphs(timesSearchBin, timesSearchBT, "Ricerca", filename2)
        draw_side_graphs(readInsertBin, readInsertBT, "Inserimento: letture", filename3)
        draw_side_graphs(readSearchBin, readSearchBT, "Ricerca: letture", filename4)

        # Confronto dei grafici
        draw_comparison_graphs(timesInsertBin, timesInsertBT, "Confronto inserimento", filename1)
        draw_comparison_graphs(timesSearchBin, timesSearchBT, "Confronto ricerca", filename2)
        draw_comparison_graphs(readInsertBin, readInsertBT, "Confronto inserimento: letture", filename3)
        draw_comparison_graphs(readSearchBin, readSearchBT, "Confronto ricerca: letture", filename4)