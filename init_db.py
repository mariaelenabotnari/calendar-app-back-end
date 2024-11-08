import sqlite3
import os
from datetime import datetime

# Define the path to the database
current_directory = os.path.dirname(os.path.abspath(__file__))
database_path = os.path.join(current_directory, 'EventLink.db')


# Function to initialize the database and create necessary tables
def init_db():
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    # Create 'loc' table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS loc (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            raion TEXT NOT NULL,
            oras TEXT NOT NULL,
            strada TEXT NOT NULL
        )
    ''')

    # Create 'organizator' table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS organizator (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            start_date TEXT NOT NULL,
            nume TEXT NOT NULL,
            domeniu TEXT NOT NULL
        )
    ''')

    # Create 'eveniment' table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS eveniment (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titlu TEXT NOT NULL,
            descriere TEXT NOT NULL,
            data TEXT NOT NULL,
            ora TEXT NOT NULL,
            tip TEXT NOT NULL,
            organizator_id INTEGER,
            loc_id INTEGER,
            FOREIGN KEY (organizator_id) REFERENCES organizator(id),
            FOREIGN KEY (loc_id) REFERENCES loc(id)
        )
    ''')

    # Commit changes and close connection
    conn.commit()
    conn.close()


# Function to insert initial event data
def insert_initial_data():
    events = [
        {'raion': 'Râșcani', 'oras': 'Chișinău', 'strada': 'Strada Tighina 25',
         'titlu': 'Conferința Tehnologică 2024',
         'descriere': 'Prezentarea celor mai recente inovații din domeniul tehnologic.',
         'data': '2024-09-20', 'ora': '10:00 - 17:00', 'tip': 'obligatoriu', 'organizator': 'Tech Moldova',
         'domeniu': 'Tehnologie'},
        {'raion': 'Botanica', 'oras': 'Chișinău', 'strada': 'Strada Dacia 41',
         'titlu': 'Atelier de Robotică Avansată',
         'descriere': 'Workshop dedicat construcției și programării roboților.',
         'data': '2024-09-22', 'ora': '12:00 - 18:00', 'tip': 'opțional', 'organizator': 'Robotica Club',
         'domeniu': 'Robotică'},
        {'raion': 'Buiucani', 'oras': 'Chișinău', 'strada': 'Strada Alba Iulia 100',
         'titlu': 'Prezentare Proiecte Software',
         'descriere': 'Studenții își prezintă proiectele de final în domeniul software.',
         'data': '2024-09-25', 'ora': '09:30 - 14:30', 'tip': 'obligatoriu',
         'organizator': 'Facultatea de Informatică UTM', 'domeniu': 'Software'},
        {'raion': 'Telecentru', 'oras': 'Chișinău', 'strada': 'Strada Miorița 27',
         'titlu': 'Ziua Porților Deschise la UTM', 'descriere': 'Eveniment de promovare a facultăților UTM.',
         'data': '2024-09-30', 'ora': '09:00 - 12:00', 'tip': 'opțional',
         'organizator': 'Universitatea Tehnică din Moldova', 'domeniu': 'Educație'},
        {'raion': 'Ciocana', 'oras': 'Chișinău', 'strada': 'Strada Meșterul Manole 3',
         'titlu': 'Târg de Inovații Tehnologice',
         'descriere': 'Expoziție de produse și servicii inovatoare dezvoltate în Moldova.',
         'data': '2024-10-05', 'ora': '10:00 - 16:00', 'tip': 'opțional', 'organizator': 'Inovație Moldova',
         'domeniu': 'Inovație'},
        {'raion': 'Centru', 'oras': 'Chișinău', 'strada': 'Strada Mitropolit Dosoftei 64',
         'titlu': 'Seminar Securitate Cibernetică',
         'descriere': 'Discuții privind riscurile și soluțiile în securitatea cibernetică.',
         'data': '2024-10-10', 'ora': '14:00 - 18:00', 'tip': 'obligatoriu', 'organizator': 'CyberSafe Moldova',
         'domeniu': 'Securitate Cibernetică'},
        {'raion': 'Râșcani', 'oras': 'Chișinău', 'strada': 'Strada Alecu Russo 38',
         'titlu': 'Simpozion Tehnologie și Mediu',
         'descriere': 'Eveniment dedicat impactului tehnologiei asupra mediului.',
         'data': '2024-10-12', 'ora': '11:00 - 15:00', 'tip': 'opțional', 'organizator': 'EcoTech Moldova',
         'domeniu': 'Mediu și Tehnologie'},
        {'raion': 'Botanica', 'oras': 'Chișinău', 'strada': 'Strada Sarmizegetusa 12',
         'titlu': 'Hackathon Antreprenorial', 'descriere': 'Eveniment pentru dezvoltarea startup-urilor în tehnologie.',
         'data': '2024-10-15', 'ora': '09:00 - 17:00', 'tip': 'opțional', 'organizator': 'Startup Moldova',
         'domeniu': 'Antreprenoriat'},
        {'raion': 'Buiucani', 'oras': 'Chișinău', 'strada': 'Strada Ion Creangă 45',
         'titlu': 'Conferința Inovații IT', 'descriere': 'Conferință despre cele mai noi tehnologii din industria IT.',
         'data': '2024-10-18', 'ora': '09:00 - 16:00', 'tip': 'obligatoriu', 'organizator': 'IT Hub Chișinău',
         'domeniu': 'Tehnologie IT'},
        {'raion': 'Telecentru', 'oras': 'Chișinău', 'strada': 'Strada Gh. Asachi 11',
         'titlu': 'Workshop UI/UX Design', 'descriere': 'Atelier pentru crearea interfețelor intuitive și atractive.',
         'data': '2024-10-20', 'ora': '10:00 - 13:00', 'tip': 'opțional', 'organizator': 'Designers Guild',
         'domeniu': 'Design UI/UX'},
        {'raion': 'Ciocana', 'oras': 'Chișinău', 'strada': 'Strada Albișoara 99',
         'titlu': 'Prezentare Tehnologie Blockchain',
         'descriere': 'Prezentare despre viitorul tehnologiei blockchain și impactul său.',
         'data': '2024-10-25', 'ora': '14:00 - 17:00', 'tip': 'opțional', 'organizator': 'Blockchain Hub Moldova',
         'domeniu': 'Blockchain'},
        {'raion': 'Râșcani', 'oras': 'Chișinău', 'strada': 'Strada Kiev 25',
         'titlu': 'Expoziție Tehnologii 5G', 'descriere': 'Expoziție de soluții tehnologice bazate pe rețelele 5G.',
         'data': '2024-10-30', 'ora': '09:00 - 15:00', 'tip': 'opțional', 'organizator': '5G Moldova',
         'domeniu': 'Tehnologie 5G'}
    ]

    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    for event in events:
        # Insert location
        cursor.execute('''INSERT INTO loc (raion, oras, strada) VALUES (?, ?, ?)''',
                       (event['raion'], event['oras'], event['strada']))
        loc_id = cursor.lastrowid

        # Check if the organizer exists
        cursor.execute('''SELECT id FROM organizator WHERE nume = ?''', (event['organizator'],))
        organizer_result = cursor.fetchone()

        if organizer_result:
            organizator_id = organizer_result[0]
        else:
            # Insert new organizer with correct domain
            cursor.execute('''INSERT INTO organizator (start_date, nume, domeniu) VALUES (?, ?, ?)''',
                           (datetime.now().strftime('%Y-%m-%d'), event['organizator'], event['domeniu']))
            organizator_id = cursor.lastrowid

        # Insert event
        cursor.execute('''INSERT INTO eveniment (titlu, descriere, data, ora, tip, organizator_id, loc_id)
                          VALUES (?, ?, ?, ?, ?, ?, ?)''',
                       (event['titlu'], event['descriere'], event['data'], event['ora'], event['tip'], organizator_id,
                        loc_id))

    conn.commit()
    conn.close()


# Main script to initialize database and insert data
if __name__ == "__main__":
    init_db()  # Create tables if not exist
    insert_initial_data()  # Insert initial event data
