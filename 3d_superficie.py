import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import glob
import os
import numpy as np
from scipy.interpolate import griddata

# Ruta donde se almacenan los archivos de Excel
file_paths = glob.glob('/home/cruz/Documentos/UNAM/Animales_II/axon_calamar/*.xlsx')  # Busca todos los archivos Excel en la carpeta

# Crear una figura para el gráfico 3D
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Diferentes colores para cada archivo
colors = ['r', 'g', 'b', 'c', 'm', 'y', 'k']

# Inicializar los límites de los ejes
x_min, x_max = float('inf'), float('-inf')
y_min, y_max = float('inf'), float('-inf')
z_min, z_max = float('inf'), float('-inf')

# Iterar sobre los archivos y graficar los datos
for idx, file_path in enumerate(file_paths):
    # Cargar el archivo de Excel
    data = pd.read_excel(file_path, sheet_name=0)
    
    # Asumiendo columnas: 'External Concentration', 'Internal Concentration', 'Membrane Potential'
    try:
        external_conc = data['External Concentration']
        internal_conc = data['Internal Concentration']
        membrane_potential = data['Membrane Potential']
        
        # Obtener el nombre del archivo sin la extensión .xlsx
        file_name = os.path.splitext(os.path.basename(file_path))[0]

        # Color para este archivo
        color = colors[idx % len(colors)]

        # Graficar los datos de cada archivo como puntos
        scatter = ax.scatter(external_conc, internal_conc, membrane_potential, 
                            c=color, label=file_name, marker='o')

        # Actualizar límites de los ejes
        x_min = min(x_min, external_conc.min())
        x_max = max(x_max, external_conc.max())
        y_min = min(y_min, internal_conc.min())
        y_max = max(y_max, internal_conc.max())
        z_min = min(z_min, membrane_potential.min())
        z_max = max(z_max, membrane_potential.max())

    except KeyError as e:
        print(f"Missing column in {file_path}: {e}")

# Definir el valor mínimo común para los ejes de concentración
common_min = min(0, x_min, y_min)

# Establecer límites de los ejes con el valor mínimo común
ax.set_xlim([common_min, x_max])
ax.set_ylim([y_max, common_min])  # Invertir la orientación del eje de concentración interna
ax.set_zlim([z_min, z_max])

# Etiquetas de los ejes
ax.set_xlabel('External Ion Concentration')
ax.set_ylabel('Internal Ion Concentration')
ax.set_zlabel('Membrane Potential (mV)')

# Graficar la superficie
for idx, file_path in enumerate(file_paths):
    # Cargar el archivo de Excel
    data = pd.read_excel(file_path, sheet_name=0)
    
    try:
        external_conc = data['External Concentration']
        internal_conc = data['Internal Concentration']
        membrane_potential = data['Membrane Potential']
        
        # Crear una malla de puntos para la interpolación de la superficie
        grid_x, grid_y = np.mgrid[x_min:x_max:100j, y_min:y_max:100j]
        grid_z = griddata((external_conc, internal_conc), membrane_potential, (grid_x, grid_y), method='cubic')

        # Verificar si grid_z tiene valores válidos
        if np.all(np.isnan(grid_z)):
            print(f"Warning: No valid grid_z values for file {file_path}. Skipping surface plot.")
            continue

        # Color para este archivo
        color = colors[idx % len(colors)]

        # Graficar la superficie con el mismo color que los puntos pero más transparente
        ax.plot_surface(grid_x, grid_y, grid_z, color=color, alpha=0.3, rstride=10, cstride=10)  # Ajustar rstride y cstride para suavizar

    except KeyError as e:
        print(f"Missing column in {file_path}: {e}")

# Agregar leyenda con los nombres de los archivos
ax.legend()

# Guardar el gráfico como imagen en lugar de mostrarlo, si hay problemas con la GUI
plt.savefig('/home/cruz/Documentos/UNAM/Animales_II/axon_calamar/3d_scatter_plot_with_surface.png')

# Mostrar el gráfico
plt.show()

plt.show()

plt.show()
