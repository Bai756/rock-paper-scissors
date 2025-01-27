function updateScore(choice) {
    fetch('/update_score', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ choice: choice })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('status').innerText = data.status;
        document.getElementById('computer_choice').innerText = data.computer_choice;
        document.getElementById('user_choice').innerText = data.user_choice;
        document.getElementById('score').innerText = data.score;
        document.getElementById('streak').innerText = data.streak;
        document.getElementById('longest_streak').innerText = data.longest_streak;

        let scoreBoard = document.getElementById('highest_score_leaderboard');
        scoreBoard.innerHTML = '';
        for (let i = 0; i < data.score_board.length; i++) {
            let li = document.createElement('li');
            li.innerText = `${data.score_board[i][0]}: ${data.score_board[i][1]}`;
            scoreBoard.appendChild(li);
        }

        let leaderboard = document.getElementById('leaderboard');
        leaderboard.innerHTML = '';
        for (let i = 0; i < data.leaderboard.length; i++) {
            let li = document.createElement('li');
            li.innerText = `${data.leaderboard[i][0]}: ${data.leaderboard[i][1]}`;
            leaderboard.appendChild(li);
        }
    });
}
