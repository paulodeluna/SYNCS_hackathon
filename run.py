from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Replace with a secure key

# A simple user database
users = {'testuser': 'password123'}

# Store questions and answers
qa_data = {}
personal_data = {}

# Dictionary to store challenges
challenges_dict = {"quadrangle": "quadrangle"}

@app.route('/')
def index():
    # Redirect to login page on startup
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Simple authentication logic
        if username in users and users[username] == password:
            session['username'] = username
            flash('Login successful!', 'success')
            return redirect(url_for('trivia'))
        else:
            flash('Invalid username or password.', 'danger')
    
    return render_template('login.html')

@app.route('/trivia', methods=['GET', 'POST'])
def trivia():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    username = session['username']
    
    if request.method == 'POST':
        question = request.form.get('question')
        answer = request.form.get('answer')
        
        # Handling custom questions
        if question and answer:
            if username not in qa_data:
                qa_data[username] = []
            qa_data[username].append((question, answer))
        
        # Handling personal questions
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

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/join_challenge')
def join_challenge():
    return redirect(url_for('challenge'))

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
    # Pass only the keys of the challenges_dict to the template
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

if __name__ == '__main__':
    app.run(debug=True)


