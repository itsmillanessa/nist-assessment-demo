import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime
import uuid
from typing import Dict, List

# Configuración de página
st.set_page_config(
    page_title="NIST Cybersecurity Framework Assessment",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS mejorado para interface visual como Fortinet
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #d32f2f 0%, #f44336 100%);
        padding: 3rem 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 3rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }
    
    .section-header {
        background: #f5f5f5;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 2rem 0 1rem 0;
        border-left: 5px solid #d32f2f;
    }
    
    .section-header h3 {
        color: #d32f2f;
        margin: 0;
        font-weight: bold;
    }
    
    .industry-card, .size-card, .tech-card {
        background: white;
        border: 2px solid #e0e0e0;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 0.5rem;
        text-align: center;
        cursor: pointer;
        transition: all 0.3s ease;
        height: 140px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }
    
    .industry-card:hover, .size-card:hover, .tech-card:hover {
        border-color: #d32f2f;
        box-shadow: 0 5px 20px rgba(211, 47, 47, 0.3);
        transform: translateY(-3px);
    }
    
    .industry-card.selected, .size-card.selected, .tech-card.selected {
        border-color: #d32f2f;
        background: linear-gradient(135deg, #ffebee 0%, #ffcdd2 100%);
        box-shadow: 0 5px 20px rgba(211, 47, 47, 0.4);
    }
    
    .card-icon {
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
    }
    
    .card-title {
        font-weight: bold;
        color: #333;
        font-size: 1rem;
        margin-bottom: 0.3rem;
    }
    
    .card-subtitle {
        color: #666;
        font-size: 0.8rem;
    }
    
    .tech-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
        gap: 1rem;
        margin: 1rem 0;
    }
    
    .continue-btn {
        background: linear-gradient(135deg, #4caf50 0%, #45a049 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 1rem 3rem;
        font-size: 1.2rem;
        font-weight: bold;
        cursor: pointer;
        transition: all 0.3s ease;
        margin: 2rem auto;
        display: block;
    }
    
    .continue-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(76, 175, 80, 0.4);
    }
    
    .progress-bar {
        background: #e0e0e0;
        border-radius: 10px;
        height: 8px;
        margin: 1rem 0;
    }
    
    .progress-fill {
        background: linear-gradient(90deg, #4caf50 0%, #45a049 100%);
        height: 100%;
        border-radius: 10px;
        transition: width 0.3s ease;
    }
    
    .step-indicator {
        display: flex;
        justify-content: center;
        align-items: center;
        margin: 2rem 0;
    }
    
    .step {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        background: #e0e0e0;
        color: white;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 1rem;
        font-weight: bold;
    }
    
    .step.active {
        background: #d32f2f;
    }
    
    .step.completed {
        background: #4caf50;
    }
    
    .vendor-badge {
        background: #2196f3;
        color: white;
        padding: 0.2rem 0.5rem;
        border-radius: 12px;
        font-size: 0.7rem;
        margin-top: 0.5rem;
    }
    
    .impact-badge {
        background: #ff9800;
        color: white;
        padding: 0.2rem 0.5rem;
        border-radius: 8px;
        font-size: 0.7rem;
        margin-top: 0.3rem;
    }
</style>
""", unsafe_allow_html=True)

# Datos de industrias con iconos
INDUSTRIES = {
    "Servicios Financieros": {
        "icon": "🏦",
        "frameworks": "SOX, PCI DSS, FFIEC, GDPR",
        "risk_level": "Alto",
        "benchmark": 78
    },
    "Gobierno y Sector Público": {
        "icon": "🏛️", 
        "frameworks": "NIST, FedRAMP, FISMA, CISA",
        "risk_level": "Alto",
        "benchmark": 72
    },
    "Salud y Farmacéutica": {
        "icon": "🏥",
        "frameworks": "HIPAA, HITECH, FDA, GDPR",
        "risk_level": "Alto", 
        "benchmark": 69
    },
    "Retail y E-commerce": {
        "icon": "🛒",
        "frameworks": "PCI DSS, GDPR, CCPA, SOX",
        "risk_level": "Medio",
        "benchmark": 64
    },
    "Manufactura e Industrial": {
        "icon": "🏭",
        "frameworks": "ICS-CERT, NERC CIP, ISO 27001",
        "risk_level": "Medio",
        "benchmark": 65
    },
    "Tecnología y Software": {
        "icon": "💻",
        "frameworks": "SOC 2, ISO 27001, GDPR, Cloud",
        "risk_level": "Alto",
        "benchmark": 75
    },
    "Energía y Utilities": {
        "icon": "⚡",
        "frameworks": "NERC CIP, ICS-CERT, NIST",
        "risk_level": "Crítico",
        "benchmark": 76
    },
    "Educación": {
        "icon": "🎓",
        "frameworks": "FERPA, NIST, ISO 27001",
        "risk_level": "Medio",
        "benchmark": 62
    }
}

# Tamaños de empresa
COMPANY_SIZES = {
    "Pequeña (1-50 empleados)": {
        "icon": "🏢",
        "budget": "< $50K anual",
        "complexity": "Básica",
        "priority": "Fundamentos"
    },
    "Mediana (51-500 empleados)": {
        "icon": "🏗️",
        "budget": "$50K - $500K anual", 
        "complexity": "Intermedia",
        "priority": "Eficiencia"
    },
    "Grande (501-5000 empleados)": {
        "icon": "🏰",
        "budget": "$500K - $5M anual",
        "complexity": "Avanzada", 
        "priority": "Integración"
    },
    "Empresa (5000+ empleados)": {
        "icon": "🌆",
        "budget": "$5M+ anual",
        "complexity": "Empresarial",
        "priority": "Optimización"
    }
}

# Catálogo de tecnologías expandido
TECHNOLOGY_CATALOG = {
    "Network Security": {
        "icon": "🔥",
        "technologies": {
            "FortiGate NGFW": {"vendor": "Fortinet", "impact": 4, "nist": "Protect"},
            "Cisco ASA/FTD": {"vendor": "Cisco", "impact": 4, "nist": "Protect"},
            "Palo Alto Networks": {"vendor": "Palo Alto", "impact": 4, "nist": "Protect"},
            "Check Point": {"vendor": "Check Point", "impact": 4, "nist": "Protect"},
            "SonicWall": {"vendor": "SonicWall", "impact": 3, "nist": "Protect"},
            "pfSense": {"vendor": "Netgate", "impact": 2, "nist": "Protect"}
        }
    },
    "Endpoint Security": {
        "icon": "💻",
        "technologies": {
            "FortiClient EMS": {"vendor": "Fortinet", "impact": 4, "nist": "Protect"},
            "CrowdStrike Falcon": {"vendor": "CrowdStrike", "impact": 5, "nist": "Detect"},
            "Microsoft Defender": {"vendor": "Microsoft", "impact": 3, "nist": "Protect"},
            "Symantec Endpoint": {"vendor": "Broadcom", "impact": 3, "nist": "Protect"},
            "Trend Micro": {"vendor": "Trend Micro", "impact": 3, "nist": "Protect"},
            "Carbon Black": {"vendor": "VMware", "impact": 4, "nist": "Detect"}
        }
    },
    "Email & Web Security": {
        "icon": "📧",
        "technologies": {
            "FortiMail": {"vendor": "Fortinet", "impact": 4, "nist": "Protect"},
            "Proofpoint": {"vendor": "Proofpoint", "impact": 4, "nist": "Protect"},
            "Mimecast": {"vendor": "Mimecast", "impact": 4, "nist": "Protect"},
            "Microsoft Defender 365": {"vendor": "Microsoft", "impact": 3, "nist": "Protect"},
            "Barracuda Email Security": {"vendor": "Barracuda", "impact": 3, "nist": "Protect"},
            "Cisco Email Security": {"vendor": "Cisco", "impact": 3, "nist": "Protect"}
        }
    },
    "Identity & Access": {
        "icon": "🔐",
        "technologies": {
            "FortiAuthenticator": {"vendor": "Fortinet", "impact": 4, "nist": "Protect"},
            "Microsoft Azure AD": {"vendor": "Microsoft", "impact": 4, "nist": "Protect"},
            "Okta": {"vendor": "Okta", "impact": 4, "nist": "Protect"},
            "Ping Identity": {"vendor": "Ping", "impact": 4, "nist": "Protect"},
            "CyberArk": {"vendor": "CyberArk", "impact": 5, "nist": "Protect"},
            "RSA SecurID": {"vendor": "RSA", "impact": 3, "nist": "Protect"}
        }
    },
    "SIEM & Analytics": {
        "icon": "📊",
        "technologies": {
            "FortiSIEM": {"vendor": "Fortinet", "impact": 5, "nist": "Detect"},
            "Splunk": {"vendor": "Splunk", "impact": 5, "nist": "Detect"},
            "IBM QRadar": {"vendor": "IBM", "impact": 4, "nist": "Detect"},
            "Microsoft Sentinel": {"vendor": "Microsoft", "impact": 4, "nist": "Detect"},
            "ArcSight": {"vendor": "Micro Focus", "impact": 4, "nist": "Detect"},
            "LogRhythm": {"vendor": "LogRhythm", "impact": 4, "nist": "Detect"}
        }
    },
    "SOC & Orchestration": {
        "icon": "🎛️",
        "technologies": {
            "FortiSOAR": {"vendor": "Fortinet", "impact": 5, "nist": "Respond"},
            "Phantom (Splunk)": {"vendor": "Splunk", "impact": 5, "nist": "Respond"},
            "Demisto (Palo Alto)": {"vendor": "Palo Alto", "impact": 5, "nist": "Respond"},
            "IBM Resilient": {"vendor": "IBM", "impact": 4, "nist": "Respond"},
            "ServiceNow SecOps": {"vendor": "ServiceNow", "impact": 4, "nist": "Respond"},
            "Swimlane": {"vendor": "Swimlane", "impact": 4, "nist": "Respond"}
        }
    },
    "Vulnerability Management": {
        "icon": "🔍",
        "technologies": {
            "FortiManager": {"vendor": "Fortinet", "impact": 3, "nist": "Identify"},
            "Qualys": {"vendor": "Qualys", "impact": 4, "nist": "Identify"},
            "Rapid7": {"vendor": "Rapid7", "impact": 4, "nist": "Identify"},
            "Tenable Nessus": {"vendor": "Tenable", "impact": 4, "nist": "Identify"},
            "OpenVAS": {"vendor": "Greenbone", "impact": 2, "nist": "Identify"},
            "Veracode": {"vendor": "Veracode", "impact": 3, "nist": "Identify"}
        }
    },
    "Data Protection": {
        "icon": "🗄️",
        "technologies": {
            "Microsoft Purview": {"vendor": "Microsoft", "impact": 4, "nist": "Protect"},
            "Symantec DLP": {"vendor": "Broadcom", "impact": 4, "nist": "Protect"},
            "Forcepoint DLP": {"vendor": "Forcepoint", "impact": 4, "nist": "Protect"},
            "Varonis": {"vendor": "Varonis", "impact": 4, "nist": "Protect"},
            "Digital Guardian": {"vendor": "Digital Guardian", "impact": 3, "nist": "Protect"},
            "Code42": {"vendor": "Code42", "impact": 3, "nist": "Protect"}
        }
    },
    "Cloud Security": {
        "icon": "☁️",
        "technologies": {
            "FortiCWP": {"vendor": "Fortinet", "impact": 4, "nist": "Protect"},
            "Prisma Cloud": {"vendor": "Palo Alto", "impact": 5, "nist": "Protect"},
            "AWS Security Hub": {"vendor": "AWS", "impact": 4, "nist": "Protect"},
            "Azure Security Center": {"vendor": "Microsoft", "impact": 4, "nist": "Protect"},
            "Google Cloud Security": {"vendor": "Google", "impact": 4, "nist": "Protect"},
            "Dome9": {"vendor": "Check Point", "impact": 3, "nist": "Protect"}
        }
    },
    "Backup & Recovery": {
        "icon": "💾",
        "technologies": {
            "Veeam": {"vendor": "Veeam", "impact": 4, "nist": "Recover"},
            "Commvault": {"vendor": "Commvault", "impact": 4, "nist": "Recover"},
            "Rubrik": {"vendor": "Rubrik", "impact": 4, "nist": "Recover"},
            "Cohesity": {"vendor": "Cohesity", "impact": 4, "nist": "Recover"},
            "AWS Backup": {"vendor": "AWS", "impact": 3, "nist": "Recover"},
            "Azure Backup": {"vendor": "Microsoft", "impact": 3, "nist": "Recover"}
        }
    }
}

class VisualNISTAssessment:
    def __init__(self):
        if 'assessment_data' not in st.session_state:
            st.session_state.assessment_data = {
                'step': 1,
                'industry': None,
                'company_size': None,
                'selected_technologies': {},
                'assessment_complete': False
            }
    
    def calculate_nist_maturity(self) -> Dict:
        """Calcula madurez NIST basada en tecnologías seleccionadas"""
        nist_functions = {
            "Identify": {"total_impact": 0, "selected_impact": 0},
            "Protect": {"total_impact": 0, "selected_impact": 0},
            "Detect": {"total_impact": 0, "selected_impact": 0},
            "Respond": {"total_impact": 0, "selected_impact": 0},
            "Recover": {"total_impact": 0, "selected_impact": 0}
        }
        
        # Calcular impactos por función NIST
        for category_name, category_data in TECHNOLOGY_CATALOG.items():
            for tech_name, tech_info in category_data["technologies"].items():
                nist_function = tech_info["nist"]
                impact = tech_info["impact"]
                
                nist_functions[nist_function]["total_impact"] += impact
                
                if st.session_state.assessment_data["selected_technologies"].get(f"{category_name}_{tech_name}", False):
                    nist_functions[nist_function]["selected_impact"] += impact
        
        # Calcular porcentajes
        results = {}
        for function, data in nist_functions.items():
            if data["total_impact"] > 0:
                percentage = (data["selected_impact"] / data["total_impact"]) * 100
                results[function] = min(percentage, 100)
            else:
                results[function] = 0
        
        overall_score = sum(results.values()) / len(results) if results else 0
        
        return {
            "function_scores": results,
            "overall_score": overall_score,
            "maturity_level": self.get_maturity_level(overall_score)
        }
    
    def get_maturity_level(self, score: float) -> int:
        """Convierte puntaje a nivel de madurez (1-5)"""
        if score >= 90: return 5
        elif score >= 75: return 4
        elif score >= 60: return 3
        elif score >= 40: return 2
        else: return 1

def main():
    assessment = VisualNISTAssessment()
    
    # Header principal
    st.markdown("""
    <div class="main-header">
        <h1>🛡️ NIST Cybersecurity Framework</h1>
        <h2>ROADMAP DE MADUREZ VISUAL</h2>
        <p>Evalúa tu madurez actual en ciberseguridad y visualiza tu camino hacia la excelencia con el portafolio completo de tecnologías</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Indicador de pasos
    current_step = st.session_state.assessment_data['step']
    
    st.markdown(f"""
    <div class="step-indicator">
        <div class="step {'completed' if current_step > 1 else 'active' if current_step == 1 else ''}">1</div>
        <div class="step {'completed' if current_step > 2 else 'active' if current_step == 2 else ''}">2</div>
        <div class="step {'completed' if current_step > 3 else 'active' if current_step == 3 else ''}">3</div>
        <div class="step {'active' if current_step == 4 else ''}">4</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Mostrar paso actual
    if current_step == 1:
        show_industry_selection()
    elif current_step == 2:
        show_company_size_selection()
    elif current_step == 3:
        show_technology_assessment()
    elif current_step == 4:
        show_results_and_roadmap(assessment)

def show_industry_selection():
    """Paso 1: Selección de industria"""
    st.markdown("""
    <div class="section-header">
        <h3>🏭 Selecciona tu Industria</h3>
        <p>Esta información nos ayuda a personalizar el análisis de madurez y las recomendaciones según el contexto de tu empresa</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Grid de industrias
    cols = st.columns(4)
    
    for i, (industry_name, industry_data) in enumerate(INDUSTRIES.items()):
        with cols[i % 4]:
            selected = st.session_state.assessment_data['industry'] == industry_name
            
            if st.button(
                f"{industry_data['icon']}\n\n**{industry_name}**\n\n{industry_data['frameworks']}\n\nPerfil de Riesgo: {industry_data['risk_level']}",
                key=f"industry_{industry_name}",
                help=f"Benchmark promedio: {industry_data['benchmark']}%"
            ):
                st.session_state.assessment_data['industry'] = industry_name
                st.rerun()
    
    # Botón continuar
    if st.session_state.assessment_data['industry']:
        st.markdown("---")
        if st.button("📍 Continuar al Assessment →", type="primary", use_container_width=True):
            st.session_state.assessment_data['step'] = 2
            st.rerun()

def show_company_size_selection():
    """Paso 2: Selección de tamaño de empresa"""
    st.markdown(f"""
    <div class="section-header">
        <h3>🏢 Tamaño de tu Organización</h3>
        <p>Industria seleccionada: <strong>{st.session_state.assessment_data['industry']}</strong></p>
    </div>
    """, unsafe_allow_html=True)
    
    # Grid de tamaños
    cols = st.columns(2)
    
    for i, (size_name, size_data) in enumerate(COMPANY_SIZES.items()):
        with cols[i % 2]:
            selected = st.session_state.assessment_data['company_size'] == size_name
            
            if st.button(
                f"{size_data['icon']}\n\n**{size_name}**\n\nPresupuesto típico: {size_data['budget']}\nComplejidad: {size_data['complexity']}\nPrioridad: {size_data['priority']}",
                key=f"size_{size_name}",
                type="primary" if selected else "secondary"
            ):
                st.session_state.assessment_data['company_size'] = size_name
                st.rerun()
    
    # Navegación
    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Anterior", use_container_width=True):
            st.session_state.assessment_data['step'] = 1
            st.rerun()
    
    with col2:
        if st.session_state.assessment_data['company_size']:
            if st.button("🔧 Assessment de Tecnologías →", type="primary", use_container_width=True):
                st.session_state.assessment_data['step'] = 3
                st.rerun()

def show_technology_assessment():
    """Paso 3: Assessment de tecnologías"""
    st.markdown("""
    <div class="section-header">
        <h3>🔧 Assessment de Tecnologías</h3>
        <p>Selecciona las tecnologías que tienes <strong>actualmente implementadas</strong> en tu organización</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Mostrar progreso
    total_techs = sum(len(cat["technologies"]) for cat in TECHNOLOGY_CATALOG.values())
    selected_techs = sum(1 for v in st.session_state.assessment_data["selected_technologies"].values() if v)
    progress = selected_techs / total_techs if total_techs > 0 else 0
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Tecnologías Seleccionadas", f"{selected_techs}/{total_techs}")
    with col2:
        st.metric("Progreso", f"{progress:.1%}")
    with col3:
        # Cálculo temporal de madurez
        temp_assessment = VisualNISTAssessment()
        temp_results = temp_assessment.calculate_nist_maturity()
        st.metric("Madurez Estimada", f"{temp_results['overall_score']:.1f}%")
    
    # Categorías de tecnologías
    for category_name, category_data in TECHNOLOGY_CATALOG.items():
        with st.expander(f"{category_data['icon']} {category_name}", expanded=True):
            
            # Grid de tecnologías en esta categoría
            cols = st.columns(3)
            
            for i, (tech_name, tech_info) in enumerate(category_data["technologies"].items()):
                with cols[i % 3]:
                    key = f"{category_name}_{tech_name}"
                    
                    # Determinar color del vendor badge
                    vendor_color = "#d32f2f" if tech_info["vendor"] == "Fortinet" else "#2196f3"
                    
                    # Checkbox con estilo de card
                    selected = st.checkbox(
                        f"**{tech_name}**",
                        key=key,
                        help=f"Vendor: {tech_info['vendor']} | Impacto NIST: {tech_info['impact']}/5 | Función: {tech_info['nist']}"
                    )
                    
                    if selected:
                        st.success(f"✅ {tech_info['vendor']}")
                        st.caption(f"🎯 Impacto: {tech_info['impact']}/5 | {tech_info['nist']}")
                    else:
                        st.info(f"📦 {tech_info['vendor']}")
                        st.caption(f"⭐ Potencial: {tech_info['impact']}/5 | {tech_info['nist']}")
                    
                    st.session_state.assessment_data["selected_technologies"][key] = selected
    
    # Navegación
    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Anterior", use_container_width=True):
            st.session_state.assessment_data['step'] = 2
            st.rerun()
    
    with col2:
        if selected_techs > 0:
            if st.button("📊 Generar Roadmap de Madurez →", type="primary", use_container_width=True):
                st.session_state.assessment_data['step'] = 4
                st.session_state.assessment_data['assessment_complete'] = True
                st.rerun()

def show_results_and_roadmap(assessment):
    """Paso 4: Resultados y roadmap"""
    results = assessment.calculate_nist_maturity()
    
    # Header de resultados
    st.markdown(f"""
    <div class="section-header">
        <h3>🎯 Análisis de Madurez Actual</h3>
        <p><strong>Industria:</strong> {st.session_state.assessment_data['industry']} | 
           <strong>Tamaño:</strong> {st.session_state.assessment_data['company_size']}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Métricas principales
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Madurez General", f"Nivel {results['maturity_level']}", f"{results['overall_score']:.1f}%")
    
    with col2:
        best_function = max(results['function_scores'].items(), key=lambda x: x[1])
        st.metric("Función Más Fuerte", best_function[0], f"{best_function[1]:.1f}%")
    
    with col3:
        weakest_function = min(results['function_scores'].items(), key=lambda x: x[1])
        st.metric("Mayor Oportunidad", weakest_function[0], f"{weakest_function[1]:.1f}%")
    
    with col4:
        industry = st.session_state.assessment_data['industry']
        if industry in INDUSTRIES:
            benchmark = INDUSTRIES[industry]["benchmark"]
            delta = results['overall_score'] - benchmark
            st.metric("vs. Industria", f"{delta:+.1f}%", f"Promedio: {benchmark:.1f}%")
    
    # Pestañas de resultados
    tab1, tab2, tab3 = st.tabs(["📊 Matriz de Madurez", "🗺️ Roadmap Visual", "📈 Recomendaciones"])
    
    with tab1:
        show_maturity_matrix(results)
    
    with tab2:
        show_visual_roadmap_display(results)
    
    with tab3:
        show_recommendations(assessment, results)
    
    # Botón para reiniciar
    st.markdown("---")
    if st.button("🔄 Realizar Nuevo Assessment", use_container_width=True):
        # Reset session state
        for key in st.session_state.keys():
            del st.session_state[key]
        st.rerun()

def show_maturity_matrix(results):
    """Muestra la matriz de madurez"""
    functions = list(results['function_scores'].keys())
    scores = list(results['function_scores'].values())
    
    # Gráfico de radar
    col1, col2 = st.columns(2)
    
    with col1:
        fig_radar = go.Figure()
        
        fig_radar.add_trace(go.Scatterpolar(
            r=scores,
            theta=functions,
            fill='toself',
            name='Madurez Actual',
            line_color='rgb(211, 47, 47)',
            fillcolor='rgba(211, 47, 47, 0.3)'
        ))
        
        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100]
                )),
            showlegend=True,
            title="Radar de Madurez NIST",
            height=400
        )
        
        st.plotly_chart(fig_radar, use_container_width=True)
    
    with col2:
        # Gráfico de barras
        colors = ['#f44336' if score < 40 else '#ff9800' if score < 60 else '#4caf50' for score in scores]
        
        fig_bar = go.Figure(data=[
            go.Bar(
                x=functions,
                y=scores,
                marker_color=colors,
                text=[f"{score:.1f}%" for score in scores],
                textposition='auto',
            )
        ])
        
        fig_bar.update_layout(
            title="Madurez por Función NIST",
            yaxis=dict(range=[0, 100]),
            height=400
        )
        
        st.plotly_chart(fig_bar, use_container_width=True)

def show_visual_roadmap_display(results):
    """Muestra el roadmap visual estilo Fortinet"""
    current_level = results['maturity_level']
    
    st.markdown(f"""
    <div style="text-align: center; margin: 2rem 0;">
        <h2>🗺️ ROADMAP VISUAL DE MADUREZ EN CIBERSEGURIDAD</h2>
        <h4>Nivel Actual: {current_level}/5 ({results['overall_score']:.1f}%)</h4>
    </div>
    """, unsafe_allow_html=True)
    
    # Crear roadmap interactivo similar a Fortinet
    levels = [
        {"level": 1, "name": "Inicial", "color": "#ffcdd2", "desc": "Procesos ad-hoc"},
        {"level": 2, "name": "Básico", "color": "#ffe0b2", "desc": "Controles básicos"},
        {"level": 3, "name": "Intermedio", "color": "#fff9c4", "desc": "Procesos definidos"},
        {"level": 4, "name": "Avanzado", "color": "#dcedc8", "desc": "Gestión integrada"},
        {"level": 5, "name": "Excelencia", "color": "#c8e6c9", "desc": "Optimización continua"}
    ]
    
    # Crear visualización del roadmap
    fig = go.Figure()
    
    # Línea de progreso
    x_pos = list(range(1, 6))
    y_pos = [1] * 5
    
    # Línea base
    fig.add_trace(go.Scatter(
        x=x_pos, y=y_pos,
        mode='lines',
        line=dict(color='lightgray', width=10),
        showlegend=False
    ))
    
    # Puntos del roadmap
    for i, level_data in enumerate(levels, 1):
        color = '#d32f2f' if i <= current_level else '#e0e0e0'
        size = 30 if i == current_level else 20
        
        fig.add_trace(go.Scatter(
            x=[i], y=[1],
            mode='markers+text',
            marker=dict(size=size, color=color, line=dict(color='white', width=3)),
            text=[f"Nivel {i}<br>{level_data['name']}"],
            textposition="top center",
            showlegend=False
        ))
    
    # Destacar posición actual
    fig.add_trace(go.Scatter(
        x=[current_level], y=[1],
        mode='markers',
        marker=dict(size=40, color='gold', symbol='star', line=dict(color='orange', width=3)),
        showlegend=False,
        name="Posición Actual"
    ))
    
    fig.update_layout(
        title="Tu Progreso en el Roadmap NIST",
        xaxis=dict(range=[0.5, 5.5], showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(range=[0.5, 1.5], showgrid=False, zeroline=False, showticklabels=False),
        height=300,
        showlegend=False
    )
    
    st.plotly_chart(fig, use_container_width=True)

def show_recommendations(assessment, results):
    """Muestra recomendaciones priorizadas"""
    st.subheader("🎯 Próximos Pasos Recomendados")
    
    # Identificar gaps de tecnología
    missing_high_impact = []
    
    for category_name, category_data in TECHNOLOGY_CATALOG.items():
        for tech_name, tech_info in category_data["technologies"].items():
            key = f"{category_name}_{tech_name}"
            if not st.session_state.assessment_data["selected_technologies"].get(key, False):
                if tech_info["impact"] >= 4:  # Solo alto impacto
                    missing_high_impact.append({
                        "name": tech_name,
                        "vendor": tech_info["vendor"],
                        "impact": tech_info["impact"],
                        "nist_function": tech_info["nist"],
                        "category": category_name
                    })
    
    # Ordenar por impacto
    missing_high_impact.sort(key=lambda x: x["impact"], reverse=True)
    
    if missing_high_impact:
        st.write("**🚀 Tecnologías de Alto Impacto Recomendadas:**")
        
        for i, tech in enumerate(missing_high_impact[:5], 1):
            with st.expander(f"🎯 Prioridad {i}: {tech['name']} ({tech['vendor']})"):
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.write(f"**Categoría:** {tech['category']}")
                    st.write(f"**Función NIST:** {tech['nist_function']}")
                    st.write(f"**Vendor:** {tech['vendor']}")
                    
                    if tech["impact"] == 5:
                        st.success("🏆 **Impacto Crítico:** Transformación significativa en madurez")
                    else:
                        st.warning("📈 **Alto Impacto:** Mejora notable en postura de seguridad")
                
                with col2:
                    st.metric("Impacto", f"{tech['impact']}/5")
                    
                    # Estimación de ROI
                    roi_months = 3 if tech["impact"] == 5 else 6
                    st.caption(f"ROI: {roi_months} meses")
    else:
        st.success("🎉 ¡Excelente! Tienes implementadas las principales tecnologías de alto impacto.")
    
    # Recomendaciones por función NIST
    st.markdown("---")
    st.subheader("📋 Recomendaciones por Función NIST")
    
    for function_name, score in results['function_scores'].items():
        if score < 70:  # Solo mostrar funciones con oportunidad de mejora
            with st.expander(f"🔧 Mejorar {function_name} ({score:.1f}%)"):
                st.write(get_function_recommendations(function_name, score))

def get_function_recommendations(function_name: str, score: float) -> str:
    """Genera recomendaciones específicas por función NIST"""
    recommendations = {
        "Identify": f"""
        **Función: Identify ({score:.1f}%)**
        
        📋 **Acciones recomendadas:**
        • Implementar herramientas de gestión de activos automatizada
        • Establecer programa formal de evaluación de vulnerabilidades
        • Desarrollar matriz de clasificación de riesgos
        • Crear inventario completo de aplicaciones y datos críticos
        """,
        "Protect": f"""
        **Función: Protect ({score:.1f}%)**
        
        🛡️ **Acciones recomendadas:**
        • Fortalecer controles de acceso e identidad (IAM/MFA)
        • Implementar soluciones de protección endpoint avanzada
        • Establecer programa de capacitación en ciberseguridad
        • Mejorar segmentación de red y controles perimetrales
        """,
        "Detect": f"""
        **Función: Detect ({score:.1f}%)**
        
        👁️ **Acciones recomendadas:**
        • Implementar plataforma SIEM centralizada
        • Establecer capacidades EDR/NDR avanzadas
        • Desarrollar programa de threat hunting
        • Crear indicadores de compromiso (IoCs) personalizados
        """,
        "Respond": f"""
        **Función: Respond ({score:.1f}%)**
        
        ⚡ **Acciones recomendadas:**
        • Desarrollar plan de respuesta a incidentes formal
        • Implementar plataforma SOAR para automatización
        • Establecer equipo CSIRT dedicado
        • Crear procedimientos de comunicación de crisis
        """,
        "Recover": f"""
        **Función: Recover ({score:.1f}%)**
        
        🔄 **Acciones recomendadas:**
        • Implementar estrategia de backup robusta
        • Desarrollar plan de continuidad de negocio
        • Establecer procedimientos de recuperación probados
        • Crear métricas de tiempo de recuperación (RTO/RPO)
        """
    }
    
    return recommendations.get(function_name, "Consultar con especialistas en ciberseguridad.")

if __name__ == "__main__":
    main()
