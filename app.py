from flask import *
from pymongo import MongoClient

import requests
from bs4 import BeautifulSoup


client = MongoClient("localhost", 27017)
db = client.likelion

app = Flask(__name__)
app.secret_key = "test"

@app.route('/')
def index():
    # TODO:
    # enable session to modify the login_status

    login_status = "login" in session and session["login"] == 'true'
    print(login_status)
    if login_status:
        all_db = list(db.likelion.find({},{'_id':0}))
        return redirect(url_for('login'))
    else:
        return redirect(url_for('login'))

@app.route('/index')
def mainpage():
    return render_template('index.html')

@app.route('/calendar')
def cal():
    all_db = list(db.likelion.find({},{'_id':0}))
    return render_template('calendar.html', all_data = all_db)

@app.route('/login', methods=["POST", "GET"])
def login():
    if request.method == "POST":
        login_status = request.form["login"]
        session["login"] = login_status
        return redirect(url_for('index'))
    else:
        login_status = "login" in session and session["login"] == 'true'
        if login_status:
            return redirect(url_for('mainpage'))
        else:
            return render_template('login.html')

@app.route('/logout', methods=["GET"])
def logout():
    session.pop("login")
    return redirect(url_for('index'))
    

@app.route('/memo', methods=['GET'])
def listing():
    # 모든 document 찾기 & _id 값은 출력에서 제외하기
    result = list(db.articles.find({},{'_id':0}))
    # articles라는 키 값으로 영화정보 내려주기
    return jsonify({'result':'success', 'articles':result})


## URL Crawling
@app.route('/memo', methods=['POST'])
def url_crawling():
	# 클라이언트로부터 데이터를 받는 부분
    url_receive = request.form['url_give']
    # Glassdoor Job position Crawling Code
    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(url_receive,headers=headers)
    # //  HTML을 BeautifulSoup이라는 라이브러리를 활용해 검색하기 용이한 상태로 만듦
    soup = BeautifulSoup(data.text, 'html.parser')
    # // job position, info etc 긁어오기
    position = soup.select_one('#main-content > section.core-rail > div > section.top-card-layout > div > div.top-card-layout__entity-info-container > div > h1').text
    company_name = soup.select_one('#main-content > section.core-rail > div > section.top-card-layout > div > div.top-card-layout__entity-info-container > div > h4 > div:nth-child(1) > span:nth-child(1) > a').text  
    company_location = soup.select_one('#main-content > section.core-rail > div > section.top-card-layout > div > div.top-card-layout__entity-info-container > div > h4 > div:nth-child(1) > span.topcard__flavor.topcard__flavor--bullet').text
    job_info = soup.select_one('#main-content > section.core-rail > div > div.decorated-job-posting__details > section.core-section-container.description > div > div > section > div').text
		
    # mongoDB에 넣는 부분
    # article = {'url': url_receive, 'comment': comment_receive, 'image': url_image,
    #            'title': url_title, 'desc': url_description}
    # db.articles.insert_one(article)
    print("Hi")
    return jsonify({'result': 'success', 'position': position, 'company_name': company_name, 'company_location': company_location, 'job_info':job_info})

@app.route('/board', methods=['GET'])
def board():
    return render_template('board.html')

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)