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

# import per la serializzazione e deserializzazione degli oggetti su disco.
import pickle
import os

# Albero binario di ricerca:
class BinaryTreeNode:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.parent = None
        self.leaf = True

class BinaryTree:
    def __init__(self):
        self.root = None

# B-Albero:
class BTreeNode:
    # è ok
    def __init__(self, tree, keys=None, children=None, leaf=True):
        self.tree = tree
        self.keys = keys or []
        self.children = children or []
        self.leaf = leaf
        if self.children:
            self.leaf = False
        for child in self.children:
            child.parent = self

    def __init__(self, n, keys=None, children=None, leaf=True):
        self.n = n                      # Numero massimo di chiavi
        self.leaf = leaf                # Flag per indicare se il nodo è una foglia
        self.keys = keys or []          # Lista di chiavi (vuota di default se non specificata)
        self.children = children or []  # Lista di puntatori ai figli (vuota di default se non specificata)

        def __str__(self):
            return str(self.keys)

        def __repr__(self):
            return str(self.keys)

        def __len__(self):
            return len(self.keys)

        def __getitem__(self, index):
            return self.keys[index]
        def __setitem__(self, index, value):
            self.keys[index] = value
        def __delitem__(self, index):
            del self.keys[index]

        def __contains__(self, key):
            return key in self.keys

        def orderKeys(self):
            self.keys.sort()



# Definizione della classe B-Albero
class BTree:
    def __init__(self, t):
        self.root = None
        self.t = t

    def __str__(self):
        return str(self.root)

    def search(self, key):
        return self.search_node(self.root, key)


    # Funzione per inserire una chiave in un albero
    def insert(self, key):
        if self.root is None:
            self.root = BTreeNode(self, key)
            write_to_disk('tree.dat', self)
            return
        else:
            self.insert_nonfull(self.root, key)
            write_to_disk('tree.dat', self)

    # Funzione per inserire una chiave in un nodo non pieno
    def insert_nonfull(self, node, key):
        if node is None:
            return
        if node.left is None and node.right is None:
            if node.key < key:
                node.right = TreeNode(key)
            else:
                node.left = TreeNode(key)
            return
        if node.key < key:
            if node.right is None:
                node.right = TreeNode(key)
            else:
                self.insert_nonfull(node.right, key)
        else:
            if node.left is None:
                node.left = TreeNode(key)
            else:
                self.insert_nonfull(node.left, key)


# Funzione per scrivere un oggetto su disco
def write_to_disk(filename, data):
    with open(filename, 'wb') as f:
        pickle.dump(data, f)

# Funzione per leggere un oggetto da disco
def read_from_disk(filename):
    with open(filename, 'rb') as f:
        return pickle.load(f)

# Funzione per creare un nuovo albero
def create_btree(t):
    tree = BTree(t)
    write_to_disk('tree.dat', tree)
    return tree

# Funzione per inserire una chiave in un albero
def insert(tree, key):
    if tree.root is None:
        tree.root = BTreeNode(key)
        write_to_disk('tree.dat', tree)
        return
    else:
        insert_nonfull(tree.root, key)
        write_to_disk('tree.dat', tree)

# Funzione per inserire una chiave in un nodo non pieno
def insert_nonfull(node, key):
    if node is None:
        return
    if node.left is None and node.right is None:
        if node.key < key:
            node.right = TreeNode(key)
        else:
            node.left = TreeNode(key)
        return
    if node.key < key:
        if node.right is None:
            node.right = TreeNode(key)
        else:
            insert_nonfull(node.right, key)
    else:
        if node.left is None:
            node.left = TreeNode(key)
        else:
            insert_nonfull(node.left, key)

# Funzione per stampare un albero
def print_tree(tree):
    print_tree_node(tree.root)

# Funzione per stampare un nodo
def print_tree_node(node):
    if node is None:
        return
    print(node.key)
    print_tree_node(node.left)
    print_tree_node(node.right)

# Funzione per cercare una chiave in un albero
def search(tree, key):
    return search_node(tree.root, key)

# Funzione per cercare una chiave in un nodo
def search_node(node, key):
    if node is None:
        return False
    if node.key == key:
        return True
    if node.key < key:
        return search_node(node.right, key)
    else:
        return search_node(node.left, key)

# Funzione per cancellare una chiave in un albero
def delete(tree, key):
    delete_node(tree.root, key)
    write_to_disk('tree.dat', tree)

# Funzione per cancellare una chiave in un nodo
def delete_node(node, key):
    if node is None:
        return
    if node.key == key:
        if node.left is None and node.right is None:
            node = None
        elif node.left is None:
            node = node.right
        elif node.right is None:
            node = node.left
        else:
            node.key = min_value(node.right)
            delete_node(node.right, node.key)
    elif node.key < key:
        delete_node(node.right, key)
    else:
        delete_node(node.left, key)

# Funzione per trovare il minimo in un nodo
def min_value(node):
    if node.left is None:
        return node.key
    return min_value(node.left)

# Funzione per trovare il massimo in un nodo
def max_value(node):
    if node.right is None:
        return node.key
    return max_value(node.right)

# Funzione per trovare il successore di un nodo
def successor(node):
    if node.right is not None:
        return min_value(node.right)
    y = node.parent
    while y is not None and node == y.right:
        node = y
        y = y.parent
    return y

# Funzione per trovare il predecessore di un nodo
def predecessor(node):
    if node.left is not None:
        return max_value(node.left)
    y = node.parent
    while y is not None and node == y.left:
        node = y
        y = y.parent
    return y

# Funzione per stampare un albero in ordine
def inorder_tree_walk(tree):
    inorder_tree_walk_node(tree.root)

# Funzione per stampare un nodo in ordine
def inorder_tree_walk_node(node):
    if node is None:
        return
    inorder_tree_walk_node(node.left)
    print(node.key)
    inorder_tree_walk_node(node.right)

# Funzione per stampare un albero in ordine inverso
def reverse_inorder_tree_walk(tree):
    reverse_inorder_tree_walk_node(tree.root)

# Funzione per stampare un nodo in ordine inverso
def reverse_inorder_tree_walk_node(node):
    if node is None:
        return
    reverse_inorder_tree_walk_node(node.right)
    print(node.key)
    reverse_inorder_tree_walk_node(node.left)

# Funzione per stampare un albero in preordine
def preorder_tree_walk(tree):
    preorder_tree_walk_node(tree.root)

# Funzione per stampare un nodo in preordine
def preorder_tree_walk_node(node):
    if node is None:
        return
    print(node.key)
    preorder_tree_walk_node(node.left)
    preorder_tree_walk_node(node.right)

# Funzione per stampare un albero in postordine
def postorder_tree_walk(tree):
    postorder_tree_walk_node(tree.root)

# Funzione per stampare un nodo in postordine
def postorder_tree_walk_node(node):
    if node is None:
        return
    postorder_tree_walk_node(node.left)
    postorder_tree_walk_node(node.right)
    print(node.key)

# Funzione per stampare un albero in ampiezza
def breadth_first_tree_walk(tree):
    queue = [tree.root]
    while len(queue) > 0:
        node = queue.pop(0)
        print(node.key)
        if node.left is not None:
            queue.append(node.left)
        if node.right is not None:
            queue.append(node.right)

# Funzione per stampare un albero in ampiezza con livelli
def breadth_first_tree_walk_with_levels(tree):
    queue = [tree.root]
    while len(queue) > 0:
        node = queue.pop(0)
        print(node.key)
        if node.left is not None:
            queue.append(node.left)
        if node.right is not None:
            queue.append(node.right)

# Funzione per stampare un albero in ampiezza con livelli e nodi
def breadth_first_tree_walk_with_levels_and_nodes(tree):
    queue = [tree.root]
    while len(queue) > 0:
        nodes = queue
        queue = []
        for node in nodes:
            print(node.key)
            if node.left is not None:
                queue.append(node.left)
            if node.right is not None:
                queue.append(node.right)
        print('---')

# Funzione per stampare un albero in ampiezza con livelli e nodi e parenti
def breadth_first_tree_walk_with_levels_and_nodes_and_parents(tree):
    queue = [tree.root]
    while len(queue) > 0:
        nodes = queue
        queue = []
        for node in nodes:
            print(node.key)
            if node.left is not None:
                queue.append(node.left)
            if node.right is not None:
                queue.append(node.right)
        print('---')

if __name__ == '__main__':
    # Esempio di utilizzo

    # Creazione di un B-Albero
    b_tree = BTree(2)  # Modificare il parametro 't' a seconda delle specifiche

    # Esempio di inserimento di nodi nel B-Albero
    b_tree.insert(...)

    # Salvataggio del B-Albero su disco
    write_to_disk('b_tree.pkl', b_tree)

    # Lettura del B-Albero da disco
    b_tree_loaded = read_from_disk('b_tree.pkl')

    # Operazioni di confronto e benchmark tra B-Albero e albero binario di ricerca

    # Ad esempio, si possono implementare operazioni di inserimento, ricerca, cancellazione
    # e confrontare il numero di nodi letti o scritti su disco in entrambi i casi.

    # Alla fine dei test, è possibile confrontare i risultati ottenuti.

    # Non dimenticare di gestire i file temporanei generati durante l'esecuzione del programma.

    # Rimuovere i file temporanei generati
    os.remove('b_tree.pkl')