<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dinosaur Quiz</title>
    <link rel="stylesheet" type="text/css" href="/static/quiz.css">
</head>
<body>

    <form action="/quiz" method="post">
        <h1>Dinosaur Quiz 🦖</h1>
        
        % for i, q in enumerate(questions):
            <div class="question-block">
                <p class="question-text"><strong>{{i + 1}}. {{q["question"]}}</strong></p>
                <input type="hidden" name="ans{{i}}" value="{{q['answer']}}">
                
                <div class="options-group">
                    % for option in q["options"]:
                        <label>
                            <input type="radio" name="q{{i}}" value="{{option}}" required>
                            <span>{{option}}</span>
                        </label>
                    % end
                </div>
            </div>
        % end
        
        <button type="submit">Submit Answers</button>
    </form>

</body>
</html>
