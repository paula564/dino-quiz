import random
import json
from collections import defaultdict
import re

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

def parse_weight(weight_str):
    cleaned = str(weight_str).lower().replace("kg", "").replace(",", "").strip()
    try:
        return float(cleaned)
    except ValueError:
        return None

def q_diet(dinos):
    dinos_with_diet = [dino for dino in dinos if dino.get("Name") and dino.get("Diet")]
    diets = ["herbivorous", "carnivorous", "omnivorous", "insectivorous" ]
    if len(dinos_with_diet) < 1:
        return None
    target_dino = random.choice(dinos_with_diet)
    incorrect = [diet for diet in diets if diet != target_dino.get("Diet")]
    return question_builder(f"What was the diet of the {target_dino.get("Name")}?", target_dino.get("Diet"), incorrect)
        

def q_period(dinos):
    dinos_with_period = [dino for dino in dinos if dino.get("Name") and dino.get("When it lived")]
    periods = list({dino["When it lived"] for dino in dinos_with_period})
    if len(dinos_with_period) < 1 or len(periods) < 4:
        return None
    target_dino = random.choice(dinos_with_period)
    incorrect = [period for period in periods if period != target_dino.get("When it lived")]
    return question_builder(f"During which period did the {target_dino.get("Name")} live?", target_dino.get("When it lived"), incorrect)

def q_odd_one_out_type(dinos):
    dinos_by_type = defaultdict(list)
    for dino in dinos:
        name = dino.get("Name")
        dino_type = dino.get("Type of dinosaur")
        if name and dino_type:
            dinos_by_type[dino_type].append(name)

    valid_types = [type for type, names in dinos_by_type.items() if len(names) >= 3]

    if not valid_types or len(dinos_by_type) < 2:
        return None

    target_type = random.choice(valid_types)
    incorrect = dinos_by_type[target_type]

    #checks that the type is not equivalent to the target type. appends the names of the dinos not matching the target type
    correct_dinos = [name for type, names in dinos_by_type.items() if type != target_type for name in names]

    if not correct_dinos:
        return None

    target_dino = random.choice(correct_dinos)

    return question_builder(f"Which of the following dinosaurs is not of the {target_type} type?", target_dino, incorrect)

def q_length(dinos):
    dinos_with_length = [dino for dino in dinos if dino.get("Name") and dino.get("Length")]
    lengths = list({dino["Length"] for dino in dinos_with_length})
    if len(dinos_with_length) < 1 or len(lengths) < 4:
        return None
    target_dino = random.choice(dinos_with_length)
    incorrect = [length for length in lengths if length != target_dino.get("Length")]
    return question_builder(f"What was the length of the {target_dino.get("Name")}?", target_dino.get("Length"), incorrect)


def q_region(dinos):
    dinos_by_region = defaultdict(list)
    
    for dino in dinos:
        name = dino.get("Name")
        dino_region = dino.get("Found in")

        if name and dino_region:
            if isinstance(dino_region, str):
                dino_region = [dino_region]
                
            for region in dino_region:
                if name not in dinos_by_region[region]:
                    dinos_by_region[region].append(name)
                    
    valid_regions = [region for region, names in dinos_by_region.items() if len(names) >= 3]
    if not valid_regions or len(dinos_by_region) < 2:
        return None
    
    correct_region = random.choice(valid_regions)
    correct = dinos_by_region[correct_region]

    #handles situation where dino in both correct and incorrect region
    incorrect_dinos = list({name for region, names in dinos_by_region.items() if region != correct_region for name in names} - set(correct))

    if len(incorrect_dinos) < 3:
        return None

    return question_builder(f"Which of these dinosaurs was found in {correct_region}?", random.choice(correct), incorrect_dinos)


def q_meaning(dinos):
    dinos_with_meaning = [dino for dino in dinos if dino.get("Name") and dino.get("Name meaning")]
    meanings = list({dino["Name meaning"] for dino in dinos_with_meaning})
    if len(dinos_with_meaning) < 1 or len(meanings) < 4:
        return None
    target_dino = random.choice(dinos_with_meaning)
    incorrect = [meaning for meaning in meanings if meaning != target_dino.get("Name meaning")]
    return question_builder(f"What is the name meaning of the {target_dino.get("Name")}?", target_dino.get("Name meaning"), incorrect)

def q_heaviest_weight(dinos):
    weights = {}
    for dino in dinos:
        if dino.get("Name") and dino.get("Weight"):
            num_weight = parse_weight(dino["Weight"])
            if num_weight is not None:
                weights[num_weight] = dino

    if len(weights) < 4:
        return None

    sample_dinos = random.sample(list(weights.values()), 4)
    heaviest_dino = max(sample_dinos, key=lambda dino: parse_weight(dino["Weight"]))

    incorrect = [dino["Name"] for dino in sample_dinos if dino["Name"] != heaviest_dino["Name"]]

    return question_builder("Of the four dinosaurs, which one was the heaviest?", heaviest_dino["Name"], incorrect)

def q_teeth(dinos):
    dinos_with_teeth = [dino for dino in dinos if dino.get("Name") and dino.get("Teeth")]
    teeth = list({dino["Teeth"] for dino in dinos_with_teeth})
    if len(dinos_with_teeth) < 1 or len(teeth) < 4:
        return None
    target_dino = random.choice(dinos_with_teeth)
    incorrect = [t.capitalize() for t in teeth if t != target_dino.get("Teeth")]
    return question_builder(f"What kind of teeth did the {target_dino.get("Name")} have?", target_dino.get("Teeth").capitalize(), incorrect)


ALL_TEMPLATES = [
    q_diet,
    q_period,
    q_odd_one_out_type,
    q_region,
    q_length,
    q_meaning,
    q_heaviest_weight,
    q_teeth
    ]


def generate_quiz(dinos, num_questions=5):
    pool = ALL_TEMPLATES[:]
    random.shuffle(pool)
    questions = []

    while pool and len(questions) < num_questions:
        #extracts template from options
        template = pool.pop()
        #tests the template with dino data
        question = template(dinos)
        #appends if valid, otherwise continues looping until 5 valid questions
        if question is not None:
            questions.append(question)
    return questions


