import sqlite3
import os
import datetime


class Database:
    def __init__(self):
        # On Android, use app's user data directory; on desktop use local dir
        try:
            from android.storage import app_storage_path  # noqa: F401
            storage = app_storage_path()
        except ImportError:
            storage = os.path.dirname(os.path.abspath(__file__))

        self.db_path = os.path.join(storage, "gym_database.db")
        self.conn = None
        self._connect()
        self._create_tables()

    def _connect(self):
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row

    def _create_tables(self):
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS customers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                age INTEGER,
                phone TEXT,
                subscription_date TEXT,
                subscription_period INTEGER,
                UNIQUE(name, phone)
            )
        ''')
        self.conn.commit()

    def add_customer(self, name, age, phone, subscription_date, subscription_period):
        try:
            self.conn.execute(
                'INSERT INTO customers (name, age, phone, subscription_date, subscription_period) VALUES (?,?,?,?,?)',
                (name, age, phone, subscription_date, subscription_period)
            )
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return "Customer with this name and phone already exists."
        except sqlite3.Error as e:
            return str(e)

    def update_customer(self, id, name, age, phone, subscription_date, subscription_period):
        try:
            self.conn.execute(
                'UPDATE customers SET name=?, age=?, phone=?, subscription_date=?, subscription_period=? WHERE id=?',
                (name, age, phone, subscription_date, subscription_period, id)
            )
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            return str(e)

    def delete_customer(self, id):
        try:
            self.conn.execute('DELETE FROM customers WHERE id=?', (id,))
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            return str(e)

    def get_all_customers(self):
        cursor = self.conn.execute('SELECT * FROM customers ORDER BY name')
        return [dict(row) for row in cursor.fetchall()]

    def get_customer_by_id(self, id):
        cursor = self.conn.execute('SELECT * FROM customers WHERE id=?', (id,))
        row = cursor.fetchone()
        return dict(row) if row else None

    def check_subscription_status(self, customer):
        try:
            sub_date = datetime.datetime.strptime(customer['subscription_date'], '%Y-%m-%d')
            expiry = sub_date + datetime.timedelta(days=customer['subscription_period'] * 30)
            return datetime.datetime.now() <= expiry
        except (ValueError, TypeError):
            return False

    def get_expiry_date(self, customer):
        sub_date = datetime.datetime.strptime(customer['subscription_date'], '%Y-%m-%d')
        return (sub_date + datetime.timedelta(days=customer['subscription_period'] * 30)).strftime('%Y-%m-%d')

    def get_active_subscriptions(self):
        return [c for c in self.get_all_customers() if self.check_subscription_status(c)]

    def get_expired_subscriptions(self):
        return [c for c in self.get_all_customers() if not self.check_subscription_status(c)]

    def export_to_csv(self, filepath, customers):
        import csv
        fieldnames = ['id', 'name', 'age', 'phone', 'subscription_date',
                      'subscription_period', 'expiry_date', 'status']
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for c in customers:
                row = dict(c)
                row['status'] = 'Active' if self.check_subscription_status(c) else 'Expired'
                row['expiry_date'] = self.get_expiry_date(c)
                writer.writerow({k: row.get(k, '') for k in fieldnames})
        return True

    def close(self):
        if self.conn:
            self.conn.close()
