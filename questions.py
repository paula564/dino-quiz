import random
import json

with open("dinos.json", "r", encoding="utf-8") as file:
    dinos = json.load(file)


def question_builder(question, correct, incorrect_options):
    options = [correct] + random.sample(incorrect_options, 3)
    random.shuffle(incorrect_options)

    return {
        "question": question,
        "options": options,
        "answer": correct
        }

def q_diet(dinos):
    dinos_with_diet = [d for d in dinos if d.get("Name") and d.get("Diet")]
    diets = ["herbivorous", "carnivorous", "omnivorous", "insectivorous" ]
    if len(dinos_with_diet) < 1:
        return None
    target_dino = random.choice(dinos_with_diet)
    incorrect = [diet for diet in diets if diet != target_dino.get("Diet")]
    return question_builder(f"What was the diet of the {target_dino.get("Name")}?", target_dino.get("Diet"), incorrect)
        

def q_period(dinos):
    dinos_with_period = [d for d in dinos if d.get("Name") and d.get("When it lived")]
    periods = list({d["When it lived"] for d in dinos_with_period})
    if len(dinos_with_period) < 1 or len(periods) < 4:
        return None
    target_dino = random.choice(dinos_with_period)
    incorrect = [period for period in periods if period != target_dino.get("When it lived")]
    return question_builder(f"During which period did the {target_dino.get("Name")} live?", target_dino.get("When it lived"), incorrect)

diet = q_diet(dinos)
period = q_period(dinos)

print(diet)
print(period)