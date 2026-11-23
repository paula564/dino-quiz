<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Quiz Results</title>
</head>
<body>
    <h1>Quiz Results</h1>
    <h2>Your Score: {{score}} / {{len(correct)}}</h2>

    <ul>
    % for i in range(len(correct)):
        <li>
            <strong>Question {{i + 1}}:</strong><br>
            % if selected[i] == correct[i]:
                Your answer: {{selected[i] or "No answer"}} (Correct)
            % else:
                Your answer: {{selected[i] or "No answer"}} (Incorrect)<br>
                Correct answer: {{correct[i]}}
            % end
        </li>
    % end
    </ul>

    <a href="/quiz">Play Again</a>
</body>
</html>


