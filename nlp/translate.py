from googletrans import Translator
translator = Translator()
result = translator.translate("shit", src="en", dest="zh-cn")
print(result.text)  # 输出：狗

