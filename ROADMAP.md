# Plan de mejora Colserlog · 2026–2028

## Objetivo

Evolucionar la PWA de seguimiento de entregas hacia una plataforma de operación **last-mile** medible, trazable y progresivamente predictiva.

## Plan aprobado e implementado en esta iteración

1. **Visibilizar la estrategia:** incorporar la hoja de ruta de cuatro fases en el modal “Visión de Futuro”.
2. **Alinear métricas:** publicar los cinco pilares de excelencia y la tabla de KPIs baseline / 12 meses / 24 meses.
3. **Aterrizar la ejecución:** mostrar arquitectura objetivo, decisión de fundación y acciones concretas para los próximos 30 días.
4. **Hacer explícito el caso económico:** incluir inversión por fase, ahorro anual estimado, ROI y payback como hipótesis sujetas a validación.
5. **Mantener la operación actual:** no cambiar el registro de entregas, almacenamiento local, escaneo, evidencia fotográfica, firma, GPS, reportes o autenticación existentes.
6. **Documentar el cambio:** actualizar README y dejar este plan versionado en el repositorio.

## Roadmap operativo

| Fase | Ventana | Prioridad | Entregables principales |
|---|---:|---|---|
| Fundación | 0–3 meses | Datos y plataforma | Backend propio, PostgreSQL + PostGIS, API versionada, SSO/roles, telemetría y dashboard dispatcher |
| Optimización | 3–9 meses | Productividad | OR-Tools/VRP, priorización de paradas, ETA predictivo y reducción de km por ruta |
| Inteligencia | 9–15 meses | Automatización | Excepciones predictivas, computer vision, geofencing y scorecard de mensajeros |
| Network Effects | 15–24 meses | Escala | Multi-bodega, re-ruteo dinámico, data warehouse, BI y feeds B2B |

## Criterios de éxito

- 100% de entregas con foto, firma y GPS.
- Latencia de sincronización menor a 5 segundos.
- Uptime objetivo del backend superior a 99.9%.
- SPH: 11 baseline → 17 a 12 meses → 22 a 24 meses.
- First-time delivery: 78% baseline → 92% a 12 meses → 97% a 24 meses.
- Costo por entrega: $2.800 COP baseline → $1.750 COP a 24 meses.

## Próximos pasos recomendados

- Ejecutar auditoría técnica externa.
- Validar baseline con datos de operación reales antes de usar las cifras de ROI para decisiones financieras.
- Diseñar el esquema PostgreSQL + PostGIS y el contrato de API.
- Construir un prototipo OR-Tools con datos dummy.
- Definir KPIs contractuales con los clientes B2B.

> La inversión, los ahorros, el ROI y el payback publicados son hipótesis del material de planeación; deben validarse con Finanzas, Operaciones, Legal y Tecnología antes de aprobar presupuesto.
