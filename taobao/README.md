## 使用文档：
### modules.py
> sleepRandom(t): 随机睡眠 t + 60~80 秒
> excel_spilt(limit): 不常用，分割表格用，limit 为分割得到的数量
> set_table(): 建表，SQL 语句存在 sec_data/sql_table.txt 中，返回 db 和 cursor
> keywords_reader(): 读入表格中的关键字，返回列表

### core.py
> Searcher 类：
> 1. 初始化：__init__(self, url, db, cursor)
> 2. 获取数据并插入数据库：get_data(self, cookies)
>
> Cookier 类: 初始化无传入参数
> 1. 自动滑动验证码：cookie_main(self, url, cookies)
>
> Downloader 类：
> 下载图片，备用


### main.py
> 需要输入要爬取的表格
> 先将 cookies 粘贴到 sec_data/cookies.txt, 然后读入

### 说明：
- 先将表格分割为多份，务必这样做，麻烦一点结果稳，可适当增加每个表格里的关键字数目
- 分割后的表格自动编号，请自己记住爬虫进度
- cookie_main 函数可以自动更新 cookie，但是尽量不要使用它，所以每爬取一个表格之后，请休息一段时间
- 并行爬虫请复制多份代码，并使用不同的 cookies
- 最后不要出现 cookies 过度使用的情况