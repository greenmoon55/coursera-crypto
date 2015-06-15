from gmpy2 import mpz
from gmpy2 import divm
from gmpy2 import isqrt
from gmpy2 import powmod


def dlog(prime, g, h):
    CONST_2_20 = 2 ** 20
    h_x1 = {}
    for x1 in xrange(CONST_2_20 + 1):
        val = divm(h, powmod(g, x1, prime), prime)
        h_x1[val] = x1
    gb = powmod(g, CONST_2_20, prime)
    for x0 in xrange(CONST_2_20 + 1):
        val = powmod(gb, x0, prime)
        if val in h_x1:
            x1 = h_x1[val]
            x = x0 * CONST_2_20 + x1
            print x
            break



if __name__ == "__main__":
    N = 179769313486231590772930519078902473361797697894230657273430081157732675805505620686985379449212982959585501387537164015710139858647833778606925583497541085196591615128057575940752635007475935288710823649949940771895617054361149474865046711015101563940680527540071584560878577663743040086340742855278549092581
    A = isqrt(mpz(N)) + 1
    x = isqrt(A * A - N)
    print A - x


    N = 648455842808071669662824265346772278726343720706976263060439070378797308618081116462714015276061417569195587321840254520655424906719892428844841839353281972988531310511738648965962582821502504990264452100885281673303711142296421027840289307657458645233683357077834689715838646088239640236866252211790085787877
    A = isqrt(mpz(N))
    N = mpz(N)
    while True:
        A += 1
        x = isqrt(A * A - N)
        p = A - x
        q = A + x
        if p * q == N:
            print p
            break

    N = 720062263747350425279564435525583738338084451473999841826653057981916355690188337790423408664187663938485175264994017897083524079135686877441155132015188279331812309091996246361896836573643119174094961348524639707885238799396839230364676670221627018353299443241192173812729276147530748597302192751375739387929
    N = mpz(N)
    A = 2 * isqrt(6 * N) + 1
    x = isqrt(A*A - 24 * N)
    p = (A - x) / 6
    q = (A + x) / 4
    print p
