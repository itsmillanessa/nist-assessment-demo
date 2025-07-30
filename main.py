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
    
    .fortinet-product-card {
        background: white;
        border: 2px solid #e0e0e0;
        border-radius: 15px;
        padding: 1rem;
        margin: 0.5rem;
        text-align: center;
        cursor: pointer;
        transition: all 0.3s ease;
        height: 140px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        align-items: center;
    }
    
    .fortinet-product-card:hover {
        border-color: #d32f2f;
        box-shadow: 0 8px 25px rgba(211, 47, 47, 0.3);
        transform: translateY(-3px);
    }
    
    .fortinet-product-card.selected {
        border-color: #d32f2f;
        background: linear-gradient(135deg, #ffebee 0%, #ffcdd2 100%);
        box-shadow: 0 8px 25px rgba(211, 47, 47, 0.4);
    }
    
    .non-fortinet-card {
        background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
        border: 2px solid #2196f3;
        border-radius: 15px;
        padding: 1rem;
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
    
    .non-fortinet-card:hover {
        box-shadow: 0 8px 25px rgba(33, 150, 243, 0.3);
        transform: translateY(-3px);
    }
    
    .non-fortinet-card.selected {
        background: linear-gradient(135deg, #c3f7ff 0%, #81d4fa 100%);
        box-shadow: 0 8px 25px rgba(33, 150, 243, 0.4);
    }
    
    .product-name {
        font-weight: bold;
        color: #d32f2f;
        font-size: 0.9rem;
        margin-bottom: 0.2rem;
    }
    
    .product-description {
        color: #666;
        font-size: 0.7rem;
        line-height: 1.2;
        margin-bottom: 0.3rem;
    }
    
    .nist-badge {
        background: #2196f3;
        color: white;
        padding: 0.1rem 0.4rem;
        border-radius: 8px;
        font-size: 0.6rem;
        font-weight: bold;
    }
    
    .level-badge {
        background: #ff9800;
        color: white;
        padding: 0.1rem 0.4rem;
        border-radius: 8px;
        font-size: 0.6rem;
        font-weight: bold;
        margin-left: 0.2rem;
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
</style>
""", unsafe_allow_html=True)

# Portfolio COMPLETO de Fortinet con niveles de madurez específicos
FORTINET_COMPLETE_PORTFOLIO = {
    "Network Security": {
        "icon": "🔥",
        "color": "#d32f2f",
        "description": "Protección perimetral y de red",
        "products": {
            "FortiGate NGFW": {
                "description": "Next-Generation Firewall con inspección profunda",
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
                "description": "Access Points seguros centralizados",
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
                "description": "Protección DDoS dedicada",
                "nist_function": "Protect",
                "impact": 4,
                "maturity_level": 4
            },
            "FortiNAC": {
                "description": "Network Access Control para IoT",
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
                "description": "Endpoint Management & Security Suite",
                "nist_function": "Protect",
                "impact": 4,
                "maturity_level": 2
            },
            "FortiEDR": {
                "description": "Endpoint Detection & Response avanzado",
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
            },
            "FortiInsight": {
                "description": "User & Entity Behavior Analytics",
                "nist_function": "Detect",
                "impact": 4,
                "maturity_level": 4
            }
        }
    },
    "Email & Web Security": {
        "icon": "📧",
        "color": "#4caf50",
        "description": "Protección de comunicaciones",
        "products": {
            "FortiMail": {
                "description": "Secure Email Gateway anti-phishing",
                "nist_function": "Protect",
                "impact": 4,
                "maturity_level": 2
            },
            "FortiWeb": {
                "description": "Web Application Firewall (WAF)",
                "nist_function": "Protect",
                "impact": 4,
                "maturity_level": 3
            },
            "FortiSandbox": {
                "description": "Advanced Threat Protection sandbox",
                "nist_function": "Detect",
                "impact": 4,
                "maturity_level": 3
            },
            "FortiPhish": {
                "description": "Phishing Simulation & Training",
                "nist_function": "Protect",
                "impact": 3,
                "maturity_level": 2
            },
            "FortiIsolator": {
                "description": "Browser Isolation remoto",
                "nist_function": "Protect",
                "impact": 3,
                "maturity_level": 4
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
            },
            "FortiPortal": {
                "description": "Portal de autoservicio para usuarios",
                "nist_function": "Protect",
                "impact": 2,
                "maturity_level": 3
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
                "description": "Security Orchestration & Response",
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
                "description": "Network Detection & Response",
                "nist_function": "Detect",
                "impact": 5,
                "maturity_level": 4
            },
            "FortiAIOps": {
                "description": "AI Operations para automatización",
                "nist_function": "Respond",
                "impact": 4,
                "maturity_level": 5
            },
            "FortiDeceptor": {
                "description": "Deception Technology para trampas",
                "nist_function": "Detect",
                "impact": 4,
                "maturity_level": 4
            },
            "FortiRecon": {
                "description": "Digital Risk Protection Service",
                "nist_function": "Identify",
                "impact": 3,
                "maturity_level": 3
            }
        }
    },
    "Management & Orchestration": {
        "icon": "⚙️",
        "color": "#795548",
        "description": "Gestión centralizada",
        "products": {
            "FortiManager": {
                "description": "Centralized Security Management",
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
            },
            "FortiConverter": {
                "description": "Configuration Migration Tool",
                "nist_function": "Identify",
                "impact": 2,
                "maturity_level": 2
            }
        }
    },
    "Cloud Security": {
        "icon": "☁️",
        "color": "#2196f3",
        "description": "Protección en la nube",
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
            "Lacework FortiCNAPP": {
                "description": "Cloud Native Application Protection",
                "nist_function": "Protect",
                "impact": 5,
                "maturity_level": 5
            },
            "FortiDevSec": {
                "description": "Application Security Testing",
                "nist_function": "Identify",
                "impact": 4,
                "maturity_level": 4
            },
            "FortiAppSec Cloud": {
                "description": "Application Security Platform",
                "nist_function": "Protect",
                "impact": 4,
                "maturity_level": 4
            }
        }
    },
    "SASE & SD-WAN": {
        "icon": "🌐",
        "color": "#00bcd4",
        "description": "Secure Access Service Edge",
        "products": {
            "FortiSASE": {
                "description": "Secure Access Service Edge completo",
                "nist_function": "Protect",
                "impact": 5,
                "maturity_level": 4
            },
            "Secure SD-WAN": {
                "description": "Software Defined WAN seguro",
                "nist_function": "Protect",
                "impact": 4,
                "maturity_level": 3
            },
            "FortiGate Cloud": {
                "description": "Virtual Firewalls en la nube",
                "nist_function": "Protect",
                "impact": 4,
                "maturity_level": 3
            }
        }
    },
    "Application Delivery": {
        "icon": "🚀",
        "color": "#8bc34a",
        "description": "Entrega segura de aplicaciones",
        "products": {
            "FortiADC": {
                "description": "Application Delivery Controller",
                "nist_function": "Protect",
                "impact": 3,
                "maturity_level": 3
            },
            "FortiGSLB": {
                "description": "Global Server Load Balancing",
                "nist_function": "Recover",
                "impact": 3,
                "maturity_level": 4
            },
            "FortiCache": {
                "description": "Web Caching y optimización",
                "nist_function": "Protect",
                "impact": 2,
                "maturity_level": 3
            }
        }
    },
    "Operational Technology": {
        "icon": "🏭",
        "color": "#ff5722",
        "description": "Seguridad para entornos OT/ICS",
        "products": {
            "FortiNAC-F": {
                "description": "Network Access Control para OT",
                "nist_function": "Identify",
                "impact": 4,
                "maturity_level": 3
            },
            "FortiGate Rugged": {
                "description": "Firewalls para entornos industriales",
                "nist_function": "Protect",
                "impact": 4,
                "maturity_level": 3
            }
        }
    }
}

# Industrias y tamaños (simplificados)
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

class CompleteFortinetAssessment:
    def __init__(self):
        if 'complete_assessment' not in st.session_state:
            st.session_state.complete_assessment = {
                'step': 1,
                'industry': None,
                'company_size': None,
                'fortinet_products': {},
                'non_fortinet_categories': {},
                'assessment_complete': False
            }
    
    def calculate_nist_maturity(self) -> Dict:
        """Calcula madurez NIST con mapeo más preciso"""
        nist_functions = {
            "Identify": {"total_impact": 0, "selected_impact": 0, "weight": 0.15},
            "Protect": {"total_impact": 0, "selected_impact": 0, "weight": 0.35},
            "Detect": {"total_impact": 0, "selected_impact": 0, "weight": 0.25},
            "Respond": {"total_impact": 0, "selected_impact": 0, "weight": 0.15},
            "Recover": {"total_impact": 0, "selected_impact": 0, "weight": 0.10}
        }
        
        # Calcular impactos por función NIST
        for category_name, category_data in FORTINET_COMPLETE_PORTFOLIO.items():
            for product_name, product_info in category_data["products"].items():
                nist_function = product_info["nist_function"]
                impact = product_info["impact"]
                maturity_factor = product_info["maturity_level"] / 5.0  # Normalizar a 0-1
                
                # El impacto se multiplica por el nivel de madurez requerido
                weighted_impact = impact * maturity_factor
                
                nist_functions[nist_function]["total_impact"] += weighted_impact
                
                # Si tiene el producto Fortinet
                if st.session_state.complete_assessment["fortinet_products"].get(f"{category_name}_{product_name}", False):
                    nist_functions[nist_function]["selected_impact"] += weighted_impact
                
                # Si tiene alternativa no-Fortinet en esta categoría
                elif st.session_state.complete_assessment["non_fortinet_categories"].get(category_name, False):
                    # Dar 60% del crédito para soluciones no-Fortinet
                    nist_functions[nist_function]["selected_impact"] += weighted_impact * 0.6
        
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
    assessment = CompleteFortinetAssessment()
    
    # Header principal
    st.markdown("""
    <div class="main-header">
        <div class="fortinet-logo">🛡️ FORTINET SECURITY FABRIC</div>
        <h2>ROADMAP DE MADUREZ VISUAL</h2>
        <p>Evalúa tu madurez actual en ciberseguridad y visualiza tu camino hacia la excelencia<br>con el portafolio completo de Fortinet Security Fabric</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Mostrar paso actual
    current_step = st.session_state.complete_assessment['step']
    
    if current_step == 1:
        show_industry_selection()
    elif current_step == 2:
        show_company_size_selection()
    elif current_step == 3:
        show_complete_fortinet_assessment()
    elif current_step == 4:
        show_complete_results(assessment)

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
                st.session_state.complete_assessment['industry'] = industry_name
                st.rerun()
    
    # Botón continuar
    if st.session_state.complete_assessment['industry']:
        st.markdown("---")
        if st.button("📍 Continuar al Assessment →", type="primary", use_container_width=True):
            st.session_state.complete_assessment['step'] = 2
            st.rerun()

def show_company_size_selection():
    """Paso 2: Selección de tamaño de empresa"""
    st.markdown(f"""
    <div class="section-header">
        <h3>🏢 Tamaño de tu Organización</h3>
        <p>Industria seleccionada: <strong>{st.session_state.complete_assessment['industry']}</strong></p>
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
                st.session_state.complete_assessment['company_size'] = size_name
                st.rerun()
    
    # Navegación
    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Anterior", use_container_width=True):
            st.session_state.complete_assessment['step'] = 1
            st.rerun()
    
    with col2:
        if st.session_state.complete_assessment['company_size']:
            if st.button("🔧 Assessment de Tecnologías Fortinet →", type="primary", use_container_width=True):
                st.session_state.complete_assessment['step'] = 3
                st.rerun()

def show_complete_fortinet_assessment():
    """Paso 3: Assessment completo de productos Fortinet"""
    st.markdown("""
    <div class="section-header">
        <h3>🔧 Assessment de Tecnologías Fortinet</h3>
        <p>Selecciona las tecnologías de <strong>Fortinet que tienes implementadas</strong> en tu organización<br>
        Si en alguna categoría no tienes Fortinet, marca "No es Fortinet" para incluir otras soluciones</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Mostrar progreso
    total_products = sum(len(cat["products"]) for cat in FORTINET_COMPLETE_PORTFOLIO.values())
    selected_fortinet = sum(1 for v in st.session_state.complete_assessment["fortinet_products"].values() if v)
    selected_non_fortinet = sum(1 for v in st.session_state.complete_assessment["non_fortinet_categories"].values() if v)
    total_selected = selected_fortinet + selected_non_fortinet
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Productos Fortinet", f"{selected_fortinet}/{total_products}")
    with col2:
        st.metric("Otras Categorías", selected_non_fortinet)
    with col3:
        # Cálculo temporal de madurez
        temp_assessment = CompleteFortinetAssessment()
        temp_results = temp_assessment.calculate_nist_maturity()
        st.metric("Madurez Estimada", f"{temp_results['overall_score']:.1f}%")
    
    # Categorías completas de productos Fortinet
    for category_name, category_data in FORTINET_COMPLETE_PORTFOLIO.items():
        st.markdown(f"""
        <div class="category-header">
            {category_data['icon']} {category_name} - {category_data['description']}
        </div>
        """, unsafe_allow_html=True)
        
        # Crear grid: productos Fortinet + opción "No es Fortinet"
        products_list = list(category_data["products"].items())
        
        # Determinar número de columnas basado en cantidad de productos
        num_products = len(products_list)
        cols_count = min(4, num_products + 1)  # +1 para "No es Fortinet"
        cols = st.columns(cols_count)
        
        # Mostrar productos Fortinet
        for i, (product_name, product_info) in enumerate(products_list):
            with cols[i % cols_count]:
                key = f"{category_name}_{product_name}"
                selected = st.session_state.complete_assessment["fortinet_products"].get(key, False)
                
                if st.button(
                    f"**{product_name}**\n\n{product_info['description']}\n\n🎯 {product_info['nist_function']} | 📊 Nivel {product_info['maturity_level']}",
                    key=f"fortinet_{key}",
                    type="primary" if selected else "secondary",
                    use_container_width=True
                ):
                    st.session_state.complete_assessment["fortinet_products"][key] = not selected
                    # Si selecciona Fortinet, deseleccionar "No es Fortinet"
                    if not selected:
                        st.session_state.complete_assessment["non_fortinet_categories"][category_name] = False
                    st.rerun()
        
        # Opción "No es Fortinet" para esta categoría
        with cols[-1]:  # Última columna
            non_fortinet_selected = st.session_state.complete_assessment["non_fortinet_categories"].get(category_name, False)
            
            if st.button(
                f"**❌ No es Fortinet**\n\nTenemos otras soluciones en esta categoría\n\n(Otros vendors)",
                key=f"non_fortinet_{category_name}",
                type="primary" if non_fortinet_selected else "secondary",
                use_container_width=True
            ):
                st.session_state.complete_assessment["non_fortinet_categories"][category_name] = not non_fortinet_selected
                # Si selecciona "No es Fortinet", deseleccionar todos los productos Fortinet de esta categoría
                if not non_fortinet_selected:
                    for product_name in category_data["products"].keys():
                        key = f"{category_name}_{product_name}"
                        st.session_state.complete_assessment["fortinet_products"][key] = False
                st.rerun()
        
        st.markdown("---")
    
    # Navegación
    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Anterior", use_container_width=True):
            st.session_state.complete_assessment['step'] = 2
            st.rerun()
    
    with col2:
        if total_selected > 0:
            if st.button("📊 Generar Roadmap de Madurez →", type="primary", use_container_width=True):
                st.session_state.complete_assessment['step'] = 4
                st.session_state.complete_assessment['assessment_complete'] = True
                st.rerun()

def show_complete_results(assessment):
    """Paso 4: Resultados completos y roadmap"""
    results = assessment.calculate_nist_maturity()
    
    # Header de resultados
    st.markdown(f"""
    <div class="section-header">
        <h2>🎯 FORTINET SECURITY FABRIC - ROADMAP DE MADUREZ</h2>
        <h3>Nivel Actual: {results['maturity_level']}/5 ({results['overall_score']:.1f}%)</h3>
        <p><strong>Industria:</strong> {st.session_state.complete_assessment['industry']} | 
           <strong>Tamaño:</strong> {st.session_state.complete_assessment['company_size']}</p>
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
        industry = st.session_state.complete_assessment['industry']
        if industry in INDUSTRIES:
            benchmark = INDUSTRIES[industry]["benchmark"]
            delta = results['overall_score'] - benchmark
            st.metric("vs. Industria", f"{delta:+.1f}%", f"Promedio: {benchmark:.1f}%")
    
    # Crear roadmap visual mejorado
    show_enhanced_fortinet_roadmap(assessment, results)
    
    # Análisis por pestañas
    tab1, tab2, tab3 = st.tabs(["📊 Análisis NIST", "🗺️ Próximos Pasos", "📈 Recomendaciones Fortinet"])
    
    with tab1:
        show_nist_detailed_analysis(results)
    
    with tab2:
        show_strategic_next_steps(assessment, results)
    
    with tab3:
        show_fortinet_specific_recommendations(assessment, results)
    
    # Botón para reiniciar
    st.markdown("---")
    if st.button("🔄 Realizar Nuevo Assessment", use_container_width=True):
        for key in st.session_state.keys():
            del st.session_state[key]
        st.rerun()

def show_enhanced_fortinet_roadmap(assessment, results):
    """Roadmap visual mejorado con productos posicionados por nivel de madurez"""
    
    # Obtener productos implementados
    implemented_products = []
    
    for category_name, category_data in FORTINET_COMPLETE_PORTFOLIO.items():
        for product_name, product_info in category_data["products"].items():
            key = f"{category_name}_{product_name}"
            if st.session_state.complete_assessment["fortinet_products"].get(key, False):
                implemented_products.append({
                    "name": product_name,
                    "category": category_name,
                    "maturity_level": product_info["maturity_level"],
                    "impact": product_info["impact"],
                    "nist_function": product_info["nist_function"]
                })
    
    # Crear figura del roadmap
    fig = go.Figure()
    
    # Colores por función NIST
    nist_colors = {
        'Identify': '#2196F3',
        'Protect': '#4CAF50', 
        'Detect': '#FF9800',
        'Respond': '#F44336',
        'Recover': '#9C27B0'
    }
    
    # Dibujar línea de progreso principal
    fig.add_trace(go.Scatter(
        x=[0.5, 5.5], y=[0.5, 5.5],
        mode='lines',
        line=dict(color='rgba(128, 128, 128, 0.3)', width=12),
        showlegend=False,
        name='Roadmap Path'
    ))
    
    # Posicionar productos implementados
    for i, product in enumerate(implemented_products):
        # Posición basada en nivel de madurez con algo de dispersión
        x_pos = product['maturity_level'] + np.random.uniform(-0.25, 0.25)
        y_pos = product['maturity_level'] + np.random.uniform(-0.25, 0.25)
        
        color = nist_colors.get(product['nist_function'], '#666666')
        
        # Tamaño basado en impacto
        marker_size = 12 + product['impact'] * 4
        
        fig.add_trace(go.Scatter(
            x=[x_pos], y=[y_pos],
            mode='markers+text',
            marker=dict(
                size=marker_size,
                color=color,
                line=dict(color='white', width=2),
                symbol='circle'
            ),
            text=[product['name'].replace('Forti', '')],
            textposition="top center",
            textfont=dict(size=7, color='black'),
            showlegend=False,
            name=product['name'],
            hovertemplate=f"<b>{product['name']}</b><br>" +
                         f"Categoría: {product['category']}<br>" +
                         f"Función NIST: {product['nist_function']}<br>" +
                         f"Impacto: {product['impact']}/5<br>" +
                         f"Nivel de madurez: {product['maturity_level']}<extra></extra>"
        ))
    
    # Marcar nivel actual de la organización
    current_level = results['maturity_level']
    fig.add_trace(go.Scatter(
        x=[current_level], y=[current_level],
        mode='markers+text',
        marker=dict(
            size=50,
            color='red',
            symbol='star',
            line=dict(color='darkred', width=4)
        ),
        text=['USTED SE<br>ENCUENTRA AQUÍ'],
        textposition="bottom center",
        textfont=dict(size=11, color='red', family='Arial Black'),
        showlegend=False,
        name="Posición Actual"
    ))
    
    # Configurar layout
    fig.update_layout(
        title={
            'text': "🗺️ ROADMAP COMPLETO - FORTINET SECURITY FABRIC",
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 24, 'color': '#d32f2f', 'family': 'Arial Black'}
        },
        xaxis=dict(
            range=[0, 6],
            showgrid=True,
            gridcolor='lightgray',
            gridwidth=1,
            title="Nivel de Madurez NIST →",
            titlefont=dict(size=14, color='#333'),
            tickmode='array',
            tickvals=[1, 2, 3, 4, 5],
            ticktext=['Nivel 1<br>Inicial', 'Nivel 2<br>Básico', 'Nivel 3<br>Intermedio', 'Nivel 4<br>Avanzado', 'Nivel 5<br>Excelencia'],
            tickfont=dict(size=10)
        ),
        yaxis=dict(
            range=[0, 6],
            showgrid=True,
            gridcolor='lightgray',
            gridwidth=1,
            title="↑ Cobertura Security Fabric",
            titlefont=dict(size=14, color='#333'),
            tickmode='array',
            tickvals=[1, 2, 3, 4, 5],
            ticktext=['Básico', 'Estándar', 'Avanzado', 'Empresarial', 'Zero Trust'],
            tickfont=dict(size=10)
        ),
        height=650,
        showlegend=False,
        plot_bgcolor='rgba(248, 249, 250, 0.8)',
        paper_bgcolor='white'
    )
    
    # Agregar anotaciones para niveles
    annotations = [
        dict(x=1, y=0.3, text="Controles<br>Básicos", showarrow=False, font=dict(size=9, color='#666')),
        dict(x=3, y=0.3, text="Security Fabric<br>Integrado", showarrow=False, font=dict(size=9, color='#666')),
        dict(x=5.5, y=5.7, text="Zero Trust<br>& AI", showarrow=False, font=dict(size=9, color='purple'))
    ]
    
    fig.update_layout(annotations=annotations)
    
    st.plotly_chart(fig, use_container_width=True)

def show_nist_detailed_analysis(results):
    """Análisis detallado NIST con pesos"""
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
        # Gráfico de barras con pesos
        weights = [0.15, 0.35, 0.25, 0.15, 0.10]  # Pesos NIST
        colors = ['#f44336' if score < 40 else '#ff9800' if score < 60 else '#4caf50' for score in scores]
        
        fig_bar = go.Figure()
        
        # Barras principales
        fig_bar.add_trace(go.Bar(
            x=functions,
            y=scores,
            marker_color=colors,
            text=[f"{score:.1f}%" for score in scores],
            textposition='auto',
            name='Puntaje'
        ))
        
        # Línea de pesos
        fig_bar.add_trace(go.Scatter(
            x=functions,
            y=[w * 100 for w in weights],
            mode='lines+markers',
            name='Peso en cálculo (%)',
            yaxis='y2',
            line=dict(color='orange', width=3)
        ))
        
        fig_bar.update_layout(
            title="Madurez por Función NIST (con pesos)",
            yaxis=dict(range=[0, 100], title="Madurez (%)"),
            yaxis2=dict(range=[0, 40], overlaying='y', side='right', title="Peso (%)"),
            height=400
        )
        
        st.plotly_chart(fig_bar, use_container_width=True)

def show_strategic_next_steps(assessment, results):
    """Próximos pasos estratégicos basados en nivel de madurez"""
    st.subheader("🎯 Roadmap Estratégico Personalizado")
    
    current_level = results['maturity_level']
    industry = st.session_state.complete_assessment['industry']
    company_size = st.session_state.complete_assessment['company_size']
    
    # Recomendaciones basadas en nivel actual
    if current_level <= 2:
        st.error("🚨 **Prioridad Crítica:** Establecer fundamentos de seguridad")
        
        st.markdown("""
        **🏗️ Fundamentos Esenciales (Próximos 6 meses):**
        
        **Nivel 1 → 2:**
        - ✅ **FortiGate NGFW** - Protección perimetral básica
        - ✅ **FortiClient EMS** - Protección de endpoints 
        - ✅ **FortiMail** - Seguridad de email
        - ✅ **FortiAuthenticator** - Autenticación multifactor
        
        **🎯 Objetivo:** Alcanzar nivel básico de protección
        **💰 Inversión estimada:** $50K - $200K según tamaño
        **📈 Impacto esperado:** +30-40 puntos de madurez
        """)
        
    elif current_level == 3:
        st.warning("⚡ **Acelerar Integración:** Fortalecer detección y respuesta")
        
        st.markdown("""
        **🔍 Capacidades de Detección (Próximos 9 meses):**
        
        **Nivel 3 → 4:**
        - 📊 **FortiSIEM** - Correlación de eventos
        - 🔍 **FortiEDR** - Detección avanzada en endpoints
        - 📈 **FortiAnalyzer** - Centralización de logs
        - 🧪 **FortiSandbox** - Análisis de amenazas
        
        **🎯 Objetivo:** SOC funcional integrado
        **💰 Inversión estimada:** $200K - $500K
        **📈 Impacto esperado:** +20-25 puntos de madurez
        """)
        
    elif current_level >= 4:
        st.success("🏆 **Optimización Avanzada:** Automatización y Zero Trust")
        
        st.markdown("""
        **🤖 Automatización y Orquestación (Próximos 12 meses):**
        
        **Nivel 4 → 5:**
        - 🎛️ **FortiSOAR** - Automatización de respuesta
        - ☁️ **FortiSASE** - Zero Trust Network Access
        - 🛡️ **FortiXDR** - Extended Detection & Response
        - 🤖 **FortiAIOps** - Operaciones con IA
        
        **🎯 Objetivo:** Zero Trust y operaciones autónomas
        **💰 Inversión estimada:** $500K - $1M+
        **📈 Impacto esperado:** +10-15 puntos de madurez
        """)
    
    # Cronograma visual
    st.subheader("📅 Cronograma de Implementación")
    
    # Crear cronograma basado en nivel actual
    timeline_data = []
    
    if current_level <= 2:
        timeline_data = [
            {"Mes": "1-2", "Actividad": "FortiGate + FortiClient", "Tipo": "Fundamentos"},
            {"Mes": "3-4", "Actividad": "FortiMail + FortiAuth", "Tipo": "Fundamentos"},
            {"Mes": "5-6", "Actividad": "Training + Optimización", "Tipo": "Fundamentos"}
        ]
    elif current_level == 3:
        timeline_data = [
            {"Mes": "1-3", "Actividad": "FortiSIEM + FortiAnalyzer", "Tipo": "Detección"},
            {"Mes": "4-6", "Actividad": "FortiEDR + FortiSandbox", "Tipo": "Detección"},
            {"Mes": "7-9", "Actividad": "SOC Integration + Training", "Tipo": "Detección"}
        ]
    else:
        timeline_data = [
            {"Mes": "1-4", "Actividad": "FortiSOAR + Automatización", "Tipo": "Avanzado"},
            {"Mes": "5-8", "Actividad": "FortiSASE + Zero Trust", "Tipo": "Avanzado"},
            {"Mes": "9-12", "Actividad": "FortiXDR + AI Operations", "Tipo": "Avanzado"}
        ]
    
    timeline_df = pd.DataFrame(timeline_data)
    st.dataframe(timeline_df, use_container_width=True, hide_index=True)

def show_fortinet_specific_recommendations(assessment, results):
    """Recomendaciones específicas de productos Fortinet"""
    st.subheader("🛡️ Recomendaciones Priorizadas del Portfolio Fortinet")
    
    # Identificar productos críticos no implementados
    missing_critical = []
    
    for category_name, category_data in FORTINET_COMPLETE_PORTFOLIO.items():
        # Si no tiene nada de Fortinet ni marcó "No es Fortinet" en esta categoría
        category_has_fortinet = any(
            st.session_state.complete_assessment["fortinet_products"].get(f"{category_name}_{prod}", False)
            for prod in category_data["products"].keys()
        )
        
        category_has_alternative = st.session_state.complete_assessment["non_fortinet_categories"].get(category_name, False)
        
        if not category_has_fortinet and not category_has_alternative:
            # Categoría completamente descubierta - crítica
            for product_name, product_info in category_data["products"].items():
                if product_info["impact"] >= 4:  # Solo alto impacto
                    missing_critical.append({
                        "name": product_name,
                        "category": category_name,
                        "description": category_data["description"],
                        "impact": product_info["impact"],
                        "maturity_level": product_info["maturity_level"],
                        "nist_function": product_info["nist_function"],
                        "priority": "Crítica - Sin cobertura"
                    })
        
        elif not category_has_fortinet and category_has_alternative:
            # Tiene alternativas pero podría mejorar con Fortinet
            for product_name, product_info in category_data["products"].items():
                if product_info["impact"] == 5:  # Solo máximo impacto
                    missing_critical.append({
                        "name": product_name,
                        "category": category_name,
                        "description": category_data["description"],
                        "impact": product_info["impact"],
                        "maturity_level": product_info["maturity_level"],
                        "nist_function": product_info["nist_function"],
                        "priority": "Media - Upgrade recomendado"
                    })
    
    # Ordenar por prioridad e impacto
    missing_critical.sort(key=lambda x: (x["priority"] == "Crítica - Sin cobertura", x["impact"], -x["maturity_level"]), reverse=True)
    
    if missing_critical:
        for i, product in enumerate(missing_critical[:6], 1):  # Top 6
            priority_icon = "🚨" if "Crítica" in product["priority"] else "📈"
            
            with st.expander(f"{priority_icon} Recomendación {i}: {product['name']} - {product['priority']}"):
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.write(f"**Categoría:** {product['category']} - {product['description']}")
                    st.write(f"**Función NIST:** {product['nist_function']}")
                    st.write(f"**Nivel de madurez:** {product['maturity_level']}/5")
                    
                    if "Crítica" in product["priority"]:
                        st.error("🚨 **Gap Crítico:** Esta categoría no tiene cobertura")
                        st.write("**Beneficio:** Protección fundamental faltante")
                    else:
                        st.warning("📈 **Oportunidad de Mejora:** Upgrade desde solución actual")
                        st.write("**Beneficio:** Integración con Security Fabric")
                
                with col2:
                    st.metric("Impacto", f"{product['impact']}/5")
                    st.metric("Nivel Req.", product['maturity_level'])
                    
                    # ROI estimado
                    roi_months = 3 if product["impact"] == 5 else 6
                    st.caption(f"ROI: {roi_months} meses")
    else:
        st.success("🎉 ¡Excelente! Tienes una cobertura sólida con el portfolio Fortinet.")
    
    # Mostrar beneficios del Security Fabric
    st.markdown("---")
    st.info("""
    **🔗 Beneficios del Fortinet Security Fabric Completo:**
    
    🎯 **Gestión Unificada:** Control centralizado desde FortiManager
    📊 **Visibilidad Total:** Correlación completa con FortiAnalyzer + FortiSIEM  
    🤖 **Automatización:** Respuesta orquestada con FortiSOAR + FortiAIOps
    🛡️ **Protección Integrada:** Sharing de inteligencia entre todos los componentes
    ⚡ **Respuesta Rápida:** Coordinación automática ante amenazas detectadas
    💰 **TCO Optimizado:** Licenciamiento unificado y soporte consolidado
    """)

if __name__ == "__main__":
    main()
