# coding: utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf8')

# 解析RSS
import feedparser
# 正则
import re
# 中文分词
import jieba 


# 返回一个RSS订阅源的标题和包含单词计数情况的字典
def getwordcounts(url):
	# 解析订阅源
	d = feedparser.parse(url)
	wc = {}

	# 循环遍历所有的文章条目
	for e in d.entries:
		if 'summary' in e: summary = e.summary
		else: summary = e.description

		# 提取一个单词列表
		words = getwords(e.title + ' ' + summary)
		for word in words:
			wc.setdefault(word, 0)
			wc[word] += 1

	return d.feed.title, wc

def getwords(html):
	# 去除所有HTML标记
	txt = re.compile(r'<[^>]+>').sub('', html)

	# 利用jieba切分词汇
	algor = jieba.cut(txt,cut_all=True)

	return [tok.lower() for tok in algor if tok!='']

	# 利用所有非字母字符拆分出单词
	#words = re.compile(r'[^A-Z^a-z]+').split(txt)

	# 转化成小写形式
	#return [word.lower() for word in words if word != '']


apcount = {}
wordcounts = {}
# 遍历所有博客
feedlist = [line for line in file('feedlist.txt')]
for feedurl in feedlist:
	title, wc = getwordcounts(feedurl)
	wordcounts[title] = wc
	for word, count in wc.items():
		apcount.setdefault(word, 0)
		# 统计单词出现在几篇博客里
		if count > 1:
			apcount[word] += 1

# 统计高频词
wordlist = []
for w, bc in apcount.items():
	frac = float(bc) / len(feedlist)
	if frac > 0.1 and frac < 0.5: wordlist.append(w)

out = file('blogdata.txt', 'w')
out.write('Blog')
# 每一列对应一个单词
for word in wordlist: out.write('\t%s' % word.strip())
out.write('\n')
for blog, wc in wordcounts.items():
	# 每一行对应一个博客名
	out.write(blog)
	for word in wordlist:
		if word in wc: out.write('\t%d' % wc[word])
		else: out.write('\t0')
	out.write('\n')