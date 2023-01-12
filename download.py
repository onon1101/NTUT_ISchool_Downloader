import os, sys
import threading
import requests
import json
import time
from contextlib import closing
from tqdm import tqdm
from queue import Queue


q = Queue()
name = [i*0 for i in range(10)]
fileSize = [i*0 for i in range(10)]
current_download_status = [i*0 for i in range(10)]

user_header = {
	"Accept"           : "text/html,application/xhtml+xml,application/xml;\
q=0.9,*/*;q=0.8",
	"Accept-Encoding"  : "gzip, deflate, br" ,
	"Accept-Language"  : "zh-TW" ,
'User-Agent': 'Mozilla/5.0 (Macintosh Intel Mac OS X 10_13_4)\
AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
	"Cache-Control": "max-age=0",
	"Upgrade-Insecure-Requests": "1",
	"Referer": "https://nportal.ntut.edu.tw/index.do?thetime=1556366755131"
}


#下載的fuc
def download(index,videoUrl,fileName,LoaclPath):
    #第幾號線程
    ThreagNumber = int(threading.current_thread().name)

    #產生檔案名稱
    # print(fileName)
    # fileName = fileName.split(' ')[1]
    saveName = LoaclPath + "\\" + fileName #影片路徑
    
    #爬蟲
    with closing(requests.get(videoUrl, stream=True )) as response:
        
        
        if response.headers.__contains__('content-length'):
            file_size = response.headers['content-length']  
        else:
            file_size = 0
        chunk_size = 1024 # 單次請求最大值
        fileSize[ThreagNumber] = content_size = int(file_size) # 內容體總大小
        

        #產生影片檔案
        with open(saveName,'wb') as file:
            for data in response.iter_content(chunk_size=chunk_size):
                #寫入影片的資料
                file.write(data)

                #回傳下載的進度
                q.put(
                    [ThreagNumber,
                    len(data)]
                )

        file.close()
        sys.exit()
        

#進度條累加計算
def progressBar(q):
    global current_download_status

    threadingName = int(q[0])
    packageSize = q[1]

    #增加進度條的進度
    name[threadingName].update(1024)
    current_download_status[threadingName] += 1024


#主要功能區
def downloadMain(data:list,fileName,LocalPath):
    
    #計算需要下載的資料有幾筆
    DataTotal = len(data)
    threads = []
    
    #編號跟資料的生成 ex: (1,'data')
    data = list(enumerate(data))


    for i in range(DataTotal):
        
        # 產生多進程 以download function 為單位
        threads.append(threading.Thread(
            target=download,
            args=(data[i][0],data[i][1],fileName[i],LocalPath),
            name=str(i)
        ))
        
        # 開始執行    
        threads[i].start()

    #等待進程都執行的差不多後
    time.sleep(1) 


    for i in range(DataTotal):
        if name[i] == 0:

            #將進度條的空位補滿            
            ProgressBarName = fileName[i]
            if len(ProgressBarName) <=26:
                ProgressBarName = ProgressBarName + " "*3

            #產生進度條並存到陣列裡面
            name[i] = tqdm(total = fileSize[i], desc=ProgressBarName, unit='B', unit_scale=True)
            
            
    #開始計算進度
    while any(fileSize[i] > current_download_status[i] for i in range(len(fileSize))):
            progressBar(q.get())


if __name__ =="__main__":
    with open('data.json') as file:
        data = json.load(file)['web']
    datalist= []
    path = "北科i學園資料\微積分"
    fileName = ['[錄] 12291329_src_presenter.mp4', '[錄] 01040827_src_presenter.mp4', '[錄] 01051320_src_presenter.mp4']
    
    for i in data:
        datalist.append(i)
    
    downloadMain(datalist,fileName, path)
    # print(threading.active_count())
    os.system('cls')
    print("下載完成, ", end='')
    input("按任意建結束");
    
    try:
        os._exit(0)
    
    except:
        print('子程序出現錯誤')
