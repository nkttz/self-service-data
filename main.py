import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from supabase import create_client, Client

load_dotenv()

app = FastAPI(title="Data Translator API")

supabase: Client = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_KEY")
)

class DictionaryPayload(BaseModel):
    client_id: str = Field(..., description="Unique ID of the client")
    user: str = Field(..., description="Name or ID of the user performing the action")
    dictionary_data: dict = Field(..., description="The dynamic JSON mapping of the database")


@app.post("/save-dictionary")
async def save_dictionary(payload: DictionaryPayload):
    try:
        supabase.table("app_metadata").insert({
            "client_id": payload.client_id,
            "dictionary": payload.dictionary_data
        }).execute()

        supabase.table("operation_logs").insert({
            "action": "save_dict",
            "user_id": payload.user
        }).execute()

        return {"status": "success", "message": "Dictionary saved and logged successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@app.get("/get-dictionary/{client_id}")
async def get_dictionary(client_id: str):
    try:
        response = supabase.table("app_metadata") \
            .select("dictionary") \
            .eq("client_id", client_id) \
            .order("created_at", desc=True) \
            .limit(1) \
            .execute()

        if not response.data:
            raise HTTPException(status_code=404, detail="Dictionary not found for this client")

        return {
            "client_id": client_id,
            "dictionary_data": response.data[0]["dictionary"]
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database query error: {str(e)}")
