import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import glob
import os

# Ruta donde se almacenan los archivos de Excel
file_paths = glob.glob('/home/cruz/Documentos/UNAM/Animales_II/celula_muscular/*.xlsx')  # Busca todos los archivos Excel en la carpeta

# Crear una figura para el gráfico 3D
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Diferentes colores para cada archivo
colors = ['r', 'g', 'b', 'c', 'm', 'y', 'k']

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

        # Graficar los datos de cada archivo
        ax.scatter(external_conc, membrane_potential, internal_conc, 
                   c=colors[idx % len(colors)], label=file_name, marker='o')

    except KeyError as e:
        print(f"Missing column in {file_path}: {e}")

# Etiquetas de los ejes
ax.set_xlabel('External Ion Concentration')
ax.set_zlabel('Membrane Potential (mV)')
ax.set_ylabel('Internal Ion Concentration')

# Agregar leyenda con los nombres de los archivos
ax.legend()

# Guardar el gráfico como imagen en lugar de mostrarlo, si hay problemas con la GUI
plt.savefig('/home/cruz/Documentos/UNAM/Animales_II/celula_muscular/3d_scatter_plot.png')

# Mostrar el gráfico
plt.show()
