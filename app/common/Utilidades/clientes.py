import httpx

API_EXTERN_BASE = "http://34.201.187.167/view/users"

async def obtener_usuario_externo(hp_id: int):
    url = f"{API_EXTERN_BASE}/{hp_id}"

    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.get(url)

    if response.status_code != 200:
        return None
    
    return response.json()