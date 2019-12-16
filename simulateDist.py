import sys
import math
import random as rngen

#Method for Bernoulli Distribution
def bernoulli(nValue, argument):
    X = []
    data = []
    if len(argument) != 1: sys.exit('Invalid choice of number of arguments : ')
    p = float(argument[0])
    if p < 0.0 or p > 1.0: sys.exit('Invalid choice of probability value : ' + str(p))
    for i in range(nValue):
        if rngen.random() <= p:
            X.append(1)
        else:
            X.append(0)
    data.append(p)
    data.append(p*(1-p))
    return [X,data]

#Method for Binomial Distribution
def binomial(nValue, argument):
    X = []
    data = []
    if len(argument) != 2: sys.exit('Invalid choice of number of arguments : ')
    n = int(argument[0])
    p = float(argument[1])
    if p < 0.0 or p > 1.0: sys.exit('Invalid choice of probability value: ' + str(p))
    for i in range(nValue):
        nS = 0
        for j in range(n):
            if rngen.random() <= p:
                nS = nS + 1
        X.append(nS)
    data.append(n*p)
    data.append(n*p*(1 - p))
    return [X,data]

#Method for Geometric Distribution
def geometric(nValue, argument):
    X = []
    data = []
    if len(argument) != 1: sys.exit('Invalid choice of number of arguments : ')
    p = float(argument[0])
    if p < 0.0 or p > 1.0: sys.exit('Invalid choice of probability value: ' + str(p))
    for i in range(nValue):
        t = 1
        while rngen.random() > p:
            t = t + 1
        X.append(t)
    data.append(1/p)
    data.append((1-p)/math.pow(p,2))
    return [X, data]

#Method for Negative Binomial Distribution
def negBinomial(nValue, argument):
    X = []
    data = []
    if len(argument) != 2: sys.exit('Invalid choice of number of arguments : ')
    k = int(argument[0])
    p = argument[1:len(argument)]
    for i in range(nValue):
        X.append(sum(geometric(k, p)[0]))
    args = float(p[0])
    data.append(k / args)
    data.append((k*(1 - args)) / math.pow(args,2))
    return [X, data]

#Method for Poisson Distribution
def poisson(nValue, argument):
    X = []
    data = []
    if len(argument) != 1: sys.exit('Invalid choice of number of arguments : ')
    lda = float(argument[0])
    for i in range(nValue):
        k = 0
        u = rngen.random()
        while u >= math.exp((0.0 - lda)):
            k = k + 1
            u = u * rngen.random()
        X.append(k)
    data.append(lda)
    data.append(lda)
    return [X, data]

#Method for Cumulative Distributive Discrete Distribution
def cdfDisc(p):
    F = []
    for i in range(len(p)):
        F.append(sum(p[0:i + 1]))
    return F

#Method for ARB-Discrete Distribution
def arbDisc(nValue, argument):
    X = []
    p = []
    for v in argument:
        p.append(float(v))
    F = cdfDisc(p)
    if F[-1] != 1: sys.exit('Summation of all probabilities needs to be equal to one')
    for i in range(nValue):
        t = 0
        u = rngen.random()
        while F[t] <= u:
            t = t + 1
        X.append(t)
    return X


def uniform(nValue, argument):
    X = []
    data = []
    if len(argument) != 2: sys.exit('Invalid choice of number of arguments : ')
    a = float(argument[0])
    b = float(argument[1])
    if a > b:
        t = a;
        a = b;
        b = t;
    for i in range(nValue):
        X.append(a + ((b - a) * rngen.random()))
    data.append((a+b)/2)
    data.append(math.pow(b-a,2)/12)
    return [X, data]


def exponential(nValue, argument):
    X = []
    data = []
    if len(argument) != 1: sys.exit('Invalid choice of number of arguments : ')
    lda = float(argument[0])
    for i in range(nValue):
        X.append((0 - (1 / lda)) * math.log(1 - rngen.random()))
    data.append(1 / lda)
    data.append(1/math.pow(lda,2))
    return [X, data]


def gamma(nValue, argument):
    X = []
    data = []
    if len(argument) != 2: sys.exit('Invalid choice of number of arguments : ')
    alp = int(argument[0])
    lda = argument[1:len(argument)]
    for i in range(nValue):
        X.append(sum(exponential(alp, lda)[0]))
    lamb = float(lda[0])
    data.append(alp/lamb)
    data.append(alp/math.pow(lamb,2))
    return [X, data]


def normal(nValue, argument):
    X = []
    data = []
    if len(argument) != 2: sys.exit('Invalid choice of number of arguments : ')
    nValue2 = int(math.ceil(float(nValue) / 2))
    mu = float(argument[0])
    sd = float(argument[1])
    for i in range(nValue2):
        u1 = rngen.random()
        u2 = rngen.random()
        z1 = math.sqrt((0 - 2) * math.log(u1)) * math.cos(2 * math.pi * u2)
        z2 = math.sqrt((0 - 2) * math.log(u1)) * math.sin(2 * math.pi * u2)
        X.append(mu + z1 * sd)
        X.append(mu + z1 * sd)
        data.append(mu)
        data.append(math.pow(sd,2))
    if nValue % 2 == 0:
        return [X, data]
    else:
        return [X[0:len(X) - 1],data]


def sampleMean(sample):
    return (float(sum(sample)) / float(len(sample)))


def sampleVar(sample, mean):
    t = 0.0
    for i in sample:
        t = t + float((i - mean) * (i - mean))
    if len(sample) == 1:
        return t
    return t / float(len(sample) - 1)


def main(argv):
    rngen.seed(3)         #Random Number Generator Seeded, any number can be used in place of '3'.
    try:
        nValue = int(argv[1])
        argument = argv[3:len(argv)]
        if argv[2].lower() == 'bernoulli':
            result = bernoulli(nValue, argument)
        elif argv[2].lower() == 'binomial':
            result = binomial(nValue, argument)
        elif argv[2].lower() == 'geometric':
            result = geometric(nValue, argument)
        elif argv[2].lower() == 'neg-binomial':
            result = negBinomial(nValue, argument)
        elif argv[2].lower() == 'poisson':
            result = poisson(nValue, argument)
        elif argv[2].lower() == 'arb-discrete':
            res = arbDisc(nValue, argument)
            result = []
            result.append(res)
        elif argv[2].lower() == 'uniform':
            result = uniform(nValue, argument)
        elif argv[2].lower() == 'exponential':
            result = exponential(nValue, argument)
        elif argv[2].lower() == 'gamma':
            result = gamma(nValue, argument)
        elif argv[2].lower() == 'normal':
            result = normal(nValue, argument)
        else:
            sys.exit('Distribution ' + argv[2] + ' is not supported')
        print('Values: ' + str(result[0]))
        if argv[2].lower() == 'arb-discrete':
            result.append([sampleMean(result[0]),sampleVar(result[0],sampleMean(result[0]))])
        print('\nSample Mean: ' + str(sampleMean(result[0])))
        print('Sample Variance: ' + str(sampleVar(result[0],sampleMean(result[0]))))
        print('\nPopulation Mean: ' + str(result[1][0]))
        print('Population Variance: ' + str(result[1][1]))
    except ValueError:
        print('Incorrect number syntax')


if __name__ == '__main__':
    main(sys.argv)