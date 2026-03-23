from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import pandas as pd
import numpy as np
import folium
import os
import webbrowser
import math
from branca.element import Element
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from PIL import Image

# WEG & Marathon warehouses
warehouses = [
    {"Warehouse Name": "Marathon (IKC)", "Latitude": 39.0228, "Longitude": -94.672, "Segments": "Generator, Electric Motor", "Empresa": "WEG e Marathon"},
    {"Warehouse Name": "Marathon (ITX)", "Latitude": 32.7767, "Longitude": -96.797, "Segments": "Generator, Electric Motor", "Empresa": "WEG e Marathon"},
    {"Warehouse Name": "Marathon (IMP)", "Latitude": 44.8408, "Longitude": -93.2983, "Segments": "Generator, Electric Motor", "Empresa": "WEG e Marathon"},
    {"Warehouse Name": "Marathon (ICH)", "Latitude": 41.9312, "Longitude": -87.9887, "Segments": "Generator, Electric Motor", "Empresa": "WEG e Marathon"},
    {"Warehouse Name": "Marathon (ITL)", "Latitude": 33.7768, "Longitude": -84.6547, "Segments": "Generator, Electric Motor", "Empresa": "WEG e Marathon"},
    {"Warehouse Name": "Marathon Canada Corp.", "Latitude": 43.589, "Longitude": -79.6441, "Segments": "Generator, Electric Motor", "Empresa": "WEG e Marathon"},
    {"Warehouse Name": "Marathon (INC)", "Latitude": 35.4737, "Longitude": -88.6843, "Segments": "Generator, Electric Motor", "Empresa": "WEG e Marathon"},
    {"Warehouse Name": "Marathon (IPA)", "Latitude": 27.9506, "Longitude": -82.4572, "Segments": "Generator, Electric Motor", "Empresa": "WEG e Marathon"},
    {"Warehouse Name": "Warehouse (IAT)", "Latitude": 40.8951, "Longitude": -75.7321, "Segments": "Generator, Electric Motor", "Empresa": "WEG e Marathon"},
    {"Warehouse Name": "Warehouse (IBO)", "Latitude": 42.1474, "Longitude": -71.8894, "Segments": "Generator, Electric Motor", "Empresa": "WEG e Marathon"},
    {"Warehouse Name": "WEG PRODUCT WAREHOUSE - WASHINGTON", "Latitude": 47.3997, "Longitude": -122.248, "Segments": "Generator, Electric Motor", "Empresa": "WEG e Marathon"},
    {"Warehouse Name": "WEG PRODUCT WAREHOUSE - CALIFORNIA", "Latitude": 34.0634, "Longitude": -117.6200, "Segments": "Generator, Electric Motor", "Empresa": "WEG e Marathon"},
    {"Warehouse Name": "WEG PRODUCT WAREHOUSE - TEXAS", "Latitude": 30.0121, "Longitude": -95.4266, "Segments": "Generator, Electric Motor", "Empresa": "WEG e Marathon"},
    {"Warehouse Name": "WEG PRODUCT WAREHOUSE - KANSAS", "Latitude": 39.1135, "Longitude": -94.8142, "Segments": "Generator, Electric Motor", "Empresa": "WEG e Marathon"},
    {"Warehouse Name": "WEG PRODUCT WAREHOUSE - ILLINOIS", "Latitude": 41.6458, "Longitude": -88.1024, "Segments": "Generator, Electric Motor", "Empresa": "WEG e Marathon"},
    {"Warehouse Name": "WEG PRODUCT WAREHOUSE - PENNSYLVANIA", "Latitude": 40.2365, "Longitude": -77.0809, "Segments": "Generator, Electric Motor", "Empresa": "WEG e Marathon"},
    {"Warehouse Name": "WEG PRODUCT WAREHOUSE - GEORGIA", "Latitude": 34.0086, "Longitude": -84.0890, "Segments": "Generator, Electric Motor", "Empresa": "WEG e Marathon"},
    # Schneider Electric
    {"Warehouse Name": "Schneider Electric (TXA)", "Latitude": 32.2205, "Longitude": -95.8306, "Segments": "Power Distribution, Industrial Automation", "Empresa": "Schneider Electric"},
    {"Warehouse Name": "Schneider Electric (TN)", "Latitude": 36.2080, "Longitude": -86.5186, "Segments": "Switchgear, Medium Voltage Equipment", "Empresa": "Schneider Electric"},
    {"Warehouse Name": "Schneider Electric (CA)", "Latitude": 34.0922, "Longitude": -117.4350, "Segments": "Electrical Distribution, Data Center Solutions", "Empresa": "Schneider Electric"},
    {"Warehouse Name": "Schneider Electric (GA)", "Latitude": 31.4174, "Longitude": -81.1526, "Segments": "Logistics Hub, Electrical Components", "Empresa": "Schneider Electric"},
    {"Warehouse Name": "Schneider Electric (IN)", "Latitude": 39.5296, "Longitude": -119.8138, "Segments": "Power Systems, Smart Grid Components", "Empresa": "Schneider Electric"},
    {"Warehouse Name": "Schneider Electric (MN)", "Latitude": 36.8468, "Longitude": -76.2859, "Segments": "Backup Power, Grid Distribution", "Empresa": "Schneider Electric"},
    {"Warehouse Name": "Schneider Electric (NJ)", "Latitude": 40.5565, "Longitude": -74.2551, "Segments": "Distribution Equipment, Electrical Panels", "Empresa": "Schneider Electric"},
    {"Warehouse Name": "Schneider Electric (MA)", "Latitude": 47.2529, "Longitude": -122.4443, "Segments": "Automation Systems, Control Panels", "Empresa": "Schneider Electric"},
    # Nidec
    {"Warehouse Name": "Advanced Motors & Drives (Sales Office)", "Latitude": 43.0957, "Longitude": -76.0590, "Segments": "Special purpose AC, DC and brushless DC motors", "Empresa": "Nidec"},
    {"Warehouse Name": "NIDEC MOTOR CORPORATION LTD (METALFORT)", "Latitude": 41.6008, "Longitude": -80.5600, "Segments": "", "Empresa": "Nidec"},
    {"Warehouse Name": "NIDEC MOTOR CORPORATION NIS US", "Latitude": 41.4380, "Longitude": -81.6650, "Segments": "", "Empresa": "Nidec"},
    {"Warehouse Name": "Nidec Motor Corporation", "Latitude": 40.3675, "Longitude": -86.5272, "Segments": "R&D, Manufacturing and Sales of Industrial, Commercial and Appliance Motors and Controls", "Empresa": "Nidec"},
    {"Warehouse Name": "NIDEC MOTOR CORPORATION MINA", "Latitude": 33.7249, "Longitude": -92.0763, "Segments": "", "Empresa": "Nidec"},
    {"Warehouse Name": "NIDEC GEMPAKER AUTOMATION, INC.", "Latitude": 37.5485, "Longitude": -121.9886, "Segments": "Manufacture and sale of high-precision robotics for the semiconductor, data storage, and flat panel display industries", "Empresa": "Nidec"},
]

# Data Centers
data_centers = [
    {"City": "Northwest", "Latitude": 47.6062, "Longitude": -122.3321, "Segment": "Primary markets"},
    {"City": "Northern California", "Latitude": 38.5758, "Longitude": -121.4789, "Segment": "Primary markets"},
    {"City": "Phoenix", "Latitude": 33.4484, "Longitude": -112.0747, "Segment": "Primary markets"},
    {"City": "Dallas", "Latitude": 32.7767, "Longitude": -96.797, "Segment": "Primary markets"},
    {"City": "Chicago", "Latitude": 41.8781, "Longitude": -87.6298, "Segment": "Primary markets"},
    {"City": "Northern Virginia", "Latitude": 38.881, "Longitude": -77.1043, "Segment": "Primary markets"},
    {"City": "Wyoming", "Latitude": 41.1399, "Longitude": -104.8202, "Segment": "Secondary markets"},
    {"City": "Omaha", "Latitude": 41.2565, "Longitude": -95.9345, "Segment": "Secondary markets"},
    {"City": "Kansas", "Latitude": 39.0558, "Longitude": -95.689, "Segment": "Secondary markets"},
    {"City": "Oklahoma", "Latitude": 35.4676, "Longitude": -97.5164, "Segment": "Secondary markets"},
    {"City": "Indiana", "Latitude": 39.7684, "Longitude": -86.1581, "Segment": "Secondary markets"},
    {"City": "Tennessee", "Latitude": 36.1627, "Longitude": -86.7816, "Segment": "Secondary markets"},
    {"City": "Mississippi", "Latitude": 32.2988, "Longitude": -90.1848, "Segment": "Secondary markets"},
    {"City": "Alabama", "Latitude": 32.3792, "Longitude": -86.3077, "Segment": "Secondary markets"},
    {"City": "North Carolina", "Latitude": 35.7796, "Longitude": -78.6382, "Segment": "Secondary markets"},
    {"City": "South Carolina", "Latitude": 34.0807, "Longitude": -81.0348, "Segment": "Secondary markets"},
    {"City": "Salt Lake City", "Latitude": 40.7608, "Longitude": -111.891, "Segment": "Emerging markets"}
]

df_warehouses = pd.DataFrame(warehouses)
df_datacenters = pd.DataFrame(data_centers)

df_datacenters.rename(columns={"Segment": "Market Category"}, inplace=True)

# Função para calcular distância haversine em km
def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # raio da Terra em km
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)
    a = (math.sin(delta_phi / 2) ** 2 +
         math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

results_empresa_categoria = []

empresas = df_warehouses['Empresa'].unique()
categorias = df_datacenters['Market Category'].unique()

for empresa in empresas:
    df_emp = df_warehouses[df_warehouses['Empresa'] == empresa]
    for categoria in categorias:
        df_cat = df_datacenters[df_datacenters['Market Category'] == categoria]
        distances = []
        for _, wh in df_emp.iterrows():
            lat_wh, lon_wh = wh['Latitude'], wh['Longitude']
            for _, dc in df_cat.iterrows():
                lat_dc, lon_dc = dc['Latitude'], dc['Longitude']
                dist = haversine(lat_wh, lon_wh, lat_dc, lon_dc)
                distances.append(dist)
        avg_dist = np.mean(distances) if distances else np.nan
        results_empresa_categoria.append({
            'Empresa': empresa,
            'Market Category': categoria,
            'Distância Média (km)': avg_dist
        })

df_result_empresa_categoria = pd.DataFrame(results_empresa_categoria)
print("Distâncias médias por empresa e categoria de mercado:")
print(df_result_empresa_categoria)

# --- Mapa interativo ---

mean_lat = df_warehouses['Latitude'].mean()
mean_lon = df_warehouses['Longitude'].mean()

m = folium.Map(location=[mean_lat, mean_lon], zoom_start=5)

color_dict = {
    'Primary markets': 'pink',
    'Secondary markets': 'purple',
    'Emerging markets': 'orange'
}

empresa_colors = {
    'WEG e Marathon': 'blue',
    'Nidec': 'green',
    'Schneider Electric': 'purple'
}

# Criar grupos para as empresas
grupo_wegemarathon = folium.FeatureGroup(name='Warehouses - WEG e Marathon')
grupo_nidec = folium.FeatureGroup(name='Warehouses - Nidec')
grupo_schneider = folium.FeatureGroup(name='Warehouses - Schneider Electric')

# Adicionar data centers
for _, dc in df_datacenters.iterrows():
    cat = dc['Market Category']
    color = color_dict.get(cat, 'gray')
    folium.CircleMarker(
        location=[dc['Latitude'], dc['Longitude']],
        radius=6,
        color=color,
        fill=True,
        fill_color=color,
        fill_opacity=0.8,
        popup=f"{dc['City']} ({cat})"
    ).add_to(m)

# Adicionar warehouses e conexões
for _, wh in df_warehouses.iterrows():
    lat_wh, lon_wh = wh['Latitude'], wh['Longitude']
    wh_name = wh['Warehouse Name']
    empresa = wh['Empresa']

    color = empresa_colors.get(empresa, 'gray')

    if empresa == 'WEG e Marathon':
        grupo = grupo_wegemarathon
    elif empresa == 'Nidec':
        grupo = grupo_nidec
    elif empresa == 'Schneider Electric':
        grupo = grupo_schneider
    else:
        continue

    # Encontrar data center mais próximo
    min_dist = float('inf')
    closest_dc = None
    for _, dc in df_datacenters.iterrows():
        dist = haversine(lat_wh, lon_wh, dc['Latitude'], dc['Longitude'])
        if dist < min_dist:
            min_dist = dist
            closest_dc = dc

    if closest_dc is None:
        continue  # segurança

    # Linha de conexão
    folium.PolyLine(
        locations=[[lat_wh, lon_wh], [closest_dc['Latitude'], closest_dc['Longitude']]],
        color='black',
        weight=2,
        opacity=0.7
    ).add_to(grupo)

    # Marcador do warehouse
    folium.Marker(
        location=[lat_wh, lon_wh],
        popup=(f"<b>{wh_name}</b><br>"
               f"<b>Empresa:</b> {empresa}<br>"
               f"<b>Segmentos:</b> {wh['Segments']}<br>"
               f"<b>Mais próximo:</b> {closest_dc['City']}<br>"
               f"<b>Distância:</b> {min_dist:.1f} km"),
        icon=folium.Icon(color=color, icon='building', prefix='fa')
    ).add_to(grupo)

# Adicionar grupos ao mapa
grupo_wegemarathon.add_to(m)
grupo_nidec.add_to(m)
grupo_schneider.add_to(m)

# Controle de camadas
folium.LayerControl().add_to(m)

# Legenda fixa
legend_html = """
<div style="
    position: fixed;
    bottom: 50px;
    left: 20px;
    width: 280px;
    z-index: 9999;
    font-size: 14px;
    background-color: white;
    padding: 10px;
    border: 2px solid grey;
    border-radius: 10px;
    box-shadow: 2px 2px 5px rgba(0,0,0,0.3);
">

<b>Legenda - Empresas (Warehouses)</b><br>
<i style="color:blue">●</i> WEG e Marathon<br>
<i style="color:green">●</i> Nidec<br>
<i style="color:purple">●</i> Schneider Electric<br><br>
<b>Legenda - Data Centers</b><br>
<i style="color:pink">●</i> Primary markets<br>
<i style="color:purple">●</i> Secondary markets<br>
<i style="color:orange">●</i> Emerging markets<br><br>
<b>Linhas pretas:</b> Conexão ao data center mais próximo
</div>
"""

m.get_root().html.add_child(Element(legend_html))

# Salvar e abrir mapa
map_path = 'mapa_com_proximidades.html'
m.save(map_path)
# Usar três barras para garantir compatibilidade em Windows e Unix
webbrowser.open('file:///' + os.path.abspath(map_path))

print(f"\nMapa salvo como {map_path}")
print("Mapa aberto no navegador")
print(f"\nTotal de warehouses: {len(df_warehouses)}")
print(f"  - WEG e Marathon: {len(df_warehouses[df_warehouses['Empresa'] == 'WEG e Marathon'])}")
print(f"  - Nidec: {len(df_warehouses[df_warehouses['Empresa'] == 'Nidec'])}")
print(f"  - Schneider Electric: {len(df_warehouses[df_warehouses['Empresa'] == 'Schneider Electric'])}")
print(f"\nTotal de data centers: {len(df_datacenters)}")
print(f"  - Primary markets: {len(df_datacenters[df_datacenters['Market Category'] == 'Primary markets'])}")
print(f"  - Secondary markets: {len(df_datacenters[df_datacenters['Market Category'] == 'Secondary markets'])}")
print(f"  - Emerging markets: {len(df_datacenters[df_datacenters['Market Category'] == 'Emerging markets'])}")
