import re

content = '<span class="nums_text">百度为您找到相关结果约7,600,000个</span>'

content = re.sub(r'[^\d.]', '', content)

print(content)
