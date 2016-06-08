#!/usr/bin/python
class Person:
  n=0
  def __init__(self,name,age):
    self.name,self.age = name,age
    Person.n = Person.n + 1  
  @staticmethod
  def how_many_people():
      return 'we have {0} people'.format(Person.n)
  @classmethod
  def how_many_peoples(cls):
      return cls.how_many_people()
a=Person("lei.yang","1")
b=Person("xiangyu","2")
print Person.how_many_people()
print Person.how_many_peoples()
