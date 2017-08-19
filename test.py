import  requests
#保存图片的一个测试
url="https://p1.pstatp.com/large/2a460002971f09d658d6?imageView2/2/w/690/h/1226"
reponse=requests.get(url)

file=open('1.jpg','wb')
file.write(reponse.content)
file.close()