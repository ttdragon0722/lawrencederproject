#import and general setting
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from data import *

options = Options()
options.add_argument("--disable-notifications")

chrome = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)


#開啟網站
chrome.get("https://www.block.tw/test/select/1")
#等待網頁載入 最多10秒 偵測到id為sendButton的元素後即停止等待
try:
    element = WebDriverWait(chrome, 10).until(
        EC.presence_of_element_located((By.ID, "sendButton"))
    )
finally:
    pass
#設定題目數量為最大 因為基本電學的總題目為474題 設定為474即可
chrome.execute_script("document.getElementById('number').setAttribute('max',474)")
questionAmount = chrome.find_element(By.XPATH,"//*[@id='number']")
questionAmount.send_keys(474)
#全選所有題目
chrome.execute_script("document.getElementById('allsub').click()")
submit = chrome.find_element(By.XPATH,"//*[@id='sendButton']")
submit.click()
#等待題目載入 最多10秒 偵測到id為exam_send的元素後即停止等待
try:
    element = WebDriverWait(chrome, 10).until(
        EC.presence_of_element_located((By.ID, "exam_send"))
    )
finally:
    pass
#直接交卷看結果
chrome.execute_script("send_question()")
#變更每頁顯示所有題目(因為題目數量為474題，所以每頁顯示474題)
chrome.execute_script("change_display(474)")
#因為有474題 所以用一個迴圈去跑474次 偵測每題的題目、選項、解析
for i in range(1,11):
    question = chrome.find_element(By.ID,"question"+str(i))
    questionText = question.find_element(By.TAG_NAME,"font").text
    #偵測四個選項中哪個是正確答案
    for j in range(1,5):
        try:
            answer = question.find_element(By.CLASS_NAME,f"ans{j} right-ans")
            answer = answer.find_element(By.CLASS_NAME,"ans-select").text
            break
        except:
            answer = ""
    #取得所有選項的文字(不包含A、B、C、D四個字)
    option1 = question.find_element(By.CLASS_NAME,"ans1").text.replace("A\n","")
    option2 = question.find_element(By.CLASS_NAME,"ans2").text.replace("B\n","")
    option3 = question.find_element(By.CLASS_NAME,"ans3").text.replace("C\n","")
    option4 = question.find_element(By.CLASS_NAME,"ans4").text.replace("D\n","")
    if "\n" in option1:
        option1 = option1.replace("\n","^",1)
        option1 = option1.replace("\n","",1)
    if "\n" in option2:
        option2 = option2.replace("\n","^",1)
        option2 = option2.replace("\n","",1)
    if "\n" in option3:
        option3 = option3.replace("\n","^",1)
        option3 = option3.replace("\n","",1)
    if "\n" in option4:
        option4 = option4.replace("\n","^",1)
        option4 = option4.replace("\n","",1)
    try:
        solutionbtn = question.find_element(By.ID,f"sol_button{i}")
        solutionbtn.click()
        #等待解析渲染完畢
        time.sleep(0.5)
        #在sol_button裡面找到class為sol bd-callout bd-callout-danger的元素
        solutionArea = solutionbtn.find_element(By.XPATH,f"//*[@id='solbutton{i}']/div")
        #再從上面的元素中找到所有的p標籤
        solution = solutionArea.text
    except:
        solution = "無解析"
    print(answer)
    addQuestion(questionText,answer,solution,"",option1,option2,option3,option4,True)
    print(f"第{i}題已加入資料庫")

time.sleep(15)