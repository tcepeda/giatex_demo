import plotly.express as px
import json
import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu

st.set_page_config(layout='wide')


#TODO change to relative path
file_path = 'src/GIATEX_dataset_merged_demo.csv'

# Try reading with different encodings
encodings_to_try = ['utf-8', 'latin-1', 'ISO-8859-1']
for encoding in encodings_to_try:
    try:
        df_giatex_original = pd.read_csv(file_path, sep=';', encoding=encoding)
        print(f"Successfully read the file with encoding: e{encoding}")
        break  # Exit the loop if successful
    except UnicodeDecodeError:
        print(f"Failed to read with encoding: {encoding}")

df_giatex_copy = df_giatex_original.copy()


#features = ['pH', 'Condutividade','Alcalinidade', 'Dureza', 'Cor_p', 'Turbidez', 'Sólidos suspensos totais', 'Carência química de oxigénio', 'Carência bioquímica de oxigénio', 'Carbono orgânico total', 'Azoto total', 'Nitratos', 'Nitritos', 'Alumínio', 'Chumbo', 'Cobre', 'Crómio total', 'Ferro',
           # 'Manganês', 'Magnésio', 'Zinco', 'Cálcio', 'Cloretos', 'Sulfatos', 'Sulfitos', 'Sulfuretos', 'Detergentes aniónicos']


features = ['pH', 'Condutividade',
            'Alcalinidade', 'Dureza',
            'Turbidez', 'Sólidos suspensos totais',
            'Carência química de oxigénio',
            'Carência bioquímica de oxigénio',
            'Nitratos', 'Cálcio']

features_units = {'pH':'un.', 'Condutividade':'mS/cm',
            'Alcalinidade': 'mg/L', 'Dureza': 'mg/L', 'Cor_p':'Pt-Co',
            'Turbidez': 'NTU', 'Sólidos suspensos totais': 'mg/L',
            'Carência química de oxigénio': 'mg/L O2',
            'Carência bioquímica de oxigénio': 'mg/L O2',
            'Carbono orgânico total': 'mg/L', 'Azoto total': 'mg/L',
            'Nitratos': 'mg/L', 'Nitritos': 'mg/L',
            'Alumínio': 'mg/L', 'Chumbo': 'mg/L',
            'Cobre': 'mg/L', 'Crómio total': 'mg/L', 
            'Ferro': 'mg/L', 'Manganês': 'mg/L', 'Magnésio': 'mg/L', 'Zinco': 'mg/L',
            'Cálcio': 'mg/L', 'Cloretos': 'mg/L', 'Sulfatos': 'mg/L',
            'Sulfitos': 'mg/L', 'Sulfuretos': 'mg/L',
            'Detergentes aniónicos': 'mg MBAS/L'}


# Filter Dataframe. Remove all non valuable columns
def clean_data(df_giatex_copy):
    # Drop columns: 'Empresa', 'snapshot' and 20 other columns
    df_giatex_copy = df_giatex_copy.drop(columns=['Empresa', 'snapshot', 'mes', 'ano', 'recolha_agua', 'indice_seca', 'precipitation', 'soil_moisture_225', 'processo_representativo', 'pre_tratamento', 'origem', 'Line', 'ID Processo', 'Estrutura', 'Fibra', 'Corante', 'Cor', 'Máquina', 'R:B', 'Banho', 'banho_representativo'])
    # Filter rows based on column: 'bacia_hidrografica'
    df_giatex_copy = df_giatex_copy[df_giatex_copy['bacia_hidrografica'].notna()]
    
    return df_giatex_copy

df_giatex_copy_clean = clean_data(df_giatex_copy.copy())

efluente = df_giatex_copy_clean['Banho simplif.'].unique()


#SIDEBAR CONTAINER--------------------------------------------------------------
st.markdown("""
<style>
[data-testid=stSidebar] {
    background-image: linear-gradient(to bottom, #DCF2F1, #FFFFFF);
}
</style>
""", unsafe_allow_html=True)

# Display the images in the sidebar
# st.sidebar.image("src/logo_oficial.png", use_column_width=True)
# st.sidebar.image("src/BARRA_2024.png", use_column_width=True)

# Display the images in the sidebar
st.sidebar.image("src/logo_oficial.png", use_column_width=True)
st.sidebar.image("src/BARRA_2024.png", use_column_width=True)

#st.sidebar.markdown('''
#<h2 style="color: #1D70B7;">DEMONSTRADOR</h2>
#''', unsafe_allow_html=True)

#Retirado para efeitos de demonstração em ambiente android

#st.sidebar.markdown('''
#<h3 style="color: #1D70B7; font-weight: normal;">Comportamento dos parâmetros físico-químicos das águas e efluentes dos processos de enobrecimento têxtil</h3>
#''', unsafe_allow_html=True)


# Define the line style (optional)
line_style = "border-top: 1px solid #E0F4F3;"  # Adjust color and thickness as needed

# Create a container for the line to divide the logos from the interactive part
with st.sidebar.container():
    st.markdown(f"<hr style='{line_style}'>", unsafe_allow_html=True)  # Add the line within the container

# Create an option menu for Banho
with st.sidebar:
    selected = option_menu("Amostras", ["Água entrada", 'Efluente bruto', 'Efluente ETAR'], 
        icons=['droplet', 'droplet-fill', 'droplet-half'],
        menu_icon="water", default_index=0,
    styles={
        "container": {"padding": "0!important", "background-color": "#fafafa"},
        "icon": {"color": "#35A8E0", "font-size": "20px"}, 
        "nav-link": {"font-size": "15px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
        "nav-link-selected": {"background-color": "#1D70B7"},
    }
)

# Display the input parameter
add_selectbox = st.sidebar.selectbox(
    "Selecione o **Parâmetro** que Quer Monitorizar",
    (features)
)

#SIDEBAR CONTAINER--------------------------------------------------------------


#DATA WRANGLING-----------------------------------------------------------------
#define variable parameter name (ph, condutividade)
variable_name = add_selectbox

#define SI units to feature selected
si_units = features_units[add_selectbox]

# Compute average parameter for each unique combination of latitude, longitude, bacia_hidrografica and banho 
average_parameter = df_giatex_copy_clean.groupby(['latitude', 'longitude', 'bacia_hidrografica',  'Banho simplif.'])[variable_name].mean().reset_index()

# Round parameter values to zero decimal places. It will improve the visual in chart
# average_parameter[variable_name] = average_parameter[variable_name].round(0)

# If value is 0, round to 3 decimal places; otherwise, round to integer
average_parameter[variable_name] = average_parameter[variable_name].apply(lambda x: round(x, 3) if 0 < x < 1 else round(x))
print(average_parameter[variable_name])

# #duplicate column and transform into string for text label in chart
average_parameter['value_str'] = average_parameter[variable_name].astype(str)

#define the Banho - água de entrada, bruto, etar
df_use_for_bubblemap = average_parameter[average_parameter['Banho simplif.'] == selected]

# combine two infos to import to the label. In order to the text will have this two informations
df_use_for_bubblemap['combined_text'] = df_use_for_bubblemap['bacia_hidrografica'] + '  ' + df_use_for_bubblemap['value_str']

# Calculate min and max values to the color range be only updated IF the parameter is changed. The efluente will not be changed
min_value = average_parameter[variable_name].min()
max_value = average_parameter[variable_name].max()
#DATA WRANGLING-----------------------------------------------------------------


# TOKEN ACCESS------------------------------------------------------------------
mapbox_access_token = "pk.eyJ1IjoiY2VwZWRhdCIsImEiOiJjbHQ1cDNwb28wM2NwMmxtc2E5MXAwdXgzIn0.yqQJpO1iKm8QvoKgsfJEfg"
# Set the Mapbox access token in Plotly
px.set_mapbox_access_token(mapbox_access_token)
# TOKEN ACCESS------------------------------------------------------------------


# MAIN CONTAINER----------------------------------------------------------------
#formatted_text = f"""<h2 style="color: #1D70B7; font-weight: bold; font-size: 50px;">Explora o Mapa do Consórcio! <br>Parâmetro: {variable_name} {si_units}</h2>"""

formatted_text = f"""<h2 style="font-weight: bold;">
<span style="font-size: 60px; color: #1D70B7;">Explora o Mapa</span> <br>
<span style="color: #35A8E0;">{variable_name} {si_units}</span></span></h2>"""

st.markdown(formatted_text, unsafe_allow_html=True)


# Create a scatter map with longitude and latitude
fig = px.scatter_mapbox(df_use_for_bubblemap,
                        lat='latitude',
                        lon='longitude',
                        color=variable_name,  # Color bubbles based on average conductivity values
                        color_continuous_scale=[[0, '#15F5BA'], [0.5, '#FCDC2A'], [1, '#FE7A36']],  # Choose any color scale you prefer
                        range_color = [min_value, max_value],
                        size=variable_name,
                        size_max = 60,
                        height=1000, 
                        hover_data={'bacia_hidrografica': True, variable_name: True, 'latitude': False, 'longitude': False, 'Banho simplif.': False, 'value_str' : False, 'combined_text': False},
                        opacity = 0.8,
                        text = 'combined_text',
                        zoom=3
                        )

# Update layout
fig.update_layout(
    mapbox_style="mapbox://styles/cepedat/clt5owqzp005k01nw4ck5a231",  # Choose map style
    mapbox_zoom=7,
    mapbox_center={"lat": 41.30425259851746, "lon": -8.279317663875982},
    modebar={"remove" : 'zoom'},
    hovermode='closest'
)

# Show the plot
# fig.show()

# Set Plotly figure layout to stretch horizontally
fig.update_layout(width=2600, height=800)  # Adjust width and height as needed

# Display the Plotly chart in Streamlit with the use_container_width option
st.plotly_chart(fig, use_container_width=True)
# MAIN CONTAINER----------------------------------------------------------------
