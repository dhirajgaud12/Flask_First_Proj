import requests
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen
import urllib.parse
import logging
import pymongo
import threading



base_flipkart_url="https://www.flipkart.com/search?q="
userinput="5g mobile within 15000"
userinput= urllib.parse.quote(userinput)

list_phones=[]
for i in range(1,6):
    list_phones.append(base_flipkart_url+userinput+"&p%5B%5D=facets.price_range.from%3DMin&p%5B%5D=facets.price_range.to%3D15000"+"&page="+str(i))
print(list_phones)

pages={}
count=0
for i in list_phones:
    count=count+1
    pages["page"+str(count)]=bs(urlopen(i).read(),"html.parser")

phone_list=[]


for i in pages.values():
    for j in range(len(i.find_all("div",{"class":"_2kHMtA"}))):
        phone_list.append(base_flipkart_url+i.find_all("div",{"class":"_2kHMtA"})[0].a['href'])

    
len(phone_list)

phonecount=0
curr_phone_comments={}
phone_comment_count=0
phone_list_dict=[]

for i in phone_list:
    phonecount=phonecount+1
    temp=requests.get(i)
    temphtml=bs(temp.text,"html.parser")
    curr_comment_list=temphtml.find_all("div",{"class":"col _2wzgFH"})    
    
    for j in curr_comment_list:
        phone_comment_count=phone_comment_count+1
        curr_phone_comments[temphtml.find("span",{"class":"B_NuCI"}).text+" Rating {}".format(str(phone_comment_count))]= j.div.p.text
        curr_phone_comments[temphtml.find("span",{"class":"B_NuCI"}).text+" Comment {}".format(str(phone_comment_count))]= j.div.div.text
        phone_list_dict.append(curr_phone_comments)


client = pymongo.MongoClient("mongodb+srv://dhirajsantosh0:testing123@cluster0.l6luhul.mongodb.net/?retryWrites=true&w=majority")
db = client['phone_db']
phone_collection = db['Phone_List']
phone_collection.insert_many(phone_list_dict)
