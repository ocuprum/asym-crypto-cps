import scipy.stats


def test(seq, name, quantile):
    print("Testing `" + name + "` RNG, with quantile:", quantile)
    print("Equal Distribution:")
    print("result:", equal_distribution(seq, quantile))
    print("Independence:")
    print("result:", independence(seq, quantile))
    print("Homogeneity:")
    print("result:", homogeneity(seq, quantile))
    print("\n")

def equal_distribution(dist, alpha):
    dist_list = [dist[i:i + 8] for i in range(0, len(dist), 8)]
    m = len(dist_list)
    n = m / 256

    countMap = {}
    for item in dist_list:
        countMap[item] = countMap.get(item, 0) + 1

    chiSquare = 0

    for count in countMap.values():
        chiSquare += ((count - n) ** 2) / n

    q = scipy.stats.chi2.ppf(1 - alpha, df=(n - 1))

    print("empiric: " + str(chiSquare) + ", theoretic: " + str(q))
    return chiSquare < q


def independence(dist, alpha):
    dist_list = [dist[i:i + 8] for i in range(0, len(dist), 8)]
    m = len(dist_list)
    n = m / 2
    chiSquare, s, k = chi2sum(dist_list)
    chiSquare = (chiSquare - 1) * n

    q = scipy.stats.chi2.ppf(1 - alpha, (s - 1) * (k - 1))

    print("empiric: " + str(chiSquare) + ", theoretic: " + str(q))
    return chiSquare < q


def homogeneity(dist, alpha):
    dist_list = [dist[i:i + 8] for i in range(0, len(dist), 8)]
    m = len(dist_list)
    r = 10
    m2 = m // r
    n = m2 / 2

    new_dist_list = [dist_list[i:i + m2] for i in range(0, len(dist_list), m2)]

    chiSquare = 0
    s, k = 0, 0
    for i in range(r):
        sub_list = new_dist_list[i]
        chiTmp, s, k = chi2sum(sub_list)
        chiSquare += (chiTmp - 1)

    chiSquare *= n

    q = scipy.stats.chi2.ppf(1 - alpha, (s - 1) * (k - 1)*r)
    print("empiric: " + str(chiSquare) + ", theoretic: " + str(q))
    return chiSquare < q


def chi2sum(dist):
    countMapFirst = {}
    countMapSecond = {}
    countMapDouble = {}

    for i in range(0, len(dist) - 1, 2):
        item = dist[i]
        itemNext = dist[(i + 1)]

        countMapFirst[item] = countMapFirst.get(item, 0) + 1
        countMapSecond[itemNext] = countMapSecond.get(itemNext, 0) + 1
        countMapDouble[(item, itemNext)] = countMapDouble.get((item, itemNext), 0) + 1

    chiSquare = 0

    for double in countMapDouble.keys():
        item, itemNext = double
        chiSquare += (countMapDouble[double] ** 2 / (countMapFirst[item] * countMapSecond[itemNext]))

    return chiSquare, len(countMapFirst), len(countMapSecond)
