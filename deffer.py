from datetime import datetime
import math
import os
import re
import shutil
import subprocess
import requests
import json
import base64
import random
import string
import time
from config import *
from gtts import gTTS
# 配置IMAGEMAGICK_BINARY环境变量
os.environ["IMAGEMAGICK_BINARY"] =x
from moviepy.editor import *
from pydub import AudioSegment
from PIL import Image
import edge_tts
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import hashlib
from nltk import *
import subprocess
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
# nltk.download('punkt')
# nltk.download('stopwords')
# nltk.download('averaged_perceptron_tagger')
from moviepy.editor import ImageClip, VideoFileClip



# 分割内容
# 保存到文件
# 文本
# 
def spliter(novel_text):
    # 创建一个名为"txt文件夹"的文件夹（如果不存在）
    if not os.path.exists("split_txt"):
        os.makedirs("split_txt")

    novel_text=clip_to_whole(novel_text)
    # 按句子分割文本
    sentences = re.split(r'(?<=[.。！？])', novel_text)

    # 合并相邻的句子
    merged_sentences = []
    current_sentence = ""
    for sentence in sentences:
        current_sentence += sentence
        if len(current_sentence) > 50:  # 合并后的句子长度超过50个字符时分割
            merged_sentences.append(current_sentence)
            current_sentence = ""
    if current_sentence:
        merged_sentences.append(current_sentence)

    # 使用TF-IDF计算句子相似度
    tfidf_vectorizer = TfidfVectorizer()
    tfidf_matrix = tfidf_vectorizer.fit_transform(merged_sentences)
    similarities = cosine_similarity(tfidf_matrix)

    similarity_threshold=0.7

    # 将相似句子组合成场景
    scenes = []
    current_scene = []
    for i in range(len(merged_sentences)):
        if not current_scene:
            current_scene.append(i)
        else:
            if similarities[current_scene[0]][i] > similarity_threshold:
                current_scene.append(i)
            else:
                scenes.append(current_scene)
                current_scene = [i]

    # 保存每个段落到文件
    for i, scene in enumerate(scenes):
        scene_sentences = [merged_sentences[i] for i in scene]
        scene_text = "".join(scene_sentences)
        filename = f"split_txt/{i+1}.txt"
        with open(filename, 'w', encoding='utf-8') as scene_file:
            scene_file.write(scene_text)
        print(scene_text)

    # 处理最后一段文本,否则会有丢失的情况
    if current_scene:
        last_scene_text = "".join([merged_sentences[i] for i in current_scene])
        last_filename = f"split_txt/{len(scenes)+1}.txt"
        with open(last_filename, 'w', encoding='utf-8') as last_scene_file:
            last_scene_file.write(last_scene_text)
        print(last_scene_text)



# add
def clip_to_whole(content):
    res_content = content.replace('"', "'").strip().replace("\n", "")
    return res_content



# 只是去掉了换行,二维
def text_clip_to_whole(contents):
    res_contents = []
    for content in contents:
        res_content=clip_to_whole(content)
        res_contents.append(res_content)
    return res_contents







# 返回的是二维数组
def text_to_voice(contents):
    try:
        shutil.rmtree('./tts')
        os.mkdir('./tts')
    except:
        pass

    voice = []

    first=1
    for lines in contents:
        filenames = []
        second=1
        for line in lines:
            # 执行相应的处理操作，例如：
            # line = line.replace('"', "'").strip().replace("\n", "")
            # filename = gtts(line)
            filename = _edge_tts(first, second, line)
            savefile(line,'./tts/'+str(first)+'.'+str(second)+'.txt')
            filenames.append(filename)
            second+=1
        first += 1
        voice.append(filenames)


# 获取音频文件名
# 0
# 二维
# def loadvoice():
#     result = []
#     current_dir = []
#     base_path = "./tts"
#     with os.scandir(base_path) as entries:
#         for entry in entries:
#             if entry.is_file() and entry.name.endswith(".mp3"):
#                 current_dir.append(os.path.join("tts", entry.name))

#     current_dir.sort()
#     result.append(current_dir)
    
#     return result



#add
# 转换为音频
def _edge_tts(first,second,content):
    # voice = 'zh-CN-YunxiNeural'
    # rate = '-4%'
    # volume = '+0%'
    # filename = './tts/%s.mp3' % content
    # tts = edge_tts.Communicate(text=content, voice=voice, rate=rate, volume=volume)
    # tts.save(filename)
    filename = 'tts/'+str(first)+"."+str(second)+'.mp3'
    cmd = 'edge-tts --voice zh-CN-YunxiNeural --text "' + content + '" --write-media %s' % filename
    subprocess.call(cmd, shell=True)
    # tts/1.1.mp3
    sound = AudioSegment.from_mp3(filename)
    duration = int(sound.duration_seconds)
    update_name = '%s.%s_duration_%f.mp3' % (filename.split('.')[0],filename.split('.')[1], duration)
    os.rename(filename, update_name)
    return update_name




# 文本生成图片
# 一维数组
# 
def text_to_pic(contents):
    i=1
    for content in contents:
        getTxt2Image(','.join(content),ADDER_PROMOTE,"./",i)
        i=i+1



#add
def getTxt2Image(text_prompt,add_prompt,localPythonExePath,num):#文生图核心方法#localPythonExePath是本地存储路径
    serverName = "server001"
    txt2img_url = Stable_diff_api+'/sdapi/v1/txt2img'
    print("提示词："+text_prompt)
    data = {'prompt': text_prompt+add_prompt+'(masterpiece:1,2), best quality, highres, original, extremely detailed wallpaper, perfect lighting,(extremely detailed CG:1.2),',
            'brach_size': 1,
        #    "sampler_name": "DPM++ 2m Karras",#可自行选择
           "steps": 20,
           "cfg_scale": 8, #提示词相关性
           "width" : 740,
           "height": 580,
           "restore_faces": "true",
           "negative_prompt": "NSFW, (worst quality:2), (low quality:2), (normal quality:2), lowres, normal quality, ((monochrome)), ((grayscale)), skin spots, acnes, skin blemishes, age spot, (ugly:1.331), (duplicate:1.331), (morbid:1.21), (mutilated:1.21), (tranny:1.331), mutated hands, (poorly drawn hands:1.5), blurry, (bad anatomy:1.21), (bad proportions:1.331), extra limbs, (disfigured:1.331), (missing arms:1.331), (extra legs:1.331), (fused fingers:1.61051), (too many fingers:1.61051), (unclear eyes:1.331), lowers, bad hands, missing fingers, extra digit,bad hands, missing fingers, (((extra arms and legs))),"
           }
    data.update(Stable_diff_conf)
    response = submit_post(txt2img_url, data)
    save_encoded_image(response.json()['images'][0], ".\pictures\image"+str(num)+".png")
    print("图片已经生成,并保存在pictures目录中")


#add
def save_encoded_image(b64_image: str, output_path: str):
   with open(output_path, "wb") as image_file:
       image_file.write(base64.b64decode(b64_image))

#add
def submit_post(url: str, data: dict):#发出Post请求
   return requests.post(url, data=json.dumps(data))




# 生成视频
# 传入两个二维数组
# 
def handle_movie(voice,txts):
    final_duration_clips = []
    txts=txts
    voice=voice
    print(len(voice))
    print(len(txts))

    for item in voice:
        duration_clips = []
        for line in item:
            filename = str(line.split('/')[-1])
            tmp = filename.split('_')
            # 获取语音文件名中的时长
            duration_clips.append(float(tmp[-1].replace('.mp3', '')))
        final_duration_clips.append(duration_clips)


    final_clip_all=None
    for i in range(len(txts)):

        # final_duration_clips[i]
        # txts[i]
        # voice[i]

        # 解说 + 字幕
        final_clip=None
        for j in range(len(txts[i])):

            # 计算当前行的起始时间和结束时间

            print("="*50)
            print("i, j ---> " + str(i) + ", " + str(j))
            print(voice[i][j])
            print(txts[i][j])
            print(final_duration_clips[i][j])
            print(str(i+1)+".png")


            start = 0
            end = start + final_duration_clips[i][j]

            print("strat:"+str(start))
            print("strat:"+str(end))

            print("="*50)


            # 添加语音剪辑
            voice_clip = AudioFileClip("./"+voice[i][j]).set_start(start).volumex(1.2)

            # 添加字幕剪辑
            screensize = (700,200)
            # txt_clip = TextClip(txts[i][j], fontsize=30, color='black', font='MaoKenWangXingYuan.ttf', stroke_color='black',stroke_width=0.3,size = screensize, method='caption')
            txt_clip = TextClip(txts[i][j], fontsize=30, color='white', font='MaoKenWangXingYuan.ttf',size = screensize, method='caption')
            txt_clip = txt_clip.set_pos('bottom').set_duration(final_duration_clips[i][j])
            txt_clip = txt_clip.set_start(start).set_end(end)

            # 计算视频中每张图片的剪辑长度
            # 定义镜头焦点效果
            def resize_func(t):
                # return 1 + 0.001*t
                return 1
            # 添加每张图片的剪辑，并设置位置、时长、帧率等属性
            image_clip = ImageClip("./pictures/image"+str(i+1)+".png").set_duration(final_duration_clips[i][j]).resize(resize_func).set_position(('center', 'center')).set_fps(25)
            # image_clip = image_clip.crossfadein(1).crossfadeout(1)


            # 将图像、字幕和音频剪辑合并为一个剪辑，并添加淡入淡出效果
            video_clip = CompositeVideoClip([image_clip,txt_clip])
            video_clip = video_clip.set_audio(voice_clip)
            if final_clip is None:  # 添加此行代码
                final_clip = video_clip  # 添加此行代码
            else:
                final_clip = concatenate_videoclips([final_clip,video_clip])


        if final_clip_all is None:  # 添加此行代码
            final_clip_all = final_clip  # 添加此行代码
        # 这一行使后来加的
        else:
            final_clip_all = concatenate_videoclips([final_clip_all,final_clip])

        # 导出视频剪辑
        # final_clip.write_videofile("video/"+str(i+1)+".mp4", fps=25)


    current_time = datetime.now()
    time_string = current_time.strftime("%Y_%m_%d_%H_%M_%S")
    print(time_string)

    # 这一行使后来加的
    final_clip_all.write_videofile("video/"+time_string+".mp4", fps=25)
    print("*"*50)
    print("完成！")




















# 内容翻译
# 一维数组
# 一维数组
def translate(fileContents):
    resultered=[]
    for fileContent in fileContents:
        textTranslatedtoEnglish=json.loads(translater(fileContent))
        resulter=textTranslatedtoEnglish['trans_result']
        resulter=handleResult(resulter)
        resultered.append(resulter)
    return resultered

# 
# 
# 
def translater(query):
    # Set your own appid/appkey.
    appid = '20230925001829106'
    appkey = 'GibMVhrk0dwgvV6Lt_iD'

    # For list of language codes, please refer to `https://api.fanyi.baidu.com/doc/21`
    from_lang = 'zh'
    to_lang =  'en'

    endpoint = 'http://api.fanyi.baidu.com'
    path = '/api/trans/vip/translate'
    url = endpoint + path

    # Generate salt and sign
    def make_md5(s, encoding='utf-8'):
        return hashlib.md5(s.encode(encoding)).hexdigest()

    salt = random.randint(32768, 65536)
    sign = make_md5(appid + query + str(salt) + appkey)

    # Build request
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    payload = {'appid': appid, 'q': query, 'from': from_lang, 'to': to_lang, 'salt': salt, 'sign': sign}

    # Send request
    r = requests.post(url, params=payload, headers=headers)
    result = r.json()

    time.sleep(0.2)

    # Show response
    return (json.dumps(result, indent=4, ensure_ascii=False))

# add
def handleResult(resulter):
    returned = ""  # 初始化一个空字符串用于存储结果
    for i in resulter:
        # resulter中的每个元素（假设是一个字典）中的dst值取出来，用逗号连接起来，最终返回一个字符串。
        returned += i['dst']+","  # 修正这里的索引
    return returned






# 提取关键词
# 一维数组
# 二位数组
def use_extract_keywords(texts):
    re_texts=[]
    for text in texts:
        re_text=extract_keywords(text)
        re_texts.append(re_text)
    return re_texts

#add
def extract_keywords(text):
    # 将文本拆分成单词
    words = text.split()

    # 创建一个用于存储短语的列表
    phrases = []

    # 创建一个集合用于跟踪已经出现过的单词
    seen_words = set()
    n=3
    # 生成n-gram短语
    for i in range(len(words) - n + 1):
        phrase = ' '.join(words[i:i + n])
        # 检查短语中是否有已经出现的单词
        if not any(word in seen_words for word in phrase.split()):
            phrases.append(phrase)
            # 将短语中的单词添加到已经出现过的单词集合中
            seen_words.update(phrase.split())

    return phrases



# 将每个段落拆分成句子,一维变二维
# 一维数组
# 二维
def dozen_txt_double(contents):
    doublelist=[]
    for content in contents:
        innerlist = []
        lines=split_sentences(content)
        for line in lines:
            innerlist.append(line)
        doublelist.append(innerlist)
    return doublelist

# add
# 将每个段落拆分成句子

def split_sentences(text):
    # 去除文本中的引号
    text = text.replace('"', '').replace('“', '').replace('”', '').replace('‘', '').replace('’', '')
    # 将文本按照换行符进行切割
    lines = text.split('\n')
    # 去除每行开头和结尾的空格，并去除空行
    lines = [line.strip() for line in lines if line.strip()]
    # 将每个段落拆分成句子
    sentences = []
    for line in lines:
        # 按照句号、问号、感叹号等标点符号进行拆分
        sentences.extend(re.split(r'[.!?。？！]+', line))

    # 去除句子开头和结尾的空格，并去除空句子
    sentences = [sentence.strip() for sentence in sentences if sentence.strip()]
    # 返回结果
    return sentences
















def delete_files_in_folder(folder_path):
    try:
        # 获取文件夹中的所有文件列表
        file_list = os.listdir(folder_path)

        # 遍历文件列表并删除每个文件
        for filename in file_list:
            file_path = os.path.join(folder_path, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)

        print("所有文件已成功删除。")
    except Exception as e:
        print("发生错误：{str(e)}")


def delete_file(file_name):
    if os.path.exists(file_name):
        os.remove(file_name)
        print("成功删除文件"+file_name)
    else:
        print("文件\""+file_name+"\"不存在，已经忽略")



def get_all_pic_files(path):
    files = []
    for i in range(1, get_cont()+1):
        filename = f"{i}.png"
        file_path = os.path.join(path, filename)
        if os.path.exists(file_path):
            files.append(file_path)
    return files




def savefile(content,name):
    # 打开文件，如果文件不存在将会创建新文件
    file = open(name, "w",encoding='utf-8')
    # 写入内容到文件
    file.write(content)
    # 关闭文件
    file.close()



# def load_voice():

#     # 指定文件夹路径
#     folder_path = './tts'

#     # 获取文件夹中所有以.mp3结尾的文件
#     mp3_files = [filename for filename in os.listdir(folder_path) if filename.endswith('.mp3')]

#     # 定义一个自定义排序函数，按照文件名中的数字部分进行排序
#     def custom_sort(filename):
#         # 提取文件名中的数字部分作为排序关键字
#         match = re.search(r'\d+', filename)
#         if match:
#             return int(match.group())
#         else:
#             return 0  # 如果没有找到数字部分，默认为0

#     # 对文件名进行排序
#     sorted_files = sorted(mp3_files, key=custom_sort)

#     return sorted_files





def load_voice():
    # 指定文件夹路径
    folder_path = './tts'

    # 获取文件夹中所有以.mp3结尾的文件
    mp3_files = [filename for filename in os.listdir(folder_path) if filename.endswith('.mp3')]

    # 定义一个自定义排序函数，按照文件名中的数字部分进行排序
    def custom_sort(filename):
        # 提取文件名中的数字部分作为排序关键字
        match = re.search(r'\d+\.\d+', filename)
        if match:
            return tuple(map(int, match.group().split('.')))
        else:
            return (0, 0)  # 如果没有找到数字部分，默认为(0,0)

    # 对文件名进行排序
    sorted_files = sorted(mp3_files, key=custom_sort)

    # 将文件名按照行号分组，存储在二维列表中
    voice = []
    for filename in sorted_files:
        match = re.search(r'(\d+)\.\d+', filename)
        if match:
            line_num = int(match.group(1))
            while line_num > len(voice):
                voice.append([])
            voice[-1].append(folder_path+'/'+filename)
    return voice






# 获取文本
# 0
# 一维
def loadtxt():
    contents=[]
    for i in range(1,get_cont()+1):
        helloFile=open("split_txt/"+str(i)+".txt",encoding='utf-8')
        fileContent=helloFile.read()
        contents.append(fileContent)
        helloFile.close()
    return contents


# 获取章节数
def get_cont():
    cont=0
    with os.scandir('split_txt') as entries:
        for entry in entries:
            if entry.is_file():
                cont=cont+1
    return cont



# 读取小说文本
# 文件名
# 文本
def get_whole_file(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        novel_text = file.read()
    return novel_text


# def get_cont2():
#     cont=0
#     with os.scandir('video') as entries:
#         for entry in entries:
#             if entry.is_file():
#                 cont=cont+1
#     return cont



# 二维list


def double_txt(contents):
    doublelist=[]
    for content in contents:
        lines=split_sentences(content)
        innerlist = []
        for line in lines:
            innerlist.append(line)
        doublelist.append(innerlist)
    return doublelist






# 重构图片
# 序号 附加的关键词
# 0
def re_create_pic(num,prom):
    delete_file('image'+str(num)+".png")
    getTxt2Image(translater(get_txt_by_num(num)),prom,"./",num)
    # getTxt2Image(translater(clip_to_whole(get_txt_by_num(num))),prom,"./",num)

#add
def get_txt_by_num(num):
    helloFile=open("split_txt/"+str(num)+".txt",encoding='utf-8')
    fileContent=helloFile.read()
    helloFile.close()
    return fileContent




def open_file_content():
    os.startfile('content.txt')



def open_floder_video():
    os.system(f'start explorer "video"')



def open_floder_pic():
    os.system(f'start explorer "pictures"')

