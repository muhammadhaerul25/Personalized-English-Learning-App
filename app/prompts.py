#PROMPT
def custom_prompt(prompt_dict, name, english_level, prompt_name):
    custom = f'Hi nama saya {name} dengan level bahasa inggris {english_level}. Mohon berikan {prompt_name} yang sesuai dengan level bahasa inggris saya!'
    prompt_dict.append({"role": "user", "content": custom})
    if prompt_name in ['pronunciation, speaking and conversation', 'context, vocabulary, and grammar', 'reading and writing']:
        prompt_dict.append({"role": "user", "content": remainder_prompt})
    return prompt_dict


def create_study_plan_prompt(english_level, goals, other_goals, start_date, end_date, days, hours):
    study_plan = f"My English level is {english_level}, so I will focus on {', '.join(goals)} + {other_goals}. I plan to start studying on {start_date} and finish on {end_date}, for a total of {days} days per week and {hours} hours per day. Based on this information, give me a study plan."
    return study_plan


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
                    Berikan user English Placement Test yang sesaui dengan English level user. Ujian ini terdiri dari tiga bagian yaitu, 1) Pronunciation, Speaking and Conversation, 2) Context, Vocabulary, and Grammar, 3) Reading and Writing. Setiap bagian selalu terdiri dari 10 soal. Berikan soal per satu bagian, kemudian saya akan memberikan jawaban untuk bagian tersebut. \
                        Kamu selalu memberikan respon dalam bahasa Inggris, dan hanya manggunakan bahasa Indonesia jika diminta \
                            Berikan Soalnya saja tanpa ada tambahan string lainnya. Yang paling penting jangan pernah memberikan jawabannya!' }]


section1_prompt = {"role": "user", "content": 'Mari kita mulai section 1: Pronunciation, Speaking, and Conversation. \
                   Berikan 10 soal berupa multiple choice yang bervariasi dan menyesuaikan dengan level bahasa inggris user. \
                   Jangan berikan saya jawabannya. Berikan respon full in English. Gunakan soal TOEFL atau IELTS sebagai referensi \
                   Jika sebelumnya saya sudah meminta soal untuk section ini, dan saya meminta lagi, maka berikan saja soal yang berbeda'}

section2_prompt = {"role": "user", "content": 'Next section 2: Context, Vocabulary, and Grammar. \
                   Berikan 10 soal berupa multiple choice atau isian yang bervariasi dan menyesuaikan dengan level bahasa inggris user. \
                   Jangan berikan saya jawabannya. Berikan respon full in English. Gunakan soal TOEFL atau IELTS sebagai referensi \
                   Jika sebelumnya saya sudah meminta soal untuk section ini, dan saya meminta lagi, maka berikan saja soal yang berbeda'}

section3_prompt = {"role": "user", "content": 'Next section 3: Reading and Writing. \
                   Berikan 10 soal berupa multiple choice atau essay yang bervariasi menyesuaikan dengan level bahasa inggris user. \
                   Jangan berikan saya jawabannya. Berikan respon full in English. Gunakan soal TOEFL atau IELTS sebagai referensi \
                   Jika sebelumnya saya sudah meminta soal untuk section ini, dan saya meminta lagi, maka berikan saja soal yang berbeda'}

answer_prompt = 'Berikut jawaban saya untuk section tersebut: '

result_prompt = {"role": "user", "content": 'Berikan result dan feedback dari  ketiga section tersebut. Dan pada bagain akhir, tentukan level kemampuan bahasa inggris dalam CEFR (A1/A2/B1/B2/C1/C2) secara keseluruhan dengann format (Your english level is {user_english_level}). \ Jangan mengatakan (I am sorry, as a language learning system I cannot determine your english level) Berikan saja result berdasarkan jawaban yang saya berikan.'}


study_plan_prompt = [{'role': 'system', 'content': \
                      'Kamu adalah sistem Personalized English Learning untuk Fitur study plan. \
                        Berikan saya study plan yang lengkap dan detail serta berikan juga tips and trick terkait study plan tersebu.'}]

remainder_prompt = "Jika saya bertanya (Recall what I learned last time), maka lihat messages sebelumnya untuk mencari tahu apa yang terakhir kali saya pelajari"

temp_prompt_user = [{"role": "user", "content": "{text}"}]

temp_prompt_assistant = [{"role": "assistant", "content": "{text}"}]