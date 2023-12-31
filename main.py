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

    def find_node(self, currentNode, key):
        if currentNode is None:
            return False
        elif key == currentNode.key:
            self.node_read += 1
            return True
        elif key < currentNode.key:
            self.node_read += 1
            return self.find_node(currentNode.left, key)
        elif key > currentNode.key:
            self.node_read += 1
            return self.find_node(currentNode.right, key)

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

    def min(self, x):
        if x.left is None:
            return x
        else:
            return self.min(x.left)

    def max(self, x):
        if x.right is None:
            return x
        else:
            return self.max(x.right)

    def transplant(self, u, v):
        if u.p is None:
            self.root = v
        elif u == u.p.left:
            u.p.left = v
        else:
            u.p.right = v
        if v is not None:
            v.p = u.p

    def delete(self, key):
        z = self.search(self.root, key)
        if z.left is None:
            self.transplant(z, z.right)
        elif z.right is None:
            self.transplant(z, z.left)
        else:
            y = self.min(z.right)
            if y.p != z:
                self.transplant(y, y.right)
                y.right = z.right
                y.right.p = y
            self.transplant(z, y)
            y.left = z.left
            y.left.p = y


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

    def delete(self, key):
        node, index = self.search(key)
        if node is not None:
            if node.leaf:
                self.delete_from_leaf(node, index)
            else:
                self.delete_from_non_leaf(node, index)
        else:
            print("The key %d is does not exist in the tree" % key)

    def delete_from_leaf(self, node, index):
        for i in range(index + 1, node.n):
            node.keys[i - 1] = node.keys[i]
        node.n -= 1
        node.node_written += 1

    def delete_from_non_leaf(self, node, index):
        key = node.keys[index]
        if node.child[index].n >= self.t:
            pred = self.get_predecessor(node, index)
            node.keys[index] = pred
            self.delete_from_leaf(node.child[index], pred)
        elif node.child[index + 1].n >= self.t:
            succ = self.get_successor(node, index)
            node.keys[index] = succ
            self.delete_from_leaf(node.child[index + 1], succ)
        else:
            self.merge(node, index)
            self.delete_from_non_leaf(node.child[index], key)

    def print(self, x, l=0):
        print("Level ", l, " ", len(x.keys), end=":")
        for i in x.keys:
            print(i, end=" ")
        print()
        l += 1
        if len(x.child) > 0:
            for i in x.child:
                self.print(i, l)

    def merge(self, node, index):
        child = node.child[index]
        sibling = node.child[index + 1]
        child.keys[self.t - 1] = node.keys[index]
        for i in range(sibling.n):
            child.keys[i + self.t] = sibling.keys[i]
        if not child.leaf:
            for i in range(sibling.n + 1):
                child.child[i + self.t] = sibling.child[i]
        for i in range(index + 1, node.n):
            node.keys[i - 1] = node.keys[i]
        for i in range(index + 2, node.n + 1):
            node.child[i - 1] = node.child[i]
        child.n += sibling.n + 1
        node.n -= 1
        node.node_written += 1
        child.node_written += 1
        sibling.node_written += 1

    def get_predecessor(self, node, index):
        node = node.child[index]
        while not node.leaf:
            node = node.child[node.n]
        return node.keys[node.n - 1]

    def get_successor(self, node, index):
        node = node.child[index + 1]
        while not node.leaf:
            node = node.child[0]
        return node.keys[0]


# Creazione di un array randomico di n elementi
def random_array(n):
    return [rand(1, n) for _ in range(n)]


def test_search(BinaryTree, BTree, array):
    print(f"\nTempi di ricerca di {len(array)} elementi:")

    timesBin = 0
    timesBT = 0
    for i in range(len(array)):
        #print(f"{array[i]} ({i + 1}° elemento)")

        start = timer()
        BinaryTree.search(BinaryTree.root, array[i])
        end = timer()
        timesBin += (end - start) * 1000

        start = timer()
        BTree.search(array[i])
        end = timer()
        timesBT += (end - start) * 1000

    print(f"Albero binario di ricerca: {timesBin} ms")
    print(f"B-albero: {timesBT} ms")

    return timesBin, timesBT


def test_insert(BinaryTree, BTree, array):
    print(f"\nTempi di inserimento di {len(array)} elementi:")
    timesBin = 0
    timesBT = 0
    for i in range(len(array)):
        #print(f"{array[i]} ({i + 1}° elemento)")

        start = timer()
        BinaryTree.insert(BinaryTreeNode(array[i]))
        end = timer()
        timesBin += (end - start) * 1000

        start = timer()
        BTree.insert(array[i])
        end = timer()
        timesBT += (end - start) * 1000

    print(f"Albero binario di ricerca: {timesBin} ms")
    print(f"B-albero: {timesBT} ms")

    return timesBin, timesBT


def test_delete(BinaryTree, BTree, array):
    print(f"\nTempi di cancellazione di {len(array)} elementi:")
    timesBin = 0
    timesBT = 0
    for i in range(len(array)):
        #print(f"{array[i]} ({i + 1}° elemento)")

        start = timer()
        BinaryTree.delete(array[i])
        end = timer()
        timesBin += (end - start) * 1000

        start = timer()
        BTree.delete(array[i])
        end = timer()
        timesBT += (end - start) * 1000

    print(f"Albero binario di ricerca: {timesBin} ms")
    print(f"B-albero: {timesBT} ms")
    return timesBin, timesBT


def draw_table(data, title, colorHead="orange", colorCell="yellow", filename = "table"):
    # Crea un nuovo grafico
    figSizeX = 8
    figSizeY = nTests / 3 + 1
    fig, ax = plt.subplots(figsize=(figSizeX, figSizeY))
    plt.title(title)

    # Unisci le liste di dati come colonne al fine di creare un array bidimensionale di dati: 'data'
    print(len(data[0]), len(data[1]), len(data[2]))
    data = np.stack(tuple(data), axis=1)

    # Intestazioni della tabella
    headers = ("N° elementi", "Albero Binario di Ricerca", "B-Albero")

    # Stile tabella
    ax.axis('off')
    table = ax.table(cellText=data, colLabels=headers, loc='center', cellLoc='center')
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
    dir = "plots/tables"
    if not os.path.exists(dir):
        os.makedirs(dir)
    path = f"./plots/tables/{filename}.png"
    fig.savefig(f"plots/table/{filename}.png", bbox_inches='tight')


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
    plt.show()

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

    plt.show()

    # salvataggio del grafico
    fig.savefig(f"./plots/comparison-graphs/{filename}.png", bbox_inches='tight')


if __name__ == '__main__':

    # Parametri step * nTests = 10000
    #step, nTests = 100, 10

    #step, nTests = 100, 100
    #step, nTests = 200, 50
    #step, nTests = 500, 20
    #step, nTests = 1000, 10
    step, nTests = 2000, 5

    ts = [100, 250, 1000]

    #ts = [20, 50, 100, 500, 1000]

    #ts = [2, 3, 20, 50]
    #ts = [2, 3, 5, 10]
    #ts = [2, 3]

    # Creazione degli array randomici
    arrays = []
    for n in range(step, step * (nTests + 1), step):
        arrays.append(random_array(n))

    # Inizializzazione liste alberi
    BinaryTrees, BTrees = [], []
    InsertTitle, SearchTitle, DeleteTitle = [], [], []
    InsertData, SearchData, DeleteData = [], [], []
    opname1, opname2, opname3 = "insert", "search", "delete"

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
    i = -1
    for t in ts:
        i += 1
        print(f"\nTest {i + 1}: t = ", t)
        # Reset delle liste tempi per un certo t
        timesInsertBin, timesInsertBT = [], []
        timesSearchBin, timesSearchBT = [], []
        timesDeleteBin, timesDeleteBT = [], []
        for a in arrays:
            # Inizializzazione alberi
            BinaryTrees.append(BinaryTree())
            BTrees.append(BTree(t))

            # Test
            tInsertBin, tInsertBT = test_insert(BinaryTrees[i], BTrees[i], a)
            tSearchBin, tSearchBT = test_search(BinaryTrees[i], BTrees[i], a)
            #tDeleteBin, tDeleteBT = test_delete(BinaryTrees[i], BTrees[i], a)
            timesInsertBin.append(tInsertBin)
            timesInsertBT.append(tInsertBT)
            timesSearchBin.append(tSearchBin)
            timesSearchBT.append(tSearchBT)
            #timesDeleteBin.append(tDeleteBin)
            #timesDeleteBT.append(tDeleteBT)

        # end ciclo su t in ts

        # Creazione dei dati per le tabelle
        InsertData.append([
            [n for n in range(step, step * (nTests + 1), step)],
            ["{:.3e}".format(val) for val in timesInsertBin],
            ["{:.3e}".format(val) for val in timesInsertBT]
        ])
        InsertTitle.append(f"Inserimento con t = {t}: tempi di esecuzione [ms]")

        SearchData.append([
            [n for n in range(step, step * (nTests + 1), step)],
            ["{:.3e}".format(val) for val in timesSearchBin],
            ["{:.3e}".format(val) for val in timesSearchBT]
        ])
        SearchTitle.append(f"Ricerca con t = {t}: tempi di esecuzione [ms]")

        #DeleteData.append([
        #    [n for n in range(step, step * (nTests + 1), step)],
        #    ["{:.3e}".format(val) for val in timesDeleteBin],
        #    ["{:.3e}".format(val) for val in timesDeleteBT]
        #])
        #DeleteTitle.append(f"Cancellazione con t = {t}: tempi di esecuzione [ms]")

        filename1 = f"{opname1}-t{t}"
        filename2 = f"{opname2}-t{t}"
        filename3 = f"{opname3}-t{t}"

        # Creazione delle tabelle
        #draw_table(InsertData[i], InsertTitle[i], "green", "lightgreen", filestring1)
        #draw_table(SearchData[i], InsertTitle[i], "purple", "pink", filestring2)
        #draw_table(DeleteData[i], InsertTitle[i], "darkredred", "red" filestring3)

        # Creazione dei grafici
        draw_side_graphs(timesInsertBin, timesInsertBT, "Inserimento", filename1)
        draw_side_graphs(timesSearchBin, timesSearchBT, "Ricerca", filename2)
        #draw_side_graphs(timesDeleteBin, timesDeleteBT, "Cancellazione", filestring3)

        # Confronto dei grafici
        draw_comparison_graphs(timesInsertBin, timesInsertBT, "Confronto inserimento", filename1)
        draw_comparison_graphs(timesSearchBin, timesSearchBT, "Confronto ricerca", filename2)
        #draw_comparison_graphs(timesDeleteBin, timesDeleteBT, "Confronto cancellazione", filestring3)