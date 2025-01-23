import httpx
from fastapi import FastAPI, HTTPException, status
from fastapi.responses import RedirectResponse

app = FastAPI()

BACKEND_URL = "https://api-space-explorer.programar.io"


@app.get("/")
async def root():
    return RedirectResponse(url="/docs")


@app.get("/players")
async def get_players():
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{BACKEND_URL}/players")

        if response.status_code != 200:
            raise HTTPException(
                status_code=500,
                detail="Failed to fetch data from backend.",
            )

        return response.json()

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get(
    "/scoreboard",
    status_code=status.HTTP_200_OK,
    summary="Get the scoreboard",
    description="Get the scoreboard of the player scores"
    )
async def get_scoreboard():
    resource_values = {
        "iron": 1,
        "silver": 3,
        "gold": 5,
        "platinum": 10,
        "fuel": 0
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{BACKEND_URL}/players")

        if response.status_code != 200:
            raise HTTPException(
                status_code=500,
                detail="Failed to fetch data from backend.",
            )

        players = response.json()
        scoreboard = []

        for player in players:
            inventory = player.get("inventory", {})
            score = sum(
                resource_values.get(resource_type.lower(), 0) * amount
                for resource_type, amount in inventory.items()
            )

            scoreboard.append({
                "playerId": player["playerId"],
                "name": player["name"],
                "score": score,
                "currentPlanetId": player.get("currentPlanetId")
            })

        scoreboard.sort(key=lambda x: x["score"], reverse=True)
        return {"scoreboard": scoreboard}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
