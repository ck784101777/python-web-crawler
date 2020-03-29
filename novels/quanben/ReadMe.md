爬取全本小说网的全部小说

小说url：http://www.qb5.tw

本爬虫项目采用Scrapy框架

## 程序分析

下面看看爬虫架构的构思，如果你不了解Scrapy的各个组件，下面的内容对你来说有点难度，还是参考我文章开篇给出的链接。

这是我创建的目录结构，按照我上面的教程，你将的到一样的目录结构

我们要用到的有

quanben.py，这是主要的爬虫文件，主要的爬虫程序将在这个文件里写

items.py，实体类，用来存放爬取过程中的各类信息

pipelines.py，项目管道

setting.py ，用于写配置项信息

我们的爬虫程序将围绕这四个内容展开


**item**

首先我们要明确实体类，也就是我们要抓取的信息有什么，一个小说需要有小说名，小说类别，章节名，小说内容

```python
import scrapy


class Novelcrapy2Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    novel_topic = scrapy.Field()
    novel_name = scrapy.Field()
    novel_chapter = scrapy.Field()
    novel_content = scrapy.Field()
```

**pipeLine** 

爬虫管道，它的作用是将得到的item信息做处理，我们的目的是爬取小说并存文件，安装小说类别-》小说名-》小说章节，这样的目录结构去存为文件


```python
import os

class Novelcrapy2Pipeline(object):
def process_item(self, item, spider):
    # D:\\小说\\主题\\斗破苍穹\\第一章   这样的形式，加后缀就即可 这里做成.txt格式的文本
    dir = "D:\\小说\\" + item['novel_topic'] + "\\" + item['novel_name']
    if not os.path.exists(dir):
        os.makedirs(dir)
 
    #章节有可能有空格，存文件不允许有空格字符，所以要做下处理
    filename=dir + "\\" + item['novel_chapter'].replace('','_') + ".txt"
    with open(filename,'w',encoding="utf-8") as f:
         f.write("".join(item['novel_content']))
 
    print('ok')
 
    return item
```

**quanben**

特别注意，这里的quanben只是我创建的spider文件的名字，并不固定，根据你创建的爬虫项目而命名，但是上面两个是绝对的。

这个文件分析起来较为复杂，首先我们明确一下我们的目的，爬取某个小说网站的全部小说并存文件。这个工程量是非常大的，而且ip极其容易被封，我测试了3个小时，爬了大概4000千多本，但是由于这个程序是并发进行的，所以你爬到的某个小说并不一定能爬全(在程序没结束前），除非你等到你的爬虫程序结束，我预估要几天的时间，这取决于你的网速和你在setting里面设置的间隔时间，我设置的是1秒，所以爬的较慢，但是你不设置的话肯定是不行的，哪怕你设置零点几秒，或者你也可以使用daili（只能打拼音），这个要去买，租一天也就十几块钱（大概100个）。注意别被封了ip，不然你之后是访问不了这个网页的了。

这个程序我分了四级解析去处理，第一级解析是拿到小说的主题名和主题链接，拿到一个主题后将控制器移交给第二级解析。

二级解析有两个函数，第一个是遍历小说的页数，第二个是获取某一页下的所有小说名和小说链接。遍历了一页后，将控制器交给二级解析的第二个函数，这也是整个爬虫程序设计巧妙的地方，因为他总是并发进行的。第二个函数获取到了小说链接后就进第三级解析。

第三级解析的作用是拿到某篇小说下的所有章节和链接，拿到后将控制器移交给第四级解析。

第四级解析就是拿小说的内容了，到这里爬虫程序就拿到所有的数据了，我们的item就已经被填满了，这时候就要把控制器移交给pipeLine爬虫管道，爬虫管道将创建目录和小说文件，之后return item，这时候就彻底完成一次流程，就像工厂里的面生产线的一次循环，其结果就是造出了某个东西，但是生产线不会结束，其实return不return无所谓，重要的是你要知道前面做了5次移交控制器，也就是说有5个函数等着继续运行（每次移交控制器后将这个函数将中断，我不知道这么说合不合适，你也可以理解为线程堵塞）。第一个移交控制权的优先运行，此时又将走一篇流程，程序将不断的进行循环，直到爬取到所有小说。



```python
import scrapy
from ..items import Novelcrapy2Item

class QuanbenSpider(scrapy.Spider):
    name = 'quanben'
    allowed_domains = ['www.qb5.tw']
    start_urls = ['http://www.qb5.tw']
# 一级解析：获取主题
def parse(self, response):
    topic_list = response.xpath('//div[@class="head_t"]/ul/li[position()>1 and position()<9]')
    for i in topic_list:
        novel_topic = i.xpath('./a/@title').get()
        link = i.xpath('./a/@href').get()
 
        yield scrapy.Request(
            url=link,
            meta={'novel_topic':novel_topic},
            callback=self.parse_page
        )
# 二级解析：遍历页码数
def parse_page(self,response):
    novel_topic = response.meta['novel_topic']
    #<a href="https://www.qb5.tw/list/1/373.html" class="last">373</a>
    page_count = response.xpath('//div[@class="pagelink"]/a[@class="last"]/text()').get()
    url=response.url
    page_count=1
    for i in (1,page_count+1,1):
        link=url[:-5] + "/" + str(i) + ".html"
        yield scrapy.Request(
            url=link,
            meta={'novel_topic':novel_topic},
            callback=self.parse_two
        )
 
# 二级解析：获取主题下小说
def parse_two(self, response):
    novel_topic = response.meta['novel_topic']
    novle_lists = response.xpath('//div[@class="zp"]')
    for i in novle_lists:
        novel_name = i.xpath('./a/@title').get()
        link = i.xpath('./a/@href').get()
        yield scrapy.Request(
            url=link,
            meta={'novel_topic':novel_topic,'novel_name':novel_name},
            callback=self.parse_three
        )
 
# 三级解析：获取小说章节
def parse_three(self,response):
    novel_topic = response.meta['novel_topic']
    novel_name = response.meta['novel_name']
    chapter_list=response.xpath('//dd')
    for i in chapter_list:
        novel_chapter=i.xpath('./a/text()').get()
        # 不同网站的章节处理方式不一样，有些是绝对路径，有些是相对路径
        # 如果是相对路径就需要拼接
        link=self.start_urls[0]+i.xpath('./a/@href').get()
        yield scrapy.Request(
            url=link,
            meta={'novel_topic':novel_topic,'novel_name':novel_name,'novel_chapter':novel_chapter},
            callback=self.parse_fuor
        )
 
# 四级解析：获取小说内容
def parse_fuor(self,response):
    novel_topic = response.meta['novel_topic']
    novel_name = response.meta['novel_name']
    novel_chapter = response.meta['novel_chapter']
 
    item = Novelcrapy2Item()
    item['novel_topic']= novel_topic
    item['novel_chapter'] = novel_chapter
    item['novel_name'] = novel_name
    item['novel_content']=response.xpath('//div[@id="content"]/text()').extract()
 
    yield item
```
**setiing**

这个里面是配置项信息，我只写了需要处理的部分，实际上有很多项可以配置。不过下面列出的是一定要配置的，特别是请求头和下载间隔。 

```python
ROBOTSTXT_OBEY = False

DOWNLOAD_DELAY = 1

DEFAULT_REQUEST_HEADERS = {
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
  'Accept-Language': 'en',
  'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Safari/537.36'
}

ITEM_PIPELINES = {
   'novelCrapy2.pipelines.Novelcrapy2Pipeline': 300,
}
```

注意：在最后一级解析的地方创建item，前面解析到的小说名，小说主题，章节名通过request的meta传递。这个非常重要，如果你在四级解析之前创建了item并为item的键赋值，那么你到最后一级解析的时候需要重新为item赋值，因为程序是并发进行的，item值可能会被其它线程的值覆盖。



## 如何运行

使用编辑器打开，执行run.py即可运行，你需要到pipeline.py里修改一下小说的存放路径，默认是D:/小说



## 效果图

![img](https://img-blog.csdnimg.cn/20200329164342442.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2NrNzg0MTAxNzc3,size_16,color_FFFFFF,t_70)

![img](https://img-blog.csdnimg.cn/20200329164357939.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2NrNzg0MTAxNzc3,size_16,color_FFFFFF,t_70)



## 待优化的地方

1.有很多地方的xpath是写死的，如果网页结构变化可能会导致整个爬虫程序不可用

2.如果可以根据操作者的要求去爬取某一类别或某一篇具体的小说将会更加人性化

3.程序有很多隐含的问题，目前我还没能测试出来，非常欢迎各位码友贴出自己的优化结果