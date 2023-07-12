from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import os
import datetime as dt

app = Flask(__name__)


@app.route("/", methods=["GET"])  # 기본 접속 시 이미지 업로드 화면 출력
def main():
    return render_template("./index.html")


@app.route("/uploadImg", methods=["POST"])  # 이미지 업로드
def uploadImg():
    lastUploadTime = str(dt.datetime.now()).replace(":", "")
    os.mkdir("./images/" + lastUploadTime)  # 폴더 생성
    lastUploadDir = os.path.join("images", lastUploadTime)
    uploadImg = request.files.getlist("images[]")  # 받은 이미지 목록을 변수에 저장
    i = 0
    for f in uploadImg:
        f.save(lastUploadDir + "/" +
               secure_filename(str(i) + ".jpg"))  # 순서대로 이미지 저장
        i += 1

    return str(lastUploadTime)


if __name__ == '__main__':
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(host="0.0.0.0", port=80)
