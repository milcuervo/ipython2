import streamlit as st
import pandas as pd
import plotly.express as px


st.text("-----------------")
ruta = 'https://github.com/juliandariogiraldoocampo/analisis_taltech/raw/refs/heads/main/explorador/Estado_de_la_prestaci%C3%B3n_del_servicio_de_energ%C3%ADa_en_Zonas_No_Interconectadas_20251021.csv'
df = pd.read_csv(ruta)

df['ENERGÍA REACTIVA'] = df['ENERGÍA REACTIVA'].str.replace(',', '').astype(float).astype(int)
df['ENERGÍA ACTIVA'] = df['ENERGÍA ACTIVA'].str.replace(',', '').astype(float).astype(int)
df['POTENCIA MÁXIMA'] = df['POTENCIA MÁXIMA'].str.replace(',', '').astype(float)

lst_cambio = [['Á','A'],['É','E'], ['Í','I'], ['Ó','O'], ['Ú','U']]

# Realizar los reemplazos en las columnas 'DEPARTAMENTO' y 'MUNICIPIO'
for i in range(5):
    df['DEPARTAMENTO'] = df['DEPARTAMENTO'].str.replace(lst_cambio[i][0],lst_cambio[i][1])
    df['MUNICIPIO'] = df['MUNICIPIO'].str.replace(lst_cambio[i][0],lst_cambio[i][1])

    # Crear una condición negativa para filtrar los departamentos no deseados
    condicion_filtro = ~df['DEPARTAMENTO'].isin([
    'ARCHIPIELAGO DE SAN ANDRES',
    'ARCHIPIELAGO DE SAN ANDRES y PROVIDENCIA',
    'ARCHIPIELAGO DE SAN ANDRES, PROVIDENCIA Y SANTA CATALINA'
    ])

df_colombia_continental = df[condicion_filtro]

df_agrupado = df_colombia_continental.groupby(['DEPARTAMENTO', 'MUNICIPIO'])[['ENERGÍA ACTIVA', 'ENERGÍA REACTIVA']].sum().reset_index()

df_pivote = df_colombia_continental.pivot_table(
    index = 'DEPARTAMENTO',
    columns = 'AÑO SERVICIO',
    values = ['ENERGÍA ACTIVA'],
    aggfunc = 'sum'
)

filas = df_colombia_continental.shape[0]
columnas = df_colombia_continental.shape[1]

# Configuración de la página ▷ el layout puede ser 'centered' o 'wide'
st.set_page_config(page_title='Aplicación Base', layout='centered')

st.markdown(
    """
	<style>
		.block-container {
			padding: 3rem 2rem 2rem 2rem;
			max-width: 1000px;
		}
    </style>
	""",
    unsafe_allow_html=True
)

##################################### CODIGO STREAMLIT ######################################


st.image('Img\Encabezado.png', width=1000)

st.title('✨Estado de Prestación del Servicio de Energía en Zonas No Interconectadas')
st.header('🐱‍👤Bootcamp Análisis de Datos - Talento Digital')

st.subheader('Tamaño del Dataset')
col1, col2 = st.columns(2)

with col1:
    st.text('Filas:')
    st.subheader(df_colombia_continental.shape[0])
with col2:
    st.text('Columnas:')
    st.subheader(df_colombia_continental.shape[1])


st.subheader('Tamaño del Dataset')
col3, col4, col5 = st.columns(3)

with col3:
    st.markdown(f"""<h3 style=
                color:#FF5733;
                background-color:#F0F0F0;
                border: 2px solid #FF5733;
                border-radius: 10px;
                margin: 10px;
                padding: 10px;
                text-align: center">
                Número de Filas<br>{filas}
                </h3>""", 
                unsafe_allow_html=True)

with col4:
    st.markdown(f"""<h3 style=
                color:#FF5733;
                background-color:#F0F0F0;
                border: 2px solid #FF5733;
                border-radius: 10px;
                margin: 10px;
                padding: 10px;
                text-align: center">
                Número de Columnas<br>{columnas}
                </h3>""", 
                unsafe_allow_html=True)
with col5:
    st.text('Filas:')
    st.subheader(df_colombia_continental.shape[0])



with st.expander("Mostrar Tabla de Datos"):
    st.dataframe(df_colombia_continental)

if st.checkbox("Mostrar detalles de lorigen de los datos:"):
    st.markdown("""
    **Fuente de los datos:**\n
    https://www.datos.gov.co/Salud-y-Protecci-n-Social/Casos-de-violencia-de-genero/dgxs-2h97/about_data \n
    **Descripción:**\n
    El conjunto de datos proporciona información sobre el estado de la prestación del servicio de energía en zonas no interconectadas de Colombia. Incluye detalles como el departamento, municipio, año de servicio, energía activa, energía reactiva y potencia máxima.
    """)
