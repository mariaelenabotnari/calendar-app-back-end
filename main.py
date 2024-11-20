import flask
from flask import Flask, render_template, request, redirect, url_for, jsonify, abort
from auth_database import verify_user

from validate import validate_event_data
from datetime import datetime, timedelta
import sqlite3
import os
from flask_cors import CORS

from flask import session

app = Flask(__name__)
current_directory = os.path.dirname(os.path.abspath(__file__))
database_path = os.path.join(current_directory, 'EventLink.db')

# Proper CORS configuration to allow requests from any origin
# Update the CORS configuration to include PATCH
CORS(app, resources={
    r"/*": {"origins": "*", "methods": ["GET", "POST", "PUT", "DELETE", "PATCH"], "headers": ["Content-Type"]}})


def get_db_connection():
    conn = sqlite3.connect(database_path, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/')
def admin():
    return 'First page'


# Handle the add event route and CORS preflight (OPTIONS) request
@app.route('/events/add', methods=['POST', 'OPTIONS'])
def add_event():
    if request.method == 'OPTIONS':
        # CORS preflight response
        return jsonify({'status': 'success'}), 200

    data = request.get_json()  # Get JSON data from the request body

    Titlu = data.get('titlu')
    Descriere = data.get('descriere')
    Data = data.get('data')
    Ora = data.get('ora')
    Tip = data.get('tip')

    Raion = data.get('raion')
    Oras = data.get('oras')
    Strada = data.get('strada')

    Nume = data.get('nume')
    Domeniu = data.get('domeniu')

    is_valid, message = validate_event_data(data)
    if not is_valid:
        return jsonify({'status': 'error', 'errors': message}), 400

    try:
        conn = get_db_connection()
        cur = conn.cursor()

        try:
            cur.execute("INSERT INTO loc (raion, oras, strada) VALUES (?, ?, ?)", (Raion, Oras, Strada))
            loc_id = cur.lastrowid
        except sqlite3.Error as e:
            conn.rollback()
            return jsonify({'status': 'error', 'message': 'Failed to insert location data', 'error': str(e)}), 500

        time = datetime.now().strftime('%Y-%m-%d')

        try:
            cur.execute("INSERT INTO organizator (start_date, nume, domeniu) VALUES (?, ?, ?)", (time, Nume, Domeniu))
            organizator_id = cur.lastrowid
        except sqlite3.Error as e:
            conn.rollback()
            return jsonify({'status': 'error', 'message': 'Failed to insert organizer data', 'error': str(e)}), 500

        try:
            cur.execute(
                "INSERT INTO eveniment (titlu, descriere, data, ora, tip, organizator_id, loc_id) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (Titlu, Descriere, Data, Ora, Tip, organizator_id, loc_id)
            )
        except sqlite3.Error as e:
            conn.rollback()
            return jsonify({'status': 'error', 'message': 'Failed to insert event data', 'error': str(e)}), 500

        conn.commit()


    except Exception as e:
        return jsonify({'status': 'error', 'message': 'Failed to process the request', 'error': str(e)}), 500


    finally:
        conn.close()

    return jsonify({
        'status': 'success',
        'message': 'Event added successfully',
        'data': {
            'titlu': Titlu,
            'descriere': Descriere,
            'data': Data,
            'ora': Ora,
            'tip': Tip,
            'raion': Raion,
            'oras': Oras,
            'strada': Strada,
            'nume': Nume,
            'domeniu': Domeniu
        }
    }), 200


@app.route('/events/<int:id>', methods=['DELETE'])
def delete_event(id):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM eveniment WHERE id = ?", (id,))
        if cur.rowcount == 0:
            abort(404, description="Event not found")
        conn.commit()
        return jsonify({'status': 'success', 'message': 'Event deleted successfully'}), 200
    except sqlite3.Error as e:
        conn.rollback()
        return jsonify({'status': 'error', 'message': 'Failed to delete event', 'error': str(e)}), 500
    finally:
        conn.close()


@app.route('/events/<int:id>', methods=['GET'])
def display_event_by_id(id):
    try:
        conn = get_db_connection()
        with conn:
            cur = conn.cursor()

            cur.execute('''
               SELECT eveniment.id, eveniment.titlu, eveniment.descriere, eveniment.data, eveniment.ora, eveniment.tip,
                      loc.raion, loc.oras, loc.strada,
                      organizator.nume, organizator.domeniu
               FROM eveniment
               JOIN loc ON eveniment.loc_id = loc.id
               JOIN organizator ON eveniment.organizator_id = organizator.id
               WHERE eveniment.id = ?
           ''', (id,))

            event = cur.fetchone()

            if event is None:
                abort(404, description="Event not found")

            return jsonify({
                'titlu': event[1],
                'descriere': event[2],
                'data': event[3],
                'ora': event[4],
                'tip': event[5],
                'loc': {
                    'raion': event[6],
                    'oras': event[7],
                    'strada': event[8]
                },
                'organizator': {
                    'nume': event[9],
                    'domeniu': event[10]
                }
            })


    except sqlite3.Error as e:
        return jsonify({'status': 'error', 'message': 'Failed to fetch event', 'error': str(e)}), 500


@app.route('/events/next_two', methods=['GET'])
def display_next_two_events():
    try:
        conn = get_db_connection()
        with conn:
            cur = conn.cursor()
            today = datetime.now().strftime('%Y-%m-%d')

            cur.execute('''
               SELECT eveniment.id, eveniment.titlu, eveniment.descriere, eveniment.data, eveniment.ora, eveniment.tip,
                      loc.raion, loc.oras, loc.strada,
                      organizator.nume, organizator.domeniu
               FROM eveniment
               JOIN loc ON eveniment.loc_id = loc.id
               JOIN organizator ON eveniment.organizator_id = organizator.id
               WHERE eveniment.data >= ?
               ORDER BY eveniment.data, eveniment.ora
               LIMIT 2
           ''', (today,))

            events = cur.fetchall()

            events_list = [{
                'id': event[0],
                'titlu': event[1],
                'descriere': event[2],
                'data': event[3],
                'ora': event[4],
                'tip': event[5],
                'loc': {
                    'raion': event[6],
                    'oras': event[7],
                    'strada': event[8]
                },
                'organizator': {
                    'nume': event[9],
                    'domeniu': event[10]
                }
            } for event in events]


    except sqlite3.Error as e:
        return jsonify({'status': 'error', 'message': 'Failed to fetch events', 'error': str(e)}), 500

    return jsonify(events_list)


@app.route('/events/current_month', methods=['GET'])
def display_events_current_month():
    try:
        conn = get_db_connection()
        with conn:
            cur = conn.cursor()

            today = datetime.now()
            first_day = today.replace(day=1)
            last_day = (today.replace(day=28) + timedelta(days=4)).replace(day=1) - timedelta(days=1)

            cur.execute('''
               SELECT eveniment.id, eveniment.titlu, eveniment.descriere, eveniment.data, eveniment.ora, eveniment.tip,
                      loc.raion, loc.oras, loc.strada,
                      organizator.nume, organizator.domeniu
               FROM eveniment
               JOIN loc ON eveniment.loc_id = loc.id
               JOIN organizator ON eveniment.organizator_id = organizator.id
               WHERE eveniment.data BETWEEN ? AND ?
           ''', (first_day.strftime('%Y-%m-%d'), last_day.strftime('%Y-%m-%d')))

            events = cur.fetchall()

            events_list = [{
                'id': event[0],
                'titlu': event[1],
                'descriere': event[2],
                'data': event[3],
                'ora': event[4],
                'tip': event[5],
                'loc': {
                    'raion': event[6],
                    'oras': event[7],
                    'strada': event[8]
                },
                'organizator': {
                    'nume': event[9],
                    'domeniu': event[10]
                }
            } for event in events]


    except sqlite3.Error as e:
        return jsonify({'status': 'error', 'message': 'Failed to fetch events', 'error': str(e)}), 500

    return jsonify(events_list)


@app.route('/events/interval', methods=['GET'])
def display_events_in_interval():
    try:
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')

        if not start_date or not end_date:
            return jsonify({'status': 'error', 'message': 'Start and end dates are required'}), 400

        try:
            start_date_obj = datetime.strptime(start_date, '%Y-%m-%d')
            end_date_obj = datetime.strptime(end_date, '%Y-%m-%d')
        except ValueError:
            return jsonify({'status': 'error', 'message': 'Invalid date format. Use YYYY-MM-DD'}), 400

        conn = get_db_connection()
        with conn:
            cur = conn.cursor()

            cur.execute('''
               SELECT eveniment.id, eveniment.titlu, eveniment.descriere, eveniment.data, eveniment.ora, eveniment.tip,
                      loc.raion, loc.oras, loc.strada,
                      organizator.nume, organizator.domeniu
               FROM eveniment
               JOIN loc ON eveniment.loc_id = loc.id
               JOIN organizator ON eveniment.organizator_id = organizator.id
               WHERE eveniment.data BETWEEN ? AND ?
           ''', (start_date_obj.strftime('%Y-%m-%d'), end_date_obj.strftime('%Y-%m-%d')))

            events = cur.fetchall()

            events_list = [{
                'id': event[0],
                'titlu': event[1],
                'descriere': event[2],
                'data': event[3],
                'ora': event[4],
                'tip': event[5],
                'loc': {
                    'raion': event[6],
                    'oras': event[7],
                    'strada': event[8]
                },
                'organizator': {
                    'nume': event[9],
                    'domeniu': event[10]
                }
            } for event in events]


    except sqlite3.Error as e:
        return jsonify({'status': 'error', 'message': 'Failed to fetch events', 'error': str(e)}), 500

    return jsonify(events_list)


@app.route('/events/patch/<int:id>', methods=['PATCH'])
def update_event(id):
    data = request.json
    try:
        conn = get_db_connection()
        with conn:
            cur = conn.cursor()

            # Fetch the current event data
            cur.execute('''
               SELECT eveniment.id, eveniment.loc_id, eveniment.organizator_id
               FROM eveniment
               WHERE id = ?
           ''', (id,))
            event = cur.fetchone()

            if event is None:
                return jsonify({'status': 'error', 'message': 'Event not found'}), 404

            eveniment_id = event['id']
            loc_id = event['loc_id']
            organizator_id = event['organizator_id']

            # Update event information if provided
            Titlu = data.get('titlu')
            Descriere = data.get('descriere')
            Data = data.get('data')
            Ora = data.get('ora')
            Tip = data.get('tip')

            Raion = data.get('raion')
            Oras = data.get('oras')
            Strada = data.get('strada')

            Nume = data.get('nume')
            Domeniu = data.get('domeniu')

            # Validate the data (assuming you have the validate_event_data function)
            is_valid, message = validate_event_data(data)
            if not is_valid:
                return jsonify({'status': 'error', 'errors': message}), 400

            # Update the location if any location-related fields are provided
            if Raion or Oras or Strada:
                cur.execute('''
                   UPDATE loc
                   SET raion = COALESCE(?, raion),
                       oras = COALESCE(?, oras),
                       strada = COALESCE(?, strada)
                   WHERE id = ?
               ''', (Raion, Oras, Strada, loc_id))

            # Update the organizer if any organizer-related fields are provided
            if Nume or Domeniu:
                cur.execute('''
                   UPDATE organizator
                   SET nume = COALESCE(?, nume),
                       domeniu = COALESCE(?, domeniu)
                   WHERE id = ?
               ''', (Nume, Domeniu, organizator_id))

            # Update the event itself
            if Titlu or Descriere or Data or Ora or Tip:
                cur.execute('''
                   UPDATE eveniment
                   SET titlu = COALESCE(?, titlu),
                       descriere = COALESCE(?, descriere),
                       data = COALESCE(?, data),
                       ora = COALESCE(?, ora),
                       tip = COALESCE(?, tip)
                   WHERE id = ?
               ''', (Titlu, Descriere, Data, Ora, Tip, eveniment_id))

        conn.commit()
        return jsonify({'status': 'success', 'message': 'Event updated successfully'}), 200


    except sqlite3.Error as e:
        conn.rollback()
        return jsonify({'status': 'error', 'message': 'Failed to update event', 'error': str(e)}), 500
    finally:
        conn.close()


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'status': 'error', 'message': 'Email and password are required'}), 400

    # Verify the user's credentials
    if verify_user(email, password):
        return jsonify({'status': 'success', 'message': 'Login successful'}), 200
    else:
        return jsonify({'status': 'error', 'message': 'Invalid email or password'}), 401


def setup_favorites_table():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS favorites (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_id INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (event_id) REFERENCES eveniment (id) ON DELETE CASCADE,
            UNIQUE(event_id)
        )
    ''')
    conn.commit()
    conn.close()


@app.route('/favorites', methods=['GET'])
def get_favorites():
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute('''
            SELECT e.id, e.titlu, e.descriere, e.data, e.ora, e.tip,
                   l.raion, l.oras, l.strada,
                   o.nume, o.domeniu
            FROM favorites f
            JOIN eveniment e ON f.event_id = e.id
            JOIN loc l ON e.loc_id = l.id
            JOIN organizator o ON e.organizator_id = o.id
        ''')

        favorites = cur.fetchall()

        favorites_list = [{
            'id': fav[0],
            'titlu': fav[1],
            'descriere': fav[2],
            'data': fav[3],
            'ora': fav[4],
            'tip': fav[5],
            'loc': {
                'raion': fav[6],
                'oras': fav[7],
                'strada': fav[8]
            },
            'organizator': {
                'nume': fav[9],
                'domeniu': fav[10]
            }
        } for fav in favorites]

        return jsonify(favorites_list)

    except sqlite3.Error as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500
    finally:
        conn.close()


@app.route('/favorites/toggle', methods=['POST'])
def toggle_favorite():
    data = request.get_json()
    event_id = data.get('event_id')

    if not event_id:
        return jsonify({'status': 'error', 'message': 'Event ID is required'}), 400

    try:
        conn = get_db_connection()
        cur = conn.cursor()

        # Check if favorite exists
        cur.execute('SELECT id FROM favorites WHERE event_id = ?', (event_id,))
        existing = cur.fetchone()

        if existing:
            # Remove favorite
            cur.execute('DELETE FROM favorites WHERE event_id = ?', (event_id,))
            status = 'removed'
        else:
            # Add favorite
            cur.execute('INSERT INTO favorites (event_id) VALUES (?)', (event_id,))
            status = 'added'

        conn.commit()
        return jsonify({'status': 'success', 'message': f'Favorite {status}'}), 200

    except sqlite3.Error as e:
        conn.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500
    finally:
        conn.close()


if __name__ == '__main__':
    setup_favorites_table()
    app.run(debug=True)
