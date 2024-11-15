import os.path

from flask import Flask, render_template, request, make_response, redirect, send_from_directory, jsonify  # 导入Flask模块功能
app = Flask(__name__)

SAVE_FOLDER = 'data_save'
os.makedirs(SAVE_FOLDER,exist_ok=True)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER,exist_ok=True)

@app.route('/home', methods=['GET'])
def home():
    return render_template("home.html")

@app.route('/tool', methods=['GET','POST'])
def tool():
    if request.method == 'POST':
        data1 = request.form['C/S']
        data2 = request.form['A/S']
        data3 = request.form['MCL']
        data4 = request.form['Q0']
        data5 = request.form['Q1']
        data6 = request.form['Q2']
        data7 = request.form['Q3']
        data8 = request.form['Q4']
        data9 = request.form['inlineRadioOptions']
        data = 'C/S：'+data1+' '+'A/S：'+data2+' '+'MCL：'+data3+' '+'Q0：'+data4+' '+'Q1：'+data5+' '+'Q2：'+data6+' '+'Q3：'+data7+' '+'Q4：'+data8+' '+'精度：'+data9

        existing_data = []
        for filename in os.listdir(SAVE_FOLDER):
            if filename.endswith('.txt'):
                with open(os.path.join(SAVE_FOLDER,filename),'r') as f:
                    existing_data.extend(f.read().splitlines())

        if data in existing_data:
            return jsonify({'message':'该数据已存在！请至模型库中进行查找下载！'}),400

        file_index = 1
        while True:
            file_name = f'{file_index}.txt'
            file_path = os.path.join(SAVE_FOLDER, file_name)
            if not os.path.exists(file_path):
                break
            file_index += 1

        with open(file_path,'w') as f:
            f.write(data)
        return jsonify({'message':'数据已成功提交！请稍后至模型库中进行下载！'})
    return render_template("tool.html")

@app.route('/database')
def database():
    return render_template("database.html")

@app.route('/team')
def team():
    return render_template("team.html")

@app.route('/contact')
def contact():
    return render_template("contact.html")

@app.route('/developer0508')
def developer():
    return render_template("developer.html")

@app.route('/upload',methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return '没有文件上传',400

    file = request.files['file']
    if file.filename == '':
        return '没有选择文件',400

    file.save(os.path.join(UPLOAD_FOLDER, file.filename))
    return '文件上传成功'


@app.route('/files', methods=['GET'])
def list_files():
    files = os.listdir(UPLOAD_FOLDER)
    return {'files': files}

@app.route('/uploads/<path:filename>', methods=['GET'])
def download_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

if __name__ == '__main__':
    app.run(debug=True)