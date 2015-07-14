#!/usr/bin/python
import pickle
class Integer:
    def __init__(self, x):
        self.x = x
    def __str__(self):
        return 'My name is integer %d' % self.x

i = Integer(7)
pickle.dump(i, open('save.p', 'wb'))
reader = pickle.load(open('save.p', 'rb'))
print reader.x
