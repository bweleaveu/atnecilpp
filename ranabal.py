import numpy as np
import pandas as pd
import plotly.graph_objects as go
import os

print("="*40)
print("3. VIZUALIZAREA POSTURII 3D (CU OASE)")
print("="*40)

folder_date = "w19"
cale_pose = os.path.join(folder_date, "w19_pose_3d.npy")
pose_3d = np.load(cale_pose)

# Extragem și remodelăm primul cadru
cadru_zero = pose_3d[0].reshape(-1, 3)
x = cadru_zero[:, 0]
y = cadru_zero[:, 1]
z = cadru_zero[:, 2]
numar_articulatii = cadru_zero.shape[0]

print(f"S-au detectat {numar_articulatii} articulații. Construim scheletul...")

# 1. Inițializăm graficul 3D
figura = go.Figure()

# 2. Definim "Harta" Oaselor în funcție de câte puncte avem în setul de date
legaturi = []
if numar_articulatii == 17: # Format COCO (ex: Human3.6M)
    legaturi = [(0,1), (0,2), (1,3), (2,4), (5,6), (5,7), (7,9), (6,8), (8,10), (5,11), (6,12), (11,12), (11,13), (13,15), (12,14), (14,16)]
elif numar_articulatii == 18: # Format OpenPose (foarte comun în MM-Fit)
    legaturi = [(1,2), (1,5), (2,3), (3,4), (5,6), (6,7), (1,8), (8,9), (9,10), (1,11), (11,12), (12,13), (1,0), (0,14), (14,16), (0,15), (15,17)]
elif numar_articulatii == 25: # Format Kinect
    legaturi = [(3,2), (2,20), (20,1), (1,0), (0,12), (0,16), (20,8), (20,4), (8,9), (9,10), (10,11), (4,5), (5,6), (6,7), (12,13), (13,14), (14,15), (16,17), (17,18), (18,19)]
elif numar_articulatii == 33: # Format MediaPipe / BlazePose
    legaturi = [(11,12), (11,13), (13,15), (12,14), (14,16), (11,23), (12,24), (23,24), (23,25), (24,26), (25,27), (26,28), (27,29), (28,30)]

# 3. Desenăm "Oasele" (liniile albastre)
for start, end in legaturi:
    if start < numar_articulatii and end < numar_articulatii:
        figura.add_trace(go.Scatter3d(
            x=[x[start], x[end]],
            y=[y[start], y[end]],
            z=[z[start], z[end]],
            mode='lines',
            line=dict(color='blue', width=4),
            showlegend=False
        ))

# 4. Desenăm Articulațiile (punctele roșii) deasupra oaselor
figura.add_trace(go.Scatter3d(
    x=x, y=y, z=z,
    mode='markers',
    marker=dict(size=6, color='red'),
    name='Articulații'
))

# 5. Setăm layout-ul corect pentru a nu deforma omul
figura.update_layout(
    title=f'Postura 3D - Schelet conectat ({numar_articulatii} puncte)',
    scene=dict(
        aspectmode='data', # FORȚEAZĂ PROPORȚIILE CORECTE 1:1:1
        xaxis=dict(title='X'),
        yaxis=dict(title='Y'),
        zaxis=dict(title='Z')
    ),
    margin=dict(l=0, r=0, b=0, t=40)
)

figura.show()