import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime, timedelta
import uuid
from typing import Dict, List

# Configuración de página
st.set_page_config(
    page_title="Fortinet Security Fabric - Enhanced Roadmap",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS mejorado con estilos para timeline
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
    
    .timeline-container {
        background: linear-gradient(135deg, #e8f5e8 0%, #f0f8f0 100%);
        border: 2px solid #4caf50;
        border-radius: 15px;
        padding: 2rem;
        margin: 2rem 0;
    }
    
    .phase-card {
        background: white;
        border: 2px solid #e0e0e0;
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
        transition: all 0.3s ease;
    }
    
    .phase-card:hover {
        border-color: #4caf50;
        box-shadow: 0 5px 15px rgba(76, 175, 80, 0.3);
    }
    
    .fortinet-section {
        background: linear-gradient(135deg, #ffebee 0%, #ffcdd2 100%);
        border: 2px solid #d32f2f;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
    }
    
    .non-fortinet-section {
        background: linear-gradient(135deg, #e8f5e8 0%, #c8e6c9 100%);
        border: 2px solid #4caf50;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
    }
    
    .technology-tag {
        background: #e3f2fd;
        border: 1px solid #2196f3;
        border-radius: 20px;
        padding: 0.3rem 0.8rem;
        margin: 0.2rem;
        display: inline-block;
        font-size: 0.8rem;
    }
</style>
""", unsafe_allow_html=True)

# Portfolio solo Fortinet con fases de implementación
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
                "maturity_level": 2,
                "implementation_phase": 1
            },
            "FortiWiFi": {
                "description": "Wireless Security integrado con FortiGate",
                "nist_function": "Protect", 
                "impact": 3,
                "maturity_level": 2,
                "implementation_phase": 1
            },
            "FortiSwitch": {
                "description": "Secure Switching con microsegmentación",
                "nist_function": "Protect",
                "impact": 4,
                "maturity_level": 3,
                "implementation_phase": 2
            },
            "FortiAP": {
                "description": "Access Points seguros gestionados centralmente",
                "nist_function": "Protect",
                "impact": 3,
                "maturity_level": 2,
                "implementation_phase": 2
            },
            "FortiExtender": {
                "description": "Conectividad LTE/5G segura para SD-WAN",
                "nist_function": "Protect",
                "impact": 3,
                "maturity_level": 3,
                "implementation_phase": 3
            },
            "FortiProxy": {
                "description": "Secure Web Proxy con inspección SSL",
                "nist_function": "Protect",
                "impact": 3,
                "maturity_level": 3,
                "implementation_phase": 3
            },
            "FortiDDoS": {
                "description": "Protección DDoS dedicada para data centers",
                "nist_function": "Protect",
                "impact": 4,
                "maturity_level": 4,
                "implementation_phase": 4
            },
            "FortiNAC": {
                "description": "Network Access Control para dispositivos IoT",
                "nist_function": "Identify",
                "impact": 4,
                "maturity_level": 3,
                "implementation_phase": 3
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
                "maturity_level": 2,
                "implementation_phase": 1
            },
            "FortiEDR": {
                "description": "Endpoint Detection & Response con IA",
                "nist_function": "Detect",
                "impact": 5,
                "maturity_level": 4,
                "implementation_phase": 3
            },
            "FortiXDR": {
                "description": "Extended Detection & Response multiplataforma",
                "nist_function": "Detect",
                "impact": 5,
                "maturity_level": 5,
                "implementation_phase": 4
            },
            "FortiDLP": {
                "description": "Data Loss Prevention para endpoints",
                "nist_function": "Protect",
                "impact": 4,
                "maturity_level": 3,
                "implementation_phase": 3
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
                "maturity_level": 2,
                "implementation_phase": 2
            },
            "FortiWeb": {
                "description": "Web Application Firewall (WAF) con ML",
                "nist_function": "Protect",
                "impact": 4,
                "maturity_level": 3,
                "implementation_phase": 2
            },
            "FortiSandbox": {
                "description": "Advanced Threat Protection con sandbox",
                "nist_function": "Detect",
                "impact": 4,
                "maturity_level": 3,
                "implementation_phase": 3
            },
            "FortiPhish": {
                "description": "Phishing Simulation & Security Training",
                "nist_function": "Protect",
                "impact": 3,
                "maturity_level": 2,
                "implementation_phase": 2
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
                "maturity_level": 3,
                "implementation_phase": 2
            },
            "FortiToken": {
                "description": "Tokens hardware y software para MFA",
                "nist_function": "Protect",
                "impact": 3,
                "maturity_level": 3,
                "implementation_phase": 2
            },
            "FortiPAM": {
                "description": "Privileged Access Management",
                "nist_function": "Protect",
                "impact": 5,
                "maturity_level": 4,
                "implementation_phase": 4
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
                "maturity_level": 4,
                "implementation_phase": 3
            },
            "FortiSOAR": {
                "description": "Security Orchestration & Automated Response",
                "nist_function": "Respond",
                "impact": 5,
                "maturity_level": 4,
                "implementation_phase": 4
            },
            "FortiAnalyzer": {
                "description": "Centralized Logging & Reporting",
                "nist_function": "Detect",
                "impact": 4,
                "maturity_level": 3,
                "implementation_phase": 2
            },
            "FortiNDR": {
                "description": "Network Detection & Response con IA",
                "nist_function": "Detect",
                "impact": 5,
                "maturity_level": 4,
                "implementation_phase": 4
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
                "maturity_level": 3,
                "implementation_phase": 2
            },
            "FortiCloud": {
                "description": "Cloud-based Management Portal",
                "nist_function": "Identify",
                "impact": 3,
                "maturity_level": 2,
                "implementation_phase": 1
            },
            "FortiMonitor": {
                "description": "Digital Experience Monitoring",
                "nist_function": "Detect",
                "impact": 3,
                "maturity_level": 3,
                "implementation_phase": 3
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
                "maturity_level": 4,
                "implementation_phase": 4
            },
            "FortiCASB": {
                "description": "Cloud Access Security Broker",
                "nist_function": "Protect",
                "impact": 4,
                "maturity_level": 4,
                "implementation_phase": 4
            },
            "FortiDevSec": {
                "description": "Application Security Testing",
                "nist_function": "Identify",
                "impact": 4,
                "maturity_level": 4,
                "implementation_phase": 5
            }
        }
    }
}

# Fases de implementación temporal
IMPLEMENTATION_PHASES = {
    1: {
        "name": "Fundamentos (0-3 meses)",
        "description": "Establecer protecciones básicas y fundamentales",
        "color": "#f44336",
        "focus": "Protect & Identify"
    },
    2: {
        "name": "Consolidación (3-6 meses)", 
        "description": "Fortalecer capacidades centrales y gestión",
        "color": "#ff9800",
        "focus": "Protect & Detect"
    },
    3: {
        "name": "Detección Avanzada (6-12 meses)",
        "description": "Implementar capacidades de detección y respuesta",
        "color": "#2196f3",
        "focus": "Detect & Respond"
    },
    4: {
        "name": "Optimización (12-18 meses)",
        "description": "Automatización y orquestación avanzada",
        "color": "#4caf50",
        "focus": "Respond & Recover"
    },
    5: {
        "name": "Excelencia (18-24 meses)",
        "description": "Zero Trust y capacidades de vanguardia",
        "color": "#9c27b0",
        "focus": "All Functions"
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

class EnhancedMultipleSelectionAssessment:
    def __init__(self):
        if 'enhanced_multi_assessment' not in st.session_state:
            st.session_state.enhanced_multi_assessment = {
                'step': 1,
                'industry': None,
                'company_size': None,
                'fortinet_products': {},  # category_product -> True/False
                'non_fortinet_categories': {},  # category -> True/False
                'assessment_complete': False
            }
    
    def calculate_enhanced_maturity(self) -> Dict:
        """Cálculo mejorado con selección múltiple Fortinet + No Fortinet"""
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
                
                # Si tiene el producto Fortinet específico
                product_key = f"{category_name}_{product_name}"
                if st.session_state.enhanced_multi_assessment["fortinet_products"].get(product_key, False):
                    nist_functions[nist_function]["selected_impact"] += weighted_impact
                    category_fortinet_count += 1
            
            # Si marcó "No es Fortinet" y NO tiene productos Fortinet en la categoría
            has_non_fortinet = st.session_state.enhanced_multi_assessment["non_fortinet_categories"].get(category_name, False)
            
            if has_non_fortinet and category_fortinet_count == 0:
                # Dar 60% del crédito total de la categoría por tener alternativas
                for product_name, product_info in category_data["products"].items():
                    nist_function = product_info["nist_function"]
                    impact = product_info["impact"]
                    maturity_factor = product_info["maturity_level"] / 5.0
                    weighted_impact = impact * maturity_factor
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
    assessment = EnhancedMultipleSelectionAssessment()
    
    # Header principal
    st.markdown("""
    <div class="main-header">
        <div class="fortinet-logo">🛡️ FORTINET SECURITY FABRIC</div>
        <h2>ROADMAP TEMPORAL DE MADUREZ</h2>
        <p>Evalúa tu infraestructura actual y planifica tu evolución hacia una estrategia de seguridad madura<br>
        <strong>Con timeline de implementación por fases (Nivel 1 al 5)</strong></p>
    </div>
    """, unsafe_allow_html=True)
    
    # Mostrar paso actual
    current_step = st.session_state.enhanced_multi_assessment['step']
    
    if current_step == 1:
        show_enhanced_industry_selection()
    elif current_step == 2:
        show_enhanced_company_size_selection()
    elif current_step == 3:
        show_enhanced_multiple_selection_assessment()
    elif current_step == 4:
        show_enhanced_results_with_timeline(assessment)

def show_enhanced_industry_selection():
    """Paso 1: Selección de industria"""
    st.markdown("""
    <div class="section-header">
        <h3>🏭 Selecciona tu Industria</h3>
        <p>Esta información nos ayuda a personalizar el roadmap temporal y las recomendaciones según las mejores prácticas de tu sector</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Grid de industrias
    cols = st.columns(4)
    
    for i, (industry_name, industry_data) in enumerate(INDUSTRIES.items()):
        with cols[i % 4]:
            if st.button(
                f"{industry_data['icon']}\n\n**{industry_name}**\n\nBenchmark: {industry_data['benchmark']}%",
                key=f"enhanced_industry_{industry_name}",
                use_container_width=True
            ):
                st.session_state.enhanced_multi_assessment['industry'] = industry_name
                st.rerun()
    
    # Botón continuar
    if st.session_state.enhanced_multi_assessment['industry']:
        st.markdown("---")
        st.success(f"✅ Industria seleccionada: **{st.session_state.enhanced_multi_assessment['industry']}**")
        if st.button("📍 Continuar al Análisis de Tamaño →", type="primary", use_container_width=True):
            st.session_state.enhanced_multi_assessment['step'] = 2
            st.rerun()

def show_enhanced_company_size_selection():
    """Paso 2: Selección de tamaño de empresa"""
    st.markdown(f"""
    <div class="section-header">
        <h3>🏢 Tamaño de tu Organización</h3>
        <p>Industria seleccionada: <strong>{st.session_state.enhanced_multi_assessment['industry']}</strong></p>
        <p>Esto determina la complejidad y timeline del roadmap recomendado</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Grid de tamaños con información adicional
    for size_name, size_data in COMPANY_SIZES.items():
        if st.button(
            f"{size_data['icon']} **{size_name}**\n\nPrioridad: {size_data['priority']}\nTimeline típico: {get_typical_timeline(size_name)}",
            key=f"enhanced_size_{size_name}",
            use_container_width=True
        ):
            st.session_state.enhanced_multi_assessment['company_size'] = size_name
            st.rerun()
    
    # Navegación
    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Anterior", use_container_width=True):
            st.session_state.enhanced_multi_assessment['step'] = 1
            st.rerun()
    
    with col2:
        if st.session_state.enhanced_multi_assessment['company_size']:
            st.success(f"✅ Tamaño seleccionado: **{st.session_state.enhanced_multi_assessment['company_size']}**")
            if st.button("🔧 Assessment de Tecnologías →", type="primary", use_container_width=True):
                st.session_state.enhanced_multi_assessment['step'] = 3
                st.rerun()

def get_typical_timeline(company_size):
    """Retorna timeline típico por tamaño de empresa"""
    timelines = {
        "Pequeña (1-50 empleados)": "6-12 meses",
        "Mediana (51-500 empleados)": "12-18 meses", 
        "Grande (501-5000 empleados)": "18-24 meses",
        "Empresa (5000+ empleados)": "24-36 meses"
    }
    return timelines.get(company_size, "12-18 meses")

def show_enhanced_multiple_selection_assessment():
    """Paso 3: Assessment mejorado con selección múltiple Fortinet + No Fortinet"""
    st.markdown("""
    <div class="section-header">
        <h3>🔧 Assessment de Tecnologías</h3>
        <p><strong>Selecciona TODAS las tecnologías Fortinet que tienes implementadas</strong><br>
        También puedes marcar "No es Fortinet" en categorías donde tengas otras soluciones</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Progreso general
    show_enhanced_progress()
    
    # Assessment por categorías
    for category_name, category_data in FORTINET_COMPLETE_PORTFOLIO.items():
        st.markdown(f"""
        <div class="category-header">
            {category_data['icon']} {category_name} - {category_data['description']}
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Sección productos Fortinet con multiselección
            st.markdown("""
            <div class="fortinet-section">
                <h4>🛡️ Productos Fortinet</h4>
                <p>Selecciona todos los productos que tienes implementados:</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Checkboxes para cada producto Fortinet
            for product_name, product_info in category_data["products"].items():
                product_key = f"{category_name}_{product_name}"
                
                selected = st.checkbox(
                    f"**{product_name}**",
                    value=st.session_state.enhanced_multi_assessment["fortinet_products"].get(product_key, False),
                    key=f"fortinet_checkbox_{product_key}",
                    help=f"{product_info['description']} | NIST: {product_info['nist_function']} | Nivel: {product_info['maturity_level']} | Fase: {product_info['implementation_phase']}"
                )
                
                st.session_state.enhanced_multi_assessment["fortinet_products"][product_key] = selected
                
                if selected:
                    st.success(f"✅ {product_name} implementado")
                    st.caption(f"🎯 NIST: {product_info['nist_function']} | 📊 Nivel {product_info['maturity_level']} | ⏱️ Fase {product_info['implementation_phase']}")
                else:
                    st.caption(f"📝 {product_info['description'][:60]}...")
        
        with col2:
            # Sección "No es Fortinet"
            st.markdown("""
            <div class="non-fortinet-section">
                <h4>🔧 Otras Soluciones</h4>
                <p>Si tienes otras tecnologías (no Fortinet) en esta categoría:</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Verificar si tiene algún producto Fortinet en esta categoría
            has_fortinet_in_category = any(
                st.session_state.enhanced_multi_assessment["fortinet_products"].get(f"{category_name}_{prod}", False)
                for prod in category_data["products"].keys()
            )
            
            non_fortinet_selected = st.checkbox(
                f"**No es Fortinet**\n\nTengo otras soluciones de terceros en {category_name}",
                value=st.session_state.enhanced_multi_assessment["non_fortinet_categories"].get(category_name, False),
                key=f"non_fortinet_checkbox_{category_name}",
                help=f"Marca esta opción si tienes soluciones de otros vendors en {category_name} (agnóstico de marca)"
            )
            st.session_state.enhanced_multi_assessment["non_fortinet_categories"][category_name] = non_fortinet_selected
            
            if non_fortinet_selected:
                if has_fortinet_in_category:
                    st.info(f"🔧 Ambiente híbrido: Fortinet + otras soluciones")
                else:
                    st.info(f"🔧 Soluciones de terceros en {category_name}")
            elif has_fortinet_in_category:
                st.success(f"🛡️ Solo Fortinet en {category_name}")
            else:
                st.warning(f"⚠️ Sin protección en {category_name}")
        
        st.markdown("---")
    
    # Navegación
    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Anterior", use_container_width=True):
            st.session_state.enhanced_multi_assessment['step'] = 2
            st.rerun()
    
    with col2:
        total_selections = get_total_technology_count()
        if total_selections > 0:
            if st.button("📊 Generar Roadmap Temporal →", type="primary", use_container_width=True):
                st.session_state.enhanced_multi_assessment['step'] = 4
                st.session_state.enhanced_multi_assessment['assessment_complete'] = True
                st.rerun()

def show_enhanced_progress():
    """Muestra progreso mejorado del assessment"""
    total_fortinet = get_fortinet_technology_count()
    total_non_fortinet = get_non_fortinet_category_count()
    categories_covered = get_categories_covered()
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Productos Fortinet", total_fortinet)
    with col2:
        st.metric("Categorías con Alternativas", total_non_fortinet)
    with col3:
        coverage_pct = (categories_covered / len(FORTINET_COMPLETE_PORTFOLIO)) * 100
        st.metric("Cobertura Total", f"{coverage_pct:.0f}%")
    with col4:
        temp_assessment = EnhancedMultipleSelectionAssessment()
        temp_results = temp_assessment.calculate_enhanced_maturity()
        st.metric("Madurez Estimada", f"{temp_results['overall_score']:.1f}%")

def get_total_technology_count():
    """Cuenta total de tecnologías seleccionadas"""
    fortinet_count = get_fortinet_technology_count()
    non_fortinet_count = get_non_fortinet_category_count()
    return fortinet_count + non_fortinet_count

def get_fortinet_technology_count():
    """Cuenta productos Fortinet seleccionados"""
    return sum(1 for selected in st.session_state.enhanced_multi_assessment["fortinet_products"].values() if selected)

def get_non_fortinet_category_count():
    """Cuenta categorías marcadas como 'No es Fortinet'"""
    return sum(1 for selected in st.session_state.enhanced_multi_assessment["non_fortinet_categories"].values() if selected)

def get_categories_covered():
    """Cuenta categorías con al menos una tecnología"""
    covered = 0
    for category_name in FORTINET_COMPLETE_PORTFOLIO.keys():
        has_fortinet = any(
            st.session_state.enhanced_multi_assessment["fortinet_products"].get(f"{category_name}_{prod}", False)
            for prod in FORTINET_COMPLETE_PORTFOLIO[category_name]["products"].keys()
        )
        has_alternative = st.session_state.enhanced_multi_assessment["non_fortinet_categories"].get(category_name, False)
        
        if has_fortinet or has_alternative:
            covered += 1
    
    return covered

def show_enhanced_results_with_timeline(assessment):
    """Resultados mejorados con timeline temporal"""
    results = assessment.calculate_enhanced_maturity()
    
    # Header de resultados
    st.markdown(f"""
    <div class="section-header">
        <h2>🎯 ROADMAP TEMPORAL - FORTINET SECURITY FABRIC</h2>
        <h3>Nivel Actual: {results['maturity_level']}/5 ({results['overall_score']:.1f}%)</h3>
        <p><strong>Industria:</strong> {st.session_state.enhanced_multi_assessment['industry']} | 
           <strong>Tamaño:</strong> {st.session_state.enhanced_multi_assessment['company_size']}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Timeline de implementación
    show_implementation_timeline(assessment, results)
    
    # Pestañas de análisis
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Estado Actual", "🗺️ Roadmap por Fases", "📈 Análisis NIST", "📋 Plan de Acción"])
    
    with tab1:
        show_current_state_analysis(assessment, results)
    
    with tab2:
        show_phased_roadmap(assessment, results)
    
    with tab3:
        show_enhanced_nist_analysis(results)
    
    with tab4:
        show_action_plan(assessment, results)
    
    # Botón para reiniciar
    st.markdown("---")
    if st.button("🔄 Realizar Nuevo Assessment", use_container_width=True):
        for key in st.session_state.keys():
            del st.session_state[key]
        st.rerun()

def show_implementation_timeline(assessment, results):
    """Muestra timeline de implementación como en la imagen"""
    st.markdown("""
    <div class="timeline-container">
        <h3>🗺️ TIMELINE DE EVOLUCIÓN - ESTRATEGIA DE SEGURIDAD MADURA</h3>
        <p>Roadmap temporal desde Nivel 1 (Inicial) hasta Nivel 5 (Excelencia)</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Crear visualización de timeline similar a la imagen
    fig = create_timeline_visualization(assessment, results)
    st.plotly_chart(fig, use_container_width=True)

def create_timeline_visualization(assessment, results):
    """Crea visualización de timeline como en la imagen"""
    fig = go.Figure()
    
    # Línea base del timeline con gradiente
    phases = list(IMPLEMENTATION_PHASES.keys())
    colors = ['#f44336', '#ff9800', '#2196f3', '#4caf50', '#9c27b0']
    
    # Línea principal del roadmap
    fig.add_trace(go.Scatter(
        x=[0.5, 5.5],
        y=[3, 3],
        mode='lines',
        line=dict(color='lightgray', width=10),
        showlegend=False,
        name='Timeline Base'
    ))
    
    # Agregar fases con colores del IMPLEMENTATION_PHASES
    for phase_num, phase_data in IMPLEMENTATION_PHASES.items():
        # Marcador de fase principal
        fig.add_trace(go.Scatter(
            x=[phase_num],
            y=[3],
            mode='markers+text',
            marker=dict(
                size=80,
                color=phase_data['color'],
                line=dict(color='white', width=4),
                opacity=0.9
            ),
            text=[f"Nivel {phase_num}"],
            textposition="middle center",
            textfont=dict(color='white', size=14, family="Arial Black"),
            showlegend=False,
            name=phase_data['name']
        ))
        
        # Título de fase arriba
        fig.add_annotation(
            x=phase_num,
            y=4.2,
            text=f"<b>{phase_data['name']}</b>",
            showarrow=False,
            font=dict(size=11, color=phase_data['color'], family="Arial Black"),
            align="center"
        )
        
        # Descripción de fase abajo
        fig.add_annotation(
            x=phase_num,
            y=1.8,
            text=phase_data['description'],
            showarrow=False,
            font=dict(size=9, color='#666666'),
            align="center",
            width=120
        )
    
    # Marcar posición actual con estrella prominente
    current_level = results['maturity_level']
    fig.add_trace(go.Scatter(
        x=[current_level],
        y=[4.8],
        mode='markers+text',
        marker=dict(
            size=30,
            color='red',
            symbol='star',
            line=dict(color='darkred', width=3)
        ),
        text=['USTED ESTÁ AQUÍ'],
        textposition="top center",
        textfont=dict(size=12, color='red', family="Arial Black"),
        showlegend=False,
        name="Posición Actual"
    ))
    
    # Agregar productos Fortinet por fase (distribuidos verticalmente)
    y_positions = np.linspace(0.8, 2.2, 8)  # 8 posiciones verticales
    product_index = 0
    
    for category_name, category_data in FORTINET_COMPLETE_PORTFOLIO.items():
        for product_name, product_info in category_data["products"].items():
            phase = product_info['implementation_phase']
            
            # Verificar si está implementado
            product_key = f"{category_name}_{product_name}"
            is_implemented = st.session_state.enhanced_multi_assessment["fortinet_products"].get(product_key, False)
            
            # Color y símbolo según implementación
            if is_implemented:
                color = '#4caf50'  # Verde para implementado
                symbol = 'circle'
                size = 15
            else:
                color = '#e0e0e0'  # Gris para no implementado
                symbol = 'circle-open'
                size = 12
            
            # Posición con algo de randomización horizontal
            x_pos = phase + np.random.uniform(-0.25, 0.25)
            y_pos = y_positions[product_index % len(y_positions)]
            
            fig.add_trace(go.Scatter(
                x=[x_pos],
                y=[y_pos],
                mode='markers+text',
                marker=dict(
                    size=size,
                    color=color,
                    symbol=symbol,
                    line=dict(color='white', width=1)
                ),
                text=[product_name.replace('Forti', '')],
                textposition="top center",
                textfont=dict(size=8, color='#333333'),
                showlegend=False,
                name=product_name,
                hovertemplate=f"<b>{product_name}</b><br>{product_info['description']}<br>Fase: {phase}<br>NIST: {product_info['nist_function']}<extra></extra>"
            ))
            
            product_index += 1
    
    # Configuración del gráfico
    fig.update_layout(
        title={
            'text': "🗺️ ROADMAP COMPLETO - TODAS LAS TECNOLOGÍAS FORTINET SECURITY FABRIC",
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 16, 'family': 'Arial Black', 'color': '#d32f2f'}
        },
        xaxis=dict(
            range=[0.3, 5.7],
            title="← Fases de Implementación Temporal →",
            titlefont=dict(size=14, color='#333333'),
            tickvals=phases,
            ticktext=[f"Nivel {p}" for p in phases],
            showgrid=False,
            zeroline=False
        ),
        yaxis=dict(
            range=[0.5, 5.2],
            showticklabels=False,
            showgrid=False,
            zeroline=False
        ),
        height=700,
        showlegend=False,
        plot_bgcolor='rgba(248,249,250,0.8)',
        paper_bgcolor='white',
        hovermode='closest'
    )
    
    return fig

def show_current_state_analysis(assessment, results):
    """Análisis del estado actual"""
    st.subheader("📊 Análisis del Estado Actual")
    
    # Métricas principales
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Madurez General", f"Nivel {results['maturity_level']}", f"{results['overall_score']:.1f}%")
    
    with col2:
        fortinet_count = get_fortinet_technology_count()
        total_fortinet = sum(len(cat["products"]) for cat in FORTINET_COMPLETE_PORTFOLIO.values())
        st.metric("Productos Fortinet", f"{fortinet_count}/{total_fortinet}")
    
    with col3:
        non_fortinet_count = get_non_fortinet_category_count()
        total_categories = len(FORTINET_COMPLETE_PORTFOLIO)
        st.metric("Categorías con Alternativas", f"{non_fortinet_count}/{total_categories}")
    
    with col4:
        industry = st.session_state.enhanced_multi_assessment['industry']
        if industry in INDUSTRIES:
            benchmark = INDUSTRIES[industry]["benchmark"]
            delta = results['overall_score'] - benchmark
            st.metric("vs. Industria", f"{delta:+.1f}%", f"Promedio: {benchmark:.1f}%")
    
    # Desglose por categorías
    st.subheader("🏗️ Cobertura por Categoría")
    
    coverage_data = []
    for category_name, category_data in FORTINET_COMPLETE_PORTFOLIO.items():
        fortinet_products = []
        for product_name in category_data["products"].keys():
            product_key = f"{category_name}_{product_name}"
            if st.session_state.enhanced_multi_assessment["fortinet_products"].get(product_key, False):
                fortinet_products.append(product_name)
        
        has_alternative = st.session_state.enhanced_multi_assessment["non_fortinet_categories"].get(category_name, False)
        total_products = len(category_data["products"])
        fortinet_count = len(fortinet_products)
        
        # Determinar estado
        if fortinet_count > 0 and has_alternative:
            status = f"🔄 Híbrido: {fortinet_count}/{total_products} Fortinet + Otras"
        elif fortinet_count > 0:
            status = f"🛡️ Fortinet: {fortinet_count}/{total_products} productos"
        elif has_alternative:
            status = "🔧 Solo otras soluciones (No Fortinet)"
        else:
            status = "❌ Sin cobertura"
        
        coverage_data.append({
            "Categoría": category_name,
            "Estado": status,
            "Productos Fortinet": fortinet_count,
            "Total Disponible": total_products,
            "Otras Soluciones": "✅" if has_alternative else "❌"
        })
    
    coverage_df = pd.DataFrame(coverage_data)
    st.dataframe(coverage_df, use_container_width=True, hide_index=True)

def show_phased_roadmap(assessment, results):
    """Muestra roadmap por fases"""
    st.subheader("🗺️ Roadmap por Fases de Implementación")
    
    current_level = results['maturity_level']
    
    for phase_num, phase_data in IMPLEMENTATION_PHASES.items():
        # Determinar estado de la fase
        if phase_num <= current_level:
            phase_status = "✅ COMPLETADO"
            status_color = "success"
        elif phase_num == current_level + 1:
            phase_status = "🎯 SIGUIENTE FASE"
            status_color = "warning"
        else:
            phase_status = "📅 FUTURO"
            status_color = "info"
        
        with st.expander(f"{phase_data['name']} - {phase_status}", expanded=(phase_num <= current_level + 1)):
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown(f"""
                <div class="phase-card">
                    <h4 style="color: {phase_data['color']};">{phase_data['name']}</h4>
                    <p><strong>Descripción:</strong> {phase_data['description']}</p>
                    <p><strong>Enfoque NIST:</strong> {phase_data['focus']}</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                if phase_status == "✅ COMPLETADO":
                    st.success("Fase completada")
                elif phase_status == "🎯 SIGUIENTE FASE":
                    st.warning("Próxima a implementar")
                else:
                    st.info("Planificación futura")
            
            # Productos recomendados para esta fase
            st.markdown("**🛡️ Productos Fortinet recomendados:**")
            
            phase_products = []
            for category_name, category_data in FORTINET_COMPLETE_PORTFOLIO.items():
                for product_name, product_info in category_data["products"].items():
                    if product_info['implementation_phase'] == phase_num:
                        # Verificar si ya está implementado
                        product_key = f"{category_name}_{product_name}"
                        is_implemented = st.session_state.enhanced_multi_assessment["fortinet_products"].get(product_key, False)
                        
                        phase_products.append({
                            "product": product_name,
                            "category": category_name,
                            "description": product_info['description'],
                            "nist": product_info['nist_function'],
                            "implemented": is_implemented,
                            "impact": product_info['impact']
                        })
            
            if phase_products:
                # Ordenar por impacto
                phase_products.sort(key=lambda x: x['impact'], reverse=True)
                
                for product in phase_products:
                    status_icon = "✅" if product['implemented'] else "⭕"
                    impact_stars = "⭐" * product['impact']
                    st.markdown(f"{status_icon} **{product['product']}** ({product['category']}) {impact_stars}")
                    st.caption(f"📝 {product['description']} | 🎯 NIST: {product['nist']}")
            else:
                st.info("No hay productos específicos para esta fase")

def show_enhanced_nist_analysis(results):
    """Análisis NIST mejorado"""
    st.subheader("📈 Análisis por Funciones NIST")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Radar chart
        functions = list(results['function_scores'].keys())
        scores = list(results['function_scores'].values())
        
        fig_radar = go.Figure()
        
        fig_radar.add_trace(go.Scatterpolar(
            r=scores + [scores[0]],  # Cerrar el polígono
            theta=functions + [functions[0]],
            fill='toself',
            name='Madurez Actual',
            line_color='rgb(211, 47, 47)',
            fillcolor='rgba(211, 47, 47, 0.3)'
        ))
        
        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True, 
                    range=[0, 100],
                    ticksuffix="%"
                )
            ),
            title="Radar de Madurez NIST",
            height=400
        )
        
        st.plotly_chart(fig_radar, use_container_width=True)
    
    with col2:
        # Análisis por función
        st.markdown("**📊 Desglose por Función:**")
        
        for function, score in results['function_scores'].items():
            if score >= 70:
                status = "🟢 Fuerte"
                color = "success"
            elif score >= 40:
                status = "🟡 Moderado"
                color = "warning"
            else:
                status = "🔴 Débil"
                color = "error"
            
            st.metric(f"{function}", f"{score:.1f}%", f"{status}")

def show_action_plan(assessment, results):
    """Plan de acción detallado"""
    st.subheader("📋 Plan de Acción Recomendado")
    
    current_level = results['maturity_level']
    next_phase = min(current_level + 1, 5)
    
    st.markdown(f"""
    **🎯 Situación Actual:**
    - Nivel de madurez: **{current_level}/5**
    - Puntaje general: **{results['overall_score']:.1f}%**
    - Próxima fase recomendada: **{IMPLEMENTATION_PHASES[next_phase]['name']}**
    """)
    
    # Identificar gaps críticos
    st.markdown("**🚨 Gaps Críticos a Abordar:**")
    
    critical_gaps = []
    for category_name, category_data in FORTINET_COMPLETE_PORTFOLIO.items():
        # Verificar si tiene cobertura en la categoría
        has_fortinet = any(
            st.session_state.enhanced_multi_assessment["fortinet_products"].get(f"{category_name}_{prod}", False)
            for prod in category_data["products"].keys()
        )
        has_alternative = st.session_state.enhanced_multi_assessment["non_fortinet_categories"].get(category_name, False)
        
        if not has_fortinet and not has_alternative:
            critical_gaps.append(category_name)
    
    if critical_gaps:
        for gap in critical_gaps:
            st.error(f"❌ **{gap}** - Sin protección en esta área crítica")
    else:
        st.success("✅ Todas las categorías tienen algún nivel de cobertura")
    
    # Recomendaciones inmediatas
    st.markdown("**⚡ Acciones Inmediatas (Próximos 3 meses):**")
    
    immediate_actions = []
    for category_name, category_data in FORTINET_COMPLETE_PORTFOLIO.items():
        for product_name, product_info in category_data["products"].items():
            if product_info['implementation_phase'] == next_phase:
                product_key = f"{category_name}_{product_name}"
                is_implemented = st.session_state.enhanced_multi_assessment["fortinet_products"].get(product_key, False)
                
                if not is_implemented:
                    immediate_actions.append({
                        "product": product_name,
                        "category": category_name,
                        "priority": "Alta" if product_info['impact'] >= 4 else "Media",
                        "impact": product_info['impact']
                    })
    
    if immediate_actions:
        # Ordenar por impacto
        immediate_actions.sort(key=lambda x: x['impact'], reverse=True)
        
        for action in immediate_actions[:5]:  # Top 5
            priority_color = "🔴" if action['priority'] == "Alta" else "🟡"
            impact_stars = "⭐" * action['impact']
            st.markdown(f"{priority_color} Implementar **{action['product']}** en {action['category']} {impact_stars} (Prioridad: {action['priority']})")
    else:
        st.info("🎉 Estás al día con las recomendaciones para tu nivel actual")

if __name__ == "__main__":
    main()
