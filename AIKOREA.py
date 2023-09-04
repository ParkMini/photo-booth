from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import os
import datetime as dt
from PIL import Image, ImageDraw, ImageFont
import qrcode

app = Flask(__name__)

@app.route("/", methods=["GET"])
def main():
    return render_template("./index.html")

@app.route("/upload2Img", methods=["POST"])
def upload2Img():
    lastUploadTime = str(dt.datetime.now()).replace(":", "").replace(" ", "_")
    lastUploadDir = os.path.join("static", lastUploadTime)
    os.mkdir(lastUploadDir)
    
    uploadImg = request.files.getlist("images[]")
    username = request.form.get('username')
    
    for idx, f in enumerate(uploadImg):
        f.save(os.path.join(lastUploadDir, f"{idx}.png"))
    
    image2Processing(lastUploadDir, username)
    createQR(lastUploadDir, lastUploadTime)
    
    return render_template("showQR.html", imgSrc=f"{lastUploadTime}/QR.jpg", imgDownloadSrc=f"http://pcs.pah.kr:904/view?key={lastUploadTime}")

def image2Processing(lastUploadDir, username):
    imgs = [Image.open(os.path.join(lastUploadDir, f"{i}.png")) for i in range(2)]
    bgImg = Image.open("./AI KOREA.png")
    
    draw = ImageDraw.Draw(bgImg)
    font = ImageFont.truetype('./GmarketSansTTF/GmarketSansTTFMedium.ttf', size=200)
    if (len(username) >= 4):
        draw.text((190, 110), username, font=font, fill="white") # 이름 4자
    else:
        draw.text((270, 110), username, font=font, fill="white") # 이름 3자
    
    newImg = Image.new("RGB", bgImg.size)
    newImg.paste(bgImg, (0, 0))
    newImg.paste(imgs[0], (100, 440))
    newImg.paste(imgs[1], (100, 1626))
    newImg.save(os.path.join(lastUploadDir, "result.jpg"))

def createQR(lastUploadDir, lastUploadTime):
    qrImg = qrcode.make(f"http://pcs.pah.kr:904/view?key={lastUploadTime}")
    qrImg.save(os.path.join(lastUploadDir, "QR.jpg"))

@app.route("/view", methods=["GET"])
def view():
    key = request.args.get("key")
    return render_template("view.html", imgSrc=f"{key}/result.jpg")

if __name__ == '__main__':
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(host="0.0.0.0", port=904)