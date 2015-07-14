http://blog.csdn.net/flydirk/article/details/8557219
http://outofmemory.cn/code-snippet/2138/python-regular-re-module-learn-note
http://zeping.blog.51cto.com/6140112/1148833
贪婪和多行:
http://xiaofeng1982.blog.163.com/blog/static/3157245820117124555434/

\d  匹配任何十进制数；它相当于类[0-9]
\D  匹配任何非数字字符；它相当于类[^0-9]
\s  匹配任何空白字符；它相当于类[ \t\n\r\f\v]
\S  匹配任何非空白字符；它相当于类[^ \t\n\r\f\v]
\w  匹配任何字母数字字符；它相当于类[a-zA-Z0-9_]
\W  匹配任何非字母数字字符；它相当于类[^a-zA-Z0-9_]

match() 
是否在字符串刚开始的位置匹配

  

search() 

扫描字符串，找到这个RE 匹配的位置

1)p = re.compile('(a(b)c)d') 
2)
>>> p = re.compile(r'\bclass\b')
>>> print p.search('no class at all')
<_sre.SRE_Match object at 0x2942920>

3)
>>> p = re.compile('(a(b)c)d')
>>> print p.search('abcd')
<_sre.SRE_Match object at 0x7f4fa890c140>
>>> print p.search('abcd').group(0)
abcd
>>> print p.search('abcd').group(1)
abc
>>> print p.search('abcd').group(2)
b

3)
>>> print p.search('abcd').groups()
('abc', 'b')
  

findall() 
找到RE 匹配的所有子串，并把它们作为一个列表返回
>>> m=re.findall("foo.*","foo1\nfoo2\n") 
>>> print m[0]
foo1
>>> print m[1]
foo2


  

finditer() 
找到RE 匹配的所有子串，并把它们作为一个迭代器返回


split() 
将字符串在RE 匹配的地方分片并生成一个列表，

  

sub() 
找到RE 匹配的所有子串，并将其用一个不同的字符串替换
>>> p = re.compile( '(blue|white|red)') 
>>> p.sub( 'colour', 'blue socks and red shoes')
  

>>> s='his dog is a dog'
>>> print re.sub(r'dog','cat',s)
his cat is a cat
>>> print re.sub(r'dog','cat',s,1)
his cat is a dog


subn() 

与sub() 相同，但返回新的字符串和替换次数

贪婪:
>>> print re.match('<.*>', s).group() 
<html><head><title>Title</title>  

s = '<html><head><title>Title</title>'
>>> print re.match('<.*?>', s).group() 
<html> 

>>> re.findall("a{2}","aaaaaaaa")
['aa', 'aa', 'aa', 'aa']


>>> s='I have a dog , IHAVE A dog , xxxx , '
>>> re.split('\s*,\s',s)
['I have a dog', 'IHAVE A dog', 'xxxx', '']
===================

多行:
>>> import re
>>> f=open('ceph.log','r')
>>> x=f.read()

>>> print x
fsfsfsaf 123232
444
555
5555 ddfdfdf

[]
>>> print x
fsfsfsaf 123232
444
555
5555 ddfdfdf


>>> print re.findall(r"\d+$",x,re.M)
['123232', '444', '555']
>>> print re.findall(r"^\d+$",x,re.M)
['444', '555']

