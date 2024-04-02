from deffer import *

def delete_folder_files(folder):
    if(folder=='pictures'):
        delete_files_in_folder('pictures')
    if(folder=='video'):
        delete_files_in_folder('video')
    if(folder=='split_txt'):
        delete_files_in_folder('split_txt')
    if(folder=='tts'):
        delete_files_in_folder('tts')


# delete_file('output.mp4')



def make_text():
    spliter(get_whole_file('content.txt'))

    print("*"*50)
    print("完成！")

def make_tts():
    contents=loadtxt()
    contents_double=dozen_txt_double(contents)
    text_to_voice(contents_double)
    print("*"*50)
    print("完成！")

def make_pic():
    contents=loadtxt()
    text_to_pic(use_extract_keywords(translate((contents))))

    print("*"*50)
    print("完成！")


def make_movie():
    handle_movie(load_voice(),double_txt(loadtxt()))
    print("*"*50)
    print("完成！")


def re_make_pic(num):
    prom=''
    re_create_pic(num,prom)

    print("*"*50)
    print("完成！")





# # # 一维片段
# contents=spliter(clip_to_whole(get_whole_file('content.txt')))
# # # 对每个维度生成照片
# text_to_pic((use_extract_keywords(translate((contents)))))
# # # 拆分为二维片段，对每一个片段进行内部拆分,一维变二维，方便语音生成和文字配
# contents_double=choose_and_use_split_func(contents)
# # # 转语音
# voice=text_to_voice(contents_double)
# # # 输出为视频
# handle_movie(load_voice(),contents_double)



