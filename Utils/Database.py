import sqlite3

DB_FILE = "estimations.db"


# ---------- CONNEXION ----------
def get_conn():
    conn = sqlite3.connect(DB_FILE, check_same_thread=False)
    conn.row_factory = sqlite3.Row  # Accès par noms de colonnes
    return conn


# ---------- INIT DB ----------
def init_db():
    conn = get_conn()
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS estimations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            numero TEXT,
            utilisateur TEXT,
            client TEXT,
            adresse TEXT,
            telephone TEXT,
            courriel TEXT,
            service TEXT,
            superficie REAL,
            description TEXT,
            montant REAL,
            taxes REAL,
            total REAL,
            date TEXT,
            status TEXT DEFAULT 'PENDING'
        )
    """)

    conn.commit()
    conn.close()


# ---------- INSERT ----------
def add_estimation(data):
    conn = get_conn()
    c = conn.cursor()

    c.execute("""
        INSERT INTO estimations (
            numero,
            utilisateur,
            client,
            adresse,
            telephone,
            courriel,
            service,
            superficie,
            description,
            montant,
            taxes,
            total,
            date,
            status
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        data.get("numero"),
        data.get("utilisateur"),
        data.get("client"),
        data.get("adresse"),
        data.get("telephone"),
        data.get("courriel"),
        data.get("service"),
        data.get("superficie"),
        data.get("description"),
        data.get("montant"),
        data.get("taxes"),
        data.get("total"),
        data.get("date_estimation"),
        "PENDING"
    ))

    conn.commit()
    conn.close()


# ---------- SELECT ----------
def get_estimations(status):
    conn = get_conn()
    c = conn.cursor()

    c.execute("""
        SELECT *
        FROM estimations
        WHERE status = ?
        ORDER BY date DESC
    """, (status,))

    results = c.fetchall()
    conn.close()

    return results


# ---------- UPDATE STATUS ----------
def update_status(estimation_id, new_status):
    conn = get_conn()
    c = conn.cursor()

    c.execute("""
        UPDATE estimations
        SET status = ?
        WHERE id = ?
    """, (
        new_status,
        estimation_id
    ))

    conn.commit()
    conn.close()


# ---------- DELETE ----------
def delete_estimation(estimation_id):
    conn = get_conn()
    c = conn.cursor()

    c.execute("""
        DELETE FROM estimations
        WHERE id = ?
    """, (estimation_id,))

    conn.commit()
    conn.close()
