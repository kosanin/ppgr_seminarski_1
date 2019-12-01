import numpy as np
import math


def Rx(alpha):
    return np.matrix([
        [1, 0, 0],
        [0, math.cos(alpha), -math.sin(alpha)],
        [0, math.sin(alpha), math.cos(alpha)]
    ])

def Ry(alpha):
    return np.matrix([
        [math.cos(alpha), 0, math.sin(alpha)],
        [0, 1, 0],
        [-math.sin(alpha), 0, math.cos(alpha)]

    ])

def Rz(alpha):
    return np.matrix([
        [math.cos(alpha), -math.sin(alpha), 0],
        [math.sin(alpha), math.cos(alpha), 0],
        [0, 0, 1]
    ])



# 1.
def eulerA2(phi, theta, psi):
    """

    :param phi: ugao rotacije oko X ose
    :param theta: ugao rotacije oko Y ose
    :param psi:  ugao rotacije oko Z ose
    :return: matrica rotacije
    """
    return np.linalg.multi_dot([Rz(psi), Ry(theta), Rx(phi)])



# 2.
def rodrigez(p, alpha):
    """

    :param p: prava rotacije
    :param alpha: ugao rotacije
    :return: matrica rotacije
    """

    px = np.matrix([[0, -p[2], p[1]],
                   [p[2], 0, -p[0]],
                   [-p[1], p[0], 0]])

    # np.outer(np.transpoe(p), p) == np.outer(p, p)
    return np.outer(p, p) + \
           np.cos(alpha) * (np.identity(3) - np.outer(3, 3)) + \
           np.sin(alpha) * px


# 3.
def eigenvector(A):
    """

    :param A: lista listi / matrica
    :return: jedinicni sopstveni vektor za lambda = 1
    """
    # (A - E)v = 0
    # jedno od resenja je [0, 0, 0] pa ce python uvek vratiti upravo to
    # zbog toga (A-E)v + 1 = 1
    T = A - np.identity(3)
    v = np.linalg.solve(T + 1, [1, 1, 1])

    return v / np.linalg.norm(v)

def perpVec(v):
    """

    :param v: jedinicni vektor
    :return:
    """

    # TODO nije uzeta greska u obzir
    # npr 1.123000e-18 == 0 => True ?

    u = [0, 1.0, 0]
    for pair in zip(u, v):
        if pair[0] != pair[1]:
            return u

    return [1.0, 0, 0]


def axisAngle(A):
    """

    :param A: matrica / lista listi
    :return: prava rotacije, ugao rotacije
    """

    p = eigenvector(A)
    u = np.cross(p, perpVec(p))
    # np.dot vraca [[...]] pa transformisemo u listu listi i uzimamo prvi element
    u_ = np.dot(A, u).tolist()[0]

    phi = math.acos(np.dot(u, u_))

    # ako je mesoviti proizvod manji od nule, menjamo orijentaciju
    if np.linalg.det([p, u, u_]) < 0:
        p = -p

    return (p, phi)



# 4.
def A2Euler(A):
    """

    :param A: Lista listi
    :return: [ugao oko Zose, ugao oko Yose, ugao oko Xose]
    """

    if (A[2][0] < 1):
        if (A[2][0] > -1):
            psi = math.atan2(A[1][0], A[0][0])
            theta = math.asin(-A[2][0])
            phi = math.atan2(A[2][1], A[2][2])

        else:
            psi = math.atan2(-A[0][1], A[1][1])
            theta = math.pi / 2
            phi = 0
    else:
        psi = math.atan2(-A[0][1], A[1][1])
        theta = - math.pi / 2
        phi = 0

    return [phi, theta, psi]

# 5.
def axisAngle2Q(p, phi):
    """

    :param p: prava rotacije
    :param phi: ugao rotacije
    :return: kvaternion td Cq = Rp(phi)
    """
    w = math.cos(phi / 2)

    # x, y, z
    v = math.sin(phi / 2) * p

    return np.append(v, w)

# 6.
def Q2AxisAngle(q):
    """

    :param q: jedinicni kvaternion = niz duzine 4
    :return: jedinicni vektor p; ugao rotacije phi td Cq = Rp(phi)
    """
    if (q[3] < 0):
        q = (-1) * q

    phi = 2 * math.acos(q[3])

    if (abs(q[3]) == 1):
        p = [1, 0, 0]
    else:
        p = q[:3] / np.linalg.norm(q[:3])

    return (p, phi)


def main():

    print()
    print("eulerA2(-math.atan(1/4), -math.asin(8/9), math.atan(4)")
    A = eulerA2(-math.atan(1/4), -math.asin(8/9), math.atan(4))
    print(A)
    print("---------------------------------------------------------")

    p, phi = axisAngle(A)
    print("axisAngle(A)")
    print(p, phi)
    print("---------------------------------------------------------")

    R = rodrigez(p, phi)
    print("rodrigez(p, phi)")
    print(R)
    print("---------------------------------------------------------")

    phi1, theta, psi = A2Euler(R.tolist())
    print("A2Euler(R)")
    print(phi1, theta, psi)
    print("---------------------------------------------------------")

    q = axisAngle2Q(p, phi)
    print("axisAngle2Q(p, phi)")
    print(q)
    print("---------------------------------------------------------")

    p1, phi2 = Q2AxisAngle(q)
    print("Q2AxisAngle(q)")
    print(p1, phi2)

if __name__ == '__main__':
    main()
