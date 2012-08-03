# coding=utf-8


class FifoList(list):
    '''List that pops from the begining.'''

    def pop(self, index=0):
        return super(FifoList, self).pop(index)
