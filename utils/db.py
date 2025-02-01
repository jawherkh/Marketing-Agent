import logging
import sqlite3

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def create_database():
    try:
        conn = sqlite3.connect('marketing_agent.db')
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS contacts (
                id INTEGER PRIMARY KEY,
                name TEXT,
                linkedin TEXT
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS emails (
                id INTEGER PRIMARY KEY,
                contact_id INTEGER,
                email TEXT,
                FOREIGN KEY(contact_id) REFERENCES contacts(id)
            )
        ''')
        conn.commit()
        logging.info("Database and tables created successfully.")
    except sqlite3.Error as e:
        logging.error(f"Database error: {e}")
    finally:
        conn.close()

def save_contact_info(contact):
    try:
        conn = sqlite3.connect('marketing_agent.db')
        cursor = conn.cursor()
        for person in contact:
            cursor.execute('''
                INSERT INTO contacts (name, linkedin) VALUES (?, ?)
            ''', (person['name'], person['linkedin']))
        conn.commit()
        logging.info("Contact information saved successfully.")
    except sqlite3.Error as e:
        logging.error(f"Database error: {e}")
    finally:
        conn.close()

def save_emails(emails):
    try:
        conn = sqlite3.connect('marketing_agent.db')
        cursor = conn.cursor()
        for email in emails:
            cursor.execute('''
                INSERT INTO emails (contact_id, email) VALUES (?, ?)
            ''', (email['contact_id'], email['email']))
        conn.commit()
        logging.info("Emails saved successfully.")
    except sqlite3.Error as e:
        logging.error(f"Database error: {e}")
    finally:
        conn.close()