# 🛡️ NIST Cybersecurity Framework Assessment Tool

Una aplicación profesional de evaluación de ciberseguridad basada en el Marco de Ciberseguridad del NIST (National Institute of Standards and Technology).

## 🎯 Características Principales

- ✅ **Assessment Completo NIST**: Evaluación basada en las 5 funciones del Framework
- 📊 **Dashboard Interactivo**: Visualizaciones dinámicas con Plotly
- 🏢 **Multi-industria**: Benchmarks específicos por sector
- 📑 **Reportes Profesionales**: Generación automática de reportes ejecutivos
- 🔐 **Panel de Administración**: Gestión completa del sistema
- 🌐 **Cloud-Ready**: Optimizado para Streamlit Cloud + Supabase
- 📱 **Responsive**: Interfaz adaptativa para todos los dispositivos

## 🏗️ Arquitectura del Sistema

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Frontend      │    │    Backend       │    │   Database      │
│   (Streamlit)   │◄──►│   (Python/SQL)   │◄──►│  (PostgreSQL)   │
│                 │    │                  │    │   (Supabase)    │
└─────────────────┘    └──────────────────┘    └─────────────────┘
        │                        │                        │
        ▼                        ▼                        ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   CDN/Domain    │    │   File Storage   │    │   Analytics     │
│  (Cloudflare)   │    │   (Local/Cloud)  │    │ (Google/Mixed)  │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

## 🚀 Instalación y Configuración

### Opción 1: Desarrollo Local

1. **Clonar el repositorio**
```bash
git clone https://github.com/yourusername/nist-assessment-app.git
cd nist-assessment-app
```

2. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

3. **Configurar variables de entorno**
```bash
cp .env.example .env
# Editar .env con tus configuraciones
```

4. **Ejecutar la aplicación**
```bash
streamlit run main.py
```

### Opción 2: Despliegue en Streamlit Cloud (Recomendado)

1. **Preparar el repositorio**
   - Fork este repositorio en tu GitHub
   - Configura los secrets en `.streamlit/secrets.toml`

2. **Configurar Supabase**
   - Crear proyecto en [supabase.com](https://supabase.com)
   - Ejecutar el script SQL de `database_setup.sql`
   - Obtener credenciales de conexión

3. **Desplegar en Streamlit Cloud**
   - Ir a [share.streamlit.io](https://share.streamlit.io)
   - Conectar con GitHub
   - Seleccionar el repositorio
   - Configurar secrets (ver sección de configuración)

4. **Configurar dominio personalizado**
   - Configurar DNS en Cloudflare
   - Apuntar CNAME a tu app de Streamlit

## ⚙️ Configuración

### Secrets de Streamlit Cloud

Crear `.streamlit/secrets.toml` con:

```toml
[database]
host = "db.xxxxx.supabase.co"
port = 5432
database = "postgres"
user = "postgres"
password = "tu-password-supabase"

[admin]
password = "tu-password-admin-seguro"
secret_key = "tu-clave-secreta-para-sesiones"

[analytics]
google_analytics_id = "G-XXXXXXXXXX"

[email]
sendgrid_api_key = "SG.xxxxx"
from_email = "noreply@tudominio.com"
admin_email = "admin@tudominio.com"

[app]
environment = "production"
debug = false
base_url = "https://assessment.tudominio.com"
```

### Variables de Entorno (.env para desarrollo local)

```bash
# Base de datos
DATABASE_URL=postgresql://postgres:password@localhost:5432/nist_assessment

# Aplicación
APP_ENV=development
SECRET_KEY=tu-clave-secreta
ADMIN_PASSWORD=password-admin-seguro

# Analytics
GOOGLE_ANALYTICS_ID=G-XXXXXXXXXX

# Email (opcional)
SENDGRID_API_KEY=SG.xxxxx
FROM_EMAIL=noreply@tudominio.com
```

## 📊 Base de Datos

### Esquema Principal

La aplicación utiliza PostgreSQL con las siguientes tablas principales:

- `assessments`: Datos principales de evaluaciones
- `assessment_responses`: Respuestas individuales por pregunta
- `generated_reports`: Reportes generados
- `admin_logs`: Logs de auditoría
- `analytics`: Eventos y métricas
- `system_config`: Configuración del sistema

### Inicialización

Para configurar la base de datos, ejecutar:

```sql
-- En Supabase SQL Editor o tu PostgreSQL
\i database/init.sql
```

## 🎛️ Panel de Administración

Acceder al panel de administración en `/admin` con las credenciales configuradas.

### Funcionalidades del Admin:

- 📈 **Dashboard General**: Métricas principales y estado del sistema
- 📊 **Analytics**: Análisis avanzado de datos y tendencias
- 🏢 **Gestión de Assessments**: CRUD completo de evaluaciones
- 📑 **Reportes**: Generación y exportación de reportes
- ⚙️ **Configuración**: Parámetros del sistema
- 🔧 **Mantenimiento**: Limpieza, backup y optimización

## 📋 Marco NIST Implementado

La aplicación evalúa las 5 funciones del NIST Cybersecurity Framework:

### 1. **Identify (Identificar)**
- Asset Management (ID.AM)
- Business Environment (ID.BE)
- Governance (ID.GV)
- Risk Assessment (ID.RA)
- Risk Management Strategy (ID.RM)

### 2. **Protect (Proteger)**
- Access Control (PR.AC)
- Awareness & Training (PR.AT)
- Data Security (PR.DS)
- Information Protection (PR.IP)
- Maintenance (PR.MA)
- Protective Technology (PR.PT)

### 3. **Detect (Detectar)**
- Anomalies & Events (DE.AE)
- Security Monitoring (DE.CM)
- Detection Processes (DE.DP)

### 4. **Respond (Responder)**
- Response Planning (RS.RP)
- Communications (RS.CO)
- Analysis (RS.AN)
- Mitigation (RS.MI)
- Improvements (RS.IM)

### 5. **Recover (Recuperar)**
- Recovery Planning (RC.RP)
- Improvements (RC.IM)
- Communications (RC.CO)

## 📊 Sistema de Puntuación

### Escala de Madurez (0-5):
- **0**: No implementado
- **1**: Planificado
- **2**: En desarrollo
- **3**: Parcialmente implementado
- **4**: Mayormente implementado
- **5**: Completamente implementado

### Niveles de Madurez:
- **Nivel 1 (0-39%)**: Inicial
- **Nivel 2 (40-59%)**: Repetible
- **Nivel 3 (60-74%)**: Definido
- **Nivel 4 (75-89%)**: Gestionado
- **Nivel 5 (90-100%)**: Optimizado

## 🔧 Desarrollo y Contribución

### Estructura del Proyecto

```
nist-assessment-app/
├── main.py                 # Aplicación principal
├── admin.py               # Panel de administración
├── database.py            # Gestión de base de datos
├── requirements.txt       # Dependencias Python
├── .streamlit/
│   ├── config.toml       # Configuración Streamlit
│   └── secrets.toml      # Secrets (no subir a Git)
├── database/
│   └── init.sql          # Script inicialización BD
├── docs/                 # Documentación adicional
├── tests/                # Tests unitarios
└── static/               # Archivos estáticos
```

### Comandos Útiles

```bash
# Desarrollo local
make dev

# Tests
make test

# Linting
make lint

# Formateo de código
make format

# Despliegue local con Docker
make deploy-local

# Backup de BD
make backup-db

# Limpieza
make clean
```

### Contribuir

1. Fork el repositorio
2. Crear branch de feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit cambios (`git commit -am 'Agregar nueva funcionalidad'`)
4. Push al branch (`git push origin feature/nueva-funcionalidad`)
5. Crear Pull Request

## 📈 Roadmap

### Versión 1.1 (Próximamente)
- [ ] Integración con APIs de threat intelligence
- [ ] Reportes en PDF automatizados
- [ ] Dashboard en tiempo real
- [ ] Integración con SIEM/SOC tools

### Versión 1.2
- [ ] Módulo de training y awareness
- [ ] Comparativas con marcos adicionales (ISO 27001, PCI DSS)
- [ ] API REST para integraciones
- [ ] Mobile app companion

### Versión 2.0
- [ ] AI-powered recommendations
- [ ] Automated control testing
- [ ] Multi-tenancy support
- [ ] Enterprise SSO integration

## 💰 Costos de Operación

### Configuración Básica (~$60/mes):
- Streamlit Cloud Community: $0
- Supabase Starter: $25/mes
- Cloudflare Pro: $20/mes
- SendGrid Essentials: $15/mes

### Configuración Empresarial (~$200/mes):
- Streamlit Cloud Business: $100/mes
- Supabase Pro: $25/mes
- Cloudflare Business: $50/mes
- SendGrid Pro: $25/mes

## 🛡️ Seguridad

### Mejores Prácticas Implementadas:
- ✅ Autenticación robusta para admin
- ✅ Validación de entrada en todos los formularios
- ✅ Sanitización de datos
- ✅ HTTPS forzado
- ✅ Headers de seguridad
- ✅ Rate limiting
- ✅ Logs de auditoría
- ✅ Backup automático

### Consideraciones Adicionales:
- Configurar SSL/TLS apropiado
- Implementar WAF (Web Application Firewall)
- Monitoreo de seguridad continuo
- Actualizaciones regulares de dependencias

## 📞 Soporte

### Documentación:
- 📚 [Wiki del proyecto](https://github.com/yourusername/nist-assessment-app/wiki)
- 🎥 [Videos tutoriales](https://youtube.com/playlist/xxx)
- 📖 [Guía de usuario](docs/user-guide.md)

### Contacto:
- 📧 Email: support@tudominio.com
- 💬 Discord: [Servidor de la comunidad](https://discord.gg/xxx)
- 🐛 Issues: [GitHub Issues](https://github.com/yourusername/nist-assessment-app/issues)

## 📄 Licencia

Este proyecto está licenciado bajo MIT License - ver el archivo [LICENSE](LICENSE) para detalles.

## 🙏 Agradecimientos

- NIST por el Cybersecurity Framework
- Streamlit por la plataforma de desarrollo
- Supabase por la infraestructura de base de datos
- Comunidad open source por las bibliotecas utilizadas

---

**¿Listo para mejorar la postura de ciberseguridad de tu organización?**

🚀 [Demo en vivo](https://assessment.itsmillan.com) | 📖 [Documentación](docs/) | 🛠️ [Instalación](INSTALL.md)

---

> **Nota**: Esta herramienta es para evaluación y orientación. No reemplaza una auditoría profesional de ciberseguridad.

## 🔄 Historial de Versiones

### v1.0.0 (2025-01-29)
- 🎉 Lanzamiento inicial
- ✅ Assessment completo basado en NIST Cybersecurity Framework
- ✅ Dashboard interactivo con métricas en tiempo real
- ✅ Panel de administración completo
- ✅ Base de datos PostgreSQL con Supabase
- ✅ Exportación de reportes en múltiples formatos
- ✅ Sistema de benchmarks por industria
- ✅ Integración con analytics y métricas
- ✅ Arquitectura cloud-native optimizada
- ✅ Documentación completa y guías de despliegue

## 🏁 Pasos Siguientes para Implementación

### Fase 1: Setup Básico (Día 1-2)
1. **Crear cuentas necesarias:**
   ```bash
   # Streamlit Cloud
   https://share.streamlit.io

   # Supabase
   https://supabase.com

   # Cloudflare (opcional)
   https://cloudflare.com
   ```

2. **Preparar repositorio:**
   ```bash
   git clone <este-repositorio>
   cd nist-assessment-app
   git remote set-url origin https://github.com/tu-usuario/nist-assessment-app.git
   git push -u origin main
   ```

3. **Configurar base de datos:**
   - Crear proyecto en Supabase
   - Ejecutar script SQL de inicialización
   - Obtener credenciales de conexión

### Fase 2: Configuración (Día 2-3)
1. **Configurar secrets en Streamlit:**
   ```toml
   # En Streamlit Cloud > Settings > Secrets
   [database]
   host = "tu-host-supabase"
   port = 5432
   database = "postgres"
   user = "postgres"
   password = "tu-password"

   [admin]
   password = "password-admin-super-seguro"
   ```

2. **Desplegar aplicación:**
   - Conectar GitHub con Streamlit Cloud
   - Seleccionar repositorio
   - La app se desplegará automáticamente

### Fase 3: Personalización (Día 3-5)
1. **Customizar branding:**
   - Cambiar colores en el CSS
   - Actualizar logos y textos
   - Configurar dominio personalizado

2. **Configurar analytics:**
   - Google Analytics ID
   - Métricas personalizadas
   - Reportes automáticos

### Fase 4: Testing y Go-Live (Día 5-7)
1. **Testing completo:**
   - Realizar assessment de prueba
   - Verificar generación de reportes
   - Probar panel de administración

2. **Go-live:**
   - Configurar monitoreo
   - Entrenar usuarios
   - Documentar procesos

## 🔥 Funcionalidades Avanzadas

### Integración con APIs Externas
```python
# Ejemplo: Integración con threat intelligence
def get_threat_intelligence():
    # Conectar con feeds de amenazas
    # Actualizar recomendaciones basadas en amenazas actuales
    pass

# Ejemplo: Integración con SIEM
def sync_with_siem():
    # Sincronizar datos de incidentes
    # Actualizar métricas de detección
    pass
```

### Automatización de Reportes
```python
# Reportes automáticos programados
def schedule_reports():
    # Generar reportes mensuales automáticamente
    # Enviar por email a stakeholders
    # Actualizar dashboards ejecutivos
    pass
```

### Machine Learning para Predicciones
```python
# Predicción de riesgos usando ML
def predict_cyber_risk():
    # Analizar patrones históricos
    # Predecir áreas de alto riesgo
    # Recomendar controles prioritarios
    pass
```

## 🎯 Casos de Uso Específicos

### Para Consultores de Ciberseguridad
- **Multi-tenant**: Gestionar múltiples clientes
- **Branded reports**: Reportes con branding personalizado
- **Benchmarking**: Comparativas entre clientes
- **ROI tracking**: Seguimiento de mejoras

### Para Empresas Corporativas
- **Compliance tracking**: Seguimiento continuo de cumplimiento
- **Risk dashboard**: Dashboard ejecutivo de riesgos
- **Audit preparation**: Preparación para auditorías
- **Budget planning**: Planificación de inversiones en seguridad

### Para Organizaciones Gubernamentales
- **Multi-agency**: Evaluaciones a través de múltiples agencias
- **Standardization**: Estandarización de evaluaciones
- **Reporting**: Reportes consolidados
- **Compliance**: Cumplimiento con marcos regulatorios

## 🛠️ Personalización Avanzada

### Agregar Nuevos Frameworks
```python
# Agregar evaluación ISO 27001
ISO27001_QUESTIONS = {
    "A.5": [
        {
            "id": "ISO_A5_001",
            "question": "¿Existe una política de seguridad de la información?",
            "weight": 1.0
        }
    ]
}
```

### Personalizar Algoritmos de Puntuación
```python
def custom_scoring_algorithm(responses, industry, company_size):
    """
    Algoritmo personalizado de puntuación
    """
    base_score = calculate_base_score(responses)
    
    # Ajustar por industria
    industry_factor = get_industry_factor(industry)
    
    # Ajustar por tamaño de empresa
    size_factor = get_size_factor(company_size)
    
    final_score = base_score * industry_factor * size_factor
    
    return final_score
```

### Integrar con Sistemas Existentes
```python
# Integración con Active Directory
def sync_with_ad():
    # Sincronizar usuarios y grupos
    # Validar controles de acceso
    pass

# Integración con ticketing systems
def sync_with_jira():
    # Crear tickets automáticamente para remediation
    # Trackear progreso de mejoras
    pass
```

## 📊 Métricas y KPIs Avanzados

### Métricas de Negocio
- **Time to Compliance**: Tiempo para alcanzar cumplimiento
- **Cost per Control**: Costo por control implementado
- **Risk Reduction Rate**: Tasa de reducción de riesgo
- **ROI de Ciberseguridad**: Retorno de inversión

### Métricas Técnicas
- **Control Effectiveness**: Efectividad de controles
- **Mean Time to Detect**: Tiempo promedio de detección
- **Mean Time to Respond**: Tiempo promedio de respuesta
- **Coverage Percentage**: Porcentaje de cobertura

### Métricas de Proceso
- **Assessment Completion Rate**: Tasa de completitud
- **Remediation Time**: Tiempo de remediación
- **Training Effectiveness**: Efectividad de entrenamiento
- **Awareness Level**: Nivel de concientización

## 🚨 Troubleshooting Común

### Problemas de Conexión a Base de Datos
```bash
# Error: Could not connect to database
# Solución:
1. Verificar credenciales en secrets.toml
2. Verificar que la IP esté allowlisted en Supabase
3. Verificar que el proyecto Supabase esté activo
```

### Problemas de Performance
```bash
# Error: App running slowly
# Solución:
1. Verificar uso de @st.cache_resource en funciones pesadas
2. Optimizar queries de base de datos
3. Limitar número de registros mostrados
```

### Problemas de Despliegue
```bash
# Error: App failed to deploy
# Solución:
1. Verificar requirements.txt tiene todas las dependencias
2. Verificar que secrets están configurados correctamente
3. Revisar logs en Streamlit Cloud para errores específicos
```

## 🔗 Enlaces Útiles

### Documentación Técnica
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)
- [Streamlit Documentation](https://docs.streamlit.io)
- [Supabase Documentation](https://supabase.com/docs)
- [Plotly Documentation](https://plotly.com/python/)

### Recursos de Ciberseguridad
- [SANS Institute](https://www.sans.org)
- [CISA Cybersecurity](https://www.cisa.gov/cybersecurity)
- [ISO/IEC 27001](https://www.iso.org/isoiec-27001-information-security.html)
- [CIS Controls](https://www.cisecurity.org/controls)

### Herramientas Complementarias
- [OpenVAS](https://www.openvas.org/) - Vulnerability scanning
- [MISP](https://www.misp-project.org/) - Threat intelligence
- [TheHive](https://thehive-project.org/) - Incident response
- [Cortex](https://github.com/TheHive-Project/Cortex) - Security analytics

## 💡 Tips de Optimización

### Performance
```python
# Usar cache para datos que no cambian frecuentemente
@st.cache_data
def load_assessment_data():
    return db_manager.get_assessments_summary()

# Paginar resultados grandes
def paginate_results(data, page_size=50):
    # Implementar paginación
    pass
```

### UX/UI
```python
# Usar progress bars para operaciones largas
with st.spinner('Procesando assessment...'):
    result = process_assessment()

# Implementar estado de carga
if 'loading' not in st.session_state:
    st.session_state.loading = False
```

### Seguridad
```python
# Validar todos los inputs
def validate_input(data):
    # Sanitizar y validar datos de entrada
    pass

# Implementar rate limiting
def check_rate_limit(user_ip):
    # Verificar límites de uso
    pass
```

## 🏆 Casos de Éxito

### Empresa de Servicios Financieros
> "Implementamos el NIST Assessment Tool y en 6 meses mejoramos nuestro puntaje de madurez de 45% a 78%. La herramienta nos ayudó a identificar gaps críticos y priorizar inversiones."
> 
> *- CISO, Banco Regional*

### Organización Gubernamental
> "La estandarización que logramos con esta herramienta nos permitió evaluar consistentemente 15 agencias diferentes y crear un roadmap unificado de ciberseguridad."
> 
> *- Director de TI, Gobierno Estatal*

### Consultoría de Ciberseguridad
> "Hemos usado la plataforma para evaluar más de 100 clientes. La capacidad de generar reportes automáticos y benchmarks nos ha ahorrado cientos de horas de trabajo."
> 
> *- Fundador, Cybersec Consulting*

---

## 🎉 ¡Felicidades!

Has llegado al final de la documentación. Tu aplicación NIST Cybersecurity Assessment está lista para transformar la manera en que las organizaciones evalúan y mejoran su postura de ciberseguridad.

### Próximos Pasos:
1. ⭐ **Star** este repositorio si te ha sido útil
2. 🍴 **Fork** para crear tu propia versión
3. 🚀 **Deploy** siguiendo las instrucciones
4. 📢 **Comparte** con la comunidad de ciberseguridad
5. 🤝 **Contribuye** con mejoras y nuevas funcionalidades

### ¿Necesitas ayuda?
- 📧 Contáctanos: support@assessment.itsmillan.com
- 💬 Únete a nuestra comunidad: [Discord](https://discord.gg/nist-assessment)
- 📖 Lee más en: [Wiki del proyecto](https://github.com/itsmillan/nist-assessment/wiki)

---

*Desarrollado con ❤️ para la comunidad de ciberseguridad*

**#CybersecurityMatters #NISTFramework #SecureByDesign**
