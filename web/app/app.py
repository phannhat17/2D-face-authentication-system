from flask import Flask, request, render_template, redirect, url_for, send_from_directory
import sqlite3
import shutil
import os
from verify import verify
from face_extract import process_image

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('users.db')
    conn.row_factory = sqlite3.Row  # This enables name-based access to columns
    return conn

@app.route('/images/<int:user_id>/<path:filename>')
def serve_image(user_id, filename):
    image_path = f"images/{user_id}/anchor/"
    return send_from_directory(image_path, filename)

@app.route('/')
def index():
    conn = get_db_connection()
    search_query = request.args.get('search')

    if search_query and search_query.isdigit():
        users = conn.execute('SELECT * FROM users WHERE id = ?', (int(search_query),)).fetchall()
    else:
        users = conn.execute('SELECT * FROM users').fetchall()

    conn.close()
    return render_template('dashboard.html', users=users)

@app.route('/delete_user/<int:id>', methods=['POST'])
def delete_user(id):
    if id == 1:
        return "Deleting the admin user is not allowed", 403

    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE id = ?', (id,)).fetchone()
    
    if user:
        image_path = image_path = f"images/{id}/"
        if os.path.exists(image_path):
            shutil.rmtree(image_path)

        conn.execute('DELETE FROM users WHERE id = ?', (id,))
        conn.commit()

    conn.close()
    return redirect(url_for('index'))

@app.route('/upload_image/<int:id>', methods=['POST'])
def upload_image(id):
    if 'user_images' in request.files:
        # Create directories if they don't exist
        upload_path = f"images/{id}/anchor/"
        processed_path = f"images/{id}/processed/"
        if not os.path.exists(upload_path):
            os.makedirs(upload_path)
        if not os.path.exists(processed_path):
            os.makedirs(processed_path)

        # Loop through each file in the request
        for file in request.files.getlist('user_images'):
            if file.filename != '':
                # Save the original file
                file_path = os.path.join(upload_path, file.filename)
                file.save(file_path)

                # Process and save the file
                processed_file_path = os.path.join(processed_path, file.filename)
                process_image(file_path, processed_file_path)

    return redirect(url_for('index'))


@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        user_id = request.form['id']
        name = request.form['name']
        image_path = f"images/{user_id}/anchor/"

        if not os.path.exists(image_path):
            os.makedirs(image_path)

        conn = get_db_connection()
        conn.execute('INSERT INTO users (id, name, image_path) VALUES (?, ?, ?)', (user_id, name, image_path))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    return render_template('add_user.html')

@app.route('/edit_user/<int:id>', methods=['GET', 'POST'])
def edit_user(id):
    if id == 1:
        return "Editing the admin user is not allowed", 403

    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE id = ?', (id,)).fetchone()

    if request.method == 'POST':
        name = request.form['name']
        image_path = request.form['image_path']

        conn.execute('UPDATE users SET name = ?, image_path = ? WHERE id = ?', (name, image_path, id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    return render_template('edit_user.html', user=user)

@app.route('/capture_image/<int:id>')
def capture_image(id):
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE id = ?', (id,)).fetchone()
    conn.close()

    if user:
        valid_path = f"images/{id}/anchor/"
        image_files = [f for f in os.listdir(valid_path) if os.path.isfile(os.path.join(valid_path, f))]
        first_image = image_files[0] if image_files else None
        return render_template('capture_image.html', user=user, first_image=first_image)
    else:
        return "User not found", 404

@app.route('/save_image', methods=['POST'])
def save_image():
    user_id = request.form['user_id']
    photo = request.files['photo']
    image_path = f"images/{user_id}/verify.png"

    if not os.path.exists(f"images/{user_id}"):
        os.makedirs(f"images/{user_id}")

    photo.save(image_path)
    process_image(image_path, image_path)
    valid_path = f"images/{user_id}/processed/"
    verified = verify(valid_path, image_path, 0.5, 0.5)
    
    return {"status": "success", "image_path": image_path, "verified": verified}


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
