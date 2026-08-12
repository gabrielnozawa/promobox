import sqlite3
from datetime import datetime
DB='data/promobox.db'

def db():
    c=sqlite3.connect(DB); c.row_factory=sqlite3.Row; return c

def init_db():
    with db() as c:
        c.execute('''CREATE TABLE IF NOT EXISTS offers(
        id INTEGER PRIMARY KEY AUTOINCREMENT,name TEXT NOT NULL,category TEXT NOT NULL,
        old_price REAL DEFAULT 0,price REAL NOT NULL,affiliate_url TEXT NOT NULL,image_url TEXT,
        scheduled_at TEXT NOT NULL,custom_text TEXT,status TEXT DEFAULT 'programada',
        created_at TEXT NOT NULL,published_at TEXT)''')
        c.commit()

def add_offer(name,category,old_price,price,url,image,scheduled,custom):
    with db() as c:
        c.execute('''INSERT INTO offers(name,category,old_price,price,affiliate_url,image_url,scheduled_at,custom_text,created_at)
        VALUES(?,?,?,?,?,?,?,?,?)''',(name,category,old_price,price,url,image,scheduled,custom,datetime.now().isoformat()))

def get_offers():
    with db() as c:return c.execute('SELECT * FROM offers ORDER BY scheduled_at DESC').fetchall()

def get_due_offers():
    now=datetime.now().isoformat(timespec='minutes')
    with db() as c:return c.execute("SELECT * FROM offers WHERE status='programada' AND scheduled_at<=? ORDER BY scheduled_at",(now,)).fetchall()

def update_status(oid,status):
    with db() as c:
        c.execute('UPDATE offers SET status=?,published_at=? WHERE id=?',(status,datetime.now().isoformat() if status=='publicada' else None,oid))

def import_offers(rows):
    n=0
    for r in rows:
        try:
            add_offer(str(r['name']),str(r.get('category') or 'Ofertas gerais'),float(r.get('old_price') or 0),float(r['price']),str(r['affiliate_url']),str(r.get('image_url') or ''),str(r.get('scheduled_at') or datetime.now().isoformat()),str(r.get('custom_text') or '')); n+=1
        except Exception: pass
    return n

def get_stats():
    with db() as c:
        total=c.execute('SELECT COUNT(*) FROM offers').fetchone()[0]
        scheduled=c.execute("SELECT COUNT(*) FROM offers WHERE status='programada'").fetchone()[0]
        published=c.execute("SELECT COUNT(*) FROM offers WHERE status='publicada'").fetchone()[0]
        failed=c.execute("SELECT COUNT(*) FROM offers WHERE status='falha'").fetchone()[0]
        return {'total':total,'scheduled':scheduled,'published':published,'pending':scheduled,'failed':failed}
