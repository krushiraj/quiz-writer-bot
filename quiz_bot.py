from selenium import webdriver
from bs4 import BeautifulSoup

URL = 'http://www.mypythonquiz.com'
START = 'Start Quiz'
QUESTION_BANK_URL = './question-bank.html'
QB_QUESTION_TAG = 'p'
QB_ANS_TAG = 'b'
Q_TEXT_CSS_SELECTOR = '.qmain>.content>div>p>b'
Q_CODE_CSS_SELECTOR = '.qmain>.content>div>pre>code'
ANSWERS_FORM = '#qform'
ANSWER_TAG = 'input'

def prepare_question_bank(url):
    content = None
    if 'http' in url:
        import requests
        response = requests.get(url)
        content = response.content
    else:
        with open(url) as qb:
            content = qb.read()
    q_bank = BeautifulSoup(content, 'html.parser')
    return q_bank


def search_in_qb(qbank, question):
    import re
    re_esc_question = re.escape(question)
    questions = qbank.find_all(QB_QUESTION_TAG)
    for question in questions:
        if question.find(string=re.compile(re_esc_question)):
            question_wrapper = question.parent
            ans = question_wrapper.find('b')
            return ans.text


def write_code_to_file(code):
    with open('sample.py', 'w') as pyfile:
        pyfile.write(code)


def run_code(filename='sample.py'):
    from subprocess import PIPE, run
    process_output = run(
        ['python3 '+filename], 
        stdout=PIPE, 
        stderr=PIPE, 
        universal_newlines=True, 
        shell=True
    )
    if process_output.returncode == 0:
        return str(process_output.stdout).strip()
    else:
        return 'error ERROR'


def get_random_option(no_of_opts):
    from random import randint
    return randint(0, no_of_opts-1)


def get_closest_answer(answer, all_answers):
    import difflib
    closest_answers = difflib.get_close_matches(
        answer,
        all_answers
    )
    if len(closest_answers) > 1:
        if closest_answers[0] == answer:
            return all_answers.index(answer)
        else:
            return all_answers.index(
                closest_answers[
                    get_random_option(len(closest_answers))
                ]
            )
    else:
        try:
            return all_answers.index(closest_answers[0])
        except IndexError:
            return (get_random_option(len(all_answers)))


def get_answer_index(question, code, answers, qb):
    answer = search_in_qb(qb, question)
    if answer:
        return answers.index(answer)
    else:
        write_code_to_file(code)
        output = run_code()
        return get_closest_answer(output, answers)


def get_question_and_solve(driver, qb):
    question_text = driver.find_element_by_css_selector(Q_TEXT_CSS_SELECTOR)
    question_code = driver.find_element_by_css_selector(Q_CODE_CSS_SELECTOR)
    options_form = driver.find_element_by_css_selector(ANSWERS_FORM)
    #answers in text form
    answers = [div.text for div in options_form.find_elements_by_tag_name('div')][:-3]
    input_elems = options_form.find_elements_by_tag_name(ANSWER_TAG)
    available_opts, submit = input_elems[:-2], input_elems[-2]
    #click on answer and then on submit
    available_opts[
        get_answer_index(question_text.text, question_code.text, answers, qb)
    ].click()
    submit.click()


def go_to_next_question(driver):
    #wait for 3 secs and click on next question
    driver.implicitly_wait(3)
    next_ques = driver.find_element_by_link_text('Next Question')
    next_ques.click()


def run_test_loop(driver, qb):
    #condition when the quiz would complete
    QUIZ_ENDED = False
    #while quiz is not complete try attempting
    while not QUIZ_ENDED:
        get_question_and_solve(driver, qb)
        go_to_next_question(driver)
        

def init_browser():
    #open the browser and go to quiz link
    driver = webdriver.Firefox()
    driver.get(URL)
    return driver


def start_quiz(driver):
    #start the quiz
    start_quiz = driver.find_element_by_link_text(START)
    start_quiz.click()


def take_quiz():
    #initialize question bank and browser
    QUESTION_BANK = prepare_question_bank(QUESTION_BANK_URL)
    driver = init_browser()
    start_quiz(driver)
    run_test_loop(driver, QUESTION_BANK)
    

if __name__ == '__main__':
    take_quiz()