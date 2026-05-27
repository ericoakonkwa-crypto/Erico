#!/usr/bin/env python3
"""
Math Quiz Game - Web App with Flask
A complete web-based math quiz game with user authentication and competition system
"""

from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import json
import os
from functools import wraps

# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'math_quiz_secret_key_2026'

# Database files
USERS_FILE = 'users.json'
COMPETITIONS_FILE = 'competitions.json'

# ==================== Helper Functions ====================

def load_users():
    """Load users from JSON"""
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_users(users):
    """Save users to JSON"""
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, indent=2)

def load_competitions():
    """Load competition data"""
    if os.path.exists(COMPETITIONS_FILE):
        with open(COMPETITIONS_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_competitions(data):
    """Save competition data"""
    with open(COMPETITIONS_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def login_required(f):
    """Decorator to require login"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# ==================== Routes ====================

@app.route('/')
def index():
    """Home page"""
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration"""
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username', '').strip()
        email = data.get('email', '').strip()
        password = data.get('password', '')
        
        users = load_users()
        
        if username in users:
            return jsonify({'success': False, 'message': 'Username already exists'}), 400
        
        if any(u['email'] == email for u in users.values()):
            return jsonify({'success': False, 'message': 'Email already registered'}), 400
        
        users[username] = {
            'email': email,
            'password': generate_password_hash(password),
            'total_score': 0,
            'scores': [],
            'registered_date': datetime.now().isoformat()
        }
        save_users(users)
        
        return jsonify({'success': True, 'message': 'Registration successful! Please login.'})
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username', '').strip()
        password = data.get('password', '')
        
        users = load_users()
        
        if username in users and check_password_hash(users[username]['password'], password):
            session['user_id'] = username
            return jsonify({'success': True, 'message': 'Login successful!'})
        
        return jsonify({'success': False, 'message': 'Invalid credentials'}), 401
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    """User logout"""
    session.clear()
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    """User dashboard"""
    user_id = session['user_id']
    users = load_users()
    user = users[user_id]
    
    total_score = user['total_score']
    quizzes_completed = len(user['scores'])
    accuracy = 0
    
    if quizzes_completed > 0:
        correct = sum(s['score'] for s in user['scores'])
        total_questions = sum(s['total_questions'] for s in user['scores'])
        accuracy = (correct / total_questions * 100) if total_questions > 0 else 0
    
    return render_template('dashboard.html', 
                         username=user_id,
                         total_score=total_score,
                         quizzes_completed=quizzes_completed,
                         accuracy=accuracy)

@app.route('/quiz')
@login_required
def quiz():
    """Quiz selection page"""
    return render_template('quiz.html')

@app.route('/api/question', methods=['POST'])
@login_required
def get_question():
    """Get a random question"""
    from question_generator import QuestionGenerator
    
    data = request.get_json()
    topic = data.get('topic')
    difficulty = data.get('difficulty')
    
    generator = QuestionGenerator()
    question = generator.generate_question(topic, difficulty)
    
    return jsonify({
        'question': question['question'],
        'answer': question['answer'],
        'topic': topic,
        'difficulty': difficulty
    })

@app.route('/api/submit-answer', methods=['POST'])
@login_required
def submit_answer():
    """Submit quiz answer and save score"""
    user_id = session['user_id']
    data = request.get_json()
    
    users = load_users()
    user = users[user_id]
    
    # Save score
    user['scores'].append({
        'topic': data['topic'],
        'difficulty': data['difficulty'],
        'score': data['score'],
        'total_questions': data['total_questions'],
        'timestamp': datetime.now().isoformat()
    })
    
    # Update total score with multiplier
    multiplier = {'easy': 1, 'medium': 2, 'hard': 3}
    mult = multiplier.get(data['difficulty'], 1)
    user['total_score'] += data['score'] * mult
    
    save_users(users)
    
    # Check if it's competition day and update rankings
    today = datetime.now()
    if today.month == 12 and today.day == 1:
        update_competition_rankings()
    
    return jsonify({'success': True, 'message': 'Score saved!'})

@app.route('/leaderboard')
def leaderboard():
    """Display leaderboard"""
    users = load_users()
    
    # Sort by total score
    sorted_users = sorted(
        [(uid, u['total_score']) for uid, u in users.items()],
        key=lambda x: x[1],
        reverse=True
    )
    
    leaderboard_data = [
        {'rank': i+1, 'username': uid, 'score': score}
        for i, (uid, score) in enumerate(sorted_users[:100])
    ]
    
    return render_template('leaderboard.html', leaderboard=leaderboard_data)

@app.route('/report-card')
@login_required
def report_card():
    """Display user's report card"""
    user_id = session['user_id']
    users = load_users()
    user = users[user_id]
    
    # Calculate statistics
    quizzes = user['scores']
    total_correct = sum(s['score'] for s in quizzes)
    total_questions = sum(s['total_questions'] for s in quizzes)
    accuracy = (total_correct / total_questions * 100) if total_questions > 0 else 0
    
    # Get competition ranking
    sorted_users = sorted(
        [(uid, u['total_score']) for uid, u in users.items()],
        key=lambda x: x[1],
        reverse=True
    )
    
    rank = next((i+1 for i, (uid, _) in enumerate(sorted_users) if uid == user_id), None)
    
    stats = {
        'username': user_id,
        'email': user['email'],
        'total_score': user['total_score'],
        'quizzes_completed': len(quizzes),
        'accuracy': round(accuracy, 2),
        'rank': rank,
        'status': get_rank_status(rank) if rank else 'Participant'
    }
    
    return render_template('report_card.html', stats=stats)

def get_rank_status(rank):
    """Get rank status"""
    if rank == 1:
        return 'GOLD WINNER - 1st Place'
    elif rank == 2:
        return 'SILVER WINNER - 2nd Place'
    elif rank == 3:
        return 'BRONZE WINNER - 3rd Place'
    elif rank and rank <= 10:
        return f'WINNER - Top {rank}'
    return 'Participant'

def update_competition_rankings():
    """Update competition rankings on Dec 1st"""
    users = load_users()
    competitions = load_competitions()
    
    today = datetime.now().strftime('%Y-12-01')
    
    sorted_users = sorted(
        [(uid, u['total_score'], u['email']) for uid, u in users.items()],
        key=lambda x: x[1],
        reverse=True
    )
    
    competition_winners = []
    for rank, (uid, score, email) in enumerate(sorted_users[:10], 1):
        competition_winners.append({
            'rank': rank,
            'username': uid,
            'email': email,
            'score': score,
            'status': get_rank_status(rank),
            'date': today
        })
    
    competitions[today] = competition_winners
    save_competitions(competitions)

@app.route('/api/hint', methods=['POST'])
@login_required
def get_hint():
    """Get a hint from Mr. Math"""
    from teacher import MrMath
    
    data = request.get_json()
    question_obj = {
        'question': data['question']
    }
    
    teacher = MrMath()
    hint = teacher.provide_hint(question_obj)
    
    return jsonify({'hint': hint})

# ==================== Error Handlers ====================

@app.errorhandler(404)
def not_found(error):
    """404 error handler"""
    return render_template('error.html', error='Page not found'), 404

@app.errorhandler(500)
def server_error(error):
    """500 error handler"""
    return render_template('error.html', error='Server error'), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
