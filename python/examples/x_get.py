#!/usr/bin/python
# -*- coding: UTF-8 -*-
class Fruit:      
    '''xxxxx'''  
    def __str__(self):
        return self.__doc__

if __name__ == "__main__":
    fruit = Fruit()
    print str(fruit)    
#    print fruit        
