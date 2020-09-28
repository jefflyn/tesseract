import os


def notify(title=None, subtitle=None, content=None):
    '''
    右侧通知消息
    os.system("""osascript -e 'display notification "content" with title "title"
                subtitle "subtitle" sound name "Submarine"'""")
    :param title: 标题
    :param subtitle: 副标题
    :param content: 通知内容
    :return:
    '''
    if title is None:
        title = '通知📢'
    if subtitle is None:
        subtitle = ''
    if content is None:
        return
    # notification = 'display notification "%s" with title "%s" subtitle "%s"' % (content, title, subtitle)
    # print(notification)
    script = """osascript -e 'display notification "%s" with title "%s" subtitle "%s"'""" % (content, title, subtitle)
    print(script)
    os.system(script)


def alert(title=None, message=None):
    '''
    弹窗提醒
    os.system("""osascript -e 'display alert "Hello World!" message "pop-up alert message."'""")
    :param title: 标题
    :param message: 提醒内容
    :return:
    '''
    if title is None:
        title = '警告⚠️'
    if message is None:
        return
    alert_script = """osascript -e 'display alert "%s" message "%s"'""" % (title, message)
    print(alert_script)
    notice = """osascript -e 'display notification "%s" with title "%s" sound name "Glass"'""" % (message, title)
    os.system(notice)
    # os.system(alert_script)


if __name__ == '__main__':
    # os.system("""osascript -e 'display notification "content" with title "title" subtitle "subtitle"'""")
    # os.system("""osascript -e 'display alert "Hello World!" message "pop-up alert message."'""")

    # notify("商品报价提醒", "苹果2101", "7400")
    # notify(title="商品报价提醒", content="苹果2101=7400")
    # notify(content="苹果2101=7400")
    alert(message="苹果2101=7400")
    alert(title="商品报价⚠️", message="苹果2101=7400")
