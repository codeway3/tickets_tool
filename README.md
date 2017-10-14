# tickets_tool
### 12306火车票查询工具

## 使用方法  
命令行运行，用-h或--help查询具体参数用法  
  
## 更新
* **2016.10**  
实现基本功能， 分析发送的请求， 提取查询信息  
添加到站日期显示， 添加硬座、商务座查询列  
日期已支持YYYYMMDD格式， 添加彩色车站信息标识  
* **2017.03**  
对于12306查询重新进行解析， 添加virtualenv， 添加包依赖信息requirement.txt  
利用docopt进行命令行参数自动解析，并按参数筛选符合条件的结果进行显示； 修复一个历时显示错误的bug  
* **2017.04**  
针对12306查询url的改动进行更新； 修复了默认不传入参数时不返回查询结果的bug  
更新 添加pinyin模块以解析汉字输入  
* **2017.07**  
由于12306数据格式大量变动， 重新分析了数据组成， 重写数据解包代码  
修新bug， 改动代码以符合PEP8  
* **2017.09**  
重构代码  
* **2017.10**  
更改url模板  
更改docopt并添加异常处理， 增强代码鲁棒性  


## 参考资料
[实验楼文档](https://www.shiyanlou.com/courses/623/labs/2072/document)  
[prettytable文档](https://code.google.com/archive/p/prettytable/wikis/Tutorial.wiki)  
[virtualenv参考资料](http://www.nowamagic.net/academy/detail/1330228)  
[docopt参考资料](http://www.tuicool.com/articles/36zyQnu)  
[汉字转拼音参考资料](http://www.cnblogs.com/code123-cc/p/4822886.html)

## ToDoList
- [x] 添加参数解析功能与对应结果筛选
- [x] 添加中文车站名查询功能
- [x] 增强代码鲁棒性
