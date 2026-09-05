# 📦 Reporte Diario de Ruta – Colserlog

Aplicación web progresiva para el registro y seguimiento de entregas diarias de paquetes. Permite capturar tiempos de ruta, estados de cada visita, visualizar estadísticas del día y promedios históricos, todo almacenado localmente en el navegador.

[![Demo](https://img.shields.io/badge/demo-GitHub%20Pages-blue)](https://kevinlink257-commits.github.io/reportes/)
_Reemplaza el enlace con la URL de tu GitHub Pages._

---

## 🚀 Características principales

- **Registro de tiempos base** – Calcula# 📦 Reporte Diario de Ruta – Colserlog

Aplicación web progresiva para el registro y seguimiento de entregas diarias de paquetes. Permite capturar tiempos de ruta, estados de cada visita, visualizar estadísticas del día y promedios históricos, todo almacenado localmente en el navegador.

[![Demo](https://img.shields.io/badge/demo-GitHub%20Pages-blue)](https://tusuario.github.io/reporte-entregas/)
_Reemplaza el enlace con la URL de tu GitHub Pages._

---

## 🚀 Características principales

- **Registro de tiempos base** – Calcula automáticamente los minutos invertidos en carga, preparación, viaje y total hasta la primera entrega.
- **Captura de visitas** – Con botones que insertan la hora actual del navegador para agilizar el registro. Soporta seis estados de paquete.
- **Tabla de detalle** – Muestra en tiempo real cada visita con su duración en minutos.
- **Dashboard diario** – Gráfica de barras con la cantidad de paquetes por estado, y tarjetas con entregados, no entregados, total visitas y promedio de tiempo por visita.
- **Estadísticas históricas** – Guarda automáticamente el total de entregas por día en `localStorage`. Calcula y muestra el promedio de entregas diario, semanal y mensual, con su propia gráfica.
- **Diseño responsive** – Adaptado para móviles y tablets.
- **Impresión / PDF** – Botón que genera una vista optimizada para imprimir o guardar como PDF.

---

## 🧠 ¿Cómo funciona?

### Almacenamiento de datos
Toda la información (visitas registradas, conteos diarios) se guarda en el **almacenamiento local del navegador** (`localStorage`). Esto significa que los datos persisten incluso si cierras o recargas la página. No se requiere conexión a internet ni base de datos externa.

### Flujo de uso típico
1. **Tiempos base**: Al iniciar la ruta, ingresa las cuatro horas clave (inicio/fin de carga, salida empresa, llegada a primera entrega). El sistema te muestra los intervalos en minutos.
2. **Registro de visitas**: Para cada cliente:
- Pulsa **"Llegada ahora"** para registrar la hora de llegada con la hora exacta.
- Selecciona el estado del paquete en el desplegable.
- Al terminar la visita, pulsa **"Salida y Registrar"** – esto registra la hora de salida actual y guarda automáticamente la visita.
- También puedes ingresar las horas manualmente y usar el botón **"Guardar Visita"**.
3. **Visualización**: La tabla de detalle se actualiza, las tarjetas de resumen cambian y la gráfica diaria se refresca.
4. **Historial**: Al final del día, el sistema guarda el total de entregas. Al abrir la página en días siguientes, los promedios históricos (diario, semanal y mensual) se calculan con todos los días registrados.

### Tecnologías utilizadas
- **HTML5 + CSS3** – Estructura y estilos responsive.
- **JavaScript (ES6)** – Lógica de negocio y manipulación del DOM.
- **Chart.js** – Generación de gráficos de barras.
- **localStorage** – Persistencia de datos en el cliente.
- **Media queries** – Adaptación a impresión. automáticamente los minutos invertidos en carga, preparación, viaje y total hasta la primera entrega.
- **Captura de visitas** – Con botones que insertan la hora actual del navegador para agilizar el registro. Soporta seis estados de paquete.
- **Tabla de detalle** – Muestra en tiempo real cada visita con su duración en minutos.
- **Dashboard diario** – Gráfica de barras con la cantidad de paquetes por estado, y tarjetas con entregados, no entregados, total visitas y promedio de tiempo por visita.
- **Estadísticas históricas** – Guarda automáticamente el total de entregas por día en `localStorage`. Calcula y muestra el promedio de entregas diario, semanal y mensual, con su propia gráfica.
- **Diseño responsive** – Adaptado para móviles y tablets.
- **Impresión / PDF** – Botón que genera una vista optimizada para imprimir o guardar como PDF.

---

## 🧠 ¿Cómo funciona?

### Almacenamiento de datos
Toda la información (visitas registradas, conteos diarios) se guarda en el **almacenamiento local del navegador** (`localStorage`). Esto significa que los datos persisten incluso si cierras o recargas la página. No se requiere conexión a internet ni base de datos externa.

### Flujo de uso típico
1. **Tiempos base**: Al iniciar la ruta, ingresa las cuatro horas clave (inicio/fin de carga, salida empresa, llegada a primera entrega). El sistema te muestra los intervalos en minutos.
2. **Registro de visitas**: Para cada cliente:
- Pulsa **"Llegada ahora"** para registrar la hora de llegada con la hora exacta.
- Selecciona el estado del paquete en el desplegable.
- Al terminar la visita, pulsa **"Salida y Registrar"** – esto registra la hora de salida actual y guarda automáticamente la visita.
- También puedes ingresar las horas manualmente y usar el botón **"Guardar Visita"**.
3. **Visualización**: La tabla de detalle se actualiza, las tarjetas de resumen cambian y la gráfica diaria se refresca.
4. **Historial**: Al final del día, el sistema guarda el total de entregas. Al abrir la página en días siguientes, los promedios históricos (diario, semanal y mensual) se calculan con todos los días registrados.

### Tecnologías utilizadas
- **HTML5 + CSS3** – Estructura y estilos responsive.
- **JavaScript (ES6)** – Lógica de negocio y manipulación del DOM.
- **Chart.js** – Generación de gráficos de barras.
- **localStorage** – Persistencia de datos en el cliente.
- **Media queries** – Adaptación a impresión.
