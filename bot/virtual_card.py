from base64 import b64encode
from io import BytesIO
from os.path import join, dirname

from html2image import Html2Image


class VirtualCard:
    def __init__(self, name, qr_code, password):
        buffer = BytesIO()
        qr_code.save(buffer, format="PNG")
        self.__code = f"data:image/png;base64,{b64encode(buffer.getvalue()).decode('utf-8')}"
        self.__name = name
        self.__psw = password
        self.__html: str = ""
        self.__css: str = ""
        self.__file: str = f"{str(self.__psw)}.svg"

    def image_base_64(self, filename):
        return f"data:image/png;base64,{b64encode(open(join(dirname(__file__), f'./fonts/{filename}.png'), 'rb').read()).decode('utf-8')} "

    def __create_structure(self):
        return """
<div class="card">
  <div class="card__front card__part">
    <img class="card__front-square card__square" src="{footer}">
    <span class="bonus_card"><b>Bonus Card</b></span>
    <div>
      <img class="xari" src="{xaribulbulbase64}">
    </div>
    <div class="card__space-75 name">
      <p class="card_name">{name}</p>
    </div>
    <div>
      <img class="qrcode" src="{code}">
    </div>
    <div class="pass">
      <p class="card_pass">{password}</p>
  </div>
  </div>
</div>
        """.format(name=self.__name, code=self.__code, password=self.__psw,
                   xaribulbulbase64=self.image_base_64("xaribulbul"),
                   footer=self.image_base_64("logo-footer")
                   )

    def __create_design(self):
        return """
        .card{
width: 420px;
height: 290px;
    -webkit-perspective: 600px;
    -moz-perspective: 600px;
    perspective:600px;
    
}
.card__part{
    box-shadow: 1px 1px #aaa3a3;
    top: 0;
    position: absolute;
    z-index: 1000;
    left: 0;
    display: inline-block;
    width: 320px;
    height: 190px;
    background: linear-gradient(to right bottom, #d112d1, #a907a9, #8d108d, #9b049b, #830083);

    border-radius: 10px;

}
.card__front{
    padding: 18px;
}
.card__front-logo{
    position: absolute;
    top: 18px;
    right: 18px;
}
.card__square {
    border-radius: 5px;
    height: 38px;
}
.card_name {
    margin-bottom: 0;
    margin-top: 55px;
    font-size: 13px;
    line-height: 18px;
    color: #fff;
    letter-spacing: 1px;
    text-transform: uppercase;
}
.bonus_card{
    position: absolute;
    top: 12px;
    right: 20px;
    font-size: 17px;
    font: 16px "Helvetica Neue", Helvetica, sans-serif;
    color: rgb(38, 38, 38);

}
.xari{
    width: 50px;
    margin-top: 30px;
    margin-left: 20px;
}
.name{
    width: 50%;
}
.qrcode{
    position: absolute;
    top: 27%;
    left: 65%;
}
.pass{
    /* position: relative;
    width: 51%; */
    position: absolute;
    left: 55%;
    top: 77%;
    font: 14px "Helvetica Neue", Helvetica, sans-serif;
}
.card_pass {
    margin-left: 50px;
    font-size: 15px;
    line-height: 18px;
    color: #fff;
    letter-spacing: 1px;
    text-transform: uppercase;
}
        """

    def __html2image(self, html, css):
        hti = Html2Image(output_path="./output", size=(370, 240))
        hti.screenshot(html_str=html, css_str=css, save_as=self.__file)
        return hti.output_path

    def generate_virtual_card(self):
        self.__html = self.__create_structure()
        self.__css = self.__create_design()
        path = self.__html2image(self.__html, self.__css)
        with open("{}/{}.svg".format(path, self.__psw), 'rb') as f:
            byte_im = f.read()
        return byte_im
