# Caso 2 — Samsung: la fuga que nadie hackeó

## Contexto
En 2023, ingenieros de Samsung pegaron código fuente confidencial y notas
internas de reuniones en ChatGPT para trabajar más rápido. En ese momento esos
datos salieron de Samsung y entraron en servidores de un tercero que la empresa
no controla. Nadie los hackeó: se fugaron porque alguien los metió,
voluntariamente, por una puerta sin vigilancia. Samsung acabó prohibiendo estas
herramientas.

Es el punto "datos" de mi mapa de ataque, pero al revés: no entra algo malo,
SALE algo que no debía. Y el "atacante" era un empleado bienintencionado.

## Mini-test — por qué no basta con prohibirlo por norma
Una norma escrita ("no peguéis secretos") es como poner la regla en el prompt:
ayuda, pero alguien la ignora, la olvida o la salta. Hace falta una barrera
lógica o física que se active sola cuando se cruza la línea. Con personas se
usan las dos capas: la norma reduce los errores honestos; la barrera técnica
atrapa al resto.

## Decisión
Me pongo en la silla del responsable de IA, antes de la fuga:

- (A) Prohibir ChatGPT y similares — **descartada**: una prohibición que no
  puedes hacer cumplir empeora la seguridad, porque la gente sigue usando la IA
  en su móvil personal (shadow AI) y pierdes toda visibilidad. El riesgo no
  desaparece, se va a donde no lo ves.
- (B) Permitir con una capa técnica (DLP) que detecte y bloquee datos sensibles
  antes de que salgan — **elegida como base**.
- (C) IA interna donde los datos nunca cruzan la frontera — **elegida para lo
  más sensible**.

Elijo **B + C combinadas**, no una sola.

## Afinados (nivel que me interesa como consultor)
1. **El gate lo pongo yo, no el proveedor.** Uso la versión enterprise del
   proveedor (contrato que no entrena con mis datos + controles de admin), pero
   la barrera que OBLIGA (el DLP que escanea la salida) vive en mi lado.
   Confío, pero verifico: no externalizo mi seguridad a un contrato ajeno.
2. **Clasifico el dato; no todo necesita lo mismo.** Todo interno es caro y el
   modelo interno suele ser más flojo (cambio potencia por contención). Ajusto
   el control a la sensibilidad: datos poco sensibles → IA cloud enterprise;
   joyas de la corona (código fuente, diseños sin lanzar) → interno o nunca.

## Patrón de decisión reutilizable
Ante "los empleados usan IA con datos de la empresa": nunca prohibir a ciegas
(crea shadow AI). Clasificar el dato, poner una barrera técnica propia en la
salida, y reservar lo interno/aislado solo para lo más sensible.
La norma informa; el gate obliga; el tier decide cuánto gate.