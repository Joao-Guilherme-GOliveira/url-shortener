from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, HttpUrl
import random
import string
import sqlite3
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

origins = [
    "http://localhost:5000",
    "http://127.0.0.1:5000",
    
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def create_table():
    conn = sqlite3.connect('links.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS links(
            code TEXT PRIMARY KEY,
            original_url TEXT NOT NULL)''')
    conn.commit()
    conn.close()

def save_link(code,url):
    conn = sqlite3.connect('links.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO links (code, original_url) VALUES (?, ?)', (code, url))
    conn.commit()
    conn.close()

def get_original_url(code):
    conn = sqlite3.connect('links.db')
    cursor = conn.cursor()
    cursor.execute('SELECT original_url FROM links WHERE code = ?', (code,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None


create_table()

class LinkRequest(BaseModel):
    url: HttpUrl

def generate_shortened(length=8):
    return ''.join(random.choices(string.ascii_letters+string.digits,k=length))

def code_exists(code):
    conn = sqlite3.connect('links.db')
    cursor = conn.cursor()
    cursor.execute('SELECT 1 FROM links WHERE code = ?', (code,))
    exists = cursor.fetchone() is not None
    conn.close()
    return exists
@app.post("/shorten")
def short_link(link_request: LinkRequest):
    url = link_request.url

    code = generate_shortened()
    while code_exists(code):
        code = generate_shortened()

    print(f"Salvando link: code={code} url={url}")
    save_link(code,str(url))
    print("Link salvo com sucesso.")

    
    short_url = f"http://localhost:8000/{code}"
    return{"short_url":short_url}


@app.get("/links")
def get_all_links():
    conn = sqlite3.connect('links.db')
    cursor = conn.cursor()
    cursor.execute('SELECT code,original_url FROM links')
    rows = cursor.fetchall()
    conn.close()
    return [{"code": code, "url": url} for code, url in rows]

@app.get("/{code}")
def redirect(code:str):
    url = get_original_url(code)
    if url:
        return RedirectResponse(url)
    else:
        raise HTTPException(status_code=404,detail="Link not found")

@app.delete("/delete/{code}")
def delete_link(code:str):
    conn = sqlite3.connect('links.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM links WHERE code = ?', (code,))
    conn.commit()
    conn.close()
    return {"message": "Link deleted successfully"}