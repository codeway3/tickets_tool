# tickets_tool
### 12306火车票查询工具
  
## 使用  
命令行运行，用-h或--help查询具体参数用法  
  
## 示例  
![image](https://github.com/codeway3/tickets_tool/blob/master/screenshot.png)
  
## 更新
* **2016.10**  
实现基本功能，分析发送的请求，提取查询信息  
添加到站日期显示，添加硬座、商务座查询列  
日期已支持YYYYMMDD格式，添加彩色车站信息标识  
* **2017.03**  
对于12306查询重新进行解析，添加virtualenv，添加包依赖信息requirement.txt  
利用docopt进行命令行参数自动解析，并按参数筛选符合条件的结果进行显示  
修复一个历时显示错误的bug  
* **2017.04**  
针对12306查询url的改动进行更新  
修复了默认不传入参数时不返回查询结果的bug  
添加pinyin模块以解析汉字输入  
* **2017.07**  
由于12306数据格式大量变动，重新分析了数据组成，重写数据解包代码  
改动代码以符合PEP8  
* **2017.09**  
重构代码  
* **2017.10**  
更改url模板  
更改docopt并添加异常处理  
增强代码鲁棒性  
* **2018.03**  
解决url使用多个硬编码模板的问题  
添加logging模块，替换print

## 已知问题  
response有时返回的不是我们需要获取的JSON数据，而是一个html文件，暂时不知道如何解决，这种情况会抛出JSON解析异常，多运行几次可以获得正确结果。
  
## ToDoList
- [x] 添加参数解析功能与对应结果筛选
- [x] 添加中文车站名查询功能
- [x] 增强代码鲁棒性
- [ ] 添加车票价格查询功能  
  
## 参考资料 
[prettytable文档](https://code.google.com/archive/p/prettytable/wikis/Tutorial.wiki)  
[virtualenv参考资料](http://www.nowamagic.net/academy/detail/1330228)  
[docopt参考资料](http://www.tuicool.com/articles/36zyQnu)  
[汉字转拼音参考资料](http://www.cnblogs.com/code123-cc/p/4822886.html)
