from pymongo import MongoClient

from flask import Flask, render_template, jsonify, request
from werkzeug.utils import secure_filename
import os
app = Flask(__name__)

client = MongoClient('localhost', 27017)
db = client.dbjungle


# HTML 화면 보여주기
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/index.html')
def index():
    return render_template('index.html')

@app.route('/tables.html')
def tables():
    return render_template('tables.html')

@app.route('/charts.html')
def charts():
    return render_template('charts.html')

@app.route('/_uploadajax', methods=['GET', 'POST'])
def uploadajax():
    if request.method == 'POST':  # POST 방식으로 전달된 경우
        file = request.files['file1']
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(os.getcwd()+"/uploads", filename))
        # f = request.form['file1']
        # 파일 객체 혹은 파일 스트림을 가져오고, html 파일에서 넘겨지는 값의 이름을 file1으로 했기 때문에 file1임.
        # f.save(f'uploads/{f.filename}') # 업로드된 파일을 특정 폴더에저장하고,
        # df_to_html = pd.read_csv(f'uploads/{f.filename}').to_html() # html로 변환하여 보여줌
        # return f.filename
        # print(f)
        # print(f)
    return jsonify({'result': 'success'})


# API 역할을 하는 부분
@app.route('/api/list', methods=['GET'])
def show_stars():
    # 1. db에서 mystar 목
    # 록 전체를 검색합니다. ID는 제외하고 like 가 많은 순으로 정렬합니다.
    # 참고) find({},{'_id':False}), sort()를 활용하면 굿!
    stars = list(db.mystar.find({}, {'_id': False}).sort('like', -1))
    # 2. 성공하면 success 메시지와 함께 stars_list 목록을 클라이언트에 전달합니다.
    return jsonify({'result': 'success', 'stars_list': stars})


@app.route('/api/like', methods=['POST'])
def like_star():
    # 1. 클라이언트가 전달한 name_give를 name_receive 변수에 넣습니다.
    name_receive = request.form['name_give']

    # 2. mystar 목록에서 find_one으로 name이 name_receive와 일치하는 star를 찾습니다.
    # star = db.mystar.find_one({'name':name_receive})

    # 3. star의 like 에 1을 더해준 new_like 변수를 만듭니다.
    # new_like = star['like']+1

    # 4. mystar 목록에서 name이 name_receive인 문서의 like 를 new_like로 변경합니다.
    # 참고: '$set' 활용하기!
    # db.mystar.update_one({'name':name_receive}, {'$set':{'like':new_like}})
    print(name_receive)
    # 5. 성공하면 success 메시지를 반환합니다.
    return jsonify({'result': 'success'})


@app.route('/api/delete', methods=['POST'])
def delete_star():
    # 1. 클라이언트가 전달한 name_give를 name_receive 변수에 넣습니다.
    name_receive = request.form['name_give']
    # 2. mystar 목록에서 delete_one으로 name이 name_receive와 일치하는 star를 제거합니다.
    db.mystar.delete_one({'name': name_receive})
    # 3. 성공하면 success 메시지를 반환합니다.
    return jsonify({'result': 'success'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
