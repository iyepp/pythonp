import requests as req
import bs4
import openpyxl as xl
import pandas as pd

# csv데이터 불러오기
df = pd.read_csv('./The list.csv')

links = df['Link']
#print(links)

# 읽어 올 웹페이지 주소
url = links

# 웹페이지 내용 읽어 오기
for u in url:
    res = req.get(u)

# 읽어 온 웹페이지 내용 출력

# 특정 요소만 검색하기, 검색한 요소 출력하기
    bs = bs4.BeautifulSoup(res.text, features = "html.parser") # 가져온 값 html 분석하기

    info = bs.select(".productnameandprice-container-standard")
    details = bs.select("#accordion-product-details")
    infoList = [] # 리스트를 선언/ 제품정보 (빈)목록

    for i in info:
        name = i.select_one('h1.product-name.product-detail-product-name').getText().strip()
        price = i.select_one('div.product-price.product-detail-price').getText().strip()
    #print(name)
    #print(price)

    for d in details:
        pn = d.select_one('div.style-number-title').span.getText().strip()
        img = "http:" + d.select_one('picture.product-thumb').img['srcset']
    #print(pn)
    #print('https:' + img)

        infoList.append({'name':name, 'price':price, 'pn':pn, 'img':img}) # 받은 결과 값을 리스트에 더한다/ 제품정보 추가
        #print(infoList)

# 불러온 내용 엑셀에 저장하기

    wb = xl.Workbook() #엑셀을 연다
    sheet = wb.active  #엑셀의 기본 시트를 가지고 온다
    sheet.title = "GUCCI LIST"

    row = 1 #열은 두번째 열에서 시작
    col = 1 #행은 첫번째 행에서 시작

    for c in infoList:
        sheet.cell(row = row, column = col).value = c["img"]
        col = col + 2
        for c in infoList:
            sheet.cell(row = row + 1, column = col).value = c["name"]
            sheet.cell(row = row + 3, column = col).value = c["pn"]
            col = col + 1
            for c in infoList:
                sheet.cell(row = row + 4, column = col).value = c["price"]
                row = row + 10

    wb.save("DS with Python.xlsx")




