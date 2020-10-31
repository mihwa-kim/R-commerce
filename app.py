from flask import Flask, render_template, jsonify, request

app = Flask(__name__)


## HTML을 주는 부분
@app.route('/')
def home():
    return render_template('personalcuration.html')


## API 역할을 하는 부분
@app.route('/curation', methods=['GET'])
def curation_get():
    weather_receive = request.args.get('title_give')
    print(title_receive)
    return jsonify({'result': 'success', 'msg': '이 요청은 GET!'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)