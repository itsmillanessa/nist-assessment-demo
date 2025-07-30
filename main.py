import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime
import uuid
from typing import Dict, List

# Configuración de página
st.set_page_config(
    page_title="Fortinet Security Fabric - NIST Assessment",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS mejorado
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
    
    .product-selection-container {
        background: white;
        border: 2px solid #e0e0e0;
        border-radius: 15px;
        padding: 1rem;
        margin: 0.5rem;
        transition: all 0.3s ease;
    }
    
    .product-selection-container:hover {
        border-color: #d32f2f;
        box-shadow: 0 5px 15px rgba(211, 47, 47, 0.2);
    }
    
    .non-fortinet-container {
        background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
        border: 2px solid #2196f3;
        border-radius: 15px;
        padding: 1rem;
        margin: 1rem 0;
        text-align: center;
    }
    
    .progress-container {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        border-left: 4px solid #4caf50;
    }
</style>
""", unsafe_allow_html=True)

# Portfolio COMPLETO de Fortinet
FORTINET_COMPLETE_PORTFOLIO = {
    "Network Security": {
        "icon": "🔥",
        "color": "#d32f2f",
        "description": "Protección perimetral y de red",
        "products": {
            "FortiGate NGFW": {
                "description": "Next-Generation Firewall con inspección profunda de paquetes",
                "nist_function": "Protect",
                "impact": 5,
                "maturity_level": 2
            },
            "FortiWiFi": {
                "description": "Wireless Security integrado con FortiGate",
                "nist_function": "Protect", 
                "impact": 3,
                "maturity_level": 2
            },
            "FortiSwitch": {
                "description": "Secure Switching con microsegmentación",
                "nist_function": "Protect",
                "impact": 4,
                "maturity_level": 3
            },
            "FortiAP": {
                "description": "Access Points seguros gestionados centralmente",
                "nist_function": "Protect",
                "impact": 3,
                "maturity_level": 2
            },
            "FortiExtender": {
                "description": "Conectividad LTE/5G segura para SD-WAN",
                "nist_function": "Protect",
                "impact": 3,
                "maturity_level": 3
            },
            "FortiProxy": {
                "description": "Secure Web Proxy con inspección SSL",
                "nist_function": "Protect",
                "impact": 3,
                "maturity_level": 3
            },
            "FortiDDoS": {
                "description": "Protección DDoS dedicada para data centers",
                "nist_function": "Protect",
                "impact": 4,
                "maturity_level": 4
            },
            "FortiNAC": {
                "description": "Network Access Control para dispositivos IoT",
                "nist_function": "Identify",
                "impact": 4,
                "maturity_level": 3
            }
        }
    },
    "Endpoint Security": {
        "icon": "💻",
        "color": "#ff9800",
        "description": "Protección y gestión de endpoints",
        "products": {
            "FortiClient EMS": {
                "description": "Endpoint Management & Security Suite completo",
                "nist_function": "Protect",
                "impact": 4,
                "maturity_level": 2
            },
            "FortiEDR": {
                "description": "Endpoint Detection & Response con IA",
                "nist_function": "Detect",
                "impact": 5,
                "maturity_level": 4
            },
            "FortiXDR": {
                "description": "Extended Detection & Response multiplataforma",
                "nist_function": "Detect",
                "impact": 5,
                "maturity_level": 5
            },
            "FortiDLP": {
                "description": "Data Loss Prevention para endpoints",
                "nist_function": "Protect",
                "impact": 4,
                "maturity_level": 3
            }
        }
    },
    "Email & Web Security": {
        "icon": "📧",
        "color": "#4caf50",
        "description": "Protección de comunicaciones",
        "products": {
            "FortiMail": {
                "description": "Secure Email Gateway con anti-phishing avanzado",
                "nist_function": "Protect",
                "impact": 4,
                "maturity_level": 2
            },
            "FortiWeb": {
                "description": "Web Application Firewall (WAF) con ML",
                "nist_function": "Protect",
                "impact": 4,
                "maturity_level": 3
            },
            "FortiSandbox": {
                "description": "Advanced Threat Protection con sandbox",
                "nist_function": "Detect",
                "impact": 4,
                "maturity_level": 3
            },
            "FortiPhish": {
                "description": "Phishing Simulation & Security Training",
                "nist_function": "Protect",
                "impact": 3,
                "maturity_level": 2
            }
        }
    },
    "Identity & Access Management": {
        "icon": "🔐",
        "color": "#9c27b0",
        "description": "Gestión de identidades y accesos",
        "products": {
            "FortiAuthenticator": {
                "description": "Multi-Factor Authentication centralizado",
                "nist_function": "Protect",
                "impact": 5,
                "maturity_level": 3
            },
            "FortiToken": {
                "description": "Tokens hardware y software para MFA",
                "nist_function": "Protect",
                "impact": 3,
                "maturity_level": 3
            },
            "FortiPAM": {
                "description": "Privileged Access Management",
                "nist_function": "Protect",
                "impact": 5,
                "maturity_level": 4
            }
        }
    },
    "SOC & Analytics": {
        "icon": "📊",
        "color": "#607d8b",
        "description": "Centro de operaciones de seguridad",
        "products": {
            "FortiSIEM": {
                "description": "Security Information & Event Management",
                "nist_function": "Detect",
                "impact": 5,
                "maturity_level": 4
            },
            "FortiSOAR": {
                "description": "Security Orchestration & Automated Response",
                "nist_function": "Respond",
                "impact": 5,
                "maturity_level": 4
            },
            "FortiAnalyzer": {
                "description": "Centralized Logging & Reporting",
                "nist_function": "Detect",
                "impact": 4,
                "maturity_level": 3
            },
            "FortiNDR": {
                "description": "Network Detection & Response con IA",
                "nist_function": "Detect",
                "impact": 5,
                "maturity_level": 4
            }
        }
    },
    "Management & Orchestration": {
        "icon": "⚙️",
        "color": "#795548",
        "description": "Gestión centralizada del Security Fabric",
        "products": {
            "FortiManager": {
                "description": "Centralized Security Management Platform",
                "nist_function": "Identify",
                "impact": 4,
                "maturity_level": 3
            },
            "FortiCloud": {
                "description": "Cloud-based Management Portal",
                "nist_function": "Identify",
                "impact": 3,
                "maturity_level": 2
            },
            "FortiMonitor": {
                "description": "Digital Experience Monitoring",
                "nist_function": "Detect",
                "impact": 3,
                "maturity_level": 3
            }
        }
    },
    "Cloud Security": {
        "icon": "☁️",
        "color": "#2196f3",
        "description": "Protección en entornos cloud",
        "products": {
            "FortiCWP": {
                "description": "Cloud Workload Protection Platform",
                "nist_function": "Protect",
                "impact": 5,
                "maturity_level": 4
            },
            "FortiCASB": {
                "description": "Cloud Access Security Broker",
                "nist_function": "Protect",
                "impact": 4,
                "maturity_level": 4
            },
            "FortiDevSec": {
                "description": "Application Security Testing",
                "nist_function": "Identify",
                "impact": 4,
                "maturity_level": 4
            }
        }
    }
}

# Industrias y tamaños
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

COMPANY_SIZES = {
    "Pequeña (1-50 empleados)": {"icon": "🏢", "priority": "Fundamentos"},
    "Mediana (51-500 empleados)": {"icon": "🏗️", "priority": "Eficiencia"}, 
    "Grande (501-5000 empleados)": {"icon": "🏰", "priority": "Integración"},
    "Empresa (5000+ empleados)": {"icon": "🌆", "priority": "Optimización"}
}

class MultipleSelectionAssessment:
    def __init__(self):
        if 'multi_assessment' not in st.session_state:
            st.session_state.multi_assessment = {
                'step': 1,
                'industry': None,
                'company_size': None,
                'fortinet_products': {},
                'non_fortinet_categories': {},
                'assessment_complete': False
            }
    
    def calculate_nist_maturity(self) -> Dict:
        """Calcula madurez NIST con selección múltiple"""
        nist_functions = {
            "Identify": {"total_impact": 0, "selected_impact": 0, "weight": 0.15},
            "Protect": {"total_impact": 0, "selected_impact": 0, "weight": 0.35},
            "Detect": {"total_impact": 0, "selected_impact": 0, "weight": 0.25},
            "Respond": {"total_impact": 0, "selected_impact": 0, "weight": 0.15},
            "Recover": {"total_impact": 0, "selected_impact": 0, "weight": 0.10}
        }
        
        # Calcular impactos por función NIST
        for category_name, category_data in FORTINET_COMPLETE_PORTFOLIO.items():
            category_fortinet_count = 0
            category_total_count = len(category_data["products"])
            
            for product_name, product_info in category_data["products"].items():
                nist_function = product_info["nist_function"]
                impact = product_info["impact"]
                maturity_factor = product_info["maturity_level"] / 5.0
                
                weighted_impact = impact * maturity_factor
                nist_functions[nist_function]["total_impact"] += weighted_impact
                
                # Si tiene el producto Fortinet
                if st.session_state.multi_assessment["fortinet_products"].get(f"{category_name}_{product_name}", False):
                    nist_functions[nist_function]["selected_impact"] += weighted_impact
                    category_fortinet_count += 1
            
            # Bonus por "No es Fortinet" solo si no tiene ningún producto Fortinet en la categoría
            if category_fortinet_count == 0 and st.session_state.multi_assessment["non_fortinet_categories"].get(category_name, False):
                # Dar 50% del crédito total de la categoría
                for product_name, product_info in category_data["products"].items():
                    nist_function = product_info["nist_function"]
                    impact = product_info["impact"]
                    maturity_factor = product_info["maturity_level"] / 5.0
                    weighted_impact = impact * maturity_factor
                    nist_functions[nist_function]["selected_impact"] += weighted_impact * 0.5
        
        # Calcular porcentajes con pesos
        results = {}
        weighted_total = 0
        
        for function, data in nist_functions.items():
            if data["total_impact"] > 0:
                percentage = (data["selected_impact"] / data["total_impact"]) * 100
                results[function] = min(percentage, 100)
                weighted_total += percentage * data["weight"]
            else:
                results[function] = 0
        
        overall_score = weighted_total
        
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
    assessment = MultipleSelectionAssessment()
    
    # Header principal
    st.markdown("""
    <div class="main-header">
        <div class="fortinet-logo">🛡️ FORTINET SECURITY FABRIC</div>
        <h2>ROADMAP DE MADUREZ VISUAL</h2>
        <p>Evalúa tu madurez actual en ciberseguridad y visualiza tu camino hacia la excelencia<br>
        con el portafolio completo de Fortinet Security Fabric</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Mostrar paso actual
    current_step = st.session_state.multi_assessment['step']
    
    if current_step == 1:
        show_industry_selection()
    elif current_step == 2:
        show_company_size_selection()
    elif current_step == 3:
        show_multiple_selection_assessment()
    elif current_step == 4:
        show_results_with_multiple_selection(assessment)

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
                f"{industry_data['icon']}\n\n**{industry_name}**\n\nBenchmark: {industry_data['benchmark']}%",
                key=f"industry_{industry_name}",
                use_container_width=True
            ):
                st.session_state.multi_assessment['industry'] = industry_name
                st.rerun()
    
    # Botón continuar
    if st.session_state.multi_assessment['industry']:
        st.markdown("---")
        if st.button("📍 Continuar al Assessment →", type="primary", use_container_width=True):
            st.session_state.multi_assessment['step'] = 2
            st.rerun()

def show_company_size_selection():
    """Paso 2: Selección de tamaño de empresa"""
    st.markdown(f"""
    <div class="section-header">
        <h3>🏢 Tamaño de tu Organización</h3>
        <p>Industria seleccionada: <strong>{st.session_state.multi_assessment['industry']}</strong></p>
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
                st.session_state.multi_assessment['company_size'] = size_name
                st.rerun()
    
    # Navegación
    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Anterior", use_container_width=True):
            st.session_state.multi_assessment['step'] = 1
            st.rerun()
    
    with col2:
        if st.session_state.multi_assessment['company_size']:
            if st.button("🔧 Assessment de Tecnologías Fortinet →", type="primary", use_container_width=True):
                st.session_state.multi_assessment['step'] = 3
                st.rerun()

def show_multiple_selection_assessment():
    """Paso 3: Assessment con selección múltiple por checkboxes"""
    st.markdown("""
    <div class="section-header">
        <h3>🔧 Assessment de Tecnologías Fortinet</h3>
        <p><strong>Selecciona TODAS las tecnologías de Fortinet que tienes implementadas</strong><br>
        Puedes seleccionar múltiples productos por categoría (ej: FortiGate + FortiSwitch + FortiAP)</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Mostrar progreso
    total_products = sum(len(cat["products"]) for cat in FORTINET_COMPLETE_PORTFOLIO.values())
    selected_fortinet = sum(1 for v in st.session_state.multi_assessment["fortinet_products"].values() if v)
    selected_non_fortinet = sum(1 for v in st.session_state.multi_assessment["non_fortinet_categories"].values() if v)
    
    # Calcular cobertura por categorías
    categories_with_fortinet = 0
    total_categories = len(FORTINET_COMPLETE_PORTFOLIO)
    
    for category_name, category_data in FORTINET_COMPLETE_PORTFOLIO.items():
        has_fortinet_in_category = any(
            st.session_state.multi_assessment["fortinet_products"].get(f"{category_name}_{prod}", False)
            for prod in category_data["products"].keys()
        )
        if has_fortinet_in_category:
            categories_with_fortinet += 1
    
    st.markdown(f"""
    <div class="progress-container">
        <h4>📈 Progreso del Assessment</h4>
        <div style="display: flex; justify-content: space-between;">
            <div><strong>Productos Fortinet:</strong> {selected_fortinet}/{total_products}</div>
            <div><strong>Categorías con Fortinet:</strong> {categories_with_fortinet}/{total_categories}</div>
            <div><strong>Otras categorías:</strong> {selected_non_fortinet}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Cálculo temporal de madurez
    temp_assessment = MultipleSelectionAssessment()
    temp_results = temp_assessment.calculate_nist_maturity()
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Productos Seleccionados", selected_fortinet)
    with col2:
        st.metric("Cobertura de Categorías", f"{(categories_with_fortinet/total_categories)*100:.0f}%")
    with col3:
        st.metric("Madurez Estimada", f"{temp_results['overall_score']:.1f}%")
    
    # Assessment por categorías con checkboxes múltiples
    for category_name, category_data in FORTINET_COMPLETE_PORTFOLIO.items():
        st.markdown(f"""
        <div class="category-header">
            {category_data['icon']} {category_name} - {category_data['description']}
        </div>
        """, unsafe_allow_html=True)
        
        # Contenedor para productos Fortinet
        with st.container():
            st.markdown("**🛡️ Productos Fortinet en esta categoría:**")
            
            # Checkboxes para productos Fortinet (selección múltiple)
            cols = st.columns(3)
            for i, (product_name, product_info) in enumerate(category_data["products"].items()):
                with cols[i % 3]:
                    key = f"{category_name}_{product_name}"
                    
                    selected = st.checkbox(
                        f"**{product_name}**",
                        value=st.session_state.multi_assessment["fortinet_products"].get(key, False),
                        key=f"checkbox_{key}",
                        help=f"{product_info['description']} | NIST: {product_info['nist_function']} | Nivel: {product_info['maturity_level']}"
                    )
                    
                    st.session_state.multi_assessment["fortinet_products"][key] = selected
                    
                    if selected:
                        st.success(f"✅ Implementado")
                        st.caption(f"🎯 NIST: {product_info['nist_function']} | 📊 Nivel {product_info['maturity_level']}")
                    else:
                        st.caption(f"📝 {product_info['description'][:50]}...")
        
        # Opción "No es Fortinet" para la categoría
        st.markdown("---")
        
        # Verificar si tiene algún producto Fortinet en esta categoría
        has_fortinet_in_category = any(
            st.session_state.multi_assessment["fortinet_products"].get(f"{category_name}_{prod}", False)
            for prod in category_data["products"].keys()
        )
        
        if not has_fortinet_in_category:
            non_fortinet_selected = st.checkbox(
                f"❌ **No tenemos Fortinet en {category_name}** - Pero tenemos otras soluciones de otros vendors",
                value=st.session_state.multi_assessment["non_fortinet_categories"].get(category_name, False),
                key=f"non_fortinet_checkbox_{category_name}",
                help=f"Marca esta opción si tienes soluciones de otros vendors en {category_name}"
            )
            st.session_state.multi_assessment["non_fortinet_categories"][category_name] = non_fortinet_selected
            
            if non_fortinet_selected:
                st.info(f"🔧 Reconocido: Tienes otras soluciones en {category_name}")
        else:
            st.success(f"🛡️ ¡Excelente! Tienes productos Fortinet en {category_name}")
            # Si tiene Fortinet, asegurar que "No es Fortinet" esté en False
            st.session_state.multi_assessment["non_fortinet_categories"][category_name] = False
        
        st.markdown("---")
    
    # Navegación
    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Anterior", use_container_width=True):
            st.session_state.multi_assessment['step'] = 2
            st.rerun()
    
    with col2:
        total_selections = selected_fortinet + selected_non_fortinet
        if total_selections > 0:
            if st.button("📊 Generar Roadmap de Madurez →", type="primary", use_container_width=True):
                st.session_state.multi_assessment['step'] = 4
                st.session_state.multi_assessment['assessment_complete'] = True
                st.rerun()

def show_results_with_multiple_selection(assessment):
    """Paso 4: Resultados con selección múltiple"""
    results = assessment.calculate_nist_maturity()
    
    # Header de resultados
    st.markdown(f"""
    <div class="section-header">
        <h2>🎯 FORTINET SECURITY FABRIC - ROADMAP DE MADUREZ</h2>
        <h3>Nivel Actual: {results['maturity_level']}/5 ({results['overall_score']:.1f}%)</h3>
        <p><strong>Industria:</strong> {st.session_state.multi_assessment['industry']} | 
           <strong>Tamaño:</strong> {st.session_state.multi_assessment['company_size']}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Análisis de cobertura
    show_coverage_analysis()
    
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
        industry = st.session_state.multi_assessment['industry']
        if industry in INDUSTRIES:
            benchmark = INDUSTRIES[industry]["benchmark"]
            delta = results['overall_score'] - benchmark
            st.metric("vs. Industria", f"{delta:+.1f}%", f"Promedio: {benchmark:.1f}%")
    
    # Roadmap visual (corregido sin errores de Plotly)
    show_corrected_roadmap(assessment, results)
    
    # Pestañas de análisis
    tab1, tab2, tab3 = st.tabs(["📊 Análisis NIST", "🗺️ Recomendaciones", "📋 Resumen Ejecutivo"])
    
    with tab1:
        show_nist_analysis_corrected(results)
    
    with tab2:
        show_multiple_selection_recommendations(assessment, results)
    
    with tab3:
        show_executive_summary(assessment, results)
    
    # Botón para reiniciar
    st.markdown("---")
    if st.button("🔄 Realizar Nuevo Assessment", use_container_width=True):
        for key in st.session_state.keys():
            del st.session_state[key]
        st.rerun()

def show_coverage_analysis():
    """Muestra análisis de cobertura por categorías"""
    st.subheader("📊 Análisis de Cobertura por Categoría")
    
    coverage_data = []
    
    for category_name, category_data in FORTINET_COMPLETE_PORTFOLIO.items():
        total_products = len(category_data["products"])
        fortinet_products = sum(
            1 for prod in category_data["products"].keys()
            if st.session_state.multi_assessment["fortinet_products"].get(f"{category_name}_{prod}", False)
        )
        has_alternative = st.session_state.multi_assessment["non_fortinet_categories"].get(category_name, False)
        
        if fortinet_products > 0:
            status = f"🛡️ Fortinet ({fortinet_products}/{total_products})"
            coverage = (fortinet_products / total_products) * 100
        elif has_alternative:
            status = "🔧 Otras soluciones"
            coverage = 50  # 50% por tener alternativas
        else:
            status = "❌ Sin cobertura"
            coverage = 0
        
        coverage_data.append({
            "Categoría": category_name,
            "Estado": status,
            "Cobertura": f"{coverage:.0f}%",
            "Productos Fortinet": f"{fortinet_products}/{total_products}"
        })
    
    coverage_df = pd.DataFrame(coverage_data)
    st.dataframe(coverage_df, use_container_width=True, hide_index=True)

def show_corrected_roadmap(assessment, results):
    """Roadmap visual corregido sin errores de Plotly"""
    st.subheader("🗺️ Roadmap Visual del Security Fabric")
    
    # Obtener productos implementados
    implemented_products = []
    
    for category_name, category_data in FORTINET_COMPLETE_PORTFOLIO.items():
        for product_name, product_info in category_data["products"].items():
            key = f"{category_name}_{product_name}"
            if st.session_state.multi_assessment["fortinet_products"].get(key, False):
                implemented_products.append({
                    "name": product_name,
                    "category": category_name,
                    "maturity_level": product_info["maturity_level"],
                    "impact": product_info["impact"],
                    "nist_function": product_info["nist_function"]
                })
    
    if implemented_products:
        # Crear figura simple sin errores
        fig = go.Figure()
        
        # Colores por función NIST
        nist_colors = {
            'Identify': '#2196F3',
            'Protect': '#4CAF50', 
            'Detect': '#FF9800',
            'Respond': '#F44336',
            'Recover': '#9C27B0'
        }
        
        # Línea de progreso principal
        fig.add_trace(go.Scatter(
            x=[0.5, 5.5], 
            y=[0.5, 5.5],
            mode='lines',
            line=dict(color='lightgray', width=8),
            showlegend=False,
            name='Roadmap'
        ))
        
        # Posicionar productos implementados
        for product in implemented_products:
            x_pos = product['maturity_level'] + np.random.uniform(-0.2, 0.2)
            y_pos = product['maturity_level'] + np.random.uniform(-0.2, 0.2)
            
            color = nist_colors.get(product['nist_function'], '#666666')
            marker_size = 12 + product['impact'] * 3
            
            fig.add_trace(go.Scatter(
                x=[x_pos], 
                y=[y_pos],
                mode='markers+text',
                marker=dict(
                    size=marker_size,
                    color=color,
                    line=dict(color='white', width=2)
                ),
                text=[product['name'].replace('Forti', '')],
                textposition="top center",
                textfont=dict(size=8),
                showlegend=False,
                name=product['name']
            ))
        
        # Marcar nivel actual
        current_level = results['maturity_level']
        fig.add_trace(go.Scatter(
            x=[current_level], 
            y=[current_level],
            mode='markers+text',
            marker=dict(
                size=40,
                color='red',
                symbol='star',
                line=dict(color='darkred', width=3)
            ),
            text=['USTED ESTÁ AQUÍ'],
            textposition="bottom center",
            textfont=dict(size=10, color='red'),
            showlegend=False,
            name="Posición Actual"
        ))
        
        # Configuración corregida
        fig.update_layout(
            title="🗺️ Roadmap de Productos Fortinet Implementados",
            xaxis=dict(
                range=[0, 6],
                title="Nivel de Madurez NIST →",
                tickvals=[1, 2, 3, 4, 5],
                ticktext=['Nivel 1', 'Nivel 2', 'Nivel 3', 'Nivel 4', 'Nivel 5']
            ),
            yaxis=dict(
                range=[0, 6],
                title="↑ Cobertura Security Fabric",
                tickvals=[1, 2, 3, 4, 5],
                ticktext=['Básico', 'Estándar', 'Avanzado', 'Empresarial', 'Zero Trust']
            ),
            height=500,
            showlegend=False
        )
        
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Selecciona algunos productos Fortinet para ver el roadmap visual.")

def show_nist_analysis_corrected(results):
    """Análisis NIST corregido"""
    functions = list(results['function_scores'].keys())
    scores = list(results['function_scores'].values())
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Radar chart simplificado
        fig_radar = go.Figure()
        
        fig_radar.add_trace(go.Scatterpolar(
            r=scores,
            theta=functions,
            fill='toself',
            name='Madurez Actual',
            line_color='rgb(211, 47, 47)'
        ))
        
        fig_radar.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
            title="Radar de Madurez NIST",
            height=400
        )
        
        st.plotly_chart(fig_radar, use_container_width=True)
    
    with col2:
        # Gráfico de barras simple
        colors = ['#f44336' if score < 40 else '#ff9800' if score < 60 else '#4caf50' for score in scores]
        
        fig_bar = go.Figure(data=[
            go.Bar(
                x=functions,
                y=scores,
                marker_color=colors,
                text=[f"{score:.1f}%" for score in scores],
                textposition='auto'
            )
        ])
        
        fig_bar.update_layout(
            title="Madurez por Función NIST",
            yaxis=dict(range=[0, 100]),
            height=400
        )
        
        st.plotly_chart(fig_bar, use_container_width=True)

def show_multiple_selection_recommendations(assessment, results):
    """Recomendaciones basadas en selección múltiple"""
    st.subheader("🎯 Recomendaciones Priorizadas")
    
    # Identificar categorías sin cobertura
    uncovered_categories = []
    partial_coverage = []
    
    for category_name, category_data in FORTINET_COMPLETE_PORTFOLIO.items():
        total_products = len(category_data["products"])
        fortinet_products = sum(
            1 for prod in category_data["products"].keys()
            if st.session_state.multi_assessment["fortinet_products"].get(f"{category_name}_{prod}", False)
        )
        has_alternative = st.session_state.multi_assessment["non_fortinet_categories"].get(category_name, False)
        
        if fortinet_products == 0 and not has_alternative:
            uncovered_categories.append(category_name)
        elif fortinet_products > 0 and fortinet_products < total_products:
            partial_coverage.append({
                "category": category_name,
                "coverage": f"{fortinet_products}/{total_products}"
            })
    
    # Mostrar recomendaciones críticas
    if uncovered_categories:
        st.error("🚨 **Categorías sin cobertura (Crítico):**")
        for category in uncovered_categories:
            st.write(f"❌ **{category}** - Sin protección en esta área")
    
    # Mostrar oportunidades de expansión
    if partial_coverage:
        st.warning("📈 **Oportunidades de expansión:**")
        for item in partial_coverage:
            st.write(f"🔧 **{item['category']}** - Cobertura parcial ({item['coverage']})")
    
    if not uncovered_categories and not partial_coverage:
        st.success("🎉 ¡Excelente cobertura del portfolio Fortinet!")

def show_executive_summary(assessment, results):
    """Resumen ejecutivo"""
    st.subheader("📋 Resumen Ejecutivo")
    
    total_products = sum(len(cat["products"]) for cat in FORTINET_COMPLETE_PORTFOLIO.values())
    selected_fortinet = sum(1 for v in st.session_state.multi_assessment["fortinet_products"].values() if v)
    
    st.markdown(f"""
    **🎯 Resultados del Assessment:**
    
    - **Nivel de Madurez:** {results['maturity_level']}/5 ({results['overall_score']:.1f}%)
    - **Productos Fortinet:** {selected_fortinet}/{total_products} implementados
    - **Industria:** {st.session_state.multi_assessment['industry']}
    - **Tamaño:** {st.session_state.multi_assessment['company_size']}
    
    **📊 Análisis por Función NIST:**
    """)
    
    for function, score in results['function_scores'].items():
        if score >= 70:
            status = "✅ Fuerte"
        elif score >= 40:
            status = "⚠️ Moderado"
        else:
            status = "❌ Débil"
        
        st.write(f"- **{function}:** {score:.1f}% {status}")

if __name__ == "__main__":
    main()
