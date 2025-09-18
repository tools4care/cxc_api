from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS abierto (ajústalo luego a tus dominios)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
@app.head("/health")
def health():
    return {"ok": True}
# --- Reminder endpoint ---
from pydantic import BaseModel
from typing import Optional

def fmt_money(n: Optional[float]) -> str:
    try:
        return f"${float(n):,.2f}"
    except Exception:
        return "$0.00"

class ReminderIn(BaseModel):
    cliente: str
    saldo: Optional[float] = None
    limite: Optional[float] = None
    disponible: Optional[float] = None
    total_cxc: Optional[float] = None
    score: Optional[int] = None

class ReminderOut(BaseModel):
    ok: bool
    message: str

@app.post("/reminder", response_model=ReminderOut)
def make_reminder(body: ReminderIn):
    nombre = (body.cliente or "cliente").strip()
    saldo = body.saldo or 0.0
    limite = body.limite or 0.0
    disponible = body.disponible if body.disponible is not None else max(0.0, limite - max(0.0, saldo))
    total_cxc = body.total_cxc

    lineas = [
        f"Hola {nombre}, ¿cómo estás?",
        f"Te recordamos tu saldo pendiente: {fmt_money(saldo)}.",
    ]
    if limite > 0:
        lineas.append(f"Límite de crédito: {fmt_money(limite)} · Disponible: {fmt_money(disponible)}.")
    if total_cxc is not None:
        lineas.append(f"Total CxC de la cuenta: {fmt_money(total_cxc)}.")
    lineas.append("Puedes pagar en efectivo, tarjeta o transferencia. ¡Gracias por tu preferencia!")
    lineas.append("— Tools4Care")

    return {"ok": True, "message": "\n".join(lineas)}
