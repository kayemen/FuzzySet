'''
DocString for FuzzySet
'''


class FuzzyVector(object):
    '''
    Discrete fuzzy vector implementation.
    Basic fuzzy vector operations of intersection, union, inversion are implemented using native python operations.
    Union - A+B
    Intersection - A*B
    Inversion - ~A
    Distance - A-B
    Count - c(A) = abs
    '''

    tnorm = 'min'
    count = 'sum'
    distance = 'l1'

    def __init__(self, fit_vector):
        if any([val > 1 or val < 0 for val in fit_vector]):
            raise ValueError(
                'Fit vector values must be between 0 and 1-Got {fit_vector}'.format(fit_vector=fit_vector))
        self.values = fit_vector[:]
        self.n = len(self.values)

    def __len__(self):
        return len(self.values)

    def __abs__(self):
        '''
        Count of fit vector
        c(A)=sum(ai)
        Alternate count definitions also supported
        '''
        if self.count == 'sum':
            return sum(self.values)
        if self.count == 'prod':
            return reduce(lambda x, y: x * y, self)

    def __repr__(self):
        return '(' + ','.join(['%.2f' % val for val in self.values]) + ')'

    def __iter__(self):
        '''
        Iterate through values in the fit vector
        '''
        for val in self.values:
            yield val

    def __getitem__(self, key):
        '''
        Get slice of values from the fuzzy vector
        '''
        return self.values[key]

    def __sub__(self, other):
        '''
        Absolute difference operator
        A-B={|ai-bi|}
        '''
        if other == 0:
            other = FuzzyVector([0 for _ in self])
        elif other == 1:
            other = FuzzyVector([1 for _ in self])
        self.validate_operands(other)
        if self.distance == 'l1':
            return abs(FuzzyVector([abs(x - y) for (x, y) in zip(self, other)]))
        raise NotImplementedError

    def __add__(self, other):
        '''
        Union operator
        A+B={max(ai, bi)}
        '''
        self.validate_operands(other)
        if self.tnorm == 'min':
            return FuzzyVector([max(x, y) for (x, y) in zip(self, other)])
        raise NotImplementedError

    def __mul__(self, other):
        '''
        Intersection operator
        A*B={min(ai, bi)}
        '''
        self.validate_operands(other)
        if self.tnorm == 'min':
            return FuzzyVector([min(x, y) for (x, y) in zip(self, other)])
        raise NotImplementedError

    def __invert__(self):
        '''
        Complement operator
        ~A={1-ai}
        '''
        return FuzzyVector([1 - x for x in self])
        # if self.tnorm == 'min':
        #     return FuzzyVector([1 - x for x in self])
        raise NotImplementedError

    def __lt__(self, other):
        '''
        Subsethood operator
        A<B = c(A*B)/c(A)
        '''
        self.validate_operands(other)
        return abs(self * other) / float(abs(self))

    @property
    def near(self):
        '''
        Nearest point in the fuzzy n-cube
        A_near = {round(ai)}
        '''
        return FuzzyVector([round(val) for val in self])

    @property
    def far(self):
        '''
        Farthest point in the fuzzy n-cube
        A_far = {1-round(ai)}
        '''
        return FuzzyVector([1 - round(val) for val in self])

    @property
    def fuzz(self):
        '''
        Ratio entropy of the fit vector. Fuzziness of the fit vector
        E(A)=c(A*~A)/c(A+~A)
        '''
        return abs(self * ~self) / abs(self + ~self)
        # return (self - self.near) / (self - self.far)

    def validate_operands(self, other):
        if not isinstance(other, FuzzyVector):
            raise TypeError('Operands must be of type FuzzyVector')
        if len(self) != len(other):
            raise IndexError('Inconsistent length fit vectors')


if __name__ == '__main__':
    pass
