import sqlite3

DB_FILE = "estimations.db"


def get_conn():
    return sqlite3.connect(DB_FILE, check_same_thread=False)


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


def add_estimation(data):
    conn = get_conn()
    c = conn.cursor()

    c.execute("""
        INSERT INTO estimations (
            numero, utilisateur, client, adresse, telephone, courriel,
            service, superficie, description, montant, taxes, total, date, status
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        data["numero"], data["utilisateur"], data["client"], data["adresse"],
        data["telephone"], data["courriel"], data["service"], data["superficie"],
        data["description"], data["montant"], data["taxes"], data["total"],
        data["date_estimation"], "PENDING"
    ))

    conn.commit()
    conn.close()


def get_estimations(status):
    conn = get_conn()
    c = conn.cursor()

    c.execute("SELECT * FROM estimations WHERE status=?", (status,))
    results = c.fetchall()

    conn.close()
    return results


def update_status(estimation_id, new_status):
    conn = get_conn()
    c = conn.cursor()

    c.execute("""
        UPDATE estimations
        SET status = ?
        WHERE id = ?
    """, (new_status, estimation_id))

    conn.commit()
    conn.close()
