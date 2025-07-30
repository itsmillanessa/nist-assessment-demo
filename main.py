import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime
import uuid
from typing import Dict, List
import math

# Configuración de página
st.set_page_config(
    page_title="Fortinet Security Fabric - NIST Assessment",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS mejorado estilo Fortinet
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
    
    .fortinet-logo {
        color: white;
        font-size: 2rem;
        font-weight: bold;
        margin-bottom: 1rem;
    }
    
    .section-header {
        background: linear-gradient(135deg, #f5f5f5 0%, #e8e8e8 100%);
        padding: 1.5rem;
        border-radius: 10px;
        margin: 2rem 0 1rem 0;
        border-left: 5px solid #d32f2f;
        text-align: center;
    }
    
    .industry-card, .size-card {
        background: white;
        border: 2px solid #e0e0e0;
        border-radius: 15px;
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
    
    .industry-card:hover, .size-card:hover {
        border-color: #d32f2f;
        box-shadow: 0 5px 20px rgba(211, 47, 47, 0.3);
        transform: translateY(-3px);
    }
    
    .industry-card.selected, .size-card.selected {
        border-color: #d32f2f;
        background: linear-gradient(135deg, #ffebee 0%, #ffcdd2 100%);
        box-shadow: 0 5px 20px rgba(211, 47, 47, 0.4);
    }
    
    .fortinet-product-card {
        background: white;
        border: 2px solid #e0e0e0;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 0.8rem;
        text-align: center;
        cursor: pointer;
        transition: all 0.3s ease;
        height: 160px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        align-items: center;
        position: relative;
    }
    
    .fortinet-product-card:hover {
        border-color: #d32f2f;
        box-shadow: 0 8px 25px rgba(211, 47, 47, 0.3);
        transform: translateY(-5px);
    }
    
    .fortinet-product-card.selected {
        border-color: #d32f2f;
        background: linear-gradient(135deg, #ffebee 0%, #ffcdd2 100%);
        box-shadow: 0 8px 25px rgba(211, 47, 47, 0.4);
    }
    
    .product-icon {
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
    }
    
    .product-name {
        font-weight: bold;
        color: #d32f2f;
        font-size: 1.1rem;
        margin-bottom: 0.3rem;
    }
    
    .product-description {
        color: #666;
        font-size: 0.8rem;
        line-height: 1.2;
        margin-bottom: 0.5rem;
    }
    
    .nist-badge {
        background: #2196f3;
        color: white;
        padding: 0.2rem 0.6rem;
        border-radius: 12px;
        font-size: 0.7rem;
        font-weight: bold;
    }
    
    .impact-stars {
        color: #ff9800;
        font-size: 0.8rem;
    }
    
    .checkbox-large {
        position: absolute;
        top: 10px;
        right: 10px;
        transform: scale(1.5);
    }
    
    .category-header {
        background: linear-gradient(135deg, #d32f2f 0%, #f44336 100%);
        color: white;
        padding: 1rem 2rem;
        border-radius: 10px;
        margin: 2rem 0 1rem 0;
        text-align: center;
        font-weight: bold;
        font-size: 1.2rem;
    }
    
    .non-fortinet-card {
        background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
        border: 2px solid #2196f3;
        border-radius: 15px;
        padding: 2rem;
        margin: 1rem;
        text-align: center;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .non-fortinet-card:hover {
        box-shadow: 0 8px 25px rgba(33, 150, 243, 0.3);
        transform: translateY(-3px);
    }
    
    .non-fortinet-card.selected {
        background: linear-gradient(135deg, #c3f7ff 0%, #81d4fa 100%);
        box-shadow: 0 8px 25px rgba(33, 150, 243, 0.4);
    }
    
    .continue-btn {
        background: linear-gradient(135deg, #4caf50 0%, #45a049 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 1.2rem 4rem;
        font-size: 1.3rem;
        font-weight: bold;
        cursor: pointer;
        transition: all 0.3s ease;
        margin: 3rem auto;
        display: block;
        text-transform: uppercase;
    }
    
    .continue-btn:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 20px rgba(76, 175, 80, 0.4);
    }
    
    .roadmap-container {
        background: white;
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        margin: 2rem 0;
        border: 2px solid #e0e0e0;
    }
    
    .level-indicator {
        text-align: center;
        margin: 2rem 0;
        padding: 1rem;
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        border-radius: 15px;
        border-left: 5px solid #d32f2f;
    }
</style>
""", unsafe_allow_html=True)

# Catálogo de productos Fortinet simplificado
FORTINET_PRODUCTS = {
    "Network Security": {
        "icon": "🔥",
        "color": "#d32f2f",
        "products": {
            "FortiGate NGFW": {
                "icon": "🛡️",
                "description": "Next-Generation Firewall - Protección perimetral avanzada y control de aplicaciones",
                "nist_function": "Protect",
                "impact": 5,
                "level_requirement": 2
            },
            "FortiWiFi": {
                "icon": "📶", 
                "description": "Secure Wireless - Protección WiFi empresarial con control de acceso",
                "nist_function": "Protect",
                "impact": 3,
                "level_requirement": 2
            },
            "FortiSwitch": {
                "icon": "🔗",
                "description": "Secure Switching - Switches seguros con microsegmentación",
                "nist_function": "Protect", 
                "impact": 3,
                "level_requirement": 3
            }
        }
    },
    "Endpoint Security": {
        "icon": "💻",
        "color": "#ff9800",
        "products": {
            "FortiClient EMS": {
                "icon": "🖥️",
                "description": "Endpoint Management - Gestión centralizada de endpoints con protección avanzada",
                "nist_function": "Protect",
                "impact": 4,
                "level_requirement": 2
            },
            "FortiEDR": {
                "icon": "🔍",
                "description": "Endpoint Detection & Response - Detección y respuesta avanzada en endpoints",
                "nist_function": "Detect",
                "impact": 5,
                "level_requirement": 4
            }
        }
    },
    "Email & Web Security": {
        "icon": "📧",
        "color": "#4caf50", 
        "products": {
            "FortiMail": {
                "icon": "✉️",
                "description": "Secure Email Gateway - Protección avanzada contra amenazas por email",
                "nist_function": "Protect",
                "impact": 4,
                "level_requirement": 2
            },
            "FortiWeb": {
                "icon": "🌐",
                "description": "Web Application Firewall - Protección de aplicaciones web y APIs",
                "nist_function": "Protect",
                "impact": 4,
                "level_requirement": 3
            },
            "FortiSandbox": {
                "icon": "🧪",
                "description": "Advanced Threat Protection - Análisis de malware avanzado en sandbox",
                "nist_function": "Detect",
                "impact": 4,
                "level_requirement": 3
            }
        }
    },
    "Identity & Access": {
        "icon": "🔐",
        "color": "#9c27b0",
        "products": {
            "FortiAuthenticator": {
                "icon": "🔑",
                "description": "Multi-Factor Authentication - Autenticación robusta y gestión de identidades",
                "nist_function": "Protect",
                "impact": 5,
                "level_requirement": 3
            },
            "FortiToken": {
                "icon": "🎫",
                "description": "Secure Token - Tokens de autenticación seguros para acceso remoto",
                "nist_function": "Protect",
                "impact": 3,
                "level_requirement": 3
            }
        }
    },
    "SOC & Analytics": {
        "icon": "📊",
        "color": "#607d8b",
        "products": {
            "FortiSIEM": {
                "icon": "📈",
                "description": "Security Information & Event Management - Correlación y análisis de eventos",
                "nist_function": "Detect",
                "impact": 5,
                "level_requirement": 4
            },
            "FortiSOAR": {
                "icon": "🎛️", 
                "description": "Security Orchestration & Response - Automatización de respuesta a incidentes",
                "nist_function": "Respond",
                "impact": 5,
                "level_requirement": 4
            },
            "FortiAnalyzer": {
                "icon": "📋",
                "description": "Security Analytics - Logging centralizado y reportes de seguridad",
                "nist_function": "Detect",
                "impact": 4,
                "level_requirement": 3
            }
        }
    },
    "Management": {
        "icon": "⚙️", 
        "color": "#795548",
        "products": {
            "FortiManager": {
                "icon": "🎮",
                "description": "Centralized Management - Gestión centralizada de infraestructura Fortinet",
                "nist_function": "Identify",
                "impact": 4,
                "level_requirement": 3
            },
            "FortiCloud": {
                "icon": "☁️",
                "description": "Cloud Management - Gestión en la nube y monitoreo remoto",
                "nist_function": "Identify", 
                "impact": 3,
                "level_requirement": 2
            }
        }
    },
    "Cloud Security": {
        "icon": "☁️",
        "color": "#2196f3",
        "products": {
            "FortiCWP": {
                "icon": "🌤️",
                "description": "Cloud Workload Protection - Protección de cargas de trabajo en la nube",
                "nist_function": "Protect",
                "impact": 4,
                "level_requirement": 4
            },
            "FortiCASB": {
                "icon": "🔐",
                "description": "Cloud Access Security Broker - Control de acceso a aplicaciones cloud",
                "nist_function": "Protect",
                "impact": 4,
                "level_requirement": 4
            }
        }
    }
}

# Industrias simplificadas
INDUSTRIES = {
    "Servicios Financieros": {"icon": "🏦", "benchmark": 78},
    "Gobierno y Sector Público": {"icon": "🏛️", "benchmark": 72}, 
    "Salud y Farmacéutica": {"icon": "🏥", "benchmark": 69},
    "Retail y E-commerce": {"icon": "🛒", "benchmark": 64},
    "Manufactura e Industrial": {"icon": "🏭", "benchmark": 65},
    "Tecnología y Software": {"icon": "💻", "benchmark": 75},
    "Energía y Utilities": {"icon": "⚡", "benchmark": 76},
    "Educación": {"icon": "🎓", "benchmark": 62}
}

# Tamaños de empresa
COMPANY_SIZES = {
    "Pequeña (1-50 empleados)": {"icon": "🏢", "priority": "Fundamentos"},
    "Mediana (51-500 empleados)": {"icon": "🏗️", "priority": "Eficiencia"}, 
    "Grande (501-5000 empleados)": {"icon": "🏰", "priority": "Integración"},
    "Empresa (5000+ empleados)": {"icon": "🌆", "priority": "Optimización"}
}

class FortinetNISTAssessment:
    def __init__(self):
        if 'fortinet_assessment' not in st.session_state:
            st.session_state.fortinet_assessment = {
                'step': 1,
                'industry': None,
                'company_size': None,
                'fortinet_products': {},
                'non_fortinet_solutions': False,
                'assessment_complete': False
            }
    
    def calculate_nist_maturity(self) -> Dict:
        """Calcula madurez NIST basada en productos Fortinet"""
        nist_functions = {
            "Identify": {"total_impact": 0, "selected_impact": 0},
            "Protect": {"total_impact": 0, "selected_impact": 0}, 
            "Detect": {"total_impact": 0, "selected_impact": 0},
            "Respond": {"total_impact": 0, "selected_impact": 0},
            "Recover": {"total_impact": 0, "selected_impact": 0}
        }
        
        # Calcular impactos por función NIST
        for category_name, category_data in FORTINET_PRODUCTS.items():
            for product_name, product_info in category_data["products"].items():
                nist_function = product_info["nist_function"]
                impact = product_info["impact"]
                
                nist_functions[nist_function]["total_impact"] += impact
                
                if st.session_state.fortinet_assessment["fortinet_products"].get(f"{category_name}_{product_name}", False):
                    nist_functions[nist_function]["selected_impact"] += impact
        
        # Bonus por soluciones no-Fortinet
        if st.session_state.fortinet_assessment["non_fortinet_solutions"]:
            for func in nist_functions.values():
                func["selected_impact"] += 2  # Bonus moderado
        
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
    
    def get_roadmap_positions(self) -> Dict:
        """Calcula posiciones de productos en el roadmap visual"""
        positions = {}
        selected_products = []
        
        # Obtener productos seleccionados
        for category_name, category_data in FORTINET_PRODUCTS.items():
            for product_name, product_info in category_data["products"].items():
                key = f"{category_name}_{product_name}"
                if st.session_state.fortinet_assessment["fortinet_products"].get(key, False):
                    selected_products.append({
                        "name": product_name,
                        "level": product_info["level_requirement"],
                        "impact": product_info["impact"],
                        "nist_function": product_info["nist_function"]
                    })
        
        return selected_products

def main():
    assessment = FortinetNISTAssessment()
    
    # Header principal
    st.markdown("""
    <div class="main-header">
        <div class="fortinet-logo">🛡️ FORTINET SECURITY FABRIC</div>
        <h2>ROADMAP DE MADUREZ VISUAL</h2>
        <p>Evalúa tu madurez actual en ciberseguridad y visualiza tu camino hacia la excelencia con el portafolio completo de Fortinet</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Indicador de pasos simplificado
    current_step = st.session_state.fortinet_assessment['step']
    
    # Mostrar paso actual
    if current_step == 1:
        show_industry_selection()
    elif current_step == 2:
        show_company_size_selection()
    elif current_step == 3:
        show_fortinet_assessment()
    elif current_step == 4:
        show_fortinet_roadmap(assessment)

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
            if st.button(
                f"{industry_data['icon']}\n\n**{industry_name}**\n\nPromedio: {industry_data['benchmark']}%",
                key=f"industry_{industry_name}",
                use_container_width=True
            ):
                st.session_state.fortinet_assessment['industry'] = industry_name
                st.rerun()
    
    # Botón continuar
    if st.session_state.fortinet_assessment['industry']:
        st.markdown("---")
        if st.button("📍 Continuar al Assessment →", type="primary", use_container_width=True):
            st.session_state.fortinet_assessment['step'] = 2
            st.rerun()

def show_company_size_selection():
    """Paso 2: Selección de tamaño de empresa"""
    st.markdown(f"""
    <div class="section-header">
        <h3>🏢 Tamaño de tu Organización</h3>
        <p>Industria seleccionada: <strong>{st.session_state.fortinet_assessment['industry']}</strong></p>
    </div>
    """, unsafe_allow_html=True)
    
    # Grid de tamaños
    cols = st.columns(2)
    
    for i, (size_name, size_data) in enumerate(COMPANY_SIZES.items()):
        with cols[i % 2]:
            if st.button(
                f"{size_data['icon']}\n\n**{size_name}**\n\nPrioridad: {size_data['priority']}",
                key=f"size_{size_name}",
                use_container_width=True
            ):
                st.session_state.fortinet_assessment['company_size'] = size_name
                st.rerun()
    
    # Navegación
    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Anterior", use_container_width=True):
            st.session_state.fortinet_assessment['step'] = 1
            st.rerun()
    
    with col2:
        if st.session_state.fortinet_assessment['company_size']:
            if st.button("🔧 Assessment de Tecnologías Fortinet →", type="primary", use_container_width=True):
                st.session_state.fortinet_assessment['step'] = 3
                st.rerun()

def show_fortinet_assessment():
    """Paso 3: Assessment de productos Fortinet"""
    st.markdown("""
    <div class="section-header">
        <h3>🔧 Assessment de Tecnologías Fortinet</h3>
        <p>Selecciona las tecnologías de Fortinet que tienes <strong>actualmente implementadas</strong> en tu organización</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Mostrar progreso
    total_products = sum(len(cat["products"]) for cat in FORTINET_PRODUCTS.values())
    selected_products = sum(1 for v in st.session_state.fortinet_assessment["fortinet_products"].values() if v)
    progress = selected_products / total_products if total_products > 0 else 0
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Productos Fortinet", f"{selected_products}/{total_products}")
    with col2:
        st.metric("Cobertura", f"{progress:.1%}")
    with col3:
        # Cálculo temporal de madurez
        temp_assessment = FortinetNISTAssessment()
        temp_results = temp_assessment.calculate_nist_maturity()
        st.metric("Madurez Estimada", f"{temp_results['overall_score']:.1f}%")
    
    # Categorías de productos Fortinet
    for category_name, category_data in FORTINET_PRODUCTS.items():
        st.markdown(f"""
        <div class="category-header">
            {category_data['icon']} {category_name}
        </div>
        """, unsafe_allow_html=True)
        
        # Grid de productos en esta categoría
        cols = st.columns(3)
        
        for i, (product_name, product_info) in enumerate(category_data["products"].items()):
            with cols[i % 3]:
                key = f"{category_name}_{product_name}"
                
                # Card de producto
                selected = st.session_state.fortinet_assessment["fortinet_products"].get(key, False)
                
                if st.button(
                    f"{product_info['icon']}\n\n**{product_name}**\n\n{product_info['description']}\n\n🎯 NIST: {product_info['nist_function']} | ⭐ Impacto: {product_info['impact']}/5",
                    key=f"product_{key}",
                    type="primary" if selected else "secondary",
                    use_container_width=True
                ):
                    st.session_state.fortinet_assessment["fortinet_products"][key] = not selected
                    st.rerun()
    
    # Opción para soluciones no-Fortinet
    st.markdown("---")
    st.markdown("""
    <div class="category-header">
        🔧 Otras Soluciones de Seguridad
    </div>
    """, unsafe_allow_html=True)
    
    # Card para no-Fortinet
    non_fortinet_selected = st.session_state.fortinet_assessment["non_fortinet_solutions"]
    
    if st.button(
        "🛠️\n\n**Tenemos otras soluciones de seguridad**\n\n(No son productos Fortinet)\n\nEsto incluye: Firewalls de otros vendors, EDR/XDR, SIEM, etc.",
        key="non_fortinet",
        type="primary" if non_fortinet_selected else "secondary",
        use_container_width=True
    ):
        st.session_state.fortinet_assessment["non_fortinet_solutions"] = not non_fortinet_selected
        st.rerun()
    
    # Navegación
    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Anterior", use_container_width=True):
            st.session_state.fortinet_assessment['step'] = 2
            st.rerun()
    
    with col2:
        total_selections = selected_products + (1 if non_fortinet_selected else 0)
        if total_selections > 0:
            if st.button("📊 Generar Roadmap de Madurez →", type="primary", use_container_width=True):
                st.session_state.fortinet_assessment['step'] = 4
                st.session_state.fortinet_assessment['assessment_complete'] = True
                st.rerun()

def show_fortinet_roadmap(assessment):
    """Paso 4: Roadmap visual de Fortinet"""
    results = assessment.calculate_nist_maturity()
    
    # Header de resultados
    st.markdown(f"""
    <div class="level-indicator">
        <h2>🎯 FORTINET SECURITY FABRIC - ROADMAP DE MADUREZ</h2>
        <h3>Nivel Actual: {results['maturity_level']}/5 ({results['overall_score']:.1f}%)</h3>
        <p><strong>Industria:</strong> {st.session_state.fortinet_assessment['industry']} | 
           <strong>Tamaño:</strong> {st.session_state.fortinet_assessment['company_size']}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Crear roadmap visual como en la imagen
    show_fortinet_visual_roadmap(assessment, results)
    
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
        industry = st.session_state.fortinet_assessment['industry']
        if industry in INDUSTRIES:
            benchmark = INDUSTRIES[industry]["benchmark"]
            delta = results['overall_score'] - benchmark
            st.metric("vs. Industria", f"{delta:+.1f}%", f"Promedio: {benchmark:.1f}%")
    
    # Tabs de análisis
    tab1, tab2, tab3 = st.tabs(["📊 Análisis NIST", "🗺️ Próximos Pasos", "📈 Recomendaciones Fortinet"])
    
    with tab1:
        show_nist_analysis(results)
    
    with tab2:
        show_next_steps(assessment, results)
    
    with tab3:
        show_fortinet_recommendations(assessment, results)
    
    # Botón para reiniciar
    st.markdown("---")
    if st.button("🔄 Realizar Nuevo Assessment", use_container_width=True):
        for key in st.session_state.keys():
            del st.session_state[key]
        st.rerun()

def show_fortinet_visual_roadmap(assessment, results):
    """Crea el roadmap visual estilo Fortinet con productos posicionados"""
    
    # Obtener productos seleccionados
    selected_products = assessment.get_roadmap_positions()
    current_level = results['maturity_level']
    
    # Crear figura con fondo de niveles
    fig = go.Figure()
    
    # Agregar áreas de fondo por nivel
    level_colors = [
        {'level': 1, 'color': 'rgba(255, 205, 210, 0.3)', 'name': 'Inicial'},
        {'level': 2, 'color': 'rgba(255, 224, 178, 0.3)', 'name': 'Básico'},
        {'level': 3, 'color': 'rgba(255, 249, 196, 0.3)', 'name': 'Intermedio'},
        {'level': 4, 'color': 'rgba(220, 237, 200, 0.3)', 'name': 'Avanzado'},
        {'level': 5, 'color': 'rgba(200, 230, 201, 0.3)', 'name': 'Excelencia'}
    ]
    
    # Dibujar línea de progreso principal
    fig.add_trace(go.Scatter(
        x=[0, 5], y=[1, 5],
        mode='lines',
        line=dict(color='rgba(128, 128, 128, 0.5)', width=8),
        showlegend=False,
        name='Roadmap Path'
    ))
    
    # Posicionar productos seleccionados en el roadmap
    for i, product in enumerate(selected_products):
        # Calcular posición basada en nivel requerido
        x_pos = product['level'] + np.random.uniform(-0.3, 0.3)  # Algo de variación horizontal
        y_pos = product['level'] + np.random.uniform(-0.2, 0.2)  # Algo de variación vertical
        
        # Color basado en función NIST
        nist_colors = {
            'Identify': '#2196F3',
            'Protect': '#4CAF50', 
            'Detect': '#FF9800',
            'Respond': '#F44336',
            'Recover': '#9C27B0'
        }
        
        color = nist_colors.get(product['nist_function'], '#666666')
        
        # Agregar producto al roadmap
        fig.add_trace(go.Scatter(
            x=[x_pos], y=[y_pos],
            mode='markers+text',
            marker=dict(
                size=15 + product['impact'] * 3,  # Tamaño basado en impacto
                color=color,
                line=dict(color='white', width=2),
                symbol='circle'
            ),
            text=[product['name'].replace('Forti', '')],  # Nombre corto
            textposition="top center",
            textfont=dict(size=8, color='black'),
            showlegend=False,
            name=product['name'],
            hovertemplate=f"<b>{product['name']}</b><br>" +
                         f"Función NIST: {product['nist_function']}<br>" +
                         f"Impacto: {product['impact']}/5<br>" +
                         f"Nivel requerido: {product['level']}<extra></extra>"
        ))
    
    # Marcar nivel actual
    fig.add_trace(go.Scatter(
        x=[current_level], y=[current_level],
        mode='markers+text',
        marker=dict(
            size=40,
            color='red',
            symbol='star',
            line=dict(color='darkred', width=3)
        ),
        text=['USTED SE ENCUENTRA AQUÍ'],
        textposition="bottom center",
        textfont=dict(size=10, color='red', family='Arial Black'),
        showlegend=False,
        name="Posición Actual"
    ))
    
    # Configurar layout del roadmap
    fig.update_layout(
        title={
            'text': "🗺️ ROADMAP COMPLETO - TODAS LAS TECNOLOGÍAS",
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 20, 'color': '#d32f2f'}
        },
        xaxis=dict(
            range=[0, 6],
            showgrid=True,
            gridcolor='lightgray',
            title="Nivel de Madurez →",
            tickmode='array',
            tickvals=[1, 2, 3, 4, 5],
            ticktext=['Nivel 1<br>Inicial', 'Nivel 2<br>Básico', 'Nivel 3<br>Intermedio', 'Nivel 4<br>Avanzado', 'Nivel 5<br>Excelencia']
        ),
        yaxis=dict(
            range=[0, 6],
            showgrid=True,
            gridcolor='lightgray',
            title="↑ Complejidad y Cobertura",
            tickmode='array',
            tickvals=[1, 2, 3, 4, 5],
            ticktext=['Básico', 'Estándar', 'Avanzado', 'Empresarial', 'Zero Trust']
        ),
        height=600,
        showlegend=False,
        plot_bgcolor='white',
        paper_bgcolor='white'
    )
    
    # Agregar anotaciones para cada nivel
    annotations = [
        dict(x=1, y=0.2, text="Cobertura Básica<br>Desde Inicial hasta Excelencia", showarrow=False, font=dict(size=8)),
        dict(x=5.5, y=5.5, text="Zero Trust & AI<br>Excelencia", showarrow=False, font=dict(size=8, color='purple'))
    ]
    
    fig.update_layout(annotations=annotations)
    
    st.plotly_chart(fig, use_container_width=True)

def show_nist_analysis(results):
    """Muestra análisis detallado NIST"""
    functions = list(results['function_scores'].keys())
    scores = list(results['function_scores'].values())
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Radar chart
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
            polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
            showlegend=True,
            title="Radar de Madurez NIST",
            height=400
        )
        
        st.plotly_chart(fig_radar, use_container_width=True)
    
    with col2:
        # Gráfico de barras
        colors = ['#f44336' if score < 40 else '#ff9800' if score < 60 else '#4caf50' for score in scores]
        
        fig_bar = go.Figure(data=[
            go.Bar(x=functions, y=scores, marker_color=colors, text=[f"{score:.1f}%" for score in scores], textposition='auto')
        ])
        
        fig_bar.update_layout(
            title="Madurez por Función NIST",
            yaxis=dict(range=[0, 100]),
            height=400
        )
        
        st.plotly_chart(fig_bar, use_container_width=True)

def show_next_steps(assessment, results):
    """Muestra próximos pasos recomendados"""
    st.subheader("🎯 Próximos Pasos en tu Roadmap")
    
    current_level = results['maturity_level']
    
    if current_level < 3:
        st.warning("🚀 **Enfoque en Fundamentos:** Establece controles básicos de seguridad")
        st.write("""
        **Prioridades inmediatas:**
        - Implementar FortiGate NGFW para protección perimetral
        - Desplegar FortiClient EMS para protección de endpoints
        - Configurar FortiMail para seguridad de email
        - Establecer FortiAuthenticator para MFA
        """)
    elif current_level < 4:
        st.info("📈 **Fortalecer Detección:** Mejora capacidades de monitoreo y análisis")
        st.write("""
        **Siguientes pasos:**
        - Implementar FortiSIEM para correlación de eventos
        - Agregar FortiEDR para detección avanzada
        - Desplegar FortiAnalyzer para centralización de logs
        - Configurar FortiSandbox para análisis de amenazas
        """)
    else:
        st.success("🏆 **Optimización Avanzada:** Automatización y orchestación")
        st.write("""
        **Nivel empresarial:**
        - Implementar FortiSOAR para automatización
        - Desplegar soluciones cloud (FortiCWP, FortiCASB)
        - Integrar con Security Fabric completo
        - Establecer Zero Trust Architecture
        """)

def show_fortinet_recommendations(assessment, results):
    """Muestra recomendaciones específicas de Fortinet"""
    st.subheader("🛡️ Recomendaciones del Portfolio Fortinet")
    
    # Identificar productos no implementados de alto impacto
    missing_products = []
    
    for category_name, category_data in FORTINET_PRODUCTS.items():
        for product_name, product_info in category_data["products"].items():
            key = f"{category_name}_{product_name}"
            if not st.session_state.fortinet_assessment["fortinet_products"].get(key, False):
                if product_info["impact"] >= 4:
                    missing_products.append({
                        "name": product_name,
                        "category": category_name,
                        "description": product_info["description"],
                        "impact": product_info["impact"],
                        "nist_function": product_info["nist_function"],
                        "level_requirement": product_info["level_requirement"]
                    })
    
    # Ordenar por impacto e importancia
    missing_products.sort(key=lambda x: (x["impact"], -x["level_requirement"]), reverse=True)
    
    if missing_products:
        for i, product in enumerate(missing_products[:5], 1):
            with st.expander(f"🎯 Recomendación {i}: {product['name']}"):
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.write(f"**Categoría:** {product['category']}")
                    st.write(f"**Descripción:** {product['description']}")
                    st.write(f"**Función NIST:** {product['nist_function']}")
                    st.write(f"**Nivel recomendado:** {product['level_requirement']}")
                    
                    if product["impact"] == 5:
                        st.success("🏆 **Impacto Crítico:** Componente esencial del Security Fabric")
                    else:
                        st.warning("📈 **Alto Impacto:** Mejora significativa en postura de seguridad")
                
                with col2:
                    st.metric("Impacto", f"{product['impact']}/5")
                    st.metric("Nivel", product['level_requirement'])
    else:
        st.success("🎉 ¡Excelente! Tienes implementados los productos Fortinet de mayor impacto.")
    
    # Mostrar beneficios del Security Fabric
    st.markdown("---")
    st.info("""
    **💡 Beneficios del Fortinet Security Fabric:**
    - Gestión centralizada desde FortiManager
    - Correlación de eventos con FortiAnalyzer
    - Automatización con FortiSOAR
    - Visibilidad completa del entorno
    - Respuesta coordinada ante amenazas
    """)

if __name__ == "__main__":
    main()
