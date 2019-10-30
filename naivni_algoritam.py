import numpy as np


# konstruise matricu koja transformise A0, B0, C0, D0 u A, B, C, D
def transform(A, B, C, D):
    # transponujemo tacku D
    D = np.matrix.transpose(np.asarray(D))

    X = np.matrix.transpose(np.asarray([A, B, C]))
    Y = D
    params = np.linalg.solve(X, Y)

    G = []
    for i in range(0, len(X)):
        G.append(list(X[i] * params))

    return G


def main():
    # TODO dodati tacke

    G = transform(A, B, C, D)
    G_inv = np.linalg.inv(G)
    H = transform(A_, B_, C_, D_)
    # P je preslikavanje koje slika A,B,C,D u A_, B_, C_, D_
    P = np.dot(H, G_inv)


if __name__ == "__main__":
    main()




