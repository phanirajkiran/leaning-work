#!/usr/bin/python
class Person:
  def __init__(self,name,age):
    self.name,self.age = name,age
  def __str__(self):
      return 'This guy is {self.name},is {self.age} old'.format(self=self)
a=Person("lei.yang","1")
print str(a)
