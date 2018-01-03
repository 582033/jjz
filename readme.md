## 基于[pushbear]的进京证办理提醒服务

> 扫描下方二维码后，在进京证可办理时， 将收到微信提醒.

![](https://mp.weixin.qq.com/cgi-bin/showqrcode?ticket=gQG_8TwAAAAAAAAAAS5odHRwOi8vd2VpeGluLnFxLmNvbS9xLzAySS1Zdk5aQ2ZlNjAxMDAwME0wNzUAAgQG4u9ZAwQAAAAA)


## 配合crontab使用

```
    #每15分钟检查一次
    */15 * * * * /usr/bin/python2.7 /home/yjiang/jjz/jjz.py
```

> 虽然增加了代理, 但还是尽量延长每次检查的时间间隔; 防止服务器ip被封导致导致一直提示无法办理

## tips

* 每天只提醒3次, 基本都是凌晨0点~5点, 建议每天1点以后办理, 更容易些
* 有什么建议或想法, 请提issue
