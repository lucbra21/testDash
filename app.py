import dash
from dash import dcc, html, dash_table
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

# Inicializar la aplicación Dash
app = dash.Dash(__name__, suppress_callback_exceptions=True)

# Datos de ejemplo
np.random.seed(42)
df = pd.DataFrame({
    'Jugador': ['Jugador ' + str(i) for i in range(1, 11)],
    'Puntos': np.random.randint(0, 30, 10),
    'Asistencias': np.random.randint(0, 15, 10),
    'Rebotes': np.random.randint(0, 20, 10),
    'Robos': np.random.randint(0, 5, 10),
    'Bloqueos': np.random.randint(0, 5, 10)
})

# Colores del tema (azul oscuro predominante)
colors = {
    'background': '#000000',
    'text': '#FFFFFF',
    'accent': '#00667F',  # Color del logo
    'border': '#FFFFFF'
}

# Creamos los gráficos de ejemplo
# Gráfico de barras
fig_barras = px.bar(
    df, x='Jugador', y='Puntos', 
    title='Puntos por Jugador',
    color_discrete_sequence=['#00667F']
)
fig_barras.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text'],
    margin=dict(l=10, r=10, t=40, b=20)
)

# Gráfico radar
categories = ['Puntos', 'Asistencias', 'Rebotes', 'Robos', 'Bloqueos']
fig_radar = go.Figure()

fig_radar.add_trace(go.Scatterpolar(
    r=[df['Puntos'].mean(), df['Asistencias'].mean(), 
       df['Rebotes'].mean(), df['Robos'].mean(), df['Bloqueos'].mean()],
    theta=categories,
    fill='toself',
    name='Equipo Promedio',
    line_color='#00667F'
))

fig_radar.update_layout(
    polar=dict(
        radialaxis=dict(
            visible=True,
            range=[0, 30]
        )),
    showlegend=False,
    title='Estadísticas del Equipo',
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text'],
    margin=dict(l=10, r=10, t=40, b=20)
)

# Gráfico de dispersión
fig_dispersion = px.scatter(
    df, x='Puntos', y='Asistencias', 
    size='Rebotes', color='Jugador',
    title='Dispersión Puntos vs Asistencias'
)
fig_dispersion.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text'],
    margin=dict(l=10, r=10, t=40, b=20)
)

# Gráfico plot (líneas)
fig_plot = px.line(
    df, x='Jugador', y=['Puntos', 'Asistencias', 'Rebotes'], 
    title='Estadísticas por Jugador'
)
fig_plot.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text'],
    margin=dict(l=10, r=10, t=40, b=20)
)

# Definir el diseño de la aplicación
app.layout = html.Div([
    # Encabezado
    html.Div([
        html.H1("Clase 3 mpad", style={'color': colors['text'], 'margin': '0', 'padding': '10px'})
    ], style={
        'backgroundColor': colors['background'],
        'borderBottom': f'1px solid {colors["border"]}',
        'textAlign': 'left'
    }),
    
    # Contenido principal (estructura de tabla)
    html.Div([
        # Primera fila
        html.Div([
            # Columna izquierda (menú)
            html.Div([
                # Logo
                html.Div([
                    html.Div("logo", style={
                        'backgroundColor': colors['accent'],
                        'color': colors['text'],
                        'borderRadius': '50%',
                        'width': '100px',
                        'height': '100px',
                        'margin': '20px auto',
                        'display': 'flex',
                        'alignItems': 'center',
                        'justifyContent': 'center'
                    })
                ], style={'textAlign': 'center'}),
                
                # Menú
                html.Div([
                    html.H3("Menu", style={
                        'color': colors['text'],
                        'borderBottom': f'1px solid {colors["border"]}',
                        'paddingBottom': '5px',
                        'marginTop': '30px'
                    }),
                    html.Ul([
                        html.Li(html.A("Player Stats", href="#", style={'color': colors['text']})),
                        html.Li(html.A("Team Stats", href="#", style={'color': colors['text']})),
                        html.Li(html.A("Summary", href="#", style={'color': colors['text']}))
                    ], style={'listStyleType': 'none', 'padding': '0'})
                ])
            ], style={
                'width': '15%',
                'backgroundColor': colors['background'],
                'color': colors['text'],
                'padding': '10px',
                'borderRight': f'1px solid {colors["border"]}',
                'height': '100%'
            }),
            
            # Columna central (gráfico de barras)
            html.Div([
                html.H3("Gráfico de barras", style={'color': colors['text'], 'textAlign': 'center'}),
                dcc.Graph(
                    id='grafico-barras',
                    figure=fig_barras,
                    style={'height': '100%'}
                )
            ], style={
                'width': '35%',
                'backgroundColor': colors['background'],
                'borderRight': f'1px solid {colors["border"]}'
            }),
            
            # Columna derecha (tabla de datos)
            html.Div([
                html.H3("Tabla de datos", style={'color': colors['text'], 'textAlign': 'center'}),
                dash_table.DataTable(
                    id='tabla',
                    columns=[{"name": i, "id": i} for i in df.columns],
                    data=df.to_dict('records'),
                    style_table={'height': '80%', 'overflowY': 'auto'},
                    style_header={
                        'backgroundColor': colors['accent'],
                        'color': colors['text']
                    },
                    style_cell={
                        'backgroundColor': colors['background'],
                        'color': colors['text'],
                        'border': f'1px solid {colors["border"]}'
                    }
                )
            ], style={'width': '50%'})
        ], style={
            'display': 'flex', 
            'height': '380px',
            'borderBottom': f'1px solid {colors["border"]}'
        }),
        
        # Segunda fila (3 gráficos)
        html.Div([
            # Gráfico radar
            html.Div([
                html.H3("Gráfico radar", style={'color': colors['text'], 'textAlign': 'center'}),
                dcc.Graph(
                    id='grafico-radar',
                    figure=fig_radar,
                    style={'height': '90%'}
                )
            ], style={
                'width': '30%',
                'borderRight': f'1px solid {colors["border"]}',
                'height': '100%'
            }),
            
            # Gráfico dispersión
            html.Div([
                html.H3("Gráfico dispersión", style={'color': colors['text'], 'textAlign': 'center'}),
                dcc.Graph(
                    id='grafico-dispersion',
                    figure=fig_dispersion,
                    style={'height': '90%'}
                )
            ], style={
                'width': '40%',
                'borderRight': f'1px solid {colors["border"]}',
                'height': '100%'
            }),
            
            # Gráfico plot
            html.Div([
                html.H3("Gráfico plot", style={'color': colors['text'], 'textAlign': 'center'}),
                dcc.Graph(
                    id='grafico-plot',
                    figure=fig_plot,
                    style={'height': '90%'}
                )
            ], style={'width': '30%', 'height': '100%'})
        ], style={
            'display': 'flex', 
            'flexDirection': 'row',
            'height': '380px'
        })
    ], style={'backgroundColor': colors['background']}),
    
    # Pie de página
    html.Div([
        html.P("Pie del dash", style={'margin': '0', 'padding': '10px'})
    ], style={
        'backgroundColor': colors['background'],
        'color': colors['text'],
        'borderTop': f'1px solid {colors["border"]}',
        'textAlign': 'center'
    })
], style={
    'fontFamily': 'Arial, sans-serif',
    'margin': '0',
    'height': '100vh',
    'backgroundColor': colors['background'],
    'display': 'flex',
    'flexDirection': 'column'
})

# Ejecutar la aplicación
if __name__ == '__main__':
    app.run(debug=True)