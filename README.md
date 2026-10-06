# 📦 Reporte Diario de Ruta – Colserlog

PWA para registrar y analizar entregas de última milla. Captura tiempos de ruta, estados de visita, evidencia fotográfica, firma, GPS y reportes, con persistencia local en el navegador.

[![Demo](https://img.shields.io/badge/demo-GitHub%20Pages-blue)](https://kevinlink257-commits.github.io/reportes/)

## 🚀 Características

- Registro de tiempos base: carga, preparación, salida y llegada a la primera entrega.
- Reparto rápido con captura manual, cámara, lector QR y OCR.
- Estados de paquete, firma, fotografías, notas de voz y evidencia de visita.
- Dashboard diario con entregados, no entregados, valor, duración y gráfica.
- Estadísticas históricas en `localStorage`.
- Manifiesto de paquetes y consulta de datos cargados.
- Diseño responsive, modo oscuro, modo conducción e instalación PWA.
- Impresión, PDF, álbum fotográfico y compartir resumen por WhatsApp.
- Modal **Visión de Futuro** con roadmap 2026–2028, pilares last-mile, KPIs, arquitectura, inversión/ROI y plan de 30 días.

## 🧭 Hoja de ruta estratégica

El plan completo está en [`ROADMAP.md`](ROADMAP.md) y también se puede consultar desde la aplicación mediante **🌌 Visión de Futuro**.

| Fase | Horizonte | Enfoque |
|---|---:|---|
| Fundación | 0–3 meses | Backend propio, PostgreSQL + PostGIS, API, SSO, roles y telemetría |
| Optimización | 3–9 meses | OR-Tools/VRP, secuenciación, priorización y ETA predictivo |
| Inteligencia | 9–15 meses | Excepciones predictivas, visión computacional, geofencing y scorecards |
| Network Effects | 15–24 meses | Multi-bodega, re-ruteo, BI, data warehouse y feeds B2B |

### KPIs objetivo

- SPH: **11 → 17 → 22** paradas por hora (baseline / 12m / 24m).
- First-time delivery: **78% → 92% → 97%**.
- Costo por entrega: **$2.800 → $2.200 → $1.750 COP**.
- SLA menor a 24 horas: **82% → 95% → 99%**.

> Las cifras de inversión, ahorro y ROI son hipótesis de planeación. Deben validarse con datos reales antes de comprometer presupuesto.

## 🧠 Datos y privacidad

La aplicación actual guarda la información en el almacenamiento local del navegador; no requiere una base de datos externa para funcionar. Las fotografías deben seguir las reglas de privacidad mostradas por la aplicación y la Ley 1581 de 2012.

La arquitectura futura contempla backend propio, autenticación empresarial, PostgreSQL + PostGIS, Redis, almacenamiento de objetos y un flujo de eventos para analítica y ML.

## 🛠️ Tecnologías

- HTML5, CSS3 y JavaScript ES6.
- Chart.js para gráficos.
- `localStorage` para persistencia local.
- HTML5 QR / ZXing para códigos.
- Tesseract.js para OCR.
- jsPDF, JSZip y html2canvas para reportes y exportaciones.
- GitHub Pages mediante GitHub Actions.

## ▶️ Uso local

Abrir `index.html` en un navegador moderno. Para probar cámara, PWA y APIs del navegador se recomienda servirlo mediante HTTPS o un servidor local.

## 📄 Licencia y operación

Este repositorio contiene la aplicación operativa de Colserlog. Revisar permisos, tratamiento de datos y configuración de despliegue antes de incorporar servicios backend o integraciones empresariales.

## Plataforma y cuenta

La aplicación ahora incorpora una base de migración a backend propio en [`backend/`](backend/): FastAPI, PostgreSQL + PostGIS, perfiles, roles, búsqueda de guías y telemetría. El despliegue local se inicia con `docker compose up --build`; GitHub Pages continúa funcionando como frontend offline mientras se configura el endpoint productivo y SSO/OIDC.

En **Ajustes → Mi cuenta**, el usuario puede cambiar su nombre y contraseña después de validar la contraseña actual. En **Reparto Rápido** puede escribir algunos dígitos y seleccionar la guía con mayor coincidencia desde el banco.
