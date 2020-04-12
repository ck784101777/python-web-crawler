## ImagesPipeline模块说明

ImagesPipeline是Scrapy中的一个pipe管道组件的一个插件模块，封装了对图片爬取的一些处理，是Scrapy给出的图片处理方案，可以避免我们重复造轮子，我们只要拿到图片链接丢给这个管道，其他的不用我们管，包括图片的命名和后缀名处理，图片存储地址（需要修改默认值），图片长宽处理等。

下面是ImagesPipeline的源码，这里仅讲两个函数

第一个函数是get_media_requests，该函数的作用是下载图片，调用item中图片的链接（我们一般将图片链接存在item中），调用Request函数进行下载，默认的函数写死了，我们还需要进行一些处理才可以拿到图片链接。

```python
def get_media_requests(self, item, info):
    return [Request(x) for x in item.get(self.images_urls_field, [])]
```

第二个函数是file_path,定义下载图片存储的路径，我们需要处理一下，以此把图片存储到我们想存储的地方

```python
def file_path(self, request, response=None, info=None):
    image_guid = hashlib.sha1(to_bytes(request.url)).hexdigest()
    return 'full/%s.jpg' % (image_guid)
```



## 程序思路

详细请看csdn讲解https://blog.csdn.net/ck784101777/article/details/105466589



## 运行程序

将项目下载到本地后使用编辑器打开如PyChram，执行run.py输入搜索内容即可

注意：需要修改setting.py里的IMAGES_STORE= 'D:\\图片\\'调整下载路径