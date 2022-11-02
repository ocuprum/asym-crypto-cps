import time
import generators.generators as gen
import tests.tests as tests

quantiles = [0.1, 0.05, 0.01]
seq1 = gen.built_in(1000000)
seq2 = gen.lehmer_low(1000000)
seq3 = gen.lehmer_high(1000000)
seq4 = gen.l20(1000000)
seq5 = gen.l89(1000000)
seq6 = gen.geffe(1000000)
seq7 = gen.wolfram(1000000)
seq8 = gen.librarian("src/me.txt", 1000000)
seq9 = gen.bbs(1000000)
seq10 = gen.bbs_bytes(1000000)
seq11 = gen.bm(1000000)
seq12 = gen.bm_bytes(1000000)

for q in quantiles:
    tests.test(seq1, "build_in", q)
    tests.test(seq2, "lehmer_low", q)
    tests.test(seq3, "lehmer_high", q)
    tests.test(seq4, "l20", q)
    tests.test(seq5, "l89", q)
    tests.test(seq6, "geffe", q)
    tests.test(seq7, "wolfram", q)
    tests.test(seq8, "librarian", q)
    tests.test(seq9, "bbs", q)
    tests.test(seq10, "bbs_bytes", q)
    tests.test(seq11, "bm", q)
    tests.test(seq12, "bm_bytes", q)

# gen.built_in(1000000)
# gen.lehmer_low(1000000)
# gen.lehmer_high(1000000)
# gen.l20(1000000)
# gen.l89(1000000)
# gen.geffe(1000000)
# gen.wolfram(1000000)
# gen.librarian('src/me.txt', 1000000)
# gen.bm(80000)
# gen.bm_bytes(80000)
# gen.bbs(1000000)
# gen.bbs_bytes(1000000)



