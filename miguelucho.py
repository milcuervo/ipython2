import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

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

# INDICADORES BASICOS DEL DATASET
filas = df.shape[0]
variables = df.shape[1]
num_deptos = df["DEPARTAMENTO"].nunique()
num_mpios = df["MUNICIPIO"].nunique()


# Cálculo de Total por Año de Energía Activa
df_activa = df_colombia_continental.pivot_table(
    columns = 'AÑO SERVICIO',
    values = ['ENERGÍA ACTIVA'],
    aggfunc = 'sum'
)

tot_25 = df_activa[2025].to_list()[0]
tot_24 = df_activa[2024].to_list()[0]
tot_23 = df_activa[2023].to_list()[0]
tot_22 = df_activa[2022].to_list()[0]
tot_21 = df_activa[2021].to_list()[0]

delta_25 = round((tot_25 - tot_24)/ tot_24*100,2)
delta_24 = round((tot_24 - tot_23)/ tot_23*100,2)
delta_23 = round((tot_23 - tot_22)/ tot_22*100,2)
delta_22 = round((tot_22 - tot_21)/ tot_21*100,2)

df_depto_anios = df_colombia_continental.groupby(['DEPARTAMENTO', 'AÑO SERVICIO'])[['ENERGÍA ACTIVA']].sum().reset_index()
departamentos = df_colombia_continental['DEPARTAMENTO'].unique().tolist()

########################################################################
#                           CODIGO STREAMLIT                           #
########################################################################
# Configuración de la página
st.set_page_config(
    page_title='Zonas No Interconectadas',
    layout='centered',
    initial_sidebar_state='collapsed'  # o expanded
)

st.markdown(
    '''
    <style>
        .block-container {
            padding: 2.5rem;
            max-width: 1200px;
        }
    ''',
    unsafe_allow_html=True
)
st.markdown('<a id="inicio"></a><br><br>', unsafe_allow_html=True)
st.image('img/Encabezado.png')

########################################################################
#                        ATRIBUTOS DEL DATASET                         #
########################################################################
st.markdown('<a id="atributos-del-dataset"></a><br>', unsafe_allow_html=True)
with st.container(border=True):
    st.subheader('Atributos del Dataset')
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Número de Variables", f'{variables}', border=True)

    with col2:
        st.metric("Número de Filas", f'{filas}', border=True)

    with col3:
        st.metric("Número de Departamentos", f'{num_deptos}', border=True)
    with col4:
        st.metric("Número de Municipios", f'{num_mpios}', border=True)

    if st.checkbox('Mostrar detalles del Origen de los datos'):
        st.write('Conjunto de datos descargados del portal de Datos Abiertos del Gobierno Nacional en:')
        st.write('https://www.datos.gov.co/Minas-y-Energ-a/Estado-de-la-prestaci-n-del-servicio-de-energ-a-en/3ebi-d83g/about_data')

    with st.expander('Mostrar el dataframe original'):
        st.dataframe(df)

    with st.expander('Mostrar Datos Energía Reactiva anual por Municipio'):
        st.dataframe(df_pivote)

###############################################################################
#     GRAFICO INTREACTIVO DE BARRAS HORIZONTALES POR DEPARTAMENTO Y AÑO       #
###############################################################################
st.markdown('<a id="evolucion-energia-activa"></a><br>', unsafe_allow_html=True)
with st.container(border=True):
    st.subheader('Evolución de Energía Activa por Departamento')

    # Desplegable para seleccionar departamento
    depto_selec = st.selectbox(
        'Selecciona un departamento:',
        options=departamentos
    )
    condicion_filtro = df_depto_anios['DEPARTAMENTO'] == depto_selec
    df_departamento = df_depto_anios[condicion_filtro]


    # Crear gráfico de barras horizontales
    fig_barras = go.Figure()

    fig_barras.add_trace(go.Bar(
        x=df_departamento['ENERGÍA ACTIVA'],
        y=df_departamento['AÑO SERVICIO'].astype(str),
        orientation='h',
        marker_color='#4E7F96',
        text=df_departamento['ENERGÍA ACTIVA'],
        texttemplate='%{text:,.0f}',
        textposition='auto',
    ))

    fig_barras.update_layout(
        height=400,
        xaxis_title='Energía Activa (kWh)',
        yaxis_title='Año',
        showlegend=False,
        yaxis={'categoryorder': 'category ascending'}
    )

    st.plotly_chart(fig_barras, use_container_width=True)

########################################################################
#                             INDICADORES                              #
########################################################################
st.markdown('<a id="indicadores"></a><br>', unsafe_allow_html=True)
with st.container(border=True):
    st.subheader('Indicadores de Energía Activa por año en Millones de Kw')
    col5, col6, col7, col8 = st.columns(4)

    col5.metric("Energía Activa 2022", f'{round(tot_22/1000000,2)} kWh', f'{delta_22} %', border=True)
    col6.metric("Energía Activa 2023", f'{round(tot_23/1000000,2)} kWh', f'{delta_23} %', border=True)
    col7.metric("Energía Activa 2024", f'{round(tot_24/1000000,2)} kWh', f'{delta_24} %', border=True)
    col8.metric("Energía Activa 2025", f'{round(tot_25/1000000,2)} kWh', f'{delta_25} %', border=True)

    df_activa = df_activa[[2022,2023,2024,2025]].T
    st.line_chart(
        data = df_activa,
        height = 200
    )

########################################################################
#                      GRAFICOS DE ENERGÍA ACTIVA                      #
########################################################################
st.markdown('<a id="graficas-energia"></a><br>', unsafe_allow_html=True)
with st.container(border=True):
    st.subheader('Gráficas de Energía Activa y Reactiva por Municipio')
    col9, col10 = st.columns(2)
    with col9:
        df_mayores = df_agrupado.sort_values(by='ENERGÍA ACTIVA', ascending=False).head(5)
        fig = px.bar(
            df_mayores,
            x = 'MUNICIPIO',
            y = 'ENERGÍA ACTIVA',
            color = 'DEPARTAMENTO',
            title = 'Top 5 - Energía Activa',
            labels = {'MUNICIPIO':'Municipio', 'ENERGÍA ACTIVA':'Energía Activa (kWh)'},
            text_auto = True,
            height=600
        )
        fig.update_xaxes(categoryorder='array', categoryarray=df_mayores['MUNICIPIO'].tolist())
        fig.update_traces(textposition='outside')
        fig.update_layout(
            height=470
        )

        st.plotly_chart(fig, use_container_width=True)

    with col10:
        df_mayores = df_agrupado.sort_values(by='ENERGÍA REACTIVA', ascending=False).head(5)
        fig = px.bar(
            df_mayores,
            x = 'MUNICIPIO',
            y = 'ENERGÍA REACTIVA',
            color = 'DEPARTAMENTO',
            title = 'Top 5 - Energía Reactiva',
            labels = {'MUNICIPIO':'Municipio', 'ENERGÍA REACTIVA':'Energía Reactiva (kWh)'},
            text_auto = True
        )
        fig.update_xaxes(categoryorder='array', categoryarray=df_mayores['MUNICIPIO'].tolist())
        fig.update_traces(textposition='outside')
        fig.update_layout(
            height=470
        )

        st.plotly_chart(fig, use_container_width=True)


    col11, col12 = st.columns(2)
    with col11:
        torta_activa = df_agrupado.groupby('DEPARTAMENTO')['ENERGÍA ACTIVA'].sum().reset_index()
        torta_activa = torta_activa.sort_values(by='ENERGÍA ACTIVA', ascending=False).head(5)
        fig1 = px.pie(
            torta_activa,
            names = 'DEPARTAMENTO',
            values = 'ENERGÍA ACTIVA',
            title = 'Paricipación Top 5 - Energía Activa',
            hole = 0.4
        )

        st.plotly_chart(fig1, use_container_width=True)

    with col12:
        torta_reactiva = df_agrupado.sort_values(by='ENERGÍA REACTIVA', ascending=False).head(5)
        fig2 = px.pie(
            torta_reactiva,
            names = 'MUNICIPIO',
            values = 'ENERGÍA REACTIVA',
            title = 'Participación Top 5 - Energía Reactiva',
            hole = 0.4,
        )

        st.plotly_chart(fig2, use_container_width=True)

    with st.expander('Mostrar Datos Energía Activa Y Reactiva por Municipio'):
        st.dataframe(df_agrupado.sort_values(by='ENERGÍA ACTIVA', ascending=False))



########################################################################
#                             MENÚ LATERAL                             #
########################################################################

with st.sidebar.container():
    st.markdown('''
        <style>
            /* Estilo de los enlaces del menú */
            [data-testid="stSidebar"] a {
                display: block;
                color: #3366AA;
                text-decoration: none;
                padding: 6px 10px;
                border-radius: 6px;
            }
            [data-testid="stSidebar"] a:hover {
                background-color: #e6e6e6;
            }
        </style>
    ''', unsafe_allow_html=True)
    st.header('Navegación')
    st.markdown('[Inicio](#inicio)')
    st.markdown('[Atributos del Dataset](#atributos-del-dataset)')
    st.markdown('[Evolución Energía Activa](#evolucion-energia-activa)')
    st.markdown('[Indicadores](#indicadores)')
    st.markdown('[Gráficas Energía](#graficas-energia)')
    st.markdown('[Mapa Colombia](#mapa-colombia)')

    st.html('<br><br><br><br>')
    st.markdown('---')
    st.html('<small><a href="mailto:ingenieria@juliangiraldo.co" target="_blank">Desarrollado por: Julian Giraldo</a></small>')

