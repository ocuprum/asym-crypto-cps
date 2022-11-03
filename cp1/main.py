import time
import generators.generators as gen
import tests.tests as t

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
    t.test(seq1, "build_in", q)
    t.test(seq2, "lehmer_low", q)
    t.test(seq3, "lehmer_high", q)
    t.test(seq4, "l20", q)
    t.test(seq5, "l89", q)
    t.test(seq6, "geffe", q)
    t.test(seq7, "wolfram", q)
    t.test(seq8, "librarian", q)
    t.test(seq9, "bbs", q)
    t.test(seq10, "bbs_bytes", q)
    t.test(seq11, "bm", q)
    t.test(seq12, "bm_bytes", q)



