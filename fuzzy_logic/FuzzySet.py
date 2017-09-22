'''
DocString for FuzzySet
'''


class FuzzyVector(object):
    tnorm = 'min'
    count = 'sum'

    def __init__(self, fit_vector):
        if any([val > 1 or val < 0 for val in fit_vector]):
            raise ValueError(
                'Fit vector values must be between 0 and 1-Got {fit_vector}'.format(fit_vector=fit_vector))
        self.values = fit_vector[:]
        self.N = len(self.values)

    def __len__(self):
        return len(self.values)

    def __abs__(self):
        if self.count == 'sum':
            return sum(self.values)
        if self.count == 'prod':
            return reduce(lambda x, y: x * y, self)

    def __repr__(self):
        return '(' + ','.join(['%.2f' % val for val in self.values]) + ')'

    def __iter__(self):
        for val in self.values:
            yield val

    def __getitem__(self, key):
        return self.values[key]

    def __sub__(self, other):
        if other == 0:
            other = FuzzyVector([0 for _ in self])
        elif other == 1:
            other = FuzzyVector([1 for _ in self])
        return FuzzyVector([abs(x - y) for (x, y) in zip(self, other)])

    def __add__(self, other):
        if not isinstance(other, FuzzyVector):
            raise TypeError('Operands must be of type FuzzyVector')
        if self.tnorm == 'min':
            return FuzzyVector([max(x, y) for (x, y) in zip(self, other)])
        raise NotImplementedError

    def __mul__(self, other):
        if not isinstance(other, FuzzyVector):
            raise TypeError('Operands must be of type FuzzyVector')
        if self.tnorm == 'min':
            return FuzzyVector([min(x, y) for (x, y) in zip(self, other)])
        raise NotImplementedError

    # def __radd__(self, other):
    #     return other + self

    # def __rmul__(self, other):
    #     return other * self

    def __invert__(self):
        if self.tnorm == 'min':
            return FuzzyVector([1 - x for x in self])
        raise NotImplementedError

    def __lt__(self, other):
        if not isinstance(other, FuzzyVector):
            raise TypeError('Operands must be of type FuzzyVector')
        return abs(self * other) / float(abs(self))

    @property
    def near(self):
        return FuzzyVector([round(val) for val in self])

    @property
    def far(self):
        return FuzzyVector([1 - round(val) for val in self])

    @property
    def fuzz(self):
        return abs(self - self.near) / abs(self - self.far)


if __name__ == '__main__':
    X = FuzzyVector((1.0, 1.0, 1.0, 1.0))
    O = FuzzyVector((0.0, 0.0, 0.0, 0.0))
    A = FuzzyVector((0.3, 0.6, 0.4, 0.2))
    B = FuzzyVector((0.4, 0.5, 0.4, 0.7))
    C = FuzzyVector((0.6, 0.7, 0.7, 1.0))
    D = FuzzyVector((1.0, 1.0, 0.0, 0.0))
    E = FuzzyVector((1.0, 0.0, 1.0, 0.0))
    M = FuzzyVector((0.5, 0.5, 0.5, 0.5))

    fit_set = [X, O, A, B, C, D, E, M]
    fit_set_name = ['X', 'O', 'A', 'B', 'C', 'D', 'E', 'M']

    print '1.26) l1 distances'
    print '     ', '     '.join(fit_set_name)
    # Hamming distance table
    for ind, i in zip(fit_set_name, fit_set):
        print ind, ':',
        for j in fit_set:
            print abs(i - j), ',',
        print

    print '=' * 80
    print '1.29) Count of vector c(A)'
    print 'Fit vector count - sum'
    # prod distance table
    for ind, i in zip(fit_set_name, fit_set):
        print ind, ':',
        print reduce(lambda x, y: x + y, i)

    print 'Fit vector count - product'
    # prod distance table
    for ind, i in zip(fit_set_name, fit_set):
        print ind, ':',
        print reduce(lambda x, y: x * y, i)

    print '=' * 80
    print '1.30) Ratio Entropy'
    # Ratio entropy
    for ind, i in zip(fit_set_name, fit_set):
        print ind, ':', ind, '_near:', i.near, ind, '_far:', i.far, 'E(%s)=' % ind,
        try:
            print '%.2f' % i.fuzz,
        except Exception as e:
            print e
            print 'NaN'
        print

    print '=' * 80
    print '1.34) Subsethood S(A,B)'
    print 'AV,B>   ', '      '.join(fit_set_name)
    for ind, a in zip(fit_set_name, fit_set):
        print ind, ':  ',
        for b in fit_set:
            try:
                print '%.2f' % (a < b), ',',
            except:
                # import traceback
                # traceback.print_exc()
                # raw_input()
                print ' NaN', ',',
        print

    E = FuzzyVector([0.9, 0.8, 0.6, 0.4, 0.2, 0.0])
    H1 = FuzzyVector([1.0, 0.8, 0.0, 0.1, 0.1, 0.0])
    H2 = FuzzyVector([0.0, 0.0, 0.7, 1.0, 0.0, 0.3])
    H3 = FuzzyVector([0.1, 0.4, 1.0, 1.0, 0.4, 0.1])

    print '=' * 80
    print '1.38) Fuzzy Bayes evaluation'
    print 'S(E, H1)=%.2f' % (E < H1)
    print 'S(E, H2)=%.2f' % (E < H2)
    print 'S(E, H3)=%.2f' % (E < H3)
