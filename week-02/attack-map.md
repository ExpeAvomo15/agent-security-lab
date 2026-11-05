# Mapa de ataque — mi agente (semana 1)

Agente: Python + claude-opus-5-5, bucle, memoria, 2 tools (get_current_time, write_note), gate run_tool.

## 1. Superficie de ataque

| Punto | Riesgo hoy | Por qué |
| --- | --- | --- |
| Modelo (opus-5-5) | Bajo | No lo controlo yo; nadie externo lo toca |
| Prompt | Bajo | Solo yo escribo; se dispara con otros usuarios o con datos externos |
| Datos de entrada | Nulo | No lee nada de fuera (sala cerrada) |
| **Tools (write_note)** | **Alto** | Actúa en el mundo real: escribe archivos |
| Salida | Bajo | Muere en la terminal; sube si la consume otro agente |

Conclusión: hoy solo hay un punto que cuidar de verdad, las **tools**. El resto está cerrado por ahora; cada uno se abriría al añadir usuarios, datos externos o encadenar agentes.

## 2. Mapeo OWASP Top 10 for LLM (2025)

A qué punto de mi agente afecta cada categoría:

- LLM01 Prompt Injection → Prompt + Datos de entrada
- LLM02 Sensitive Information Disclosure → Salida
- LLM03 Supply Chain → Modelo + dependencias del proyecto
- LLM04 Data and Model Poisoning → Datos de entrada (cuando haya RAG)
- LLM05 Improper Output Handling → Salida (crítico si la consume otro agente)
- LLM06 Excessive Agency → Tools (write_note): el punto caliente
- LLM07 System Prompt Leakage → Prompt / Salida
- LLM08 Vector and Embedding Weaknesses → Datos de entrada (futuro RAG)
- LLM09 Misinformation → Salida (el modelo alucina)
- LLM10 Unbounded Consumption → Bucle (llamadas sin límite)

Observación: varias categorías (LLM01, LLM04, LLM08) apuntan a puntos que HOY tengo cerrados. Son el mapa de lo que se abrirá según crezca el agente. La categoría viva hoy es LLM06 (Excessive Agency), sobre las tools.