import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# 1. Cargar el CSV y solo leer las columnas necesarias
archivo_csv = "transacciones.csv"  # Reemplaza con el nombre de tu archivo
df = pd.read_csv(archivo_csv, usecols=["Cuenta", "Codigo", "Importe"], dtype={"Cuenta": str, "Codigo": str, "Importe": float}, encoding="latin1")

# 2. Eliminar filas con valores nulos en las columnas clave
df = df.dropna(subset=["Cuenta", "Codigo", "Importe"])

# 3. Crear el grafo dirigido
G = nx.DiGraph()

# 4. Agregar nodos y aristas con pesos
for _, row in df.iterrows():
    origen = row["Cuenta"]
    destino = row["Codigo"]
    monto = row["Importe"]
    
    if G.ha_edge(origen, destino):
        G[origen][destino]["weight"] += monto  # Sumar montos si la transacción ya existe
    else:
        G.add_edge(origen, destino, weight=monto)

# 5. Dibujar la red de transacciones
plt.figure(figsize=(12, 7))
pos = nx.spring_layout(G, seed=42)  # Distribuir los nodos en el gráfico

# Dibujar nodos y aristas
nx.draw(G, pos, with_labels=True, node_size=800, node_color="lightblue", edge_color="gray", font_size=8, font_weight="bold")

# Dibujar etiquetas con montos de transacción
edge_labels = {(u, v): f"{d['weight']:.2f}" for u, v, d in G.edges(data=True)}
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=7)

plt.title("Red de Transacciones")
plt.show()
