import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Button, TextBox
import numpy as np

# --- Recorridos automáticos ---
def obtener_recorrido(Grafo, source_node="1", tipo_busqueda="DFS"):
    if tipo_busqueda.upper() == "DFS":
        recorrido = list(nx.dfs_preorder_nodes(Grafo, source=source_node))
    elif tipo_busqueda.upper() == "BFS":
        edges = nx.bfs_edges(Grafo, source=source_node)
        recorrido = [source_node] + [v for u, v in edges]
    else:
        raise ValueError("Tipo de búsqueda no soportado. Usa 'DFS' o 'BFS'.")
    return recorrido

# --- Configuración del grafo base ---
def setup_graph(ax):
    Grafo = nx.Graph()
    edges = [
        ('1', '2'), ('1', '5'), ('1', '1'),
        ('2', '3'), ('2', '5'),
        ('3', '4'),
        ('4', '5'), ('4', '6')
    ]
    Grafo.add_edges_from(edges)

    pos = {
        '1': (1.5, 1.0),
        '2': (1.0, 2.5),
        '5': (2.5, 2.0),
        '3': (1.8, 4.0),
        '4': (3.5, 3.5),
        '6': (4.5, 4.0)
    }

    ax.clear()
    ax.set_title('Recorrido en Grafo', fontsize=16)
    nx.draw_networkx_edges(Grafo, pos, ax=ax, width=1.5, edge_color='gray')
    nx.draw_networkx_nodes(Grafo, pos, node_size=1200, node_color='lightgray', edgecolors='navy', ax=ax)
    nx.draw_networkx_labels(Grafo, pos, font_size=16, font_weight='bold', ax=ax)
    ax.set_axis_off()

    luz = ax.scatter([], [], s=1800, c='yellow', edgecolors='black', linewidths=1.5, zorder=3)
    texto = ax.text(0.5, -0.05, "Esperando recorrido...", transform=ax.transAxes, ha="center", fontsize=14, color="blue")

    return Grafo, pos, luz, texto

# --- Animación paso a paso ---
def actualizar(frame, pos, recorrido, luz, texto):
    nodo_actual = recorrido[frame]
    xy = np.array([pos[nodo_actual]])
    luz.set_offsets(xy)
    texto.set_text(f"Nodo Actual: {nodo_actual} (Paso {frame+1}/{len(recorrido)})")
    return luz, texto

# --- Ejecutar DFS o BFS ---
def ejecutar_tipo(tipo):
    global anim, Grafo, pos, luz, texto
    recorrido = obtener_recorrido(Grafo, source_node="1", tipo_busqueda=tipo)
    print(f"{tipo.upper()} → {recorrido}")
    anim = FuncAnimation(fig, actualizar, fargs=(pos, recorrido, luz, texto),
                         frames=len(recorrido), interval=1500, repeat=False, blit=True)
    plt.draw()

# --- Ejecutar recorrido manual ---
def ejecutar_manual(event):
    global anim, pos, luz, texto
    entrada = textbox_manual.text.strip()
    nodos = [n.strip() for n in entrada.split(',') if n.strip() in pos_base]
    if not nodos:
        print("Recorrido inválido o nodos no reconocidos.")
        return
    print(f"Recorrido manual: {nodos}")
    anim = FuncAnimation(fig, actualizar, fargs=(pos, nodos, luz, texto),
                         frames=len(nodos), interval=1500, repeat=False, blit=True)
    plt.draw()

# --- Inicialización ---
fig, ax = plt.subplots(figsize=(8, 8))
plt.subplots_adjust(bottom=0.3)

# Posiciones base para validación
pos_base = {
    '1': (1.5, 1.0),
    '2': (1.0, 2.5),
    '5': (2.5, 2.0),
    '3': (1.8, 4.0),
    '4': (3.5, 3.5),
    '6': (4.5, 4.0)
}

# Botones DFS y BFS
ax_dfs = plt.axes([0.15, 0.05, 0.2, 0.06])
ax_bfs = plt.axes([0.65, 0.05, 0.2, 0.06])
btn_dfs = Button(ax_dfs, 'Recorrido DFS')
btn_bfs = Button(ax_bfs, 'Recorrido BFS')
btn_dfs.on_clicked(lambda event: ejecutar_tipo("DFS"))
btn_bfs.on_clicked(lambda event: ejecutar_tipo("BFS"))

# Caja de texto y botón manual
ax_manual = plt.axes([0.15, 0.18, 0.7, 0.05])
textbox_manual = TextBox(ax_manual, 'Recorrido Manual:', initial='1,2,5,4')

ax_btn_manual = plt.axes([0.35, 0.11, 0.3, 0.06])
btn_manual = Button(ax_btn_manual, 'Ejecutar Manual')
btn_manual.on_clicked(ejecutar_manual)

# Grafo inicial
Grafo, pos, luz, texto = setup_graph(ax)

plt.show()