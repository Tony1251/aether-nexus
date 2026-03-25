import sqlite3
import os
from cryptography.fernet import Fernet

class TenantManager:
    def __init__(self, db_path="tenants.db", key_path="secret.key"):
        self.db_path = db_path
        self.key_path = key_path
        self._init_key()
        self._init_db()

    def _init_key(self):
        if not os.path.exists(self.key_path):
            with open(self.key_path, "wb") as f: f.write(Fernet.generate_key())
        with open(self.key_path, "rb") as f: self.key = f.read()
        self.cipher = Fernet(self.key)

    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        conn.execute('''CREATE TABLE IF NOT EXISTS tenants
                        (id TEXT PRIMARY KEY, shop_name TEXT, shopify_token TEXT)''')
        conn.commit()
        conn.close()

    def get_tenant_token(self, tenant_id):
        conn = sqlite3.connect(self.db_path)
        row = conn.execute("SELECT shopify_token FROM tenants WHERE id=?", (tenant_id,)).fetchone()
        conn.close()
        return self.cipher.decrypt(row[0].encode()).decode() if row else None

    def add_tenant(self, tenant_id, shop_name, token):
        encrypted_token = self.cipher.encrypt(token.encode()).decode()
        conn = sqlite3.connect(self.db_path)
        conn.execute("INSERT OR REPLACE INTO tenants VALUES (?, ?, ?)", (tenant_id, shop_name, encrypted_token))
        conn.commit()
        conn.close()
