<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Quiz Results</title>
    <link rel="stylesheet" type="text/css" href="/static/results.css">
</head>
<body>
    <div class="results-card">
        <h1>Quiz Results 🦖</h1>
        <h2 class="score-banner">Your Score: {{score}} / {{len(correct)}}</h2>

        <ul class="results-list">
        % for i in range(len(correct)):
            % is_correct = (selected[i] == correct[i])
            <li class="{{'correct' if is_correct else 'incorrect'}}">
                <span class="question-title">Question {{i + 1}}</span>
                % if is_correct:
                    <p class="answer-text">Your answer: <strong>{{selected[i] or "No answer"}}</strong> ✓</p>
                % else:
                    <p class="answer-text">Your answer: <strong>{{selected[i] or "No answer"}}</strong> ✗</p>
                    <p class="correct-answer">Correct answer: <strong>{{correct[i]}}</strong></p>
                % end
            </li>
        % end
        </ul>

        <a href="/quiz" class="play-again-btn">Play Again</a>
    </div>
</body>
</html>
