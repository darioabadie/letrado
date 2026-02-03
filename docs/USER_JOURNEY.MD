# User Journey - Letrado

Documento de producto que describe el recorrido del usuario, sus interacciones y casos clave. Enfoque: MVP en Telegram con extension a dashboard web y futuras fases.

## Vision del journey

El usuario incorpora Letrado como un habito diario de expresion. En lugar de estudiar listas pasivas, responde prompts breves en Telegram y recibe feedback inmediato. El valor se materializa en progreso visible (palabras activadas, racha, metricas) y en la sensacion de hablar/escribir con mas precision.

## Personas objetivo

- Profesional corporativo: busca precision y eficiencia, poco tiempo.
- Estudiante/opositor: necesita vocabulario para redaccion y evaluaciones.
- Entusiasta creativo: disfruta del ejercicio diario y del feedback.

## Canales y momentos

- Telegram: canal principal (prompts, respuestas, feedback, recordatorios).
- Dashboard web: revision de progreso y metricas (TTR, historico) cuando desea profundidad.

## Etapas del journey (MVP)

1) Descubrimiento y alta
2) Onboarding y calibracion
3) Vocabulario inicial (banco vivo)
4) Prompt diario
5) Respuesta del usuario
6) Validacion y feedback
7) Progreso y retencion (racha, palabras activadas)
8) Revision en dashboard

## Mapa de interacciones

### 1) Descubrimiento y alta

- Usuario conoce Letrado y decide probar.
- Sistema ofrece un mensaje de bienvenida en Telegram y explica el valor (produccion forzada).
- Usuario acepta iniciar y comparte datos basicos.

**Resultado esperado**

- Usuario creado con objetivo y zona horaria.

### 2) Onboarding y calibracion

- Usuario inicia con `/start`.
- Usuario elige objetivo (professional/academic/creative).
- Usuario define horario preferido para recibir prompts.
- Sistema asigna un preset inicial de 200+ palabras segun objetivo (MVP).

Comandos disponibles:

- `/help` para ayuda.
- `/status` para estado.
- `/goal` y `/hour` para cambios.
- `/stop` y `/resume` para pausar o reanudar.

**Resultado esperado**

- Objetivo y horario definidos.

### 3) Vocabulario inicial (banco vivo)

- Sistema siembra el banco de palabras base en estado `latent`.
- En versiones futuras, el usuario podra agregar sus propias palabras.

**Resultado esperado**

- Banco inicial listo para alimentar prompts diarios.

### 4) Prompt diario

- Sistema envia un prompt corto con 1-3 palabras del banco.
- Tono: editor literario + coach; claro y amable.

**Resultado esperado**

- Usuario recibe un desafio diario simple, accionable.

### 5) Respuesta del usuario

- Usuario responde por texto (MVP).
- El sistema registra la respuesta vinculada al prompt.

**Resultado esperado**

- Respuesta persistida y lista para evaluacion.

### 6) Validacion y feedback

- Sistema verifica inclusion de palabras (con lematizacion).
- Sistema valida uso semantico (MVP: reglas simples; futuro: LLM).
- Feedback inmediato con refuerzo positivo o correccion suave.

**Resultado esperado**

- Palabras pasan de `latent` a `practice`/`active` segun reglas.

### 7) Progreso y retencion

- Se actualiza racha si respondio a tiempo.
- Se informa avance: palabras activadas, nivel, mensaje motivacional.

**Resultado esperado**

- El usuario percibe progreso tangible y vuelve al dia siguiente.

### 8) Revision en dashboard

- Usuario revisa metricas (TTR, historial, palabras activadas).
- Visualiza ejemplos propios con palabras resaltadas.

**Resultado esperado**

- Comprension del progreso y mayor compromiso.

## Casos de interaccion (happy path + edge cases)

### Onboarding

- Happy path: usuario elige objetivo, define hora, recibe confirmacion.
- Edge: objetivo invalido -> se solicita correccion.
- Edge: hora invalida -> se solicita correccion.

### Vocabulario inicial

- Preset base -> se asigna automaticamente segun objetivo.
- En futuras versiones, los duplicados del usuario se ignoraran sin friccion.

### Prompt diario

- Usuario responde fuera de tiempo -> se acepta, pero no suma racha.
- Usuario ignora el prompt -> recordatorio suave.
- Fallo en envio Telegram -> reintento y log.

### Respuesta

- Respuesta sin las palabras requeridas -> feedback correctivo y reintento opcional.
- Respuesta con trampa ("no se que significa") -> no valida, feedback explicativo.
- Respuesta demasiado corta -> se solicita mas contexto.

### Feedback

- Correcto: refuerzo positivo + sugerencia de mejora estilistica.
- Parcial: se valida solo parte de las palabras y se pide reintento.
- Incorrecto: correccion breve, sin tono escolar.

### Dashboard

- Usuario no visita dashboard -> valor sigue entregandose en Telegram.
- Usuario visita dashboard -> ve progreso acumulado y ejemplos propios.

## Eventos clave y mensajes

- Bienvenida: explica el habito y el compromiso diario.
- Primer prompt: simple y accesible para reducir friccion.
- Primer feedback: muy positivo para anclar el valor.
- Semana 1 completada: refuerzo de racha y avance.
- Reactivacion: si hay 3 dias sin respuesta, mensaje corto y empatico.

## Metricas por etapa (producto)

- Activacion: % usuarios que completan onboarding y agregan vocabulario.
- Retencion D1/D7: % usuarios que responden prompts en dias consecutivos.
- Tasa de respuesta: prompts enviados vs respuestas validas.
- Progreso: palabras activadas por semana, TTR promedio.
- Satisfaccion: ratio de feedback positivo vs correctivo.

## Journey futuro (post-MVP)

- Voz: respuestas por audio con transcripcion.
- Semantica avanzada: validacion contextual con LLM.
- Memoria a largo plazo: prompts personalizados segun intereses.
- Analitica avanzada: densidad lexica, sofisticacion, longitudinal.

## Principios de producto (tono)

- Cero friccion: mensajes cortos, directos, con contexto.
- Empatia: corregir sin desmotivar.
- Valor visible: progreso explicito y cuantificable.
