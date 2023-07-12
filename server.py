from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import os
import datetime as dt
from PIL import Image
import qrcode

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
    imageProcessing(lastUploadDir)
    return str(lastUploadTime)


def imageProcessing(lastUploadDir):
    for i in range(4):
        img = Image.open(lastUploadDir + "/" + str(i) + ".jpg")
        # 이미지를 530px, 700px으로 크기 수정
        img_resize = img.resize((530, 700), Image.LANCZOS)
        img_resize.save(lastUploadDir + "/" + str(i) + "_resize.jpg")

    # 이미지 합치기
    imgs = []
    for i in range(4):
        imgs.append(Image.open(lastUploadDir + "/" + str(i) + "_resize.jpg"))
    bgImg = Image.open("./background.png")
    bgImg_size = bgImg.size
    newImg = Image.new("RGB", (bgImg_size[0], bgImg_size[1]))
    newImg.paste(bgImg, (0, 0))
    newImg.paste(imgs[0], (51, 213))
    newImg.paste(imgs[1], (615, 213))
    newImg.paste(imgs[2], (51, 950))
    newImg.paste(imgs[3], (615, 950))
    newImg.save(lastUploadDir + "/" + "result.jpg") # 합쳐진 이미지 저장



if __name__ == '__main__':
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(host="0.0.0.0", port=80)
