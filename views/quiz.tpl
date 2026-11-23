<!DOCTYPE html>
<html>
<head><title>Dinosaur Quiz</title></head>
<body>
<form action="/quiz" method="post">
% for i, q in enumerate(questions):
            <p><strong>{{i + 1}}. {{q["question"]}}</strong></p>
            
            % for option in q["options"]:
                <label>
                    <input type="radio" name="q{{i}}" value="{{option}}" required>
                    {{option}}
                </label><br>
            % end
        % end
        <br>
        <button type="submit">Submit Answers</button>
</form>
</body>
</html>