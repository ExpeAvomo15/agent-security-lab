# Caso 1 — Air Canada: un chatbot que inventó una política

## Contexto
Air Canada desplegó un chatbot de atención al cliente. Un usuario preguntó por
los descuentos por duelo y el bot se inventó una política de reembolso que no
existía. El usuario actuó confiando en esa respuesta; Air Canada se negó a
cumplirla y el caso acabó en un tribunal, que condenó a la empresa: es
responsable de lo que dice su IA igual que de lo que dice su web. El bot solo
producía texto, sin herramientas, y aun así causó un daño real e irreversible,
porque había un humano que se fiaba (el usuario fue el canal de salida).

## Decisión
Me pongo en la silla del responsable de IA, antes del incidente, con tres
opciones:

- (A) Chatbot libre con aviso legal — **descartada**: el aviso legal no exime a
  la empresa de lo que afirma su IA; el usuario asume que el bot habla por ella.
- (B) Chatbot que solo responde citando texto literal de la base de
  conocimiento — **viable pero descartada**: mata la experiencia de usuario y
  pierde el tono conversacional que justifica el proyecto.
- (C) No desplegar hasta tener grounding + verificación de salida —
  **elegida**: cuesta más tiempo, pero es la única que ataca la causa raíz.

## Arquitectura propuesta
1. **Grounding por RAG.** El modelo conversacional se conecta a una fuente de
   datos verificada de la empresa (documentos no estructurados). Responde desde
   ahí, con tono amigable, en lugar de desde su memoria.
2. **Verificador de salida (LLM-as-a-judge).** Una segunda IA, con temperatura
   casi neutra, comprueba la respuesta antes de enviarla al usuario. Solo marca
   si la información es correcta o no; si lo es, se envía.
3. **Caché de preguntas frecuentes.** Las preguntas más repetidas se dejan con
   respuesta predeterminada en el chat, para que el usuario las encuentre y el
   modelo no tenga que generarlas cada vez (ahorro de tokens).
4. **Puerta a humano en temas críticos.** Ante asuntos delicados, el sistema
   redirige automáticamente al usuario a un agente humano.

## Compromisos (trade-offs)
- Más tiempo de desarrollo y mayor coste por consulta (RAG + dos llamadas a
  modelo).
- A cambio: se elimina la causa raíz del incidente (la alucinación sobre datos
  oficiales) y se gana una defensa auditable.

## Brechas de seguridad detectadas en mi propio diseño
1. **¿Quién verifica al verificador?** El verificador es también un LLM y lee el
   mismo RAG que el generador. Si la fuente de datos se envenena, ambas IAs leen
   la mentira y se dan la razón: el verificador da una falsa sensación de
   seguridad. Mitigación: para datos críticos, verificar contra algo difícil de
   engañar (el texto exacto del documento, una regla determinista), no otra
   opinión de IA.
2. **El caché puede quedar obsoleto.** Una respuesta cacheada se vuelve falsa
   cuando cambia la política. Necesita un dueño y un disparador atados a la
   actualización de la fuente de verdad; si no, se reproduce el mismo incidente
   con el propio caché.
3. **La redirección de temas críticos no puede vivir en el prompt.** Una regla
   escrita en el prompt es evitable (frases raras, otro idioma, prompt
   injection). La redirección debe ejecutarse en un filtro determinista fuera
   del modelo, por el que el modelo no pueda colarse.

## Patrón de decisión reutilizable
Para un sistema de IA de cara al público y de alto riesgo:
**grounding + verificación independiente + puerta a humano para lo crítico, y la
parte que hace cumplir las reglas nunca vive dentro del prompt.**