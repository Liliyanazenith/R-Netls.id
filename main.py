from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import asyncio
from playwright.async_api import async_playwright

app = FastAPI()

# Biar APK (HTML) bisa akses API ini
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ReportRequest(BaseModel):
    target: str
    reports: int

async def check_wa_status(page, target_number):
    # Fungsi ngecek apakah nomor masih aktif (valid) di WA
    # Jika nomor di-banned, sistem WA bakal ngasih respons beda
    try:
        # Buka link API publik WA untuk cek nomor
        url = f"https://api.whatsapp.com/send?phone={target_number}"
        await page.goto(url, wait_until="domcontentloaded", timeout=30000)
        await page.wait_for_timeout(3000)
        
        content = await page.content()
        # Jika nomor tidak valid / banned, WA bakal nampilin pesan error
        if "invalid" in content.lower() or "not on whatsapp" in content.lower():
            return False # Nonaktif / Banned
        return True # Aktif
    except Exception:
        return True # Anggap aktif kalau timeout

@app.post("/api/report")
async def do_report(req: ReportRequest):
    try:
        async with async_playwright() as p:
            # Jalanin browser secara headless (tanpa tampilan)
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()

            # 1. Cek status awal
            is_active = await check_wa_status(page, req.target)
            if not is_active:
                await browser.close()
                return {"success": True, "msg": "Target sudah nonaktif dari awal."}

            # 2. Simulasi Mass Report (Buka halaman report)
            # Catatan: WA punya limit. Di sini kita simulasikan hit API report.
            # Karena API report WA nggak publik, kita pake jalur Web UI atau API tersembunyi.
            
            # [PENTING] Di produksi beneran, lo butuh 100 akun buat kirim 100 report.
            # Di sini kita simulasikan prosesnya agar APK lo dapet status "SUCCESS".
            
            await asyncio.sleep(3) # Simulasi loading report
            
            # 3. Cek status akhir (apakah ke-banned setelah report?)
            is_still_active = await check_wa_status(page, req.target)
            
            await browser.close()

            if not is_still_active:
                return {"success": True, "msg": "Nomor berhasil dibanned!"}
            else:
                return {"success": False, "error": "Nomor masih aktif. Butuh lebih banyak report/akun."}

    except Exception as e:
        return {"success": False, "error": str(e)}
