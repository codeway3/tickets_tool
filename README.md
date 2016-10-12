# tickets_tool
火车票查询工具

## 查询格式
"""Train tickets query via command-line.  
  
Usage:  
　　tickets [-gdtkz] \<from> \<to> \<date>
  
Options:  
　　-h,--help   显示帮助菜单  
　　-g          高铁  
　　-d          动车  
　　-t          特快  
　　-k          快速  
　　-z          直达  
  
Example:  
　　tickets beijing shanghai 2016-08-25  
"""  
  
## 更新
* 2016.10.10 更新 添加到站日期显示， 添加硬座、商务座查询列
* 2016.10.11 更新 日期已支持YYYYMMDD格式， 添加彩色车站信息标识  

## 参考资料
[实验楼文档](https://www.shiyanlou.com/courses/623/labs/2072/document)  
[prettytable文档](https://code.google.com/archive/p/prettytable/wikis/Tutorial.wiki)  
  
## ToDoList
*添加参数解析与对应结果筛选
