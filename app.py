
from flask import Flask, render_template, jsonify, request
from werkzeug.utils import secure_filename
import json
import os
from urllib.parse import urlparse, urlsplit
import pandas as pd
ALLOWED_EXTENSIONS = set(['txt', 'csv'])
app = Flask(__name__)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def process_hour(df):
    df.Timestamp = pd.to_datetime(df.Timestamp)
    df['Time'] = df.Timestamp.dt.strftime('%Y-%m-%d %H')

    count = df.groupby('Time').count().Timestamp
    x = count.index.to_list()
    y = count.values.tolist()

    return {'x': x, 'y': y}

def process_pie(df):
    normal_log = df.loc[df.Status.astype(str).str.isnumeric(), :].copy()
    _,_,normal_log['Path_path'],normal_log['Path_query'],_ = zip(*normal_log['Path'].map(urlsplit))
    normal_log.loc[normal_log['Path_path'].str.contains('/events/event'), 'Path_path'] = '/events/event'
    normal_log.loc[normal_log['Path_path'].str.contains('/notice/notice'), 'Path_path'] = '/notice/notice'
    normal_log.loc[normal_log['Path_path'].str.contains('/shops/shop'), 'Path_path'] = '/shops/shop'
    path_grouped = normal_log.groupby(['Path_path'], as_index=False)['Timestamp'].count().rename(columns={"Timestamp": "count"})
    path_count = path_grouped.sort_values('count', ascending=False, )
    split_df = path_count.iloc[0:5].sort_values('count', ascending=False, )
    split_df['per'] = split_df['count'].apply(lambda g: '%0.1f' % ((g / split_df['count'].sum()) * 100))

    return {'labels': split_df['Path_path'].to_list(), 'per': split_df['per'].to_list()}


# HTML 화면 보여주기
@app.route('/', methods=['GET', 'POST'])
def home():
   if request.method == 'POST':
      return 'POST'
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


@app.route('/uploadajax', methods=['POST'])
def upload():
    file = request.files['file']

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(os.getcwd()+"/uploads", filename))
        df = pd.read_csv(f'uploads/{filename}')

        # timestamp = df.Timestamp.to_list()
        # host = df.Host.to_list()
        # status = df.Status.to_list()
        # df_json = {
        #     'timestamp': timestamp,
        #     'status': status,
        #     'host': host
        # }

        return jsonify({'result': 'success','count': len(df), 'data': process_hour(df), 'data2': process_pie(df)})
    else:
        return jsonify({'result': 'false'})


# API 역할을 하는 부분
@app.route('/api/list', methods=['GET'])
def show_stars():
    df = pd.read_csv(f'uploads/38.140.103.156.csv')
    df_json = df.to_json(orient='records')
    parsed = json.loads(df_json)
    return jsonify({'result': 'success', 'stars_list': json.dumps(parsed, indent=4)})


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
    app.run('0.0.0.0', port=8080, debug=True)
