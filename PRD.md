# Product Requirements Document (PRD): Letrado (Nombre Clave)


## 1. Resumen Ejecutivo

Letrado es una solución SaaS B2C diseñada para combatir la atrofia del vocabulario activo en hablantes nativos de español. A diferencia de las plataformas tradicionales de aprendizaje de idiomas (L2) como Duolingo, Letrado utiliza un enfoque de "producción forzada" integrado directamente en WhatsApp.

El objetivo es reducir la fricción del aprendizaje mediante el uso de una interfaz familiar, utilizando Inteligencia Artificial Generativa (LLM) para crear estímulos diarios que obliguen al usuario a utilizar palabras de un "banco léxico personal" en contextos significativos, cerrando la brecha entre el vocabulario pasivo y el activo.

## 2. Planteamiento del Problema y Oportunidad

**El Problema:** Existe una simplificación lingüística generalizada y una dependencia de un "lenguaje económico". Los profesionales y estudiantes carecen de herramientas para sofisticar su lengua materna; las apps actuales se enfocan en enseñar idiomas desde cero o en ejercicios pasivos (selección múltiple) que no mejoran la fluidez verbal real.

**La Oportunidad:** El mercado EdTech en Latinoamérica está en auge. Existe un vacío de mercado para una herramienta de "upskilling comunicativo" que combine la comodidad de los chatbots de WhatsApp (como AudioLingo o Parlai) con la profundidad analítica de herramientas de corpus lingüístico.

## 3. Perfil de Usuario (User Personas)

- **El Profesional Corporativo:** Necesita mejorar su elocuencia y precisión léxica para correos, presentaciones y negociaciones. Busca eficiencia y bajo compromiso de tiempo.
- **El Opositor/Estudiante Universitario:** Necesita enriquecer su vocabulario para redactar ensayos académicos o superar pruebas orales.
- **El Entusiasta de las Letras:** Disfruta del aprendizaje y busca "fitness mental" a través de la escritura diaria (journaling).

## 4. Requerimientos Funcionales (FR)

### Módulo 1: Onboarding y Calibración (Core)

El sistema debe entender el punto de partida del usuario para no sugerir palabras demasiado básicas ni excesivamente arcaicas.

- **FR-01: Ingesta de Vocabulario Inicial.** El usuario debe poder ingresar manualmente palabras que desea aprender. Adicionalmente, el sistema propondrá un set inicial basado en un breve test de nivel.
- **FR-02: Definición de Objetivos.** El usuario seleccionará su foco: Profesional, Académico, o Literario/Creativo.

### Módulo 2: Motor de Interacción en WhatsApp (Interface)

La interfaz principal será WhatsApp Business API para garantizar la mínima fricción.

- **FR-03: Disparador de Estímulos (Daily Trigger).** El sistema enviará un mensaje diario (configurable por el usuario) con un "Prompt de Producción Forzada".
  - Ejemplo: "Buenos días. Describe tu plan para hoy utilizando obligatoriamente los términos 'procrastinar' y 'efímero'".
- **FR-04: Recepción Multimodal.** El sistema debe aceptar respuestas tanto en texto como en notas de voz (transcritas vía API de Whisper o similar).

### Módulo 3: Procesamiento de Lenguaje Natural (NLP Backend)

El núcleo inteligente que evalúa la calidad de la respuesta.

- **FR-05: Verificación de Restricciones.** El algoritmo debe verificar si el usuario incluyó las palabras solicitadas (lemmatización incluida: efímero -> efímera cuenta como válido).
- **FR-06: Análisis de Contexto Semántico.** La IA debe determinar si la palabra se usó correctamente. Si el usuario hace "trampa" (ej: "No sé qué significa efímero"), el sistema no debe validar el punto.
- **FR-07: Feedback Empático e Inteligente.**
  - Si el uso es correcto: Refuerzo positivo.
  - Si es incorrecto o impreciso: Corrección sutil y alentadora, evitando un tono escolar rígido.
  - Sugerencia de mejora: "Has usado bien la palabra, pero podrías sonar más elegante si dijeras...".

### Módulo 4: Sistema de Progresión y Gamificación

Mecánicas para retener al usuario sin infantilizar la experiencia.

- **FR-08: Banco de Palabras "Vivo".** Las palabras tienen estados:
  - Latente (Nueva).
  - En Práctica (Sugerida en prompts recientes).
  - Activada (Usada correctamente X veces en contextos distintos).
- **FR-09: Rachas (Streaks).** Contador visual de días consecutivos cumpliendo el reto para fomentar el hábito.

### Módulo 5: Analítica y Dashboard (Web View)

Dado que WhatsApp es limitado para visualizaciones complejas, se requiere una vista web complementaria para métricas profundas.

- **FR-10: Cálculo de Riqueza Léxica (TTR).** El sistema calculará la Relación Tipo-Token (Type-Token Ratio) de las interacciones del usuario. La fórmula a implementar en el backend es: $$TTR = \frac{V}{N}$$ donde $V$ son los tipos únicos y $N$ el total de palabras.
- **FR-11: Reporte de Densidad y Sofisticación.** Gráficos que muestren la evolución de la complejidad del vocabulario del usuario a lo largo del tiempo, similar a herramientas como Voyant Tools.
- **FR-12: Historial de Chat Analizado.** Posibilidad de ver conversaciones pasadas con las palabras clave resaltadas.

## 5. Requerimientos No Funcionales (NFR)

- **NFR-01: Privacidad y Seguridad.** Cumplimiento estricto de GDPR. Los datos de las entradas (que pueden ser personales/diario) deben estar cifrados y no utilizarse para re-entrenar modelos públicos sin consentimiento explícito.
- **NFR-02: Latencia.** El feedback de la IA en WhatsApp no debe tardar más de 5 segundos para mantener la fluidez de la conversación.
- **NFR-03: Tono de la IA.** La "personalidad" del bot debe ser un híbrido entre un editor literario y un coach de vida: paciente, culto, pero cercano.

## 6. Arquitectura Técnica Propuesta

Basada en la investigación de soluciones existentes:

- **Frontend:** WhatsApp Business API.
- **Orquestador:** Backend (Python/Node.js) que gestiona la lógica de estados de palabras y usuarios.
- **Motor IA:** Integración con API de LLM (ej: GPT-4o o Claude 3.5) con system prompts diseñados para "forced production".
- **Base de Datos Vectorial:** Para dotar de memoria a largo plazo al bot (recordar intereses del usuario para generar preguntas relevantes).

## 7. Matriz de Priorización (MoSCoW)

| Prioridad | Requerimiento | Justificación |
| --- | --- | --- |
| Must Have (Crítico) | Integración con WhatsApp (FR-03) | La baja fricción es la ventaja competitiva clave. |
| Must Have | Motor de Producción Forzada (FR-04, FR-05) | Es el core value pedagógico que diferencia la app de Duolingo. |
| Should Have (Importante) | Métricas TTR y Dashboard (FR-10, FR-11) | Necesario para demostrar valor tangible al usuario profesional. |
| Should Have | Memoria a largo plazo de intereses (FR-06) | Aumenta la personalización y evita que las preguntas sean genéricas. |
| Could Have (Deseable) | Input por Voz (FR-04) | Mejora la accesibilidad, aunque el texto es prioritario para la precisión léxica inicial. |
| Won't Have (MVP) | Clases en vivo o tutores humanos | Se prioriza la escalabilidad de la IA y el modelo SaaS automatizado. |

## 8. Riesgos y Mitigación

- **Riesgo:** El usuario se frustra si la IA no reconoce un sinónimo válido.
  - **Mitigación:** Calibrar el prompt de la IA para ser flexible ("Validar si el sentido es correcto aunque la palabra varíe ligeramente, pero recordar el objetivo").
- **Riesgo:** Costo de la API de WhatsApp.
  - **Mitigación:** Modelo de suscripción Freemium donde el usuario gratuito tiene límites de mensajes diarios.
