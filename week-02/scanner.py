# Attack surface scanner: inspects an agent's tools and flags the risky ones.

# The agent's tool definitions (same shape as in agent.py).
TOOLS = [
    {"name": "get_current_time", "description": "Returns the current time as HH:MM"},
    {"name": "write_note", "description": "Appends a note to the user's notes file"},
    {"name": "delete_file", "description": "Deletes a file"}
]
ALLOWED_TOOLS = {"get_current_time", "write_note"}

# Words that signal a tool ACTS on the world (not just reads).
ACTS_ON_WORLD = ["write", "send", "delete", "remove", "execute", "run",
                 "create", "update", "append", "pay", "transfer", "post"]

def classify(tool):
    text = (tool["name"] + " " + tool["description"]).lower()
    if any(word in text for word in ACTS_ON_WORLD):
        return "HIGH", "acts on the world"
    return "LOW", "read-only"

def scan(tools, allowed):
    print("=== Attack surface scan ===\n")
    high_allowed = 0
    for t in tools:
        risk, why = classify(t)
        is_allowed = t["name"] in allowed
        flag = "  <-- allowed + HIGH: must be gated" if (risk == "HIGH" and is_allowed) else ""
        if risk == "HIGH" and is_allowed:
            high_allowed += 1
        print(f"{t['name']:<20} | allowed: {'yes' if is_allowed else 'no ':<3} | risk: {risk:<4} ({why}){flag}")
    print(f"\nSummary: {high_allowed} high-risk tool(s) allowed. Make sure run_tool gates them.")

if __name__ == "__main__":
    scan(TOOLS, ALLOWED_TOOLS)

# --- Límites de este escáner (saberlos es parte de la seguridad) ---
# 1. Lee la DESCRIPCIÓN de la tool, no su código real. Una tool cuya
#    descripción no coincida con lo que hace (p. ej. "Tidies up the
#    workspace" que en realidad borra archivos) pasaría como LOW.
# 2. Es engañable por tool poisoning: si un atacante controla las
#    descripciones, puede disfrazar tools peligrosas con texto manso.
# Conclusión: las palabras clave son un primer filtro rápido, NO una
# defensa. La defensa real es el gate en run_tool, que mira lo que
# ocurre en EJECUCIÓN, no lo que promete la descripción.