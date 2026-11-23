<!DOCTYPE html>
<html>
<head><title>Dinosaur Quiz</title></head>
<body>
% for i, q in enumerate(questions):
            <p><strong>{{i + 1}}. {{q["question"]}}</strong></p>
            
            % for option in q["options"]:
                <label>
                    <input type="radio" name="q{{i}}" value="{{option}}" required>
                    {{option}}
                </label><br>
            % end
        % end
</body>
</html>