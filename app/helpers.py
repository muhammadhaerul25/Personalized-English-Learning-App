import re
import time

#TEST FUNCTIONS
def test_response(mode, message):
    time.sleep(1)
    return 'mode: ' + mode + '\n' + 'message: ' + message

def test_questions():
    time.sleep(3)
    text_question = "1. How do you pronounce the word \"schedule\"?\na. /ʃedjuːl/\nb. /skedjuːl/\nc. /ʃedule/\nd. /skedule/\n\n2. Which of the following words has stress on the second syllable?\na. banana\nb. acquire\nc. cinema\nd. advise\n\n3. Which of the following words has a voiced consonant sound?\na. tick\nb. chip\nc. dug\nd. vase\n\n4. Which of the following sentences is correct in terms of intonation?\na. He is coming here today?\nb. He is coming here today!\nc. He is coming here today.\nd. He is coming here today;\n\n5. Which of the following words has a different vowel sound from the other three?\na. meat\nb. seat\nc. meaty\nd. seatbelt\n\n6. Which of the following words has a silent \"k\"?\na. knee\nb. knit\nc. knife\nd. know\n\n7. Which of the following sentences contains a word with a glottal stop?\na. He hit the ball over the fence.\nb. She is going to the store to buy some milk.\nc. I don't know what you're talking about.\nd. We need to water the plants before we leave.\n\n8. Which of the following words is stressed on the first syllable?\na. allow\nb. despair\nc. complex\nd. neglect\n\n9. Which of the following sounds is produced by the lips?\na. /f/\nb. /s/\nc. /z/\nd. /ʃ/\n\n10. Which of the following words has a different stress pattern from the other three?\na. important\nb. beautiful\nc. interesting\nd. comfortable\n"
    questions = re.split('\n\n+', text_question)
    return questions

def extract_english_level(result):
    pattern = r'(A1|A2|B1|B2|C1|C3)'
    match = re.search(pattern, result)
    if match:
        english_level = match.group()
        return english_level
    else:
        return None
    
def english_level_mapping(english_level):
    english_level_map = {
        'A1': 'A1 (Beginner)',
        'A2': 'A2 (Elementary)',
        'B1': 'B1 (Intermediate)',
        'B2': 'B2 (Upper Intermediate)',
        'C1': 'C1 (Advanced)',
        'C2': 'C2 (Proficient)'
    }
    if english_level in english_level_map:
        return english_level_map[english_level]
    else:
        return 'Unknown'

def is_any_english_level(english_level):
    if english_level == 'Unknown' or english_level == None or english_level == '':
        english_level = f"Your English level is currently unknown. For the best learning experience, I recommend you to take a placement test first."
    else:
        english_level = f'Your English level is {english_level}.'
    return english_level
