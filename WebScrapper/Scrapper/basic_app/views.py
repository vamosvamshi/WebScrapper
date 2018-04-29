from django.shortcuts import render
from basic_app import forms
from django.http import *
import csv
from bs4 import BeautifulSoup
import requests
import re
from time import sleep
import multiprocessing
import glob
from tkinter import *
import re
import time
import datetime
import urllib.request
import bs4 as bs
import xlsxwriter
import math
import os
from pyexcel.cookbook import merge_all_to_a_book

# Create your views here.
def index(request):
    return render(request, 'basic_app/index.html')

def google(request):
    form4 = forms.FormName_google()
    if request.method == 'POST':
        form4 = forms.FormName_google(request.POST)

        if form4.is_valid():
            print("validation success")
            TICKER = form4.cleaned_data["GoogleCompanyTicker"]
            STARTDATE = form4.cleaned_data["StartDay"]
            STARTMONTH = form4.cleaned_data["StartMonth"]
            STARTYEAR = form4.cleaned_data["StartYear"]
            ENDDAY = form4.cleaned_data["EndDay"]
            ENDMONTH = form4.cleaned_data["EndMonth"]
            ENDYEAR = form4.cleaned_data["EndYear"]
            response = StreamingHttpResponse(google_write(TICKER,STARTDATE,STARTMONTH,STARTYEAR,ENDDAY,ENDMONTH,ENDYEAR))
            return response
    return render(request, 'basic_app/Google.html',{'form4':form4})

def google_write(tckr,sd,sm,sy,ed,em,ey):

    '''sets the end and start dates from the text file to the values that would be used in the string and convert them to a string'''
    ticker = tckr.upper().strip()
    m1 = str(sm).strip()
    d1 = str(sd).strip()
    y1 = str(sy).strip()

    m2 = str(em).strip()
    d2 = str(ed).strip()
    y2 = str(ey).strip()
    start_date = ("{}/{}/{}".format(d1, m1, y1))
    print("start date is {}".format(start_date))
    end_date = ("{}/{}/{}".format(d2, m2, y2))
    # print("end date is {}".format(end_date))
    '''set the ticker value from the text file'''

    start_timestamp = time.mktime(datetime.datetime.strptime(start_date, "%d/%m/%Y").timetuple())
    end_timestamp = time.mktime(datetime.datetime.strptime(end_date, "%d/%m/%Y").timetuple())

    days = (end_timestamp - start_timestamp) / 86400
    effective_days = days * (5 / 7)
    pages = effective_days / 200
    print("timestamp difference {} days is {} and effective days is {} pages is{}".format((
        end_timestamp - start_timestamp), days, effective_days, math.ceil(pages)))

    no_of_pages = math.ceil(pages)

    list_count = 0
    split_nn_list = []
    xList = []
    month = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']

    for page_count in range(0,no_of_pages,1):

        url1 = "https://finance.google.com/finance/historical?q=NASDAQ:"+ticker+"&startdate="+month[int(
         m1)-1]+"+"+d1+"%2C+"+y1+"&enddate="+month[int(
            m2)-1]+"+"+d2+"%2C+"+y2+"&num=200&ei=HV3FWauPPIi_jAHlsozoAQ&start="+str(page_count*200)
        a = urllib.request.urlopen(url1).read()

        soup = bs.BeautifulSoup(a,'html.parser')

        table = soup.find_all('table',{'class':'gf-table historical_price'})
        '''xList filters the data from the website and appends it in the form of a string'''
        for x in table:
            xList.append(x.text)
        print("page "+str(page_count)+" done")
        '''split_nn_list will hold the total array of data particular to each day, splitting on \n\n'''
        try:
            split_nn_list.append(xList[int(page_count)].split('\n\n'))
        except:
            pass

    '''this is to print all whole list of values for all the pages info gathered'''
    #print('split_nn_list is \n',split_nn_list)
    workbook = xlsxwriter.Workbook('C:/Users/vamshi/Desktop/DATA_EXTRACTION/google/'+ticker+'--Google Finance Data.xlsx')
    worksheet = workbook.add_worksheet()
    '''j = 1 for incrementing the counter for writing the data into rows of excel'''
    j=1
    for a in split_nn_list:
        for b in a:
            row_string = 'A' + str(j)
            '''indiv_list is the single row element consisting of all the data required to be put in the row'''
            indiv_list = b.split('\n')
            yield(b)
            worksheet.write_row(row_string,indiv_list)
            j = j+1
        '''reinitializing the row_string to be zero after each iteration '''
        row_string = ''
    workbook.close()

def yahoo(request):
    form5 = forms.FormName_yahoo()
    if request.method == 'POST':
        form5 = forms.FormName_yahoo(request.POST)

        if form5.is_valid():
            print("validation success")
            TICKER = form5.cleaned_data["YahooCompanyTicker"]
            STARTDATE = form5.cleaned_data["StartDay"]
            STARTMONTH = form5.cleaned_data["StartMonth"]
            STARTYEAR = form5.cleaned_data["StartYear"]
            ENDDAY = form5.cleaned_data["EndDay"]
            ENDMONTH = form5.cleaned_data["EndMonth"]
            ENDYEAR = form5.cleaned_data["EndYear"]
            response = StreamingHttpResponse(yahoo_write(TICKER,STARTDATE,STARTMONTH,STARTYEAR,ENDDAY,ENDMONTH,ENDYEAR))
            return response
    return render(request, 'basic_app/Yahoo.html',{'form5':form5})

def yahoo_write(tckr,sd,sm,sy,ed,em,ey):
    ticker = tckr.upper().strip()
    m1 = str(sm).strip()
    d1 = str(sd).strip()
    y1 = str(sy).strip()

    m2 = str(em).strip()
    d2 = str(ed).strip()
    y2 = str(ey).strip()
    startdate = str(m1+"/"+d1+"/"+y1)
    enddate = str(m2+"/"+d2+"/"+y2)

    print (" start date is %s and type is %s " %(startdate,type(startdate)))
    print ("end date is %s and type is %s "%(enddate,type(enddate)))
    print("ticker is %s and type is %s" %(ticker,type(ticker)))

    timestamp_startdate = int(time.mktime(datetime.datetime.strptime(startdate, "%m/%d/%Y").timetuple()))
    timestamp_enddate = int(time.mktime(datetime.datetime.strptime(enddate, "%m/%d/%Y").timetuple()))
    timestamp_difference = int(timestamp_enddate) - int(timestamp_startdate)
    actual_end = (timestamp_enddate)
    actual_start = (timestamp_startdate)

    print("start time is ", int(timestamp_startdate))
    print("end time is ", int(timestamp_enddate))
    print("difference in timestamp is ", ((timestamp_enddate) - (timestamp_startdate)))

    step = int(10540800)
    table_complete = []

    pool_input_list = []
    pool_input_tuple = ()
    j=0
    for i in range(actual_start, actual_end, step):
        timestamp_startdate = timestamp_enddate - 10540800
        if (timestamp_startdate <= actual_start):
            timestamp_startdate = actual_start
        url_page = "https://finance.yahoo.com/quote/" + ticker + "/history?period1=" + str(
            timestamp_startdate) + "&period2=" + str(timestamp_enddate) + "&interval=1d&filter=history&frequency=1d"

        pool_input_list.append([[j,url_page]])
        timestamp_enddate = timestamp_startdate - 86400
        j = j+1
    pool_input_tuple = tuple(pool_input_list)
    print(pool_input_tuple)

    p = multiprocessing.Pool(processes=4)
    p.map(parsing_yahoo, pool_input_tuple)


    merge_all_to_a_book(glob.glob("C:/Users/vamshi/Desktop/DATA_EXTRACTION/yahoo/"+str(ticker)+"/*.xlsx"), "C:/Users/vamshi/Desktop/DATA_EXTRACTION/yahoo/"+str(ticker)+"/Yahoo Data combined.xlsx")


    rd = glob.glob("C:/Users/vamshi/Desktop/DATA_EXTRACTION/yahoo/"+str(ticker)+"/*.txt")
    with  open("C:/Users/vamshi/Desktop/DATA_EXTRACTION/yahoo/"+str(ticker)+"/Yahoo Data combined.txt","wb") as outfile:
        for f in rd:
            with open(f, "rb") as infille:
                outfile.write(infille.read())

    file = open("C:/Users/vamshi/Desktop/DATA_EXTRACTION/yahoo/"+str(ticker)+"/Yahoo Data combined.txt")
    lines = file.readlines()
    for line in lines:
        yield(line)
    file.close()


def parsing_yahoo(poolinput):
    k = re.findall("[A-Z]+", poolinput[0][1])
    print("k is {}",k)
    table_complete=[]
    for i in range(len(poolinput)):

        url = poolinput[i][1]
        print(poolinput[i][0])

        url1 = urllib.request.urlopen(url).read()

        soup = bs.BeautifulSoup(url1, 'html.parser')

        table = soup.find_all('tr')
        # append into table_complete the values after each iteration.
        table_complete.append(table)

    if not os.path.exists("C:/Users/vamshi/Desktop/DATA_EXTRACTION/yahoo/" + k[0]):
        os.makedirs("C:/Users/vamshi/Desktop/DATA_EXTRACTION/yahoo/" + k[0] + "/")
    workbook  = xlsxwriter.Workbook("C:/Users/vamshi/Desktop/DATA_EXTRACTION/yahoo/" + str(k[0]) + "/" + str(
        poolinput[i][0]).strip() + ".xlsx")
    worksheet = workbook.add_worksheet()

    f = open("C:/Users/vamshi/Desktop/DATA_EXTRACTION/yahoo/" + str(k[0]) + "/" + str(poolinput[i][0]).strip()+".txt","w+")
    print("process " + str(poolinput[i][0]) + " done")

    # initializing values to set the cell numbers
    i = 0
    j = 0
    for x in table_complete:
        for y in x:
            f.write(y.text + "\n\n")
            for z in y:
                #f.write(y.text + "\n\n")
                worksheet.write(j, i, z.text)
                print(z.text, end=",,")
                #yield (str(z.text + "\n"))
                i = i + 1
            i = 0
            print("\n")
            j = j + 1
    workbook.close()

def ebay(request):
    form3 = forms.FormName_ebay()
    if request.method == 'POST':
        form3 = forms.FormName_ebay(request.POST)

        if form3.is_valid():
            print("validation success")
            ITEMNO = form3.cleaned_data["EbayProductCode"]
            print("Item No is "+ITEMNO)
            response = StreamingHttpResponse(ebay_write(ITEMNO))
            return response
    return render(request, 'basic_app/Ebay.html',{'form3':form3})

def ebay_write(itm):

    item_number = itm.strip()
    '''item number of the product, different items have different items numbers in ebay'''
    '''change the ones that says itm =  "some number" to change the comments displayed'''
    #item_number = item_no[-1].strip()

    url1 = "https://www.ebay.com/urw/product-reviews/" + str(item_number) + "?_itm=1000047616"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'}
    a = requests.get(url1, headers=headers)
    soup = BeautifulSoup(a.content, "html.parser")

    '''to find the page number of the last page, so as to make it possible to loop so many times'''
    page_number = []
    try:
        table1 = soup.find_all("a", {"class": " spf-link"})
        for item in table1:
            page_number.append(item.text)
        '''last page it the second from the last'''
        print("last page number is " + page_number[-2])
        last_page = page_number[-2]
    except IndexError:
        last_page = 1

    pool_input_list = []
    pool_input_tuple = ()
    for i in range(int(last_page) + 1):
        url_last_page = url1 + "&pgn=" + str(i).strip()
        # print("url for page %d is %s"%(i,url_last_page))
        pool_input_list.append([[i, url_last_page]])
    pool_input_tuple = tuple(pool_input_list)
    print(pool_input_tuple)

    '''
    pool_input1 = ([[0, 'https://www.ebay.com/urw/product-reviews/110891711?_itm=1000047616&pgn=0'],
                   [1, 'https://www.ebay.com/urw/product-reviews/110891711?_itm=1000047616&pgn=1']],
                 [[0, 'https://www.ebay.com/urw/product-reviews/110891711?_itm=1000047616&pgn=0'],
                  [1, 'https://www.ebay.com/urw/product-reviews/110891711?_itm=1000047616&pgn=1']])

    pool_input1 = ([[0, 'https://www.ebay.com/urw/product-reviews/110891711?_itm=1000047616&pgn=0']],
                    [[1, 'https://www.ebay.com/urw/product-reviews/110891711?_itm=1000047616&pgn=1']],
                   [[0, 'https://www.ebay.com/urw/product-reviews/110891711?_itm=1000047616&pgn=0']],
                    [[1, 'https://www.ebay.com/urw/product-reviews/110891711?_itm=1000047616&pgn=1']])'''

    p = multiprocessing.Pool(processes=4)
    p.map(ParsingPage_ebay, pool_input_tuple)
    rd = glob.glob("C:/Users/vamshi/Desktop/DATA_EXTRACTION/ebay/"+str(item_number)+"/*.txt")
    with open("C:/Users/vamshi/Desktop/DATA_EXTRACTION/ebay/"+str(item_number)+"/Ebay Comments combined.txt","wb") as outfile:
         for f in rd:
            with open(f, "rb") as infille:
                outfile.write(infille.read())

    file = open("C:/Users/vamshi/Desktop/DATA_EXTRACTION/ebay/"+str(item_number)+"/Ebay Comments combined.txt")
    lines = file.readlines()
    for line in lines:
        yield(line)
    file.close()

def ParsingPage_ebay(pool_input1):
    k = re.findall("\d+",pool_input1[0][1])
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'}
    for i in range(len(pool_input1)):
        if not os.path.exists("C:/Users/vamshi/Desktop/DATA_EXTRACTION/ebay/"+k[0]):
            os.makedirs("C:/Users/vamshi/Desktop/DATA_EXTRACTION/ebay/"+k[0]+"/")
        f = open("C:/Users/vamshi/Desktop/DATA_EXTRACTION/ebay/"+k[0]+"/"+ str(pool_input1[i][0]).strip() + ".txt","w+")
        print("url from ParsingPage "+pool_input1[i][1])
        a = requests.get(pool_input1[i][1], headers=headers)
        soup = BeautifulSoup(a.content, "lxml")
        table2 = soup.find_all("p", {"itemprop": "reviewBody"})
        print("process " + str(pool_input1[i][0]) + " done")
        print(pool_input1[i][1])
        for item in table2:
            #yield(item.text)
            print(item.text)
            try:
                f.write(item.text + "\n\n")
            except:
                pass
        f.close()

def bestbuy(request):
    form2 = forms.FormName_bestbuy()
    if request.method == 'POST':
        form2 = forms.FormName_bestbuy(request.POST)

        if form2.is_valid():
            print("validation success")
            BESTBUYCODE = form2.cleaned_data["BestBuyProductCode"]
            print("BESTBUYCODE is "+BESTBUYCODE)
            response = StreamingHttpResponse(bestbuy_write(BESTBUYCODE))
            return response
    return render(request, 'basic_app/BestBuy.html',{'form2':form2})

def bestbuy_write(bbpc):
    product_id = str(bbpc).strip()
    url = "https://www.bestbuy.com/site/reviews/s/"+product_id
    #url = "https://www.bestbuy.com/site/reviews/s/"+str(product_id)+"?page=2&sort=MOST_HELPFUL"
    print(url)

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'}
    a = requests.get(url, headers=headers)

    soup = BeautifulSoup(a.content, "html.parser")
    # print(soup.text)
    page_number=[]
    table1 = soup.find_all("span",{"class":"message-text"})
    for item in table1:
        page_number.append(item.text)
        print(item.text)

    print("items in page_number are ",page_number[:])
    split_message = page_number[0].split(" ")
    print("the number of reviews are ",split_message[-2].replace(",",""))
    last_page = int(split_message[-2].replace(",",""))
    last_page=(last_page/20)+1
    print("last page is ",last_page)

    pool_input_list = []
    pool_input_tuple = ()
    for i in range(int(last_page) + 1):
        url_last_page = "https://www.bestbuy.com/site/reviews/s/" + str(product_id) + "?page=" + str(
            i) + "&sort=MOST_HELPFUL"
        pool_input_list.append([[i, url_last_page]])
    pool_input_tuple = tuple(pool_input_list)
    print(pool_input_tuple)

    p = multiprocessing.Pool(processes=4)
    p.map(ParsingPage_bestbuy, pool_input_tuple)
    #print("total time taken in multiprocessing pool is " + str(time.time() - t1))
    rd = glob.glob("C:/Users/vamshi/Desktop/DATA_EXTRACTION/bestbuy/"+str(product_id)+"/*.txt")
    with open("C:/Users/vamshi/Desktop/DATA_EXTRACTION/bestbuy/"+str(product_id)+"/BestBuy Comments combined.txt",
              "wb") as outfile:
        for f in rd:
            with open(f, "rb") as infille:
                outfile.write(infille.read())

    file = open("C:/Users/vamshi/Desktop/DATA_EXTRACTION/bestbuy/"+str(product_id)+"/BestBuy Comments combined.txt")
    lines = file.readlines()
    for line in lines:
        yield(line)
    file.close()


def ParsingPage_bestbuy(pool_input1):
    k = re.findall("\d+", pool_input1[0][1])
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'}
    for i in range(len(pool_input1)):
        if not os.path.exists("C:/Users/vamshi/Desktop/DATA_EXTRACTION/bestbuy/"+k[0]):
            os.makedirs("C:/Users/vamshi/Desktop/DATA_EXTRACTION/bestbuy/"+k[0]+"/")
        f = open("C:/Users/vamshi/Desktop/DATA_EXTRACTION/bestbuy/"+k[0]+"/"+ str(pool_input1[i][0]).strip() + ".txt",
                 "w+")
        #url1 = "https://www.bestbuy.com/site/reviews/s/" + str(product_id) + "?page=" + str(i) + "&sort=MOST_HELPFUL"
        a = requests.get(pool_input1[i][1], headers=headers)
        soup = BeautifulSoup(a.content, "html.parser")
        table2 = soup.find_all("p", {"class": "pre-white-space"})
        print("process " + str(pool_input1[i][0]) + " done")
        for item in table2:
            print(item.text)
            try:
                f.write(item.text + "\n\n")
            except:
                pass
    f.close()

def amazon(request):
    form1 = forms.FormName_amazon()
    if request.method == 'POST':
        form1 = forms.FormName_amazon(request.POST)

        if form1.is_valid():
            print("validation success")
            ASIN = form1.cleaned_data["AmazonProductCode"]
            print("ASIN is "+ASIN)
            response = StreamingHttpResponse(amazon_write(ASIN))
            return response
    return render(request, 'basic_app/Amazon.html',{'form1':form1})

def amazon_write(nm):
    ASIN = nm.strip()

    url2 = "http://www.amazon.com/product-reviews/" + ASIN + "/ref" \
                                                             "=cm_cr_arp_d_paging_btm_2?ie=UTF8&reviewerType=all_reviews"

    print(url2)

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'}
    a = requests.get(url2, headers=headers)

    soup = BeautifulSoup(a.content, "html.parser")
    table1 = soup.find_all("li", {"class": "page-button"})
    page = []

    for item in table1:
        item_removed_comma = (item.text).replace(",", "")
        page.append(int(item_removed_comma))
    print(page)
    page_max = page[-1]

    pool_input_list=[]
    pool_input_tuple=()
    for i in range(page_max):
        url2 = "http://www.amazon.com/product-reviews/" + ASIN + "/ref" \
                "=cm_cr_arp_d_paging_btm_2?ie=UTF8&reviewerType=all_reviews&pageNumber=" + str(i)
        pool_input_list.append([[i, url2]])
    pool_input_tuple = tuple(pool_input_list)
    print(pool_input_tuple)

    p = multiprocessing.Pool(processes=4)
    p.map(parsing_amazon, pool_input_tuple)

    rd = glob.glob("C:/Users/vamshi/Desktop/DATA_EXTRACTION/amazon/"+str(ASIN)+"/*.txt")
    with open("C:/Users/vamshi/Desktop/DATA_EXTRACTION/amazon/"+str(ASIN)+"/Amazon Comments combined.txt", "wb") as outfile:
        for f in rd:
            with open(f, "rb") as infille:
                outfile.write(infille.read())

    file = open("C:/Users/vamshi/Desktop/DATA_EXTRACTION/amazon/"+str(ASIN)+"/Amazon Comments combined.txt")
    lines = file.readlines()
    for line in lines:
        yield(line)
    file.close()
    '''
    # table = soup.find_all("div","span", { "class":"a-row review-data","class":"a-size-base review-text",\
    f = open("C:/Users/vamshi/Desktop/DATA_EXTRACTION/amazon/"+ASIN+"--Amazon Comments.txt", "w+")
    for i in range(1, page_max, 1):

        url2 = "http://www.amazon.com/product-reviews/" + ASIN + "/ref" \
                                            "=cm_cr_arp_d_paging_btm_2?ie=UTF8&reviewerType=all_reviews&pageNumber=" + str(i)
        print(url2)
        a = requests.get(url2, headers=headers)
        soup = BeautifulSoup(a.content, "html.parser")
        table2 = soup.find_all("span", {"class": "review-text"})

        # this is for printing the commments and writing the lines to the file.
        for item in table2:
            yield(item.text+"\n\n")
            try:
                f.write(item.text + "\n\n")
            except:
                pass

    f.close()'''
def parsing_amazon(pool_input):
    k = re.findall("[A-Z0-9]+", pool_input[0][1])
    print("k is ")
    print (k)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'}

    for i in range(len(pool_input)):
        #f = open("E:/Graduate Project/finance data/Amazon Comments.txt" + str(pool_input[i][0]).strip() + ".txt", "w+")
        if not os.path.exists("C:/Users/vamshi/Desktop/DATA_EXTRACTION/amazon/" + k[0]):
            os.makedirs("C:/Users/vamshi/Desktop/DATA_EXTRACTION/amazon/" + k[0] + "/")
        f = open("C:/Users/vamshi/Desktop/DATA_EXTRACTION/amazon/"+str(k[0])+"/" + str(pool_input[i][0]).strip()
                 +".txt",
                                                                       "w+")
        print(pool_input[i][1])
        url=pool_input[i][1]
        a = requests.get(url, headers=headers)
        #soup = BeautifulSoup(a.content, "lxml")
        soup = BeautifulSoup(a.content, "html.parser")
        table2 = soup.find_all("span", {"class": "review-text"})
        print("process " + str(pool_input[i][0]) + " done")
        # this is for printing the commments and writing the lines to the file.
        for item in table2:
            print(item.text + "\n")
            try:
                f.write(item.text + "\n\n")
            except:
                pass

    f.close()

def relative(request):
    return render(request, 'basic_app/relative_url_templates.html')
