import numpy as np
def show_visual_roadmap_chart(results):
    """Crea el gráfico visual mejorado con diseño más profesional y natural"""
    st.markdown("""
    <div style="background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%); border: 2px solid #64748b; border-radius: 15px; padding: 1rem; margin: 1rem 0;">
        <h3 style="color: #1e293b; text-align: center; margin-bottom: 0.5rem; font-size: 1.1rem;">🗺️ FORTINET SECURITY FABRIC</h3>
        <p style="text-align: center; color: #64748b; margin-bottom: 0.5rem; font-size: 0.85rem;">ROADMAP PROFESIONAL - EVOLUCIÓN DE MADUREZ</p>
    </div>
    """, unsafe_allow_html=True)
    
    current_level = results['maturity_level']
    
    # Crear figura con diseño mejorado
    fig = go.Figure()
    
    # Definir colores más elegantes y profesionales
    level_colors = ['#fef2f2', '#fef3e2', '#eff6ff', '#ecfdf5', '#faf5ff']
    level_borders = ['#fecaca', '#fed7aa', '#bfdbfe', '#bbf7d0', '#e9d5ff']
    level_names = ['Nivel 1\nInicial', 'Nivel 2\nBásico', 'Nivel 3\nIntermedio', 'Nivel 4\nAvanzado', 'Nivel 5\nExcelencia']
    level_descriptions = ['Fundamentos\n(0-3 meses)', 'Consolidación\n(3-6 meses)', 'Detección Avanzada\n(6-12 meses)', 'Optimización\n(12-18 meses)', 'Zero Trust & AI\n(18-24 meses)']
    
    # FONDO NATURAL: Crear un degradado de fondo más natural
    for i in range(5):
        # Zona principal con gradiente suave
        fig.add_shape(
            type="rect",
            x0=i+0.6, y0=0, x1=i+1.4, y1=6,
            fillcolor=level_colors[i],
            opacity=0.3,
            layer="below",
            line=dict(color=level_borders[i], width=1, dash='dot')
        )
        
        # Líneas de separación más elegantes
        if i < 4:
            fig.add_shape(
                type="line",
                x0=i+1.4, y0=0, x1=i+1.4, y1=6,
                line=dict(color='#cbd5e1', width=1.5, dash='solid'),
                layer="below"
            )
        
        # Headers de nivel más profesionales
        fig.add_annotation(
            x=i+1, y=5.8,
            text=f"<b>{level_names[i]}</b>",
            showarrow=False,
            font=dict(size=10, color='#1e293b', family="Inter"),
            align="center",
            bgcolor="rgba(255, 255, 255, 0.9)",
            bordercolor=level_borders[i],
            borderwidth=1,
            borderpad=4
        )
        
        # Timeline en la parte inferior más sutil
        fig.add_annotation(
            x=i+1, y=0.4,
            text=level_descriptions[i],
            showarrow=False,
            font=dict(size=8, color='#64748b', family="Inter"),
            align="center"
        )
    
    # CURVA DE MADUREZ: Línea más suave y profesional
    x_curve = np.linspace(0.6, 5.4, 20)  # Más puntos para suavidad
    # Función exponencial suave para madurez natural
    y_curve = 0.8 + 4.2 * (1 - np.exp(-0.8 * (x_curve - 0.6))) + 0.1 * np.sin(2 * np.pi * (x_curve - 0.6) / 5)
    
    # Gradiente en la línea de madurez
    fig.add_trace(go.Scatter(
        x=x_curve,
        y=y_curve,
        mode='lines',
        line=dict(
            color='rgba(67, 56, 202, 0.8)',
            width=5,
            shape='spline',
            smoothing=1.3
        ),
        showlegend=False,
        name='Curva de Madurez'
    ))
    
    # Sombra de la curva para profundidad
    fig.add_trace(go.Scatter(
        x=x_curve,
        y=y_curve - 0.1,
        mode='lines',
        line=dict(color='rgba(67, 56, 202, 0.2)', width=8),
        showlegend=False,
        fill=None
    ))
    
    # Hitos importantes en la curva
    milestone_positions = [1, 2, 3, 4, 5]
    for pos in milestone_positions:
        y_pos = 0.8 + 4.2 * (1 - np.exp(-0.8 * (pos - 0.6))) + 0.1 * np.sin(2 * np.pi * (pos - 0.6) / 5)
        
        fig.add_trace(go.Scatter(
            x=[pos],
            y=[y_pos],
            mode='markers',
            marker=dict(
                size=10,
                color='#4338ca',
                symbol='circle',
                line=dict(color='white', width=2)
            ),
            showlegend=False
        ))
    
    # DISTRIBUCIÓN INTELIGENTE DE PRODUCTOS
    category_y_ranges = {
        "Network Security": (1.0, 2.0),
        "Endpoint Security": (2.1, 2.8),
        "Email & Web Security": (2.9, 3.6),
        "Identity & Access Management": (1.5, 2.5),
        "SOC & Analytics": (3.7, 4.4),
        "Management & Orchestration": (4.5, 5.2),
        "Cloud Security": (3.8, 4.6),
        "OT & IoT Security": (3.2, 4.0)
    }
    
    # Contadores para distribución uniforme
    phase_product_counts = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
    
    for category_name, category_data in FORTINET_COMPLETE_PORTFOLIO.items():
        y_min, y_max = category_y_ranges.get(category_name, (2.0, 3.0))
        
        for product_name, product_info in category_data["products"].items():
            phase = product_info['implementation_phase']
            
            # Verificar implementación
            product_key = f"{category_name}_{product_name}"
            is_implemented = st.session_state.professional_assessment["fortinet_products"].get(product_key, False)
            
            # Posición más natural
            count = phase_product_counts[phase]
            x_offset = (count % 5 - 2) * 0.05  # Distribución horizontal más sutil
            y_pos = y_min + (y_max - y_min) * (count / 10.0) + np.random.uniform(-0.05, 0.05)
            
            x_pos = phase + x_offset
            phase_product_counts[phase] += 1
            
            # Estilo más profesional
            if is_implemented:
                color = '#059669'
                size = 12
                symbol = 'circle'
                line_color = '#065f46'
                line_width = 2
                opacity = 0.9
            else:
                impact_colors = {5: '#dc2626', 4: '#ea580c', 3: '#3b82f6', 2: '#8b5cf6', 1: '#64748b'}
                color = impact_colors.get(product_info['impact'], '#64748b')
                size = 6 + product_info['impact']
                symbol = 'circle-open'
                line_color = color
                line_width = 1.5
                opacity = 0.7
            
            # Nombre limpio del producto
            product_display = product_name.replace('Forti', '').replace(' for OT', '').strip()
            if len(product_display) > 12:
                product_display = product_display[:10] + '...'
            
            fig.add_trace(go.Scatter(
                x=[x_pos],
                y=[y_pos],
                mode='markers+text',
                marker=dict(
                    size=size,
                    color=color,
                    symbol=symbol,
                    line=dict(color=line_color, width=line_width),
                    opacity=opacity
                ),
                text=[product_display],
                textposition="top center",
                textfont=dict(size=6, color='#1e293b', family="Inter"),
                showlegend=False,
                name=product_name,
                hovertemplate=(
                    f"<b>{product_name}</b><br>"
                    f"📁 {category_name}<br>"
                    f"📊 Fase {phase} - Impacto {product_info['impact']}<br>"
                    f"🎯 {product_info['nist_function']}<br>"
                    f"{'✅ Implementado' if is_implemented else '⭕ Recomendado'}<br>"
                    f"💡 {product_info['description'][:60]}..."
                    "<extra></extra>"
                )
            ))
    
    # PIN PROFESIONAL "USTED ESTÁ AQUÍ"
    pin_x = current_level
    pin_y = 5.6
    
    # Pin principal (más elegante)
    fig.add_trace(go.Scatter(
        x=[pin_x],
        y=[pin_y],
        mode='markers+text',
        marker=dict(
            size=25,
            color='#dc2626',
            symbol='diamond',
            line=dict(color='#7f1d1d', width=3)
        ),
        text=['📍'],
        textfont=dict(size=16, color='#ffffff'),
        showlegend=False,
        name="Posición Actual"
    ))
    
    # Texto del pin más profesional
    fig.add_annotation(
        x=pin_x,
        y=pin_y - 0.3,
        text="<b>SU POSICIÓN ACTUAL</b>",
        showarrow=True,
        arrowhead=2,
        arrowsize=1,
        arrowwidth=2,
        arrowcolor="#dc2626",
        ax=0,
        ay=-30,
        font=dict(size=10, color='#dc2626', family="Inter Bold"),
        bgcolor="rgba(255, 255, 255, 0.95)",
        bordercolor="#dc2626",
        borderwidth=2,
        borderpad=6
    )
    
    # Indicador en la curva de madurez
    if current_level <= 5:
        curve_y = 0.8 + 4.2 * (1 - np.exp(-0.8 * (current_level - 0.6))) + 0.1 * np.sin(2 * np.pi * (current_level - 0.6) / 5)
        
        fig.add_trace(go.Scatter(
            x=[current_level],
            y=[curve_y],
            mode='markers',
            marker=dict(
                size=20,
                color='#dc2626',
                symbol='circle',
                line=dict(color='#ffffff', width=4)
            ),
            showlegend=False
        ))
        
        # Línea conectora del pin a la curva
        fig.add_shape(
            type="line",
            x0=pin_x, y0=pin_y-0.1,
            x1=current_level, y1=curve_y+0.1,
            line=dict(color='#dc2626', width=2, dash='dot'),
            layer="above"
        )
    
    # LEYENDA PROFESIONAL
    fig.add_annotation(
        x=2.5, y=0.7,
        text=(
            "🗺️ <b>Portfolio Completo Fortinet Security Fabric</b><br>"
            "🟢 <b>Verde:</b> Tecnología Implementada | ⚪ <b>Círculos:</b> Recomendada para implementar<br>"
            "📈 <b>Tamaño = Nivel de Impacto</b> | 📍 <b>Pin Rojo:</b> Su posición actual de madurez<br>"
            "💙 <b>Curva Azul:</b> Trayectoria natural de evolución hacia la excelencia"
        ),
        showarrow=False,
        font=dict(size=9, color='#374151', family="Inter"),
        align="center",
        bgcolor="rgba(248, 250, 252, 0.98)",
        bordercolor="#cbd5e1",
        borderwidth=1,
        borderpad=10
    )
    
    # Configuración del layout más profesional
    fig.update_layout(
        title={
            'text': "🛡️ FORTINET SECURITY FABRIC - ROADMAP DE MADUREZ PROFESIONAL",
            'x': 0.5,
            'font': {'size': 16, 'color': '#1e293b', 'family': "Inter Bold"}
        },
        height=550,
        showlegend=False,
        plot_bgcolor='rgba(248, 250, 252, 0.5)',
        paper_bgcolor='white',
        hovermode='closest',
        margin=dict(t=60, b=50, l=40, r=40)
    )
    
    # Ejes más limpios y profesionales
    fig.update_xaxes(
        range=[0.5, 5.5],
        title={
            'text': "→ Evolución Natural de Madurez en Ciberseguridad",
            'font': {'size': 12, 'color': '#374151', 'family': "Inter"}
        },
        tickvals=[1, 2, 3, 4, 5],
        ticktext=['Nivel 1', 'Nivel 2', 'Nivel 3', 'Nivel 4', 'Nivel 5'],
        showgrid=False,
        zeroline=False,
        tickfont={'size': 10, 'family': "Inter"},
        linecolor='#cbd5e1',
        linewidth=1
    )
    
    fig.update_yaxes(
        range=[0, 6],
        title={
            'text': "↑ Amplitud y Profundidad de Cobertura",
            'font': {'size': 12, 'color': '#374151', 'family': "Inter"}
        },
        showticklabels=False,
        showgrid=True,
        gridcolor='rgba(203, 213, 225, 0.3)',
        zeroline=False,
        linecolor='#cbd5e1',
        linewidth=1
    )
    
    # Mostrar el gráfico
    st.plotly_chart(fig, use_container_width=True)
    
    # Información adicional profesional
    st.markdown("""
    <div style="background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%); border: 2px solid #0ea5e9; border-radius: 12px; padding: 1.5rem; margin: 1rem 0;">
        <h4 style="color: #0369a1; margin-bottom: 0.8rem;">📊 Interpretación del Roadmap Profesional</h4>
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; font-size: 0.9rem;">
            <div>
                <p><strong>📍 Pin Rojo:</strong> Indica su nivel actual de madurez</p>
                <p><strong>💙 Curva Azul:</strong> Trayectoria óptima de evolución</p>
                <p><strong>🟢 Círculos Verdes:</strong> Tecnologías ya implementadas</p>
            </div>
            <div>
                <p><strong>⚪ Círculos Abiertos:</strong> Próximas tecnologías a implementar</p>
                <p><strong>📈 Tamaño:</strong> Representa el impacto en su madurez</p>
                <p><strong>🏗️ Columnas:</strong> Fases de implementación estructuradas</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
