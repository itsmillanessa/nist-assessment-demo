import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np  # ← AGREGADO: Import de numpy para las funciones matemáticas
from datetime import datetime, timedelta
import uuid
from typing import Dict, List

# Configuración de página
st.set_page_config(
    page_title="Fortinet Security Fabric - Professional Roadmap",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS profesional con tamaño fijo controlado
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    .stApp {
        font-family: 'Inter', sans-serif;
        max-width: 1000px;
        margin: 0 auto;
        font-size: 14px;
    }
    
    .main-header {
        background: linear-gradient(135deg, #1e3a8a 0%, #3730a3 50%, #7c3aed 100%);
        padding: 1.5rem 1rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 1.5rem;
        box-shadow: 0 15px 30px rgba(0,0,0,0.1);
        position: relative;
        overflow: hidden;
    }
    
    .fortinet-logo {
        color: white;
        font-size: 1.75rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        position: relative;
        z-index: 1;
    }
    
    .main-header h2 {
        font-size: 1.25rem;
        margin: 0.5rem 0;
        font-weight: 600;
    }
    
    .main-header p {
        font-size: 0.9rem;
        margin: 0;
        opacity: 0.9;
    }
    
    .section-header {
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
        padding: 1.25rem;
        border-radius: 12px;
        margin: 1.25rem 0;
        border-left: 5px solid #3730a3;
        text-align: center;
        box-shadow: 0 3px 6px rgba(0, 0, 0, 0.05);
    }
    
    .section-header h3 {
        font-size: 1.1rem;
        margin-bottom: 0.5rem;
        color: #1e293b;
    }
    
    .section-header p {
        font-size: 0.85rem;
        margin: 0;
        color: #64748b;
    }
    
    .category-header {
        background: linear-gradient(135deg, #3730a3 0%, #7c3aed 100%);
        color: white;
        padding: 0.875rem 1.25rem;
        border-radius: 12px;
        margin: 1.25rem 0;
        text-align: center;
        font-weight: 600;
        font-size: 1rem;
        box-shadow: 0 6px 12px rgba(55, 48, 163, 0.3);
    }
    
    .timeline-container {
        background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%);
        border: 2px solid #22c55e;
        border-radius: 15px;
        padding: 1.25rem;
        margin: 1.25rem 0;
        box-shadow: 0 8px 20px rgba(34, 197, 94, 0.1);
    }
    
    .timeline-container h3 {
        font-size: 1.1rem;
        margin-bottom: 0.5rem;
        color: #15803d;
    }
    
    .timeline-container p {
        font-size: 0.85rem;
        margin: 0;
        color: #16a34a;
    }
    
    .fortinet-section {
        background: linear-gradient(135deg, #fef2f2 0%, #fee2e2 100%);
        border: 2px solid #dc2626;
        border-radius: 12px;
        padding: 1rem;
        margin: 0.875rem 0;
        box-shadow: 0 3px 6px rgba(220, 38, 38, 0.1);
    }
    
    .fortinet-section h4 {
        font-size: 1rem;
        margin-bottom: 0.75rem;
        color: #dc2626;
    }
    
    .non-fortinet-section {
        background: linear-gradient(135deg, #f0f9ff 0%, #dbeafe 100%);
        border: 2px solid #2563eb;
        border-radius: 12px;
        padding: 1rem;
        margin: 0.875rem 0;
        box-shadow: 0 3px 6px rgba(37, 99, 235, 0.1);
    }
    
    .non-fortinet-section h4 {
        font-size: 1rem;
        margin-bottom: 0.75rem;
        color: #2563eb;
    }
    
    .metric-card {
        background: white;
        border-radius: 12px;
        padding: 0.875rem;
        box-shadow: 0 3px 6px rgba(0, 0, 0, 0.05);
        border: 1px solid #e5e7eb;
        text-align: center;
        margin-bottom: 0.75rem;
    }
    
    .metric-card h3 {
        font-size: 1.25rem;
        margin: 0 0 0.25rem 0;
        font-weight: 700;
    }
    
    .metric-card p {
        font-size: 0.75rem;
        margin: 0;
        color: #64748b;
    }
    
    /* Ajustes específicos para Streamlit */
    .stButton > button {
        font-size: 0.8rem !important;
        padding: 0.4rem 0.875rem !important;
        width: 100% !important;
        border-radius: 6px !important;
    }
    
    .stCheckbox > label {
        font-size: 0.8rem !important;
    }
    
    .stMetric > label {
        font-size: 0.75rem !important;
    }
    
    .stDataFrame {
        font-size: 0.8rem !important;
    }
    
    /* Media queries más específicos */
    @media (max-width: 768px) {
        .stApp {
            max-width: 95%;
            font-size: 13px;
        }
        
        .main-header {
            padding: 1rem 0.75rem;
        }
        
        .stButton > button {
            font-size: 0.75rem !important;
            padding: 0.35rem 0.75rem !important;
        }
    }
</style>
""", unsafe_allow_html=True)

# Portfolio expandido con todas las tecnologías
FORTINET_COMPLETE_PORTFOLIO = {
    "Network Security": {
        "icon": "🔥",
        "color": "#dc2626",
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
        "color": "#ea580c",
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
        "color": "#16a34a",
        "description": "Protección de comunicaciones y contenido web",
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
            },
            "Perception Point": {
                "description": "Advanced Email Security con IA de Fortinet",
                "nist_function": "Protect",
                "impact": 4,
                "maturity_level": 3,
                "implementation_phase": 3
            }
        }
    },
    "Identity & Access Management": {
        "icon": "🔐",
        "color": "#7c3aed",
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
            },
            "FortiTrust": {
                "description": "Identity Verification y Trust Platform",
                "nist_function": "Identify",
                "impact": 4,
                "maturity_level": 4,
                "implementation_phase": 4
            }
        }
    },
    "SOC & Analytics": {
        "icon": "📊",
        "color": "#0f766e",
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
            },
            "FortiDeceptor": {
                "description": "Deception Technology para detección temprana",
                "nist_function": "Detect",
                "impact": 4,
                "maturity_level": 4,
                "implementation_phase": 4
            }
        }
    },
    "Management & Orchestration": {
        "icon": "⚙️",
        "color": "#78716c",
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
            },
            "FortiView": {
                "description": "Network Visibility y Asset Discovery",
                "nist_function": "Identify",
                "impact": 3,
                "maturity_level": 3,
                "implementation_phase": 3
            }
        }
    },
    "Cloud Security": {
        "icon": "☁️",
        "color": "#2563eb",
        "description": "Protección en entornos cloud y DevSecOps",
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
            },
            "FortiCNAPP": {
                "description": "Cloud Native Application Protection Platform",
                "nist_function": "Protect",
                "impact": 5,
                "maturity_level": 5,
                "implementation_phase": 5
            },
            "FortiGSLB": {
                "description": "Global Server Load Balancing",
                "nist_function": "Protect",
                "impact": 3,
                "maturity_level": 4,
                "implementation_phase": 4
            }
        }
    },
    "OT & IoT Security": {
        "icon": "🏭",
        "color": "#b45309",
        "description": "Seguridad para Operational Technology e IoT",
        "products": {
            "FortiNDR for OT": {
                "description": "Network Detection & Response para entornos OT",
                "nist_function": "Detect",
                "impact": 5,
                "maturity_level": 4,
                "implementation_phase": 4
            },
            "FortiGuard OT": {
                "description": "Threat Intelligence para sistemas industriales",
                "nist_function": "Identify",
                "impact": 4,
                "maturity_level": 4,
                "implementation_phase": 4
            },
            "FortiSIEM OT": {
                "description": "SIEM especializado para entornos industriales",
                "nist_function": "Detect",
                "impact": 4,
                "maturity_level": 4,
                "implementation_phase": 4
            }
        }
    }
}

# Fases de implementación temporal
IMPLEMENTATION_PHASES = {
    1: {
        "name": "Fundamentos (0-3 meses)",
        "description": "Establecer protecciones básicas y fundamentales",
        "color": "#dc2626",
        "focus": "Protect & Identify",
        "timeline": "Inmediato"
    },
    2: {
        "name": "Consolidación (3-6 meses)", 
        "description": "Fortalecer capacidades centrales y gestión",
        "color": "#ea580c",
        "focus": "Protect & Detect",
        "timeline": "Corto Plazo"
    },
    3: {
        "name": "Detección Avanzada (6-12 meses)",
        "description": "Implementar capacidades de detección y respuesta",
        "color": "#2563eb",
        "focus": "Detect & Respond",
        "timeline": "Mediano Plazo"
    },
    4: {
        "name": "Optimización (12-18 meses)",
        "description": "Automatización y orquestación avanzada",
        "color": "#16a34a",
        "focus": "Respond & Recover",
        "timeline": "Largo Plazo"
    },
    5: {
        "name": "Excelencia (18-24 meses)",
        "description": "Zero Trust y capacidades de vanguardia",
        "color": "#7c3aed",
        "focus": "All Functions",
        "timeline": "Visión Futura"
    }
}

# Industrias y tamaños expandidos
INDUSTRIES = {
    "Servicios Financieros": {
        "icon": "🏦", 
        "benchmark": 78,
        "priorities": ["Compliance", "Zero Trust", "Fraud Prevention"],
        "regulations": ["PCI-DSS", "SOX", "GDPR"],
        "critical_products": ["FortiPAM", "FortiAuthenticator", "FortiSIEM"],
        "next_steps": "Priorizar gestión de identidades privilegiadas y cumplimiento regulatorio"
    },
    "Gobierno y Sector Público": {
        "icon": "🏛️", 
        "benchmark": 72,
        "priorities": ["National Security", "Citizen Data Protection", "Critical Infrastructure"],
        "regulations": ["FISMA", "FedRAMP", "NIST 800-53"],
        "critical_products": ["FortiGate", "FortiNAC", "FortiAnalyzer"],
        "next_steps": "Implementar controles de seguridad gubernamentales y protección de infraestructura crítica"
    }, 
    "Salud y Farmacéutica": {
        "icon": "🏥", 
        "benchmark": 69,
        "priorities": ["Patient Privacy", "Medical Device Security", "Research Protection"],
        "regulations": ["HIPAA", "FDA", "GxP"],
        "critical_products": ["FortiNAC", "FortiEDR", "FortiDLP"],
        "next_steps": "Asegurar dispositivos médicos y proteger datos de pacientes"
    },
    "Retail y E-commerce": {
        "icon": "🛒", 
        "benchmark": 64,
        "priorities": ["Customer Data", "Payment Security", "Supply Chain"],
        "regulations": ["PCI-DSS", "GDPR", "CCPA"],
        "critical_products": ["FortiWeb", "FortiDDoS", "FortiToken"],
        "next_steps": "Fortalecer protección de aplicaciones web y seguridad de pagos"
    },
    "Manufactura e Industrial": {
        "icon": "🏭", 
        "benchmark": 65,
        "priorities": ["OT Security", "Supply Chain", "IP Protection"],
        "regulations": ["IEC 62443", "NERC CIP", "TSA"],
        "critical_products": ["FortiNDR for OT", "FortiNAC", "FortiGate"],
        "next_steps": "Segmentar redes OT/IT y proteger sistemas de control industrial"
    },
    "Tecnología y Software": {
        "icon": "💻", 
        "benchmark": 75,
        "priorities": ["DevSecOps", "IP Protection", "Cloud Security"],
        "regulations": ["SOC 2", "ISO 27001", "GDPR"],
        "critical_products": ["FortiDevSec", "FortiCWP", "FortiCNAPP"],
        "next_steps": "Integrar seguridad en el ciclo de desarrollo y proteger workloads cloud"
    },
    "Energía y Utilities": {
        "icon": "⚡", 
        "benchmark": 76,
        "priorities": ["Critical Infrastructure", "SCADA Security", "Grid Protection"],
        "regulations": ["NERC CIP", "TSA", "IEC 62443"],
        "critical_products": ["FortiNDR for OT", "FortiSIEM OT", "FortiGate"],
        "next_steps": "Implementar monitoreo de sistemas críticos y segmentación OT"
    },
    "Educación": {
        "icon": "🎓", 
        "benchmark": 62,
        "priorities": ["Student Privacy", "Research Security", "Campus Safety"],
        "regulations": ["FERPA", "GDPR", "COPPA"],
        "critical_products": ["FortiNAC", "FortiClient", "FortiAuthenticator"],
        "next_steps": "Controlar acceso de dispositivos personales y proteger datos estudiantiles"
    }
}

COMPANY_SIZES = {
    "Pequeña (1-50 empleados)": {
        "icon": "🏢", 
        "priority": "Fundamentos", 
        "timeline": "6-12 meses",
        "focus": ["FortiGate", "FortiClient", "FortiMail"],
        "next_steps": "Establecer protecciones básicas de red y endpoints"
    },
    "Mediana (51-500 empleados)": {
        "icon": "🏗️", 
        "priority": "Eficiencia", 
        "timeline": "12-18 meses",
        "focus": ["FortiAnalyzer", "FortiAuthenticator", "FortiManager"],
        "next_steps": "Centralizar gestión e implementar visibilidad"
    }, 
    "Grande (501-5000 empleados)": {
        "icon": "🏰", 
        "priority": "Integración", 
        "timeline": "18-24 meses",
        "focus": ["FortiSIEM", "FortiEDR", "FortiSOAR"],
        "next_steps": "Implementar SOC y capacidades de detección avanzada"
    },
    "Empresa (5000+ empleados)": {
        "icon": "🌆", 
        "priority": "Optimización", 
        "timeline": "24-36 meses",
        "focus": ["FortiXDR", "FortiCNAPP", "FortiNDR"],
        "next_steps": "Evolucionar hacia Zero Trust y automatización completa"
    }
}

class ProfessionalAssessment:
    def __init__(self):
        if 'professional_assessment' not in st.session_state:
            st.session_state.professional_assessment = {
                'step': 1,
                'industry': None,
                'company_size': None,
                'fortinet_products': {},
                'non_fortinet_categories': {},
                'assessment_complete': False
            }
    
    def calculate_enhanced_maturity(self) -> Dict:
        """Cálculo mejorado con selección múltiple"""
        nist_functions = {
            "Identify": {"total_impact": 0, "selected_impact": 0, "weight": 0.15},
            "Protect": {"total_impact": 0, "selected_impact": 0, "weight": 0.35},
            "Detect": {"total_impact": 0, "selected_impact": 0, "weight": 0.25},
            "Respond": {"total_impact": 0, "selected_impact": 0, "weight": 0.15},
            "Recover": {"total_impact": 0, "selected_impact": 0, "weight": 0.10}
        }
        
        for category_name, category_data in FORTINET_COMPLETE_PORTFOLIO.items():
            category_fortinet_count = 0
            
            for product_name, product_info in category_data["products"].items():
                nist_function = product_info["nist_function"]
                impact = product_info["impact"]
                maturity_factor = product_info["maturity_level"] / 5.0
                
                weighted_impact = impact * maturity_factor
                nist_functions[nist_function]["total_impact"] += weighted_impact
                
                product_key = f"{category_name}_{product_name}"
                if st.session_state.professional_assessment["fortinet_products"].get(product_key, False):
                    nist_functions[nist_function]["selected_impact"] += weighted_impact
                    category_fortinet_count += 1
            
            has_non_fortinet = st.session_state.professional_assessment["non_fortinet_categories"].get(category_name, False)
            
            if has_non_fortinet and category_fortinet_count == 0:
                for product_name, product_info in category_data["products"].items():
                    nist_function = product_info["nist_function"]
                    impact = product_info["impact"]
                    maturity_factor = product_info["maturity_level"] / 5.0
                    weighted_impact = impact * maturity_factor
                    nist_functions[nist_function]["selected_impact"] += weighted_impact * 0.6
        
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
        if score >= 90: return 5
        elif score >= 75: return 4
        elif score >= 60: return 3
        elif score >= 40: return 2
        else: return 1

def main():
    assessment = ProfessionalAssessment()
    
    # Header principal
    st.markdown("""
    <div class="main-header">
        <div class="fortinet-logo">🛡️ FORTINET SECURITY FABRIC</div>
        <h2>PROFESSIONAL ROADMAP DE MADUREZ</h2>
        <p>Plataforma profesional para evaluar y planificar la evolución de su estrategia de ciberseguridad<br>
        <strong>Incluye FortiCNAPP, Perception Point y tecnologías de vanguardia</strong></p>
    </div>
    """, unsafe_allow_html=True)
    
    current_step = st.session_state.professional_assessment['step']
    
    if current_step == 1:
        show_professional_industry_selection()
    elif current_step == 2:
        show_professional_company_size_selection()
    elif current_step == 3:
        show_professional_assessment()
    elif current_step == 4:
        show_professional_results(assessment)

def show_professional_industry_selection():
    st.markdown("""
    <div class="section-header">
        <h3>🏭 Selecciona tu Industria</h3>
        <p>Personalización del roadmap según mejores prácticas del sector</p>
    </div>
    """, unsafe_allow_html=True)
    
    cols = st.columns(4)
    
    for i, (industry_name, industry_data) in enumerate(INDUSTRIES.items()):
        with cols[i % 4]:
            if st.button(
                f"{industry_data['icon']}\n\n**{industry_name}**\n\nBenchmark: {industry_data['benchmark']}%",
                key=f"prof_industry_{industry_name}",
                use_container_width=True
            ):
                st.session_state.professional_assessment['industry'] = industry_name
                st.rerun()
    
    if st.session_state.professional_assessment['industry']:
        st.markdown("---")
        st.success(f"✅ Industria seleccionada: **{st.session_state.professional_assessment['industry']}**")
        if st.button("📍 Continuar →", type="primary", use_container_width=True):
            st.session_state.professional_assessment['step'] = 2
            st.rerun()

def show_professional_company_size_selection():
    st.markdown(f"""
    <div class="section-header">
        <h3>🏢 Tamaño de Organización</h3>
        <p>Industria: <strong>{st.session_state.professional_assessment['industry']}</strong></p>
    </div>
    """, unsafe_allow_html=True)
    
    for size_name, size_data in COMPANY_SIZES.items():
        if st.button(
            f"{size_data['icon']} **{size_name}**\n\nPrioridad: {size_data['priority']}\nTimeline: {size_data['timeline']}",
            key=f"prof_size_{size_name}",
            use_container_width=True
        ):
            st.session_state.professional_assessment['company_size'] = size_name
            st.rerun()
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Anterior", use_container_width=True):
            st.session_state.professional_assessment['step'] = 1
            st.rerun()
    
    with col2:
        if st.session_state.professional_assessment['company_size']:
            if st.button("🔧 Assessment →", type="primary", use_container_width=True):
                st.session_state.professional_assessment['step'] = 3
                st.rerun()

def show_professional_assessment():
    st.markdown("""
    <div class="section-header">
        <h3>🔧 Assessment Profesional de Tecnologías</h3>
        <p>Selecciona productos Fortinet implementados y marca categorías con soluciones de terceros</p>
    </div>
    """, unsafe_allow_html=True)
    
    show_professional_progress()
    
    for category_name, category_data in FORTINET_COMPLETE_PORTFOLIO.items():
        st.markdown(f"""
        <div class="category-header">
            {category_data['icon']} {category_name} - {category_data['description']}
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.markdown("""
            <div class="fortinet-section">
                <h4>🛡️ Productos Fortinet</h4>
            </div>
            """, unsafe_allow_html=True)
            
            # Grid de productos en 2 columnas
            product_cols = st.columns(2)
            products = list(category_data["products"].items())
            
            for i, (product_name, product_info) in enumerate(products):
                with product_cols[i % 2]:
                    product_key = f"{category_name}_{product_name}"
                    
                    selected = st.checkbox(
                        f"**{product_name}**",
                        value=st.session_state.professional_assessment["fortinet_products"].get(product_key, False),
                        key=f"prof_fortinet_{product_key}",
                        help=f"{product_info['description']}"
                    )
                    
                    st.session_state.professional_assessment["fortinet_products"][product_key] = selected
                    
                    if selected:
                        st.success(f"✅ Implementado", icon="✅")
                        st.caption(f"🎯 {product_info['nist_function']} | Nivel {product_info['maturity_level']} | Fase {product_info['implementation_phase']}")
                    else:
                        st.caption(f"📝 {product_info['description'][:50]}...")
        
        with col2:
            st.markdown("""
            <div class="non-fortinet-section">
                <h4>🔧 Otras Soluciones</h4>
            </div>
            """, unsafe_allow_html=True)
            
            non_fortinet_selected = st.checkbox(
                f"**Soluciones de Terceros**\n\nTenemos otras tecnologías en {category_name}",
                value=st.session_state.professional_assessment["non_fortinet_categories"].get(category_name, False),
                key=f"prof_non_fortinet_{category_name}",
                help=f"Incluye cualquier solución no-Fortinet en {category_name}"
            )
            st.session_state.professional_assessment["non_fortinet_categories"][category_name] = non_fortinet_selected
            
            # Status de la categoría
            has_fortinet = any(
                st.session_state.professional_assessment["fortinet_products"].get(f"{category_name}_{prod}", False)
                for prod in category_data["products"].keys()
            )
            
            if has_fortinet and non_fortinet_selected:
                st.success("🔄 Ambiente Híbrido")
            elif has_fortinet:
                st.success("🛡️ Solo Fortinet")
            elif non_fortinet_selected:
                st.info("🔧 Solo Terceros")
            else:
                st.error("⚠️ Sin Protección")
        
        st.markdown("---")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Anterior", use_container_width=True):
            st.session_state.professional_assessment['step'] = 2
            st.rerun()
    
    with col2:
        if get_total_selection_count() > 0:
            if st.button("📊 Generar Roadmap Profesional →", type="primary", use_container_width=True):
                st.session_state.professional_assessment['step'] = 4
                st.rerun()

def show_professional_progress():
    fortinet_count = sum(1 for v in st.session_state.professional_assessment["fortinet_products"].values() if v)
    non_fortinet_count = sum(1 for v in st.session_state.professional_assessment["non_fortinet_categories"].values() if v)
    categories_covered = sum(1 for cat in FORTINET_COMPLETE_PORTFOLIO.keys() if has_coverage_in_category(cat))
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h3 style="color: #dc2626; margin: 0;">{}</h3>
            <p style="margin: 0;">Productos Fortinet</p>
        </div>
        """.format(fortinet_count), unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h3 style="color: #2563eb; margin: 0;">{}</h3>
            <p style="margin: 0;">Categorías con Terceros</p>
        </div>
        """.format(non_fortinet_count), unsafe_allow_html=True)
    
    with col3:
        coverage_pct = (categories_covered / len(FORTINET_COMPLETE_PORTFOLIO)) * 100
        st.markdown("""
        <div class="metric-card">
            <h3 style="color: #16a34a; margin: 0;">{:.0f}%</h3>
            <p style="margin: 0;">Cobertura Total</p>
        </div>
        """.format(coverage_pct), unsafe_allow_html=True)
    
    with col4:
        temp_assessment = ProfessionalAssessment()
        temp_results = temp_assessment.calculate_enhanced_maturity()
        st.markdown("""
        <div class="metric-card">
            <h3 style="color: #7c3aed; margin: 0;">{:.1f}%</h3>
            <p style="margin: 0;">Madurez Estimada</p>
        </div>
        """.format(temp_results['overall_score']), unsafe_allow_html=True)

def has_coverage_in_category(category_name):
    has_fortinet = any(
        st.session_state.professional_assessment["fortinet_products"].get(f"{category_name}_{prod}", False)
        for prod in FORTINET_COMPLETE_PORTFOLIO[category_name]["products"].keys()
    )
    has_alternative = st.session_state.professional_assessment["non_fortinet_categories"].get(category_name, False)
    return has_fortinet or has_alternative

def get_total_selection_count():
    fortinet_count = sum(1 for v in st.session_state.professional_assessment["fortinet_products"].values() if v)
    non_fortinet_count = sum(1 for v in st.session_state.professional_assessment["non_fortinet_categories"].values() if v)
    return fortinet_count + non_fortinet_count

def show_professional_results(assessment):
    results = assessment.calculate_enhanced_maturity()
    
    st.markdown(f"""
    <div class="section-header">
        <h2>🎯 ROADMAP PROFESIONAL - FORTINET SECURITY FABRIC</h2>
        <h3>Nivel de Madurez: {results['maturity_level']}/5 ({results['overall_score']:.1f}%)</h3>
        <p><strong>Industria:</strong> {st.session_state.professional_assessment['industry']} | 
           <strong>Tamaño:</strong> {st.session_state.professional_assessment['company_size']}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Timeline corregido sin errores
    show_simplified_timeline(results)
    
    # AGREGAR ESTAS DOS LÍNEAS - Nuevas secciones de beneficios
    show_maturity_benefits(results)
    show_fortinet_value_proposition()
    
    tab1, tab2, tab3 = st.tabs(["📊 Análisis Actual", "🗺️ Roadmap por Fases", "📈 NIST Framework"])
    
    with tab1:
        show_current_analysis(results)
    
    with tab2:
        show_phase_roadmap(results)
    
    with tab3:
        show_nist_analysis(results)
    
    with st.expander("🎯 Próximos Pasos Recomendados", expanded=True):
        show_next_steps_recommendations(results)
    
    if st.button("🔄 Nuevo Assessment", use_container_width=True):
        for key in st.session_state.keys():
            del st.session_state[key]
        st.rerun()

def show_simplified_timeline(results):
    st.markdown("""
    <div class="timeline-container">
        <h3>🗺️ TIMELINE DE EVOLUCIÓN HACIA EXCELENCIA</h3>
        <p>Su posición actual y roadmap hacia una estrategia de seguridad madura</p>
    </div>
    """, unsafe_allow_html=True)
    
    current_level = results['maturity_level']
    cols = st.columns(5)
    
    for i, (phase_num, phase_data) in enumerate(IMPLEMENTATION_PHASES.items()):
        with cols[i]:
            is_current = phase_num == current_level
            is_completed = phase_num <= current_level
            
            if is_current:
                st.markdown(f"""
                <div style='text-align: center;'>
                    <div style='width: 70px; height: 70px; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto; font-weight: bold; background: {phase_data['color']}; color: white; border: 4px solid #dc2626; font-size: 1.2rem; box-shadow: 0 4px 12px rgba(220, 38, 38, 0.4);'>
                        {phase_num}
                    </div>
                    <div style='margin-top: 0.8rem; font-size: 0.9rem; font-weight: 600; line-height: 1.3;'>{phase_data['name']}</div>
                    <div style='margin-top: 0.3rem; font-size: 0.8rem; color: #6b7280;'>{phase_data['timeline']}</div>
                    <div style='margin-top: 0.8rem;'><strong style='color: #dc2626; font-size: 0.8rem;'>🎯 USTED ESTÁ AQUÍ</strong></div>
                </div>
                """, unsafe_allow_html=True)
            elif is_completed:
                st.markdown(f"""
                <div style='text-align: center;'>
                    <div style='width: 60px; height: 60px; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto; font-weight: bold; background: {phase_data['color']}; color: white; opacity: 0.8;'>
                        {phase_num}
                    </div>
                    <div style='margin-top: 0.5rem; font-size: 0.85rem; font-weight: 600; line-height: 1.3;'>{phase_data['name']}</div>
                    <div style='margin-top: 0.25rem; font-size: 0.75rem; color: #6b7280;'>{phase_data['timeline']}</div>
                    <div style='margin-top: 0.5rem;'><span style='color: #16a34a; font-size: 0.8rem;'>✅ Completado</span></div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style='text-align: center;'>
                    <div style='width: 60px; height: 60px; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto; font-weight: bold; background: #e5e7eb; color: #6b7280; border: 2px dashed #9ca3af;'>
                        {phase_num}
                    </div>
                    <div style='margin-top: 0.5rem; font-size: 0.85rem; font-weight: 600; line-height: 1.3; color: #6b7280;'>{phase_data['name']}</div>
                    <div style='margin-top: 0.25rem; font-size: 0.75rem; color: #9ca3af;'>{phase_data['timeline']}</div>
                    <div style='margin-top: 0.5rem;'><span style='color: #6b7280; font-size: 0.8rem;'>📅 Futuro</span></div>
                </div>
                """, unsafe_allow_html=True)
    
    # Línea de progreso
    st.markdown("""
    <div style='margin: 2rem auto; max-width: 80%;'>
        <div style='height: 4px; background: #e5e7eb; border-radius: 2px; position: relative;'>
            <div style='height: 100%; background: linear-gradient(90deg, #dc2626 0%, #ea580c 25%, #2563eb 50%, #16a34a 75%, #7c3aed 100%); border-radius: 2px; width: {}%;'></div>
        </div>
        <div style='text-align: center; margin-top: 0.5rem; font-size: 0.8rem; color: #6b7280;'>
            Progreso de Implementación: {}%
        </div>
    </div>
    """.format((current_level / 5) * 100, int((current_level / 5) * 100)), unsafe_allow_html=True)
    
    st.markdown("---")
    show_visual_roadmap_chart(results)

def show_maturity_benefits(results):
    """Muestra los beneficios específicos por nivel de madurez"""
    current_level = results['maturity_level']
    
    st.markdown("""
    <div style="background: linear-gradient(135deg, #fef7ff 0%, #fae8ff 100%); border: 3px solid #a855f7; border-radius: 20px; padding: 2rem; margin: 2rem 0;">
        <h3 style="color: #7c3aed; text-align: center; margin-bottom: 1.5rem;">💎 BENEFICIOS DE SU NIVEL DE MADUREZ ACTUAL</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Definir beneficios por nivel
    MATURITY_BENEFITS = {
        1: {
            "title": "🛡️ Nivel 1 - Protección Básica Establecida",
            "color": "#dc2626",
            "benefits": [
                "✅ Reducción del 60-70% en incidentes básicos de seguridad",
                "✅ Cumplimiento de requisitos regulatorios fundamentales",
                "✅ Visibilidad básica de amenazas en tiempo real",
                "✅ Protección perimetral sólida contra ataques comunes"
            ],
            "business_impact": "🎯 ROI: Reducción de costos operativos del 15-20%",
            "next_level_preview": "El siguiente nivel le dará gestión centralizada y mayor eficiencia"
        },
        2: {
            "title": "🏗️ Nivel 2 - Gestión Centralizada y Eficiencia",
            "color": "#ea580c", 
            "benefits": [
                "✅ Reducción del 40% en tiempo de gestión de seguridad",
                "✅ Visibilidad completa de toda la infraestructura",
                "✅ Respuesta automática a incidentes básicos",
                "✅ Consolidación de herramientas y reducción de complejidad"
            ],
            "business_impact": "🎯 ROI: Ahorro del 25-30% en costos operativos",
            "next_level_preview": "El siguiente nivel implementará detección avanzada con IA"
        },
        3: {
            "title": "🔍 Nivel 3 - Detección Avanzada con Inteligencia",
            "color": "#2563eb",
            "benefits": [
                "✅ Detección del 95% de amenazas avanzadas en tiempo real",
                "✅ Reducción del 80% en tiempo de investigación de incidentes", 
                "✅ Prevención proactiva de ataques zero-day",
                "✅ Correlación inteligente de eventos de seguridad"
            ],
            "business_impact": "🎯 ROI: Prevención de pérdidas por $500K-2M anuales",
            "next_level_preview": "El siguiente nivel automatizará completamente la respuesta"
        },
        4: {
            "title": "🤖 Nivel 4 - Automatización y Orquestación Completa",
            "color": "#16a34a",
            "benefits": [
                "✅ Respuesta automática al 90% de incidentes en < 5 minutos",
                "✅ Reducción del 70% en personal dedicado a operaciones de seguridad",
                "✅ Protección adaptativa basada en comportamiento",
                "✅ Integración completa con procesos de negocio"
            ],
            "business_impact": "🎯 ROI: Optimización de recursos del 40-50%",
            "next_level_preview": "El siguiente nivel implementará Zero Trust completo"
        },
        5: {
            "title": "🏆 Nivel 5 - Excelencia en Zero Trust",
            "color": "#7c3aed",
            "benefits": [
                "✅ Arquitectura Zero Trust completa y adaptativa",
                "✅ Prevención del 99.9% de brechas de seguridad",
                "✅ Optimización continua con machine learning",
                "✅ Liderazgo en innovación de ciberseguridad"
            ],
            "business_impact": "🎯 ROI: Ventaja competitiva y reducción de riesgos del 60%",
            "next_level_preview": "¡Ha alcanzado la excelencia en ciberseguridad!"
        }
    }
    
    current_benefits = MATURITY_BENEFITS[current_level]
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%); border: 3px solid {current_benefits['color']}; border-radius: 16px; padding: 2rem; margin: 1rem 0;">
            <h4 style="color: {current_benefits['color']}; margin-bottom: 1.5rem;">{current_benefits['title']}</h4>
        """, unsafe_allow_html=True)
        
        st.markdown("**🎁 Sus Beneficios Actuales:**")
        for benefit in current_benefits['benefits']:
            st.markdown(f"&nbsp;&nbsp;&nbsp;&nbsp;{benefit}")
        
        st.markdown(f"<br><strong style='color: {current_benefits['color']};'>{current_benefits['business_impact']}</strong>", unsafe_allow_html=True)
        
        if current_level < 5:
            st.info(f"💡 **Vista Previa del Siguiente Nivel:** {current_benefits['next_level_preview']}")
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        # Gráfico de beneficios acumulativos
        levels = list(range(1, 6))
        roi_values = [20, 30, 45, 50, 60]
        
        fig_benefits = go.Figure()
        colors = ['#dc2626', '#ea580c', '#2563eb', '#16a34a', '#7c3aed']
        
        for i, (level, roi, color) in enumerate(zip(levels, roi_values, colors)):
            opacity = 1.0 if level <= current_level else 0.3
            fig_benefits.add_trace(go.Bar(
                x=[level],
                y=[roi],
                marker_color=color,
                opacity=opacity,
                showlegend=False
            ))
        
        fig_benefits.add_trace(go.Scatter(
            x=[current_level],
            y=[roi_values[current_level-1]],
            mode='markers+text',
            marker=dict(size=20, color='#dc2626', symbol='star'),
            text=['USTED'],
            textposition='top center',
            showlegend=False
        ))
        
        fig_benefits.update_layout(
            title="📈 ROI Acumulativo por Nivel",
            xaxis_title="Nivel de Madurez",
            yaxis_title="ROI (%)",
            height=300,
            margin=dict(t=50, b=30, l=30, r=30)
        )
        
        st.plotly_chart(fig_benefits, use_container_width=True)

def show_fortinet_value_proposition():
    """Muestra por qué Fortinet vs otras soluciones"""
    st.markdown("""
    <div style="background: linear-gradient(135deg, #ecfdf5 0%, #d1fae5 100%); border: 3px solid #10b981; border-radius: 20px; padding: 2rem; margin: 2rem 0;">
        <h3 style="color: #047857; text-align: center; margin-bottom: 1.5rem;">⚡ ¿POR QUÉ FORTINET SECURITY FABRIC?</h3>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style="background: white; border-radius: 12px; padding: 1.5rem; box-shadow: 0 4px 12px rgba(0,0,0,0.1); height: 280px;">
            <h4 style="color: #dc2626; text-align: center;">🏆 VS. SOLUCIONES PUNTUALES</h4>
            <ul style="font-size: 0.9rem; line-height: 1.6;">
                <li><strong>85% menos</strong> de complejidad operativa</li>
                <li><strong>60% reducción</strong> en costos totales</li>
                <li><strong>Una sola plataforma</strong> vs. 10-15 herramientas</li>
                <li><strong>Integración nativa</strong> sin APIs complejas</li>
                <li><strong>Visibilidad unificada</strong> en una sola consola</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: white; border-radius: 12px; padding: 1.5rem; box-shadow: 0 4px 12px rgba(0,0,0,0.1); height: 280px;">
            <h4 style="color: #2563eb; text-align: center;">🚀 BENEFICIOS ÚNICOS</h4>
            <ul style="font-size: 0.9rem; line-height: 1.6;">
                <li><strong>Security Fabric:</strong> Inteligencia compartida</li>
                <li><strong>FortiGuard Labs:</strong> Threat Intelligence líder</li>
                <li><strong>ASIC Propietarios:</strong> Performance superior</li>
                <li><strong>Automatización:</strong> Respuesta en segundos</li>
                <li><strong>Escalabilidad:</strong> De SMB a Enterprise</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="background: white; border-radius: 12px; padding: 1.5rem; box-shadow: 0 4px 12px rgba(0,0,0,0.1); height: 280px;">
            <h4 style="color: #16a34a; text-align: center;">💰 IMPACTO ECONÓMICO</h4>
            <ul style="font-size: 0.9rem; line-height: 1.6;">
                <li><strong>ROI del 300%</strong> en primer año</li>
                <li><strong>Payback:</strong> 6-8 meses típico</li>
                <li><strong>OPEX:</strong> 40-50% menos vs. competencia</li>
                <li><strong>Productividad:</strong> +60% del equipo IT</li>
                <li><strong>Compliance:</strong> Auditorías automáticas</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

def show_current_analysis(results):
    st.subheader("📊 Análisis del Estado Actual")
    
    col1, col2, col3, col4 = st.columns(4)
    
    fortinet_count = sum(1 for v in st.session_state.professional_assessment["fortinet_products"].values() if v)
    total_fortinet = sum(len(cat["products"]) for cat in FORTINET_COMPLETE_PORTFOLIO.values())
    non_fortinet_count = sum(1 for v in st.session_state.professional_assessment["non_fortinet_categories"].values() if v)
    
    with col1:
        st.metric("Madurez General", f"Nivel {results['maturity_level']}", f"{results['overall_score']:.1f}%")
    
    with col2:
        st.metric("Productos Fortinet", f"{fortinet_count}/{total_fortinet}")
    
    with col3:
        st.metric("Categorías con Terceros", f"{non_fortinet_count}/{len(FORTINET_COMPLETE_PORTFOLIO)}")
    
    with col4:
        industry = st.session_state.professional_assessment['industry']
        if industry in INDUSTRIES:
            benchmark = INDUSTRIES[industry]["benchmark"]
            delta = results['overall_score'] - benchmark
            st.metric("vs. Industria", f"{delta:+.1f}%")

    # Tabla de cobertura
    st.subheader("🏗️ Cobertura por Categoría")
    
    coverage_data = []
    for category_name, category_data in FORTINET_COMPLETE_PORTFOLIO.items():
        fortinet_products = [
            product for product in category_data["products"].keys()
            if st.session_state.professional_assessment["fortinet_products"].get(f"{category_name}_{product}", False)
        ]
        
        has_alternative = st.session_state.professional_assessment["non_fortinet_categories"].get(category_name, False)
        total_products = len(category_data["products"])
        fortinet_count = len(fortinet_products)
        
        if fortinet_count > 0 and has_alternative:
            status = f"🔄 Híbrido ({fortinet_count}/{total_products} Fortinet + Terceros)"
        elif fortinet_count > 0:
            status = f"🛡️ Fortinet ({fortinet_count}/{total_products})"
        elif has_alternative:
            status = "🔧 Solo Terceros"
        else:
            status = "❌ Sin Cobertura"
        
        coverage_data.append({
            "Categoría": category_name,
            "Estado": status,
            "Productos Implementados": ", ".join(fortinet_products) if fortinet_products else "Ninguno"
        })
    
    df = pd.DataFrame(coverage_data)
    st.dataframe(df, use_container_width=True, hide_index=True)

def show_phase_roadmap(results):
    st.subheader("🗺️ Roadmap por Fases de Implementación")
    
    current_level = results['maturity_level']
    
    for phase_num, phase_data in IMPLEMENTATION_PHASES.items():
        if phase_num <= current_level:
            status = "✅ COMPLETADO"
            expanded = False
        elif phase_num == current_level + 1:
            status = "🎯 SIGUIENTE FASE"
            expanded = True
        else:
            status = "📅 FUTURO"
            expanded = False
        
        with st.expander(f"Fase {phase_num}: {phase_data['name']} - {status}", expanded=expanded):
            st.markdown(f"""
            <div class="phase-card">
                <h4 style="color: {phase_data['color']};">🎯 {phase_data['name']}</h4>
                <p><strong>Descripción:</strong> {phase_data['description']}</p>
                <p><strong>Enfoque NIST:</strong> {phase_data['focus']}</p>
                <p><strong>Timeline:</strong> {phase_data['timeline']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Productos de esta fase
            phase_products = []
            for category_name, category_data in FORTINET_COMPLETE_PORTFOLIO.items():
                for product_name, product_info in category_data["products"].items():
                    if product_info['implementation_phase'] == phase_num:
                        product_key = f"{category_name}_{product_name}"
                        is_implemented = st.session_state.professional_assessment["fortinet_products"].get(product_key, False)
                        
                        phase_products.append({
                            "product": product_name,
                            "category": category_name,
                            "implemented": is_implemented,
                            "impact": product_info['impact']
                        })
            
            if phase_products:
                st.markdown("**🛡️ Productos Fortinet recomendados:**")
                phase_products.sort(key=lambda x: x['impact'], reverse=True)
                
                for product in phase_products:
                    status_icon = "✅" if product['implemented'] else "⭕"
                    priority = "🔴 Alta" if product['impact'] >= 4 else "🟡 Media"
                    st.markdown(f"{status_icon} **{product['product']}** ({product['category']}) - {priority}")

def show_nist_analysis(results):
    st.subheader("📈 Análisis del Framework NIST")
    
    col1, col2 = st.columns(2)
    
    with col1:
        for function, score in results['function_scores'].items():
            if score >= 70:
                color = "#16a34a"
                status = "Fuerte"
            elif score >= 40:
                color = "#ea580c"
                status = "Moderado"
            else:
                color = "#dc2626"
                status = "Débil"
            
            st.markdown(f"""
            <div style="margin: 1rem 0;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <strong>{function}</strong>
                    <span style="color: {color};">{score:.1f}% - {status}</span>
                </div>
                <div style="background: #e5e7eb; height: 8px; border-radius: 4px; margin-top: 0.5rem;">
                    <div style="background: {color}; height: 100%; width: {score}%; border-radius: 4px;"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("**📊 Recomendaciones por Función NIST:**")
        
        weakest_function = min(results['function_scores'].items(), key=lambda x: x[1])
        strongest_function = max(results['function_scores'].items(), key=lambda x: x[1])
        
        st.info(f"🎯 **Prioridad Alta**: Fortalecer {weakest_function[0]} ({weakest_function[1]:.1f}%)")
        st.success(f"✅ **Fortaleza**: {strongest_function[0]} ({strongest_function[1]:.1f}%)")
        
        avg_score = sum(results['function_scores'].values()) / len(results['function_scores'])
        st.metric("Puntaje Promedio NIST", f"{avg_score:.1f}%")

def show_next_steps_recommendations(results):
    """Próximos pasos recomendados basados en industria y tamaño"""
    st.markdown("""
    <div style="background: linear-gradient(135deg, #fef2f2 0%, #fee2e2 100%); border: 3px solid #dc2626; border-radius: 20px; padding: 2rem; margin: 1rem 0;">
        <h3 style="color: #dc2626; text-align: center; margin-bottom: 1.5rem;">🎯 Próximos Pasos Recomendados</h3>
    </div>
    """, unsafe_allow_html=True)
    
    industry = st.session_state.professional_assessment['industry']
    company_size = st.session_state.professional_assessment['company_size']
    current_level = results['maturity_level']
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%); border: 2px solid #3b82f6; border-radius: 16px; padding: 1.5rem; margin: 0.5rem 0;">
            <h4 style="color: #1d4ed8; margin-bottom: 1rem;">📊 Análisis de Madurez Contextual</h4>
        </div>
        """, unsafe_allow_html=True)
        
        if industry in INDUSTRIES:
            industry_data = INDUSTRIES[industry]
            benchmark = industry_data["benchmark"]
            
            col_metric1, col_metric2 = st.columns(2)
            with col_metric1:
                st.metric("Nivel Actual", current_level, f"{results['overall_score']:.1f}%")
            with col_metric2:
                expected_level = 4.2 if company_size == "Empresa (5000+ empleados)" else 3.5
                st.metric("Nivel Esperado", f"{expected_level}", "Por debajo del promedio" if current_level < expected_level else "")
        
        st.markdown("**🔍 Análisis para {} / {}**".format(company_size, industry))
        
        if company_size in COMPANY_SIZES:
            size_data = COMPANY_SIZES[company_size]
            st.info(f"Existe una brecha significativa entre su nivel actual y lo esperado para {company_size}.")
            
            st.markdown("**🎯 Prioridades de {} / {}:**".format(company_size.split()[0], industry))
            if industry in INDUSTRIES:
                priorities = INDUSTRIES[industry]["priorities"]
                for i, priority in enumerate(priorities, 1):
                    st.write(f"{i}. {priority}")
            
            st.markdown("**⚠️ Desafíos Típicos:**")
            challenges = ["Amenazas sofisticadas", "Regulatory compliance", "Digital transformation"]
            for challenge in challenges:
                st.write(f"• {challenge}")
    
    with col2:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%); border: 2px solid #22c55e; border-radius: 16px; padding: 1.5rem; margin: 0.5rem 0;">
            <h4 style="color: #15803d; margin-bottom: 1rem;">🚀 Próximos Pasos Estratégicos</h4>
        </div>
        """, unsafe_allow_html=True)
        
        if company_size in COMPANY_SIZES and industry in INDUSTRIES:
            size_data = COMPANY_SIZES[company_size]
            industry_data = INDUSTRIES[industry]
            
            st.markdown("**📋 Acciones Inmediatas (Próximos 3 meses):**")
            
            critical_products = industry_data["critical_products"]
            implemented_critical = []
            missing_critical = []
            
            for product in critical_products:
                found = False
                for category_name, category_data in FORTINET_COMPLETE_PORTFOLIO.items():
                    if product in category_data["products"]:
                        product_key = f"{category_name}_{product}"
                        if st.session_state.professional_assessment["fortinet_products"].get(product_key, False):
                            implemented_critical.append(product)
                            found = True
                            break
                if not found or product not in [p for p in implemented_critical]:
                    missing_critical.append(product)
            
            st.markdown(f"1. **{industry_data['next_steps']}**")
            st.markdown(f"2. **{size_data['next_steps']}**")
            
            if missing_critical:
                st.markdown("3. **Implementar productos críticos faltantes:**")
                for product in missing_critical[:3]:
                    st.write(f"   • {product}")
            
            st.markdown("4. **Mejorar visibilidad y monitoreo continuo**")
            st.markdown("5. **Establecer métricas de seguridad**")
            
            if "regulations" in industry_data:
                st.markdown("**📜 Cumplimiento Regulatorio:**")
                for reg in industry_data["regulations"]:
                    st.write(f"• {reg}")
    
    st.markdown("""
    <div style="background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%); border: 2px solid #0ea5e9; border-radius: 16px; padding: 1.5rem; margin: 1rem 0;">
        <h4 style="color: #0369a1; margin-bottom: 1rem;">🗺️ Roadmap Personalizado para {} / {}</h4>
    </div>
    """.format(company_size.split()[0], industry), unsafe_allow_html=True)
    
    phases_data = []
    for phase_num, phase_data in IMPLEMENTATION_PHASES.items():
        if phase_num <= current_level + 2:
            status = "✅ Completado" if phase_num <= current_level else "🎯 Siguiente" if phase_num == current_level + 1 else "📅 Futuro"
            phases_data.append({
                "Fase": f"Nivel {phase_num}",
                "Nombre": phase_data['name'],
                "Estado": status,
                "Timeline": phase_data['timeline'],
                "Enfoque": phase_data['focus']
            })
    
    df_roadmap = pd.DataFrame(phases_data)
    st.dataframe(df_roadmap, use_container_width=True, hide_index=True)

def show_visual_roadmap_chart(results):
    """Crea el gráfico visual mejorado con diseño más profesional y natural"""
    st.markdown("""
    <div style="background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%); border: 2px solid #64748b; border-radius: 15px; padding: 1rem; margin: 1rem 0;">
        <h3 style="color: #1e293b; text-align: center; margin-bottom: 0.5rem; font-size: 1.1rem;">🗺️ FORTINET SECURITY FABRIC</h3>
        <p style="text-align: center; color: #64748b; margin-bottom: 0.5rem; font-size: 0.85rem;">ROADMAP PROFESIONAL - EVOLUCIÓN DE MADUREZ</p>
    </div>
    """, unsafe_allow_html=True)
    
    current_level = results['maturity_level']
    fig = go.Figure()
    
    level_colors = ['#fef2f2', '#fef3e2', '#eff6ff', '#ecfdf5', '#faf5ff']
    level_borders = ['#fecaca', '#fed7aa', '#bfdbfe', '#bbf7d0', '#e9d5ff']
    level_names = ['Nivel 1\nInicial', 'Nivel 2\nBásico', 'Nivel 3\nIntermedio', 'Nivel 4\nAvanzado', 'Nivel 5\nExcelencia']
    level_descriptions = ['Fundamentos\n(0-3 meses)', 'Consolidación\n(3-6 meses)', 'Detección Avanzada\n(6-12 meses)', 'Optimización\n(12-18 meses)', 'Zero Trust & AI\n(18-24 meses)']
    
    # FONDO NATURAL
    for i in range(5):
        fig.add_shape(
            type="rect",
            x0=i+0.6, y0=0, x1=i+1.4, y1=6,
            fillcolor=level_colors[i],
            opacity=0.3,
            layer="below",
            line=dict(color=level_borders[i], width=1, dash='dot')
        )
        
        if i < 4:
            fig.add_shape(
                type="line",
                x0=i+1.4, y0=0, x1=i+1.4, y1=6,
                line=dict(color='#cbd5e1', width=1.5, dash='solid'),
                layer="below"
            )
        
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
        
        fig.add_annotation(
            x=i+1, y=0.4,
            text=level_descriptions[i],
            showarrow=False,
            font=dict(size=8, color='#64748b', family="Inter"),
            align="center"
        )
    
    # CURVA DE MADUREZ
    x_curve = np.linspace(0.6, 5.4, 20)
    y_curve = 0.8 + 4.2 * (1 - np.exp(-0.8 * (x_curve - 0.6))) + 0.1 * np.sin(2 * np.pi * (x_curve - 0.6) / 5)
    
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
    
    fig.add_trace(go.Scatter(
        x=x_curve,
        y=y_curve - 0.1,
        mode='lines',
        line=dict(color='rgba(67, 56, 202, 0.2)', width=8),
        showlegend=False,
        fill=None
    ))
    
    # Hitos en la curva
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
    
    # DISTRIBUCIÓN DE PRODUCTOS
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
    
    phase_product_counts = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
    
    for category_name, category_data in FORTINET_COMPLETE_PORTFOLIO.items():
        y_min, y_max = category_y_ranges.get(category_name, (2.0, 3.0))
        
        for product_name, product_info in category_data["products"].items():
            phase = product_info['implementation_phase']
            
            product_key = f"{category_name}_{product_name}"
            is_implemented = st.session_state.professional_assessment["fortinet_products"].get(product_key, False)
            
            count = phase_product_counts[phase]
            x_offset = (count % 5 - 2) * 0.05
            y_pos = y_min + (y_max - y_min) * (count / 10.0) + np.random.uniform(-0.05, 0.05)
            
            x_pos = phase + x_offset
            phase_product_counts[phase] += 1
            
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
    
    # Indicador en la curva
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
        
        fig.add_shape(
            type="line",
            x0=pin_x, y0=pin_y-0.1,
            x1=current_level, y1=curve_y+0.1,
            line=dict(color='#dc2626', width=2, dash='dot'),
            layer="above"
        )
    
    # LEYENDA
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
    
    # CONFIGURACIÓN
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
    
    st.plotly_chart(fig, use_container_width=True)
    
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
    
    show_roadmap_statistics(results)

def show_roadmap_statistics(results):
    """Muestra estadísticas del roadmap"""
    total_products = sum(len(cat["products"]) for cat in FORTINET_COMPLETE_PORTFOLIO.values())
    implemented_products = sum(1 for v in st.session_state.professional_assessment["fortinet_products"].values() if v)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Productos Totales",
            total_products,
            "En el roadmap"
        )
    
    with col2:
        st.metric(
            "Productos Implementados",
            implemented_products,
            f"{(implemented_products/total_products)*100:.1f}% completado"
        )
    
    with col3:
        products_next_phase = sum(
            1 for cat in FORTINET_COMPLETE_PORTFOLIO.values()
            for product_info in cat["products"].values()
            if product_info["implementation_phase"] == results['maturity_level'] + 1
        )
        st.metric(
            "Próxima Fase",
            products_next_phase,
            "productos recomendados"
        )
    
    with col4:
        coverage = sum(1 for cat in FORTINET_COMPLETE_PORTFOLIO.keys() if has_coverage_in_category(cat))
        st.metric(
            "Cobertura de Categorías",
            f"{coverage}/{len(FORTINET_COMPLETE_PORTFOLIO)}",
            f"{(coverage/len(FORTINET_COMPLETE_PORTFOLIO))*100:.0f}%"
        )

if __name__ == "__main__":
    main()
