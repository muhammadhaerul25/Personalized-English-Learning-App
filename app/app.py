from flask import Flask, render_template, request, jsonify
import openai
import time
import re



API_Key = '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'
openai.api_key = API_Key

pronunciation_prompt = [{'role': 'system', 'content': \
             'Kamu adalah sistem Personalized English Learning untuk Fitur pronunciation, speaking and conversation.\
                Kamu harus bertindak interaktif dengan user, adaptif dalam memberikan respon, dan menyesuaikan kemampuan bahasa Inggris user. \
                    Kita dapat melakukan conversation, kamu memberikan saran vocabulary, memperbaiki kesalahan grammar, dan hal lainnya terkait pronunciation and conversation. \
                        Kamu selalu memberikan respon dalam bahasa Inggris, dan hanya manggunakan bahasa Indonesia jika diminta'}]

context_prompt = [{'role': 'system', 'content': \
             'Kamu adalah sistem Personalized English Learning untuk Fitur context, vocabulary, and grammar.\
                Kamu harus bertindak interaktif dengan user, adaptif dalam memberikan respon, dan menyesuaikan kemampuan bahasa Inggris user. \
                    Kamu dapat menjelaskan context, menjelaskan arti words tertentu, membuat kalimat menggunakan words tertentu, memperbaiki kesalahan grammar, menulis kalimat menggunakan form/tenses tertentu.\
                        Kamu selalu memberikan respon dalam bahasa Inggris, dan hanya manggunakan bahasa Indonesia jika diminta'}]


reading_prompt = [{'role': 'system', 'content': \
             'Kamu adalah sistem Personalized English Learning untuk Fitur reading and writing.\
                Kamu harus bertindak interaktif dengan user, adaptif dalam memberikan respon, dan menyesuaikan kemampuan bahasa Inggris user. \
                    Kamu dapat menulis sebuah text dengan skenario tertentu, menjelaskan sebuah teks sesuai keinginan user, memperbaiki penulisan teks, menyimpulkan teks, meringkat teks, menyederhanakan teks, dan memperindah teks\
                        Kamu selalu memberikan respon dalam bahasa Inggris, dan hanya manggunakan bahasa Indonesia jika diminta'}]

placement_test_prompt = [{'role': 'system', 'content': \
                'Kamu adalah sistem Personalized English Learning untuk Fitur placement test. \
                    Berikan saya English Placement Test. Ujian ini terdiri dari tiga bagian yaitu, 1) Pronunciation, Speaking and Conversation, 2) Context, Vocabulary, and Grammar, 3) Reading and Writing. Setiap bagian selalu terdiri dari 10 soal berupa pilihan ganda atau esai. Berikan soal per satu bagian, kemudian saya akan memberikan jawaban untuk bagian tersebut, . Saya akan mengatakan next untuk masuk ke bagian selanjutnya dan begitu seterusnya. \
                        Kamu selalu memberikan respon dalam bahasa Inggris, dan hanya manggunakan bahasa Indonesia jika diminta \
                            Berikan Soalnya saja tanpa ada tambahan string lainnya. Yang paling penting jangan pernah memberikan jawabannya!' }]


app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/learning')
def learning():
    return render_template('learning.html')

@app.route('/placement-test')
def placement_test():
    return render_template('placement_test.html')

@app.route('/placement-test1')
def placement_test1():
    return render_template('placement_test1.html')

@app.route('/placement-test2')
def placement_test2():
    return render_template('placement_test2.html')


@app.route('/chat', methods=['POST'])
def chat():
    try:
        message = request.json['user_input']
        mode = request.json['mode']
        if message and mode:
            response = test_response(mode, message)
            return jsonify({'message': response})
        else:
            return jsonify({'message': 'Maaf, pesan tidak ditemukan'})
    except:
        return jsonify({'message': 'Maaf, terjadi kesalahan pada server'})


def test_response(mode, message):
    time.sleep(1)
    return 'mode: ' + mode + '\n' + 'message: ' + message


def get_response(mode, message):
    if mode == 'pronunciation':
        pronunciation_prompt.append({"role": "user", "content": message})
        chat = openai.ChatCompletion.create(
                model="gpt-3.5-turbo", messages=pronunciation_prompt
            )
        response = chat.choices[0].message.content

    elif mode == 'context':
        context_prompt.append({"role": "user", "content": message})
        chat = openai.ChatCompletion.create(
                model="gpt-3.5-turbo", messages=context_prompt
            )
        response = chat.choices[0].message.content

    elif mode == 'reading':
        reading_prompt.append({"role": "user", "content": message})
        chat = openai.ChatCompletion.create(
                model="gpt-3.5-turbo", messages=reading_prompt
            )
        response = chat.choices[0].message.content

    else:
        response = 'Maaf, mode tidak ditemukan'
    
    return response


@app.route('/section1')
def section1():
    try:
        placement_test_prompt.append({"role": "user", "content": 'Mari kita mulai section 1: Pronunciation, Speaking, and Conversation dengan 10 soal berupa multiple choice atau essay'})
        chat = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=placement_test_prompt
        )
        response = chat.choices[0].message.content

        pattern = r'\d+\..*?(?=\d+\.|$)'
        pattern2 = r"(?m)^(?:\d+\.).*?(?:\b10\..*?)(?=\n\d+\.|\n$)"
        questions = re.findall(pattern2, response, re.DOTALL)
        questions = questions[0].split("\n\n")
        
    except Exception as e:
        print(f"An error occurred: {e}")
        questions = test_questions()

    return jsonify({"questions": questions})


def test_questions():
    time.sleep(3)
    text_question = "1. How do you pronounce the word \"schedule\"?\na. /ʃedjuːl/\nb. /skedjuːl/\nc. /ʃedule/\nd. /skedule/\n\n2. Which of the following words has stress on the second syllable?\na. banana\nb. acquire\nc. cinema\nd. advise\n\n3. Which of the following words has a voiced consonant sound?\na. tick\nb. chip\nc. dug\nd. vase\n\n4. Which of the following sentences is correct in terms of intonation?\na. He is coming here today?\nb. He is coming here today!\nc. He is coming here today.\nd. He is coming here today;\n\n5. Which of the following words has a different vowel sound from the other three?\na. meat\nb. seat\nc. meaty\nd. seatbelt\n\n6. Which of the following words has a silent \"k\"?\na. knee\nb. knit\nc. knife\nd. know\n\n7. Which of the following sentences contains a word with a glottal stop?\na. He hit the ball over the fence.\nb. She is going to the store to buy some milk.\nc. I don't know what you're talking about.\nd. We need to water the plants before we leave.\n\n8. Which of the following words is stressed on the first syllable?\na. allow\nb. despair\nc. complex\nd. neglect\n\n9. Which of the following sounds is produced by the lips?\na. /f/\nb. /s/\nc. /z/\nd. /ʃ/\n\n10. Which of the following words has a different stress pattern from the other three?\na. important\nb. beautiful\nc. interesting\nd. comfortable\n"
    questions = re.split('\n\n+', text_question)
    return questions


@app.route('/submit-answer', methods=['POST'])
def submit_answer():
    data = request.get_json()
    answers = data.get('answers')
    # Lakukan apa yang diinginkan dengan jawaban yang diterima
    return 'Jawaban berhasil diterima'



if __name__ == '__main__':
    app.run(debug=True)
