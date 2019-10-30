import numpy as np
from  numpy.linalg import svd, multi_dot
import math




def mat_korespodencije(x, xp):
    return [[0, 0, 0, -xp[2] * x[0],  -xp[2] * x[1], -xp[2] * x[2], xp[1] * x[0], xp[1] * x[1], xp[1] * x[2]],
            [xp[2] * x[0], xp[2] * x[1], xp[2] * x[2], 0, 0, 0, -xp[0] * x[0], -xp[0] * x[1], -xp[0] * x[2]]]



def dlt(originals, dests):
    A = []
    # za svaku tacku i njenu sliku dobijamo dve vrse koje dodajemo u matricu A
    for original, dest in zip(originals, dests):
        tmp = mat_korespodencije(original, dest)
        A.append(tmp[0])
        A.append(tmp[1])

    # svd dekompozicija
    u, d, v = svd(A, full_matrices=True)

    # uzimamo poslednju vrstu matrice v
    P = list(v[8])

    # konstruisemo matricu preslikavanja
    P = [P[i:i + 3] for i in range(0, len(P), 3)]
    return np.matrix(P)

#
# originals = [[-3, -1, 1],
#              [3, -1, 1],
#              [1, 1, 1],
#              [-1, 1, 1],
#              [1, 2, 3],
#              [-8, -2, 1]]
#
# dests = [[-2, -1, 1],
#              [2, -1, 1],
#              [2, 1, 1],
#              [-2, 1, 1],
#              [2, 1, 4],
#              [-16, -5, 4]]


def homogenizacija(ps):
    new_ps = []
    for o in ps:
        last_coordinate = o[2]
        new_ps.append([x / last_coordinate for x in o])
    return new_ps


def teziste(tacke):
    # izdvajamo x(odnosno y) koordinate u niz
    xs = [t[0] for t in tacke]
    ys = [t[1] for t in tacke]
    # vracamo tacku koja za koordinate ima aritmeticke sredine nizova
    return [sum(xs) * 1.0 / len(xs),
            sum(ys) * 1.0 / len(ys)]


def mat_translacije_tezista(t):
    return [[1, 0, -t[0]],
            [0, 1, -t[1]],
            [0, 0,  1]]


def coef_homotetije(translated_points):
    tmp = [math.sqrt(x[0] * x[0] + x[1] * x[1]) for x in translated_points]
    alpha = (sum(tmp) * 1.0 / len(tmp))
    return math.sqrt(2) / alpha


def mat_skaliranja(k):
    return [[k, 0, 0],
            [0, k, 0],
            [0, 0, 1]]


def point_transformer(ps):
    # funkcija koja konstruise matricu T = SG
    # G <- translacija
    # S <- homotetija

    t = teziste(ps)
    # transliramo tacke matricom G
    translated_ps = [list(np.dot(mat_translacije_tezista(t), np.transpose(x))) for x in ps]

    k = coef_homotetije(translated_ps)
    # racunamo T = SG
    return np.dot(mat_skaliranja(k), mat_translacije_tezista(t))


def normalize_points(ps, T):
    # vraca M' = TM
    return list(map(lambda t: list(np.dot(T, np.transpose(t))), ps))

def normDLT(originals, dests):

    originals = homogenizacija(originals)
    dests = homogenizacija(dests)

    T = point_transformer(originals)
    Tp = point_transformer(dests)

    # Skaliranje i transliranje tacaka
    ogs = normalize_points(originals, T)
    ds = normalize_points(dests, Tp)

    # racunanje DLT nad normalizovanim tackama
    P_ = dlt(ogs, ds)

    return multi_dot([np.linalg.inv(Tp), P_, T])

