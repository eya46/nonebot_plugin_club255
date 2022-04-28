# 自动推送255帖子

## 环境

+ nonebot2
+ nonebot-plugin-apscheduler
+ nonebot-adapter-onebot
+ httpx


## 配置
### 必填
+ 255_url
  > 255_url = "https://???????.com/"
  >
  > 某255俱乐部的网址，最后的 / 必须要有
+ apscheduler_autostart
  > apscheduler_autostart=True
  > 
  > 必填这个，不填的话好像不会自动执行

### 选填
+ 255_push_friends
  > 255_push_friends = [123456,456789]
  > 
  > 要推送的QQ
+ 255_push_groups
  > 255_push_groups = [11111,22222]
  > 
  > 要推送的群聊
+ 255_push_minutes
  > 255_push_minutes = 10
  > 
  > 间隔多少分钟推送
+ 255_push_bot
  > 255_push_bot = 11122222
  > 
  > 指定推送的机器人QQ
+ 255_pictures_max
    > 255_pictures_max = 4
  > 
    > 每次推送帖子，最大显示的图片数
  > 
+ 255_tid_max_num
    > 255_tid_max_num = 10
  > 
    > 每次最大获取的帖子数, 限制低于25
+ 255_if_show_avatar
  > 255_if_show_avatar = True
  > 
  > 是否显示发帖者头像 


## 待更新
> 发帖用户信息中
>
> 经验:182 
> 
> 改为
> 
> 等级: 5 猫耳开关(182/200)