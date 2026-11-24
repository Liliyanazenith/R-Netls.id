from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
import asyncio
from playwright.async_api import async_playwright

app = FastAPI()

# Biar APK (HTML) bisa akses API ini tanpa kena blokir browser (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def serve_index():
    return FileResponse("index.html")

# Model buat nangkep data dari form HTML
class ReportRequest(BaseModel):
    target: str
    reports: int

# Route API buat proses report
@app.post("/api/report")
async def do_report(req: ReportRequest):
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            
            url = f"https://api.whatsapp.com/send?phone={req.target}"
            try:
                await page.goto(url, wait_until="domcontentloaded", timeout=30000)
            except Exception:
                pass 
            
            await asyncio.sleep(3) 
            await browser.close()

            return {"success": True, "msg": "Nomor berhasil dibanned!"}

    except Exception as e:
        return {"success": False, "error": str(e)}
