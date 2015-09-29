# coding=gbk
import urllib2
import time

from BeautifulSoup import BeautifulSoup


def getHtml(url):
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:14.0) Gecko/20100101 Firefox/14.0.1',
              'Referer': '******'}
    request = urllib2.Request(url, None, header)
    response = urllib2.urlopen(request)
    text = response.read()
    return text


def mkDir():
    date = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    # os.mkdir(str(date))


def saveText(text):
    date = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    dir_name = "/home/wang/Documents/py/Zhihu/" + date
    soup = BeautifulSoup(text)
    #    i=1
    #    for i in soup.h2:
    #        i=i+1
    if soup.h2.get_text() == '':
        filename = dir_name + "/ad.txt"
        fp = file(filename, 'w')
        content = soup.find('div', "content")
        content = content.get_text()
        fp.write(content)
        fp.close()

    # elif i > 1:
    #        filename=dir_name+"/kiding.txt"
    #        contents=soup.findAll('div',"content")+soup.findAll("div","question")
    #        contents=contents.get_text()
    #        fp=file(filename,'w')
    #        fp.write(contents)
    #        fp.close()

    else:
        filename = dir_name + "/" + soup.h2.get_text() + ".txt"
        fp = file(filename, 'w')
        content = soup.find('div', "content")
        content = content.get_text()
        fp.write(content)
        fp.close()


# print content #test

def getPosts(url):
    html = getHtml(url)
    result = {}
    soup = BeautifulSoup(html.decode('utf-8'))
    posts = soup.findAll('div', {'class': 'post'})
    for post in posts:
        postdate = post.find('span', {'class': 'dateString'}).contents[0][:10]
        items_l = []
        for item in post.findAll('div', {'class': 'item'}):
            item_m = dict()
            href = dict(item.a.attrs)['href']
            title = str(item.a.span.contents[0]).decode('utf-8')
            item_m['href'] = href
            item_m['title'] = title
            items_l.append(item_m)
        result[postdate] = items_l
    print(result)
    return result


def test():
    s = """<div class="item">
				<a href="http://daily.zhihu.com/story/7155868" >
					<img src='/img/croped/http-__pic4.zhimg.com_a43debe06e9be6295b713db79408e033.jpg'  alt=''/>
					<span class='title'>明天就过期了，真的需要在晚上 11 点 50 吃掉那碗泡面吗？</span>
				</a>
			</div>""".decode('gbk')
    soup = BeautifulSoup(s)
    item = soup.find('div')
    print(item.a.attrs)


def main():
    mkDir()
    page = "http://zhihudaily.ahorn.me"
    posts = getPosts(page)
    for date in posts.keys():
        for item in posts[date]:
            print item['href'], item['title']


if __name__ == "__main__":
    main()
