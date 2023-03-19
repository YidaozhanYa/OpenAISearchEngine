# OpenAISearchEngine

🔍 Interactive chat-based search engine with OpenAI, inspired by New Bing.

# Dependencies

Because it's VERY SLOW to call OpenAI API with OpenAI Python library or other HTTP libraries, so this program depends on `curl` to call OpenAI API via shell command & subprocess.

# Usage

```bash
python3 main.py
```

# Demo

```markdown
[user](#message)
你知道 New Bing 搜索引擎吗？

[assistant](#online_search)
New Bing 搜索引擎

[system](#search_result)
[{"title": "新必应（New Bing）国内申请与使用教程 - 知乎", "snippet": "常见问题 如果访问不了，你可以清除一下浏览器必应的 Cookie，地址栏重新输入必应链接：bing.com"}, {"title": "新必应（New Bing）使用指南 - 知乎", "snippet": "新必应（New Bing）是微软推出的一款基于GPT4模型的智能搜索引擎，它不仅可以提供高质量的搜索结果，还可以与用户进行自然语言交互，提供各种有趣和实用的功能。本文将介绍如何申请和使用新必应，以及它的一些特色功能。如何申请新必应"}, {"title": "总是跳转到国内版(cn.bing.com)？New Bing使用全攻略 - 掘金", "snippet": "四、手机访问New Bing 现在（更新时间2023.2.28）微软已经将New Bing带上了手机。 现在有了更方面的访问途径，使用手机的Bing App使用New Bing的Chat功能。 但国内的应用商城应该是名叫“微软必应”的阉割版，我这里找到了微软官方的下载地址："}, {"title": "新必应（New Bing）国内申请与使用教程 - 掘金", "snippet": "新必应（New Bing）国内申请与使用教程 下载安装 Edge dev 版本，这个版本可以直接申请(不用梯子) ... 多内容聚合浏览、多引擎快捷搜索 、多工具便捷提效、多模式随心畅享，你想要的，这里都有！ 前往安装 ..."}, {"title": "无需魔法，新版 New Bing 使用方法全攻略！_腾讯新闻", "snippet": "添加搜索引擎 需要注意的是。 在添加必应搜索引擎时，我们要手动添加“必应英文”的搜索参数 setmkt=en-US。 英文原版： 图片搜索： 以图搜图： 特别是“以图搜图”。 如果必应检测到你上一次，使用的是“必应搜索国内版”，那么以图搜图功能就会显示为空白。"}]

[assistant](#response)
是的，新必应是微软推出的一款基于GPT4模型的智能搜索引擎。它不仅可以提供高质量的搜索结果，还可以与用户进行自然语言交互，提供各种有趣和实用的功能。可以使用以下步骤安装并使用新必应：1.下载安装Edge dev版本；2.在Edge浏览器中添加搜索引擎；3.使用手机Bing App访问New Bing；4.了解New Bing提供的各种特色功能。
```