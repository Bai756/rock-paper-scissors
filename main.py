from flask import Flask, render_template, session, request, redirect, url_for, jsonify
import secrets

app = Flask(__name__)
app.secret_key="super secret key because I don't care"

choices = ['Rock', 'Paper', 'Scissors']
leaderboard = {}
score_board = {}

@app.route('/')
def index():
    if 'name' not in session:
        return redirect(url_for('choose_name'))
    if 'score' not in session:
        session['score'] = 0
    if 'streak' not in session:
        session['streak'] = 0
    if 'longest_streak' not in session:
        session['longest_streak'] = 0
    if 'status' not in session:
        session['status'] = ""

    sorted_leaderboard = dict(sorted(leaderboard.items(), key=lambda item: item[1], reverse=True))
    sorted_score_board = dict(sorted(score_board.items(), key=lambda item: item[1], reverse=True))
    
    return render_template('index.html', 
                           status=session['status'], 
                           score=session['score'], 
                           streak=session['streak'], 
                           longest_streak=session['longest_streak'], 
                           leaderboard=sorted_leaderboard, 
                           score_board=sorted_score_board)

@app.route('/choose_name', methods=['GET', 'POST'])
def choose_name():
    if request.method == 'POST':
        session['name'] = request.form['name']
        return redirect(url_for('index'))
    return render_template('choose_name.html')

@app.route('/update_score', methods=['POST'])
def update_score():

    computer_choice = secrets.choice(choices)
    user_choice = request.get_json().get('choice')

    if user_choice == computer_choice:
        session['status'] = "It's a tie!"
    elif (user_choice == 'Rock' and computer_choice == 'Scissors') or (user_choice == 'Paper' and computer_choice == 'Rock') or (user_choice == 'Scissors' and computer_choice == 'Paper'):
        session['score'] += 1
        session['status'] = "You win!"
    else:
        session['status'] = "You lose!"

    if session['status'] == "You win!":
        session['streak'] += 1
        if session['streak'] > session['longest_streak']:
            session['longest_streak'] = session['streak']
    elif session['status'] == "You lose!":
        session['streak'] = 0

    score_board[session['name']] = session['score']
    leaderboard[session['name']] = session['longest_streak']

    sorted_leaderboard = sorted(leaderboard.items(), key=lambda item: item[1], reverse=True)
    sorted_score_board = sorted(score_board.items(), key=lambda item: item[1], reverse=True)

    return jsonify({
            "status": session['status'],
            "computer_choice": computer_choice,
            "user_choice": user_choice,
            "score": session['score'],
            "streak": session['streak'],
            "longest_streak": session['longest_streak'],
            "leaderboard": sorted_leaderboard,
            "score_board": sorted_score_board
        })

@app.route('/reset', methods=['GET','POST'])
def reset():
    session['score'] = 0
    session['streak'] = 0
    session['status'] = ""
    session['longest_streak'] = 0
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)