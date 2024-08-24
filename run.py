from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify, get_flashed_messages
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Replace with a secure key
app.config['UPLOAD_FOLDER'] = 'uploads'  # Ensure this directory exists or create it

# A simple user database
users = {'Paulo': 'password123'}

# Store questions and answers
qa_data = {}
personal_data = {}

# Dictionary to store challenges
challenges_dict = {"Quadrangle": "quadrangle"}

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username in users and users[username] == password:
            session['username'] = username
            session['points'] = 0  # Reset points to 0 on login
            flash('Login successful!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password.', 'danger')
    
    # Retrieve flashed messages and clear them
    messages = get_flashed_messages(with_categories=True)
    return render_template('login.html', messages=messages)


@app.route('/home')
def home():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    username = session['username']
    points = session.get('points', 0)
    return render_template('home.html', username=username, points=points)

@app.route('/trivia', methods=['GET', 'POST'])
def trivia():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    username = session['username']
    
    if request.method == 'POST':
        question = request.form.get('question')
        answer = request.form.get('answer')
        
        if question and answer:
            if username not in qa_data:
                qa_data[username] = []
            qa_data[username].append((question, answer))
        
        major = request.form.get('major')
        introvert_extrovert = request.form.get('introvert-extrovert')
        
        if major or introvert_extrovert:
            personal_data[username] = {
                'major': major,
                'introvert_extrovert': introvert_extrovert
            }
    
    user_qa = qa_data.get(username, [])
    user_personal_data = personal_data.get(username, {})
    
    return render_template('trivia.html', username=username, qa_data=user_qa, personal_data=user_personal_data)

@app.route('/dashboard')
def dashboard():
    return "Welcome to the Dashboard!"

@app.route('/join_challenge')
def join_challenge():
    return redirect(url_for('trivia'))

@app.route('/add_challenge')
def add_challenge():
    return redirect(url_for('create'))

@app.route('/redirect_to_login')
def redirect_to_login():
    return redirect(url_for('trivia'))

@app.route('/create_challenge', methods=['POST'])
def create_challenge():
    challenge_name = request.form.get('name')
    if challenge_name:
        challenges_dict[challenge_name] = challenge_name
    return redirect(url_for('challenge'))

@app.route('/challenge')
def challenge():
    challenges = list(challenges_dict.keys())
    return render_template('challenge.html', challenges=challenges)

@app.route('/validate_challenge', methods=['POST'])
def validate_challenge():
    input_name = request.form.get('challenge_name')
    if input_name in challenges_dict:
        return jsonify({"status": "success", "message": "Challenge exists!"})
    else:
        return jsonify({"status": "error", "message": "Challenge does not exist."})

@app.route('/create')
def create():
    return render_template('create.html')

@app.route('/quadrangle')
def quadrangle():
    return render_template('quadrangle.html')

@app.route('/submit_quadrangle', methods=['POST'])
def submit_quadrangle():
    brick_count = request.form.get('brick_count')
    image_file = request.files.get('challenge_image')

    if not brick_count or not image_file:
        return jsonify({'success': False, 'message': 'Error: Please fill in all fields and upload an image.'})

    # Save the uploaded image
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
        
    filename = os.path.join(app.config['UPLOAD_FOLDER'], image_file.filename)
    image_file.save(filename)

    if brick_count == '69':
        if 'points' in session:
            session['points'] += 50
        else:
            session['points'] = 50
        return jsonify({'success': True, 'message': 'Correct! You have earned 50 points.'})
    else:
        return jsonify({'success': False, 'message': 'Incorrect. No points added.'})

@app.route('/friend')
def friend():
    return render_template('friend.html')

@app.route('/submit_quiz', methods=['POST'])
def submit_quiz():
    data = request.json
    points = data.get('points', 0)

    if 'points' in session:
        session['points'] += points
    else:
        session['points'] = points

    return jsonify({'message': f'Quiz submitted! Your current points: {session["points"]}'})

@app.route('/beckham')
def beckham():
    return render_template('beckham.html')

if __name__ == '__main__':
    app.run(debug=True)


