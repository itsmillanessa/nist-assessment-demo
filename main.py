import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import uuid
import json
from typing import Dict, List

# Configuración de página
st.set_page_config(
    page_title="NIST Cybersecurity Framework Assessment",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS para un look profesional
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #1e3a8a 0%, #3b82f6 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .metric-card {
        background: #f8fafc;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #3b82f6;
        margin: 1rem 0;
    }
    
    .framework-section {
        background: #ffffff;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }
    
    .stButton > button {
        background: linear-gradient(90deg, #3b82f6 0%, #1d4ed8 100%);
        color: white;
        border-radius: 8px;
        border: none;
        padding: 0.5rem 2rem;
        font-weight: 600;
    }
    
    .assessment-progress {
        background: #dbeafe;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #93c5fd;
    }
</style>
""", unsafe_allow_html=True)

# NIST Cybersecurity Framework - Definiciones
NIST_FRAMEWORK = {
    "Identify": {
        "description": "Desarrollar una comprensión organizacional para gestionar el riesgo de ciberseguridad",
        "categories": ["Asset Management", "Business Environment", "Governance", "Risk Assessment"]
    },
    "Protect": {
        "description": "Desarrollar e implementar salvaguardas apropiadas para asegurar la entrega de servicios críticos",
        "categories": ["Access Control", "Awareness & Training", "Data Security", "Protective Technology"]
    },
    "Detect": {
        "description": "Desarrollar e implementar actividades apropiadas para identificar la ocurrencia de un evento de ciberseguridad",
        "categories": ["Anomalies & Events", "Security Monitoring", "Detection Processes"]
    },
    "Respond": {
        "description": "Desarrollar e implementar actividades apropiadas para tomar acción respecto a un incidente detectado",
        "categories": ["Response Planning", "Communications", "Analysis", "Mitigation"]
    },
    "Recover": {
        "description": "Desarrollar e implementar actividades apropiadas para mantener planes de resiliencia",
        "categories": ["Recovery Planning", "Improvements", "Communications"]
    }
}

# Preguntas de assessment simplificadas para demo
ASSESSMENT_QUESTIONS = {
    "Identify": [
        {
            "id": "ID_001",
            "question": "¿Su organización mantiene un inventario actualizado de todos los activos de hardware?",
            "weight": 0.9
        },
        {
            "id": "ID_002", 
            "question": "¿Su organización mantiene un inventario actualizado de todos los activos de software?",
            "weight": 0.9
        },
        {
            "id": "ID_003",
            "question": "¿Se han identificado y documentado todos los procesos críticos de negocio?",
            "weight": 0.8
        },
        {
            "id": "ID_004",
            "question": "¿Existe una política de ciberseguridad formal aprobada por la alta dirección?",
            "weight": 1.0
        }
    ],
    "Protect": [
        {
            "id": "PR_001",
            "question": "¿Está implementado un sistema de autenticación multifactor (MFA)?",
            "weight": 0.9
        },
        {
            "id": "PR_002",
            "question": "¿El personal recibe capacitación regular en concientización de ciberseguridad?",
            "weight": 0.8
        },
        {
            "id": "PR_003",
            "question": "¿Los datos sensibles están clasificados y protegidos adecuadamente?",
            "weight": 1.0
        },
        {
            "id": "PR_004",
            "question": "¿Se mantienen actualizados todos los sistemas con los últimos parches de seguridad?",
            "weight": 0.9
        }
    ],
    "Detect": [
        {
            "id": "DE_001",
            "question": "¿Existe un sistema de monitoreo continuo para detectar anomalías?",
            "weight": 0.9
        },
        {
            "id": "DE_002",
            "question": "¿Se monitorean continuamente los logs de seguridad?",
            "weight": 0.8
        },
        {
            "id": "DE_003",
            "question": "¿Existen procesos formales para la detección de amenazas?",
            "weight": 0.7
        }
    ],
    "Respond": [
        {
            "id": "RS_001",
            "question": "¿Existe un plan de respuesta a incidentes documentado y probado?",
            "weight": 1.0
        },
        {
            "id": "RS_002",
            "question": "¿Están definidos los canales de comunicación durante incidentes?",
            "weight": 0.8
        },
        {
            "id": "RS_003",
            "question": "¿Existen procedimientos para contener y mitigar incidentes?",
            "weight": 0.9
        }
    ],
    "Recover": [
        {
            "id": "RC_001",
            "question": "¿Existe un plan de continuidad de negocio actualizado?",
            "weight": 1.0
        },
        {
            "id": "RC_002",
            "question": "¿Se documentan las lecciones aprendidas después de incidentes?",
            "weight": 0.7
        }
    ]
}

# Datos de ejemplo para benchmarks
DEMO_BENCHMARKS = {
    "Tecnología": {"avg_score": 72.5, "total_assessments": 45},
    "Servicios Financieros": {"avg_score": 68.2, "total_assessments": 32},
    "Manufactura": {"avg_score": 65.8, "total_assessments": 28},
    "Salud": {"avg_score": 70.1, "total_assessments": 22},
    "Gobierno": {"avg_score": 74.3, "total_assessments": 18}
}

class NISTAssessment:
    def __init__(self):
        self.responses = {}
        self.session_id = str(uuid.uuid4())
        
    def calculate_function_score(self, function_name: str) -> float:
        """Calcula el puntaje para una función específica del NIST Framework"""
        questions = ASSESSMENT_QUESTIONS.get(function_name, [])
        if not questions:
            return 0.0
            
        total_weight = sum(q["weight"] for q in questions)
        weighted_score = 0.0
        
        for question in questions:
            response = self.responses.get(question["id"], 0)
            weighted_score += response * question["weight"]
            
        return (weighted_score / total_weight) * 20 if total_weight > 0 else 0.0  # Convert 0-5 to 0-100
    
    def calculate_overall_score(self) -> float:
        """Calcula el puntaje general del assessment"""
        function_scores = []
        for function_name in NIST_FRAMEWORK.keys():
            score = self.calculate_function_score(function_name)
            function_scores.append(score)
        
        return sum(function_scores) / len(function_scores) if function_scores else 0.0
    
    def get_maturity_level(self, score: float) -> str:
        """Determina el nivel de madurez basado en el puntaje"""
        if score >= 90:
            return "Optimizado (Nivel 5)"
        elif score >= 75:
            return "Gestionado (Nivel 4)"
        elif score >= 60:
            return "Definido (Nivel 3)"
        elif score >= 40:
            return "Repetible (Nivel 2)"
        else:
            return "Inicial (Nivel 1)"

def main():
    # Header principal
    st.markdown("""
    <div class="main-header">
        <h1>🛡️ NIST Cybersecurity Framework Assessment</h1>
        <p>Evaluación profesional de madurez en ciberseguridad basada en el Marco de Ciberseguridad del NIST</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar para navegación
    st.sidebar.title("🔐 Panel de Control")
    
    # Información de la organización
    with st.sidebar.expander("📋 Información de la Organización", expanded=True):
        company_name = st.text_input("Nombre de la Organización", placeholder="Ej: Acme Corp")
        industry = st.selectbox("Industria", [
            "Seleccionar...", "Servicios Financieros", "Salud", "Manufactura", 
            "Tecnología", "Educación", "Gobierno", "Energía", "Retail", "Otros"
        ])
        company_size = st.selectbox("Tamaño de la Organización", [
            "Seleccionar...", "Pequeña (1-50 empleados)", "Mediana (51-500 empleados)", 
            "Grande (501-5000 empleados)", "Empresa (5000+ empleados)"
        ])
    
    # Inicializar assessment
    if 'assessment' not in st.session_state:
        st.session_state.assessment = NISTAssessment()
    
    assessment = st.session_state.assessment
    
    # Pestañas principales
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Assessment", "📈 Resultados", "🗺️ Roadmap", "📊 Benchmarks"])
    
    with tab1:
        st.header("🔍 Evaluación NIST Cybersecurity Framework")
        
        # Mostrar progreso
        total_questions = sum(len(questions) for questions in ASSESSMENT_QUESTIONS.values())
        answered_questions = len([r for r in assessment.responses.values() if r > 0])
        progress = answered_questions / total_questions if total_questions > 0 else 0
        
        st.markdown(f"""
        <div class="assessment-progress">
            <h4>📈 Progreso del Assessment</h4>
            <p>Preguntas completadas: {answered_questions} de {total_questions} ({progress:.1%})</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.progress(progress)
        
        # Assessment por función NIST
        for function_name, function_data in NIST_FRAMEWORK.items():
            with st.expander(f"{function_name} - {function_data['description']}", expanded=False):
                st.write(f"**Categorías:** {', '.join(function_data['categories'])}")
                
                questions = ASSESSMENT_QUESTIONS.get(function_name, [])
                for question in questions:
                    response = st.radio(
                        question["question"],
                        options=[0, 1, 2, 3, 4, 5],
                        format_func=lambda x: ["No implementado", "Planificado", "En desarrollo", "Parcialmente implementado", "Mayormente implementado", "Completamente implementado"][x],
                        key=question["id"],
                        horizontal=True
                    )
                    assessment.responses[question["id"]] = response
    
    with tab2:
        st.header("📊 Resultados del Assessment")
        
        if answered_questions > 0:
            # Puntajes por función
            col1, col2 = st.columns(2)
            
            with col1:
                function_scores = {}
                for function_name in NIST_FRAMEWORK.keys():
                    score = assessment.calculate_function_score(function_name)
                    function_scores[function_name] = score
                
                # Gráfico de barras
                fig_bar = px.bar(
                    x=list(function_scores.keys()),
                    y=list(function_scores.values()),
                    title="Puntajes por Función NIST",
                    labels={'x': 'Funciones', 'y': 'Puntaje (%)'},
                    color=list(function_scores.values()),
                    color_continuous_scale='RdYlGn'
                )
                fig_bar.update_layout(height=400)
                st.plotly_chart(fig_bar, use_container_width=True)
            
            with col2:
                # Gráfico de radar
                fig_radar = go.Figure()
                fig_radar.add_trace(go.Scatterpolar(
                    r=list(function_scores.values()),
                    theta=list(function_scores.keys()),
                    fill='toself',
                    name='Puntaje Actual'
                ))
                fig_radar.update_layout(
                    polar=dict(
                        radialaxis=dict(
                            visible=True,
                            range=[0, 100]
                        )),
                    showlegend=True,
                    title="Vista Radar - Madurez NIST",
                    height=400
                )
                st.plotly_chart(fig_radar, use_container_width=True)
            
            # Métricas principales
            overall_score = assessment.calculate_overall_score()
            maturity_level = assessment.get_maturity_level(overall_score)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Puntaje General", f"{overall_score:.1f}%", delta=None)
            with col2:
                st.metric("Nivel de Madurez", maturity_level, delta=None)
            with col3:
                st.metric("Progreso", f"{progress:.1%}", delta=None)
                
            # Comparación con la industria
            if industry and industry != "Seleccionar...":
                benchmark = DEMO_BENCHMARKS.get(industry)
                if benchmark:
                    st.subheader(f"📊 Comparación con la Industria: {industry}")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        delta_score = overall_score - benchmark['avg_score']
                        st.metric(
                            "vs. Promedio Industria", 
                            f"{benchmark['avg_score']:.1f}%",
                            delta=f"{delta_score:+.1f}%"
                        )
                    with col2:
                        percentile = 50 + (delta_score / 30) * 50  # Aproximación simple
                        percentile = max(5, min(95, percentile))
                        st.metric("Percentil Estimado", f"{percentile:.0f}%")
        else:
            st.info("Complete el assessment para ver los resultados.")
    
    with tab3:
        st.header("🗺️ Roadmap de Mejora")
        
        if answered_questions > 0:
            st.subheader("📈 Plan de Mejora Recomendado")
            
            # Identificar áreas de mejora
            function_scores = {}
            for function_name in NIST_FRAMEWORK.keys():
                score = assessment.calculate_function_score(function_name)
                function_scores[function_name] = score
            
            # Ordenar por puntaje (menor a mayor)
            sorted_functions = sorted(function_scores.items(), key=lambda x: x[1])
            
            st.write("**Prioridad de Mejora (basada en puntajes más bajos):**")
            
            recommendations = {
                "Identify": [
                    "Implementar un sistema de gestión de activos (CMDB)",
                    "Desarrollar políticas de clasificación de información",
                    "Establecer un programa formal de evaluación de riesgos"
                ],
                "Protect": [
                    "Implementar autenticación multifactor en todos los sistemas críticos",
                    "Desarrollar un programa de capacitación en ciberseguridad",
                    "Establecer controles de acceso basados en roles"
                ],
                "Detect": [
                    "Implementar un SIEM (Security Information and Event Management)",
                    "Establecer monitoreo continuo de la red",
                    "Desarrollar capacidades de threat hunting"
                ],
                "Respond": [
                    "Desarrollar y probar un plan de respuesta a incidentes",
                    "Establecer un equipo de respuesta a incidentes (CSIRT)",
                    "Implementar procedimientos de comunicación de crisis"
                ],
                "Recover": [
                    "Desarrollar un plan de continuidad de negocio",
                    "Implementar backups automatizados y probados",
                    "Establecer un plan de recuperación ante desastres"
                ]
            }
            
            for i, (function_name, score) in enumerate(sorted_functions, 1):
                priority_color = ["🔴", "🟡", "🟢", "🔵", "🟣"][i-1]
                
                with st.expander(f"{priority_color} Prioridad {i}: {function_name} ({score:.1f}%)"):
                    st.write(f"**Descripción:** {NIST_FRAMEWORK[function_name]['description']}")
                    st.write("**Acciones recomendadas:**")
                    
                    for rec in recommendations.get(function_name, []):
                        st.write(f"• {rec}")
        else:
            st.info("Complete el assessment para generar el roadmap de mejora.")
    
    with tab4:
        st.header("📊 Benchmarks de la Industria")
        
        # Mostrar benchmarks por industria
        benchmark_df = pd.DataFrame.from_dict(DEMO_BENCHMARKS, orient='index')
        benchmark_df.reset_index(inplace=True)
        benchmark_df.rename(columns={'index': 'Industria', 'avg_score': 'Puntaje Promedio', 'total_assessments': 'Total Evaluaciones'}, inplace=True)
        
        # Gráfico de benchmarks
        fig_benchmark = px.bar(
            benchmark_df,
            x='Industria',
            y='Puntaje Promedio',
            title="Puntaje Promedio por Industria",
            color='Puntaje Promedio',
            color_continuous_scale='RdYlGn'
        )
        fig_benchmark.update_xaxes(tickangle=45)
        st.plotly_chart(fig_benchmark, use_container_width=True)
        
        # Tabla de benchmarks
        st.subheader("📋 Datos Detallados por Industria")
        st.dataframe(benchmark_df, use_container_width=True, hide_index=True)
        
        # Insights
        st.subheader("💡 Insights del Mercado")
        best_industry = benchmark_df.loc[benchmark_df['Puntaje Promedio'].idxmax(), 'Industria']
        worst_industry = benchmark_df.loc[benchmark_df['Puntaje Promedio'].idxmin(), 'Industria']
        
        col1, col2 = st.columns(2)
        with col1:
            st.success(f"🏆 **Mejor Industria:** {best_industry}")
        with col2:
            st.warning(f"📈 **Mayor Oportunidad:** {worst_industry}")

if __name__ == "__main__":
    main()
