from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from app.database import engine, Base
from app import models
from app.utilidades.recordatoriosAuto import iniciar_scheduler

from app.routers import deudas, poderes, asambleas, votaciones, casos_juridicos

app = FastAPI(title="Servicio MODULOJurídico SOSPHIA", version="3.0")

#Base.metadata.create_all(bind=engine)

@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SOPHIA API</title>

    <style>
        body {
            margin: 0;
            padding: 0;
            font-family: "Segoe UI", Arial, sans-serif;
            background: linear-gradient(135deg, #4cafef, #3f51b5);
            color: #fff;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            text-align: center;
        }

        .card {
            background: rgba(255, 255, 255, 0.13);
            padding: 40px;
            border-radius: 15px;
            backdrop-filter: blur(10px);
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            max-width: 480px;
            width: 90%;
            animation: fadeIn 1s ease;
        }

        h1 {
            font-size: 2.4rem;
            margin-bottom: 10px;
        }

        p {
            font-size: 1.1rem;
            margin-bottom: 15px;
            color: #e3e3e3;
        }

        a {
            display: inline-block;
            margin-top: 15px;
            padding: 12px 25px;
            background: #ffffff;
            color: #3f51b5;
            border-radius: 6px;
            font-weight: bold;
            text-decoration: none;
            box-shadow: 0 3px 10px rgba(0,0,0,0.2);
            transition: 0.3s;
        }

        a:hover {
            background: #e0e0e0;
            transform: scale(1.05);
        }

        @keyframes fadeIn {
            from {
                opacity: 0;
                transform: translateY(20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

    </style>
</head>

<body>
    <div class="card">
        <h1>✨ SOSPHIA-MJ API</h1>
        <p>Bienvenido al MJ de SOSPHIA<br><strong>SOPHIA PH Management Modulo Juridico</strong></p>
        <p style="font-size: 0.9rem;">Explora la documentación y los endpoints disponibles</p>
        
        <a href="/docs">📘 Ir a Swagger UI</a>
        <a href="/redoc" style="margin-left: 10px;">📙 Redoc</a>
    </div>
</body>
</html>
    """

iniciar_scheduler()

#IMPLEMENTACION DE LOS ROUTERS
app.include_router(deudas.router)
app.include_router(poderes.router)
app.include_router(asambleas.router)
app.include_router(votaciones.router)
app.include_router(casos_juridicos.router)