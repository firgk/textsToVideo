from flask import *
import os
from main import *
from threading import*


app = Flask(__name__,static_folder="", template_folder="")


@app.route('/')
def index():
    # 获取图片文件夹中的文件列表
    print(os.getcwd())
    split_txt_files = os.listdir('split_txt')
    split_txt_files_cont=len(split_txt_files)
    text_contents=[]
    for item in range(1, split_txt_files_cont + 1):
        with open('split_txt/' + str(item) + '.txt', 'r', encoding='utf-8') as file:
            text_content = file.read()
            text_contents.append(text_content)
    return render_template('index.html', split_txt_files_cont=split_txt_files_cont,text_contents=text_contents)

    

@app.route('/delete_folder_fileser')
def delete_folder_fileser():
    delete_folder_files('split_txt')
    delete_folder_files('pictures')
    delete_folder_files('tts')
    # delete_folder_files('video')
    return redirect(url_for('index'))
    
@app.route('/make_texter')
def make_texter():
    thread = Thread(target=make_text)
    thread.start()
    return redirect(url_for('index'))

@app.route('/make_ttser')
def make_ttser():
    thread = Thread(target=make_tts)
    thread.start()
    return redirect(url_for('index'))


@app.route('/make_picer')
def make_picer():
    thread = Thread(target=make_pic)
    thread.start()
    return redirect(url_for('index'))


@app.route('/make_movieer')
def make_movieer():
    thread = Thread(target=make_movie)
    thread.start()
    return redirect(url_for('index'))

# @app.route('/re_make_picer/<id>')
# def re_make_picer(id):
#     thread = Thread(target=re_make_pic, args=(id,))
#     thread.start()
#     return redirect(url_for('index'))


@app.route('/re_make_picer/<id>')
def re_make_picer(id):
    thread = Thread(target=re_make_pic, args=(id,))
    thread.start()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return 'Success'
    
    return render_template('index.html')




@app.route('/open_file_contenter')
def open_file_contenter():
    thread = Thread(target=open_file_content)
    thread.start()
    return redirect(url_for('index'))



@app.route('/open_floder_videoer')
def open_floder_videoer():
    thread = Thread(target=open_floder_video)
    thread.start()
    return redirect(url_for('index'))



@app.route('/open_floder_picer')
def open_floder_picer():
    thread = Thread(target=open_floder_pic)
    thread.start()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
