from flask import Flask, render_template, request, redirect, url_for, flash, session

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Replace with a secure key

# A simple user database
users = {'testuser': 'password123'}

# Store questions and answers
qa_data = {}

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Simple authentication logic
        if username in users and users[username] == password:
            session['username'] = username
            flash('Login successful!', 'success')
            return redirect(url_for('login_page'))
        else:
            flash('Invalid username or password.', 'danger')
    
    return render_template('login.html')

@app.route('/login_page', methods=['GET', 'POST'])
def login_page():
    if 'username' not in session:
        return redirect(url_for('home'))
    
    username = session['username']
    
    if request.method == 'POST':
        question = request.form['question']
        answer = request.form['answer']
        
        if username not in qa_data:
            qa_data[username] = []
        qa_data[username].append((question, answer))
    
    user_qa = qa_data.get(username, [])
    
    return render_template('login_page.html', username=username, qa_data=user_qa)

@app.route('/dashboard')
def dashboard():
    return "Welcome to the Dashboard!"

if __name__ == '__main__':
    app.run(debug=True)


