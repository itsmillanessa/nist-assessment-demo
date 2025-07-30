import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime
import uuid

# Configuración de página
st.set_page_config(
    page_title="NIST Cybersecurity Maturity Assessment",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS para el roadmap visual
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 3rem 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }
    
    .technology-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin: 1rem 0;
        border-left: 5px solid #4CAF50;
        transition: all 0.3s ease;
    }
    
    .technology-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
    }
    
    .maturity-level {
        display: inline-block;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: bold;
        text-align: center;
        margin: 0.3rem;
    }
    
    .level-1 { background: #ffcdd2; color: #c62828; }
    .level-2 { background: #ffe0b2; color: #ef6c00; }
    .level-3 { background: #fff9c4; color: #f57f17; }
    .level-4 { background: #dcedc8; color: #689f38; }
    .level-5 { background: #c8e6c9; color: #388e3c; }
    
    .nist-function {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 2rem;
        border-radius: 15px;
        margin: 1rem 0;
        border-left: 6px solid #667eea;
    }
    
    .technology-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 1rem;
        margin: 1rem 0;
    }
    
    .roadmap-container {
        background: white;
        border-radius: 15px;
        padding: 2rem;
        box-shadow: 0 5px 20px rgba(0,0,0,0.1);
        margin: 2rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Mapeo de tecnologías a funciones NIST y niveles de madurez
TECHNOLOGY_MAPPING = {
    "Security Foundation": {
        "icon": "🔍",
        "nist_function": "Identify",
        "technologies": {
            "Asset Management Tool": {
                "impact": 3,
                "description": "Inventario automatizado de activos",
                "nist_categories": ["ID.AM-1", "ID.AM-2"]
            },
            "Vulnerability Scanner": {
                "impact": 3,
                "description": "Identificación de vulnerabilidades",
                "nist_categories": ["ID.RA-1", "ID.RA-2"]
            },
            "Risk Management Platform": {
                "impact": 4,
                "description": "Gestión formal de riesgos",
                "nist_categories": ["ID.RM-1", "ID.RM-2"]
            },
            "Compliance Management": {
                "impact": 3,
                "description": "Gestión de cumplimiento normativo",
                "nist_categories": ["ID.GV-1", "ID.GV-3"]
            }
        }
    },
    "Protective Controls": {
        "icon": "🛡️",
        "nist_function": "Protect",
        "technologies": {
            "Firewall/NGFW": {
                "impact": 4,
                "description": "Control de acceso de red perimetral",
                "nist_categories": ["PR.AC-3", "PR.AC-4"]
            },
            "Endpoint Protection (EPP)": {
                "impact": 3,
                "description": "Protección antimalware en endpoints",
                "nist_categories": ["PR.PT-1", "PR.PT-2"]
            },
            "Email Security": {
                "impact": 3,
                "description": "Protección contra amenazas por email",
                "nist_categories": ["PR.PT-1", "PR.DS-5"]
            },
            "Web Security/Proxy": {
                "impact": 2,
                "description": "Filtrado y protección web",
                "nist_categories": ["PR.PT-1", "PR.DS-5"]
            },
            "Multi-Factor Authentication": {
                "impact": 4,
                "description": "Autenticación robusta",
                "nist_categories": ["PR.AC-1", "PR.AC-7"]
            },
            "Identity Management (IAM)": {
                "impact": 4,
                "description": "Gestión centralizada de identidades",
                "nist_categories": ["PR.AC-1", "PR.AC-4"]
            },
            "Data Loss Prevention (DLP)": {
                "impact": 3,
                "description": "Prevención de pérdida de datos",
                "nist_categories": ["PR.DS-1", "PR.DS-5"]
            },
            "Backup & Recovery": {
                "impact": 4,
                "description": "Respaldo y recuperación de datos",
                "nist_categories": ["PR.IP-4", "RC.RP-1"]
            },
            "Security Awareness Training": {
                "impact": 3,
                "description": "Capacitación en ciberseguridad",
                "nist_categories": ["PR.AT-1", "PR.AT-2"]
            }
        }
    },
    "Detection & Monitoring": {
        "icon": "👁️",
        "nist_function": "Detect",
        "technologies": {
            "SIEM/Log Management": {
                "impact": 4,
                "description": "Correlación y análisis de eventos",
                "nist_categories": ["DE.CM-1", "DE.CM-3"]
            },
            "Endpoint Detection & Response (EDR)": {
                "impact": 4,
                "description": "Detección avanzada en endpoints",
                "nist_categories": ["DE.CM-1", "DE.AE-2"]
            },
            "Network Detection & Response (NDR)": {
                "impact": 3,
                "description": "Monitoreo de tráfico de red",
                "nist_categories": ["DE.CM-1", "DE.AE-1"]
            },
            "Security Operations Center (SOC)": {
                "impact": 5,
                "description": "Centro de operaciones de seguridad",
                "nist_categories": ["DE.CM-4", "DE.DP-2"]
            },
            "Threat Intelligence": {
                "impact": 3,
                "description": "Inteligencia de amenazas",
                "nist_categories": ["DE.CM-8", "DE.DP-4"]
            },
            "Intrusion Detection System (IDS)": {
                "impact": 2,
                "description": "Detección de intrusiones",
                "nist_categories": ["DE.CM-1", "DE.AE-1"]
            }
        }
    },
    "Incident Response": {
        "icon": "⚡",
        "nist_function": "Respond",
        "technologies": {
            "Incident Response Platform": {
                "impact": 4,
                "description": "Orquestación de respuesta",
                "nist_categories": ["RS.RP-1", "RS.CO-2"]
            },
            "Security Orchestration (SOAR)": {
                "impact": 4,
                "description": "Automatización de respuesta",
                "nist_categories": ["RS.MI-1", "RS.AN-3"]
            },
            "Digital Forensics Tools": {
                "impact": 3,
                "description": "Análisis forense digital",
                "nist_categories": ["RS.AN-1", "RS.AN-2"]
            },
            "Crisis Communication": {
                "impact": 2,
                "description": "Comunicación durante crisis",
                "nist_categories": ["RS.CO-1", "RS.CO-4"]
            },
            "Incident Response Team": {
                "impact": 4,
                "description": "Equipo especializado (CSIRT)",
                "nist_categories": ["RS.RP-1", "RS.MI-2"]
            }
        }
    },
    "Recovery & Continuity": {
        "icon": "🔄",
        "nist_function": "Recover",
        "technologies": {
            "Business Continuity Planning": {
                "impact": 4,
                "description": "Planificación de continuidad",
                "nist_categories": ["RC.RP-1", "RC.CO-3"]
            },
            "Disaster Recovery": {
                "impact": 4,
                "description": "Recuperación ante desastres",
                "nist_categories": ["RC.RP-1", "RC.IM-1"]
            },
            "Cloud Backup Services": {
                "impact": 3,
                "description": "Respaldo en la nube",
                "nist_categories": ["RC.RP-1", "PR.IP-4"]
            },
            "High Availability Systems": {
                "impact": 3,
                "description": "Sistemas de alta disponibilidad",
                "nist_categories": ["RC.RP-1", "PR.IP-3"]
            },
            "Recovery Testing": {
                "impact": 3,
                "description": "Pruebas de recuperación",
                "nist_categories": ["RC.RP-1", "RC.IM-1"]
            }
        }
    }
}

# Benchmarks por industria simplificados
INDUSTRY_BENCHMARKS = {
    "Servicios Financieros": {"avg_score": 78, "maturity_level": 4},
    "Tecnología": {"avg_score": 75, "maturity_level": 4},
    "Salud": {"avg_score": 69, "maturity_level": 3},
    "Manufactura": {"avg_score": 65, "maturity_level": 3},
    "Gobierno": {"avg_score": 72, "maturity_level": 4},
    "Educación": {"avg_score": 62, "maturity_level": 3},
    "Energía": {"avg_score": 76, "maturity_level": 4},
    "Retail": {"avg_score": 64, "maturity_level": 3}
}

class TechnologyBasedAssessment:
    def __init__(self):
        self.selected_technologies = {}
        self.session_id = str(uuid.uuid4())
    
    def calculate_function_maturity(self, function_name: str) -> float:
        """Calcula madurez por función NIST"""
        total_impact = 0
        selected_impact = 0
        
        for category_name, category_data in TECHNOLOGY_MAPPING.items():
            if category_data["nist_function"] == function_name:
                for tech_name, tech_data in category_data["technologies"].items():
                    total_impact += tech_data["impact"]
                    if self.selected_technologies.get(f"{category_name}_{tech_name}", False):
                        selected_impact += tech_data["impact"]
        
        if total_impact == 0:
            return 0
        
        percentage = (selected_impact / total_impact) * 100
        return min(percentage, 100)
    
    def calculate_overall_maturity(self) -> float:
        """Calcula madurez general"""
        function_scores = []
        for function in ["Identify", "Protect", "Detect", "Respond", "Recover"]:
            score = self.calculate_function_maturity(function)
            function_scores.append(score)
        
        return sum(function_scores) / len(function_scores) if function_scores else 0
    
    def get_maturity_level(self, score: float) -> int:
        """Convierte puntaje a nivel de madurez (1-5)"""
        if score >= 90:
            return 5
        elif score >= 75:
            return 4
        elif score >= 60:
            return 3
        elif score >= 40:
            return 2
        else:
            return 1
    
    def get_recommendations(self) -> Dict:
        """Genera recomendaciones basadas en gaps"""
        recommendations = []
        
        for category_name, category_data in TECHNOLOGY_MAPPING.items():
            missing_techs = []
            for tech_name, tech_data in category_data["technologies"].items():
                if not self.selected_technologies.get(f"{category_name}_{tech_name}", False):
                    missing_techs.append({
                        "name": tech_name,
                        "impact": tech_data["impact"],
                        "description": tech_data["description"],
                        "function": category_data["nist_function"]
                    })
            
            if missing_techs:
                # Ordenar por impacto descendente
                missing_techs.sort(key=lambda x: x["impact"], reverse=True)
                recommendations.extend(missing_techs[:3])  # Top 3 por categoría
        
        # Ordenar todas las recomendaciones por impacto
        recommendations.sort(key=lambda x: x["impact"], reverse=True)
        return recommendations[:10]  # Top 10 general

def main():
    # Header principal
    st.markdown("""
    <div class="main-header">
        <h1>🛡️ NIST Cybersecurity Maturity Assessment</h1>
        <h3>Evaluación Basada en Portfolio de Tecnologías</h3>
        <p>Mapeo automático de tecnologías de seguridad a las 5 funciones del Framework NIST</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    st.sidebar.title("🏢 Información Organizacional")
    
    with st.sidebar.expander("Datos de la Empresa", expanded=True):
        company_name = st.text_input("Nombre de la Organización", placeholder="Ej: Acme Corp")
        industry = st.selectbox("Industria", [
            "Seleccionar...",
            "Servicios Financieros",
            "Tecnología", 
            "Salud",
            "Manufactura",
            "Gobierno",
            "Educación",
            "Energía",
            "Retail"
        ])
        company_size = st.selectbox("Tamaño Organizacional", [
            "Seleccionar...",
            "Pequeña (1-50 empleados)",
            "Mediana (51-500 empleados)", 
            "Grande (501-5000 empleados)",
            "Empresa (5000+ empleados)"
        ])
    
    # Inicializar assessment
    if 'tech_assessment' not in st.session_state:
        st.session_state.tech_assessment = TechnologyBasedAssessment()
    
    assessment = st.session_state.tech_assessment
    
    # Tabs principales
    tab1, tab2, tab3, tab4 = st.tabs([
        "🔧 Portfolio de Tecnologías", 
        "📊 Matriz de Madurez", 
        "🗺️ Roadmap Visual", 
        "📈 Análisis Comparativo"
    ])
    
    with tab1:
        show_technology_portfolio(assessment)
    
    with tab2:
        show_maturity_matrix(assessment, industry)
    
    with tab3:
        show_visual_roadmap(assessment)
    
    with tab4:
        show_comparative_analysis(assessment, industry, company_size)

def show_technology_portfolio(assessment):
    """Selección de tecnologías por categoría"""
    st.header("🔧 Selecciona las Tecnologías de tu Portfolio")
    st.markdown("Marca las tecnologías de ciberseguridad que tu organización tiene implementadas:")
    
    for category_name, category_data in TECHNOLOGY_MAPPING.items():
        with st.expander(f"{category_data['icon']} {category_name} - Función NIST: {category_data['nist_function']}", expanded=True):
            
            st.markdown(f"**Función NIST:** {category_data['nist_function']}")
            
            # Grid de tecnologías
            cols = st.columns(2)
            
            for i, (tech_name, tech_data) in enumerate(category_data["technologies"].items()):
                with cols[i % 2]:
                    key = f"{category_name}_{tech_name}"
                    
                    # Checkbox con información
                    selected = st.checkbox(
                        f"**{tech_name}**",
                        key=key,
                        help=f"Impacto: {tech_data['impact']}/5 - {tech_data['description']}"
                    )
                    
                    assessment.selected_technologies[key] = selected
                    
                    # Mostrar descripción e impacto
                    if selected:
                        st.success(f"✅ {tech_data['description']}")
                        st.caption(f"🎯 Impacto en madurez: {tech_data['impact']}/5")
                    else:
                        st.info(f"📝 {tech_data['description']}")
                        st.caption(f"⭐ Impacto potencial: {tech_data['impact']}/5")
    
    # Resumen rápido
    total_selected = sum(1 for v in assessment.selected_technologies.values() if v)
    total_available = sum(len(cat["technologies"]) for cat in TECHNOLOGY_MAPPING.values())
    
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Tecnologías Seleccionadas", f"{total_selected}/{total_available}")
    
    with col2:
        coverage = (total_selected / total_available) * 100
        st.metric("Cobertura del Portfolio", f"{coverage:.1f}%")
    
    with col3:
        overall_maturity = assessment.calculate_overall_maturity()
        st.metric("Madurez Estimada", f"{overall_maturity:.1f}%")

def show_maturity_matrix(assessment, industry):
    """Matriz de madurez visual"""
    st.header("📊 Matriz de Madurez NIST")
    
    # Calcular madurez por función
    functions = ["Identify", "Protect", "Detect", "Respond", "Recover"]
    function_scores = {}
    function_levels = {}
    
    for function in functions:
        score = assessment.calculate_function_maturity(function)
        level = assessment.get_maturity_level(score)
        function_scores[function] = score
        function_levels[function] = level
    
    overall_score = assessment.calculate_overall_maturity()
    overall_level = assessment.get_maturity_level(overall_score)
    
    # Métricas principales
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Madurez General", f"Nivel {overall_level}", f"{overall_score:.1f}%")
    
    with col2:
        best_function = max(function_scores.items(), key=lambda x: x[1])
        st.metric("Función Más Fuerte", best_function[0], f"{best_function[1]:.1f}%")
    
    with col3:
        weakest_function = min(function_scores.items(), key=lambda x: x[1])
        st.metric("Mayor Oportunidad", weakest_function[0], f"{weakest_function[1]:.1f}%")
    
    with col4:
        if industry != "Seleccionar...":
            benchmark = INDUSTRY_BENCHMARKS.get(industry, {"avg_score": 65})
            delta = overall_score - benchmark["avg_score"]
            st.metric("vs. Industria", f"{delta:+.1f}%", f"Promedio: {benchmark['avg_score']:.1f}%")
    
    # Gráfico de radar
    col1, col2 = st.columns(2)
    
    with col1:
        # Radar chart
        fig_radar = go.Figure()
        
        fig_radar.add_trace(go.Scatterpolar(
            r=list(function_scores.values()),
            theta=functions,
            fill='toself',
            name='Madurez Actual',
            line_color='rgb(103, 126, 234)',
            fillcolor='rgba(103, 126, 234, 0.3)'
        ))
        
        # Línea de benchmark si hay industria seleccionada
        if industry != "Seleccionar...":
            benchmark_scores = [INDUSTRY_BENCHMARKS.get(industry, {"avg_score": 65})["avg_score"]] * 5
            fig_radar.add_trace(go.Scatterpolar(
                r=benchmark_scores,
                theta=functions,
                fill='toself',
                name=f'Promedio {industry}',
                line_color='rgb(255, 152, 0)',
                fillcolor='rgba(255, 152, 0, 0.1)'
            ))
        
        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100]
                )),
            showlegend=True,
            title="Radar de Madurez por Función NIST",
            height=400
        )
        
        st.plotly_chart(fig_radar, use_container_width=True)
    
    with col2:
        # Gráfico de barras por función
        colors = ['#f44336' if score < 40 else '#ff9800' if score < 60 else '#4caf50' for score in function_scores.values()]
        
        fig_bar = go.Figure(data=[
            go.Bar(
                x=list(function_scores.keys()),
                y=list(function_scores.values()),
                marker_color=colors,
                text=[f"{score:.1f}%" for score in function_scores.values()],
                textposition='auto',
            )
        ])
        
        fig_bar.update_layout(
            title="Madurez por Función NIST",
            xaxis_title="Funciones",
            yaxis_title="Nivel de Madurez (%)",
            yaxis=dict(range=[0, 100]),
            height=400
        )
        
        st.plotly_chart(fig_bar, use_container_width=True)
    
    # Matriz detallada por función
    st.subheader("🎯 Detalle por Función NIST")
    
    for function in functions:
        score = function_scores[function]
        level = function_levels[function]
        
        # Determinar color del badge
        level_class = f"level-{level}"
        
        with st.expander(f"{TECHNOLOGY_MAPPING[list(TECHNOLOGY_MAPPING.keys())[functions.index(function)]]['icon']} {function} - Nivel {level} ({score:.1f}%)"):
            
            # Mostrar tecnologías de esta función
            function_techs = []
            for category_name, category_data in TECHNOLOGY_MAPPING.items():
                if category_data["nist_function"] == function:
                    for tech_name, tech_data in category_data["technologies"].items():
                        key = f"{category_name}_{tech_name}"
                        is_selected = assessment.selected_technologies.get(key, False)
                        function_techs.append({
                            "name": tech_name,
                            "selected": is_selected,
                            "impact": tech_data["impact"],
                            "description": tech_data["description"]
                        })
            
            # Mostrar tecnologías implementadas vs no implementadas
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**✅ Tecnologías Implementadas:**")
                implemented = [tech for tech in function_techs if tech["selected"]]
                if implemented:
                    for tech in implemented:
                        st.success(f"🔧 {tech['name']} (Impacto: {tech['impact']}/5)")
                else:
                    st.warning("No hay tecnologías implementadas en esta función")
            
            with col2:
                st.markdown("**🎯 Oportunidades de Mejora:**")
                missing = [tech for tech in function_techs if not tech["selected"]]
                if missing:
                    # Ordenar por impacto
                    missing.sort(key=lambda x: x["impact"], reverse=True)
                    for tech in missing[:3]:  # Top 3
                        st.info(f"📈 {tech['name']} (Impacto: {tech['impact']}/5)")
                else:
                    st.success("¡Todas las tecnologías implementadas!")

def show_visual_roadmap(assessment):
    """Roadmap visual estilo Fortinet"""
    st.header("🗺️ Roadmap Visual de Madurez")
    
    # Calcular estado actual
    overall_score = assessment.calculate_overall_maturity()
    current_level = assessment.get_maturity_level(overall_score)
    
    # Crear visualización del roadmap
    st.markdown(f"""
    <div class="roadmap-container">
        <h2 style="text-align: center; color: #333;">🎯 NIST CYBERSECURITY FRAMEWORK - ROADMAP DE MADUREZ</h2>
        <h4 style="text-align: center; color: #666;">Nivel Actual: {current_level}/5 ({overall_score:.1f}%)</h4>
    </div>
    """, unsafe_allow_html=True)
    
    # Crear el roadmap interactivo
    levels = [
        {"level": 1, "name": "Inicial", "color": "#ffcdd2", "desc": "Procesos ad-hoc"},
        {"level": 2, "name": "Básico", "color": "#ffe0b2", "desc": "Algunos controles implementados"},
        {"level": 3, "name": "Intermedio", "color": "#fff9c4", "desc": "Procesos definidos"},
        {"level": 4, "name": "Avanzado", "color": "#dcedc8", "desc": "Procesos gestionados"},
        {"level": 5, "name": "Excelencia", "color": "#c8e6c9", "desc": "Optimización continua"}
    ]
    
    # Crear gráfico de roadmap
    fig = go.Figure()
    
    # Línea de progreso
    x_pos = list(range(1, 6))
    y_pos = [1] * 5
    
    # Agregar línea base
    fig.add_trace(go.Scatter(
        x=x_pos, y=y_pos,
        mode='lines',
        line=dict(color='lightgray', width=8),
        showlegend=False
    ))
    
    # Agregar puntos por nivel
    for i, level_data in enumerate(levels, 1):
        color = '#4CAF50' if i <= current_level else '#E0E0E0'
        size = 25 if i == current_level else 15
        
        fig.add_trace(go.Scatter(
            x=[i], y=[1],
            mode='markers+text',
            marker=dict(
                size=size,
                color=color,
                line=dict(color='white', width=2)
            ),
            text=[f"Nivel {i}<br>{level_data['name']}"],
            textposition="top center",
            textfont=dict(size=12, color='black'),
            showlegend=False,
            name=f"Nivel {i}"
        ))
    
    # Marcar posición actual
    fig.add_trace(go.Scatter(
        x=[current_level], y=[1],
        mode='markers',
        marker=dict(
            size=35,
            color='red',
            symbol='star',
            line=dict(color='white', width=3)
        ),
        showlegend=False,
        name="Posición Actual"
    ))
    
    fig.update_layout(
        title="Roadmap de Madurez NIST",
        xaxis=dict(
            range=[0.5, 5.5],
            showgrid=False,
            zeroline=False,
            showticklabels=False
        ),
        yaxis=dict(
            range=[0.5, 1.5],
            showgrid=False,
            zeroline=False,
            showticklabels=False
        ),
        height=300,
        showlegend=False
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Próximos pasos recomendados
    st.subheader("🎯 Próximos Pasos Recomendados")
    
    recommendations = assessment.get_recommendations()
    
    if recommendations:
        st.markdown("**Top 5 Tecnologías Recomendadas para Avanzar:**")
        
        for i, rec in enumerate(recommendations[:5], 1):
            priority_color = "🔴" if rec["impact"] >= 4 else "🟡" if rec["impact"] >= 3 else "🟢"
            
            with st.expander(f"{priority_color} Prioridad {i}: {rec['name']} (Función: {rec['function']})"):
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.write(f"**Descripción:** {rec['description']}")
                    st.write(f"**Función NIST:** {rec['function']}")
                    
                    # Beneficios estimados
                    if rec["impact"] >= 4:
                        st.success("🚀 **Alto Impacto:** Mejora significativa en madurez")
                    elif rec["impact"] >= 3:
                        st.warning("📈 **Impacto Medio:** Mejora notable en madurez")
                    else:
                        st.info("🔧 **Impacto Básico:** Mejora incremental")
                
                with col2:
                    st.metric("Impacto", f"{rec['impact']}/5")
                    
                    # ROI estimado
                    roi_months = 6 if rec["impact"] >= 4 else 12
                    st.caption(f"ROI estimado: {roi_months} meses")
    else:
        st.success("🎉 ¡Excelente! Tienes un portfolio completo de tecnologías implementadas.")

def show_comparative_analysis(assessment, industry, company_size):
    """Análisis comparativo con benchmarks"""
    st.header("📈 Análisis Comparativo")
    
    overall_score = assessment.calculate_overall_maturity()
    
    if industry == "Seleccionar...":
        st.warning("⚠️ Selecciona tu industria para ver comparativas detalladas")
        return
    
    benchmark = INDUSTRY_BENCHMARKS.get(industry, {"avg_score": 65, "maturity_level": 3})
    
    # Comparativa principal
    col1, col2, col3 = st.columns(3)
    
    with col1:
        delta_score = overall_score - benchmark["avg_score"]
        st.metric(
            "Tu Madurez vs. Industria",
            f"{overall_score:.1f}%",
            delta=f"{delta_score:+.1f}%"
        )
    
    with col2:
        current_level = assessment.get_maturity_level(overall_score)
        delta_level = current_level - benchmark["maturity_level"]
        st.metric(
            "Nivel vs. Promedio",
            f"Nivel {current_level}",
            delta=f"{delta_level:+} niveles" if delta_level != 0 else "En promedio"
        )
    
    with col3:
        # Calcular percentil aproximado
        if delta_score > 15:
            percentile = 90
        elif delta_score > 5:
            percentile = 75
        elif delta_score > -5:
            percentile = 50
        elif delta_score > -15:
            percentile = 25
        else:
            percentile = 10
        
        st.metric("Percentil Estimado", f"{percentile}%")
    
    # Gráfico comparativo
    comparison_data = {
        'Categoría': ['Tu Organización', f'Promedio {industry}', 'Objetivo Recomendado'],
        'Madurez': [overall_score, benchmark["avg_score"], 85],
        'Color': ['#4CAF50', '#FF9800', '#2196F3']
    }
    
    fig = px.bar(
        comparison_data,
        x='Categoría',
        y='Madurez',
        color='Categoría',
        color_discrete_map={
            'Tu Organización': '#4CAF50',
            f'Promedio {industry}': '#FF9800',
            'Objetivo Recomendado': '#2196F3'
        },
        title=f"Comparativa de Madurez - {industry}"
    )
    
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)
    
    # Insights y recomendaciones
    st.subheader("💡 Insights del Análisis")
    
    if delta_score > 10:
        st.success(f"🏆 **Excelente:** Tu organización está significativamente por encima del promedio de {industry}")
        st.info("💡 **Recomendación:** Considera compartir mejores prácticas y liderar iniciativas de la industria")
    elif delta_score > 0:
        st.info(f"👍 **Bueno:** Estás por encima del promedio de {industry}")
        st.warning("📈 **Recomendación:** Continúa mejorando para alcanzar el nivel de excelencia")
    elif delta_score > -10:
        st.warning(f"⚠️ **En desarrollo:** Estás cerca del promedio de {industry}")
        st.error("🎯 **Recomendación:** Prioriza las tecnologías de mayor impacto para cerrar la brecha")
    else:
        st.error(f"🚨 **Crítico:** Estás significativamente por debajo del promedio de {industry}")
        st.error("🆘 **Recomendación:** Plan de mejora urgente enfocado en controles básicos")

if __name__ == "__main__":
    main()
