"""Dynamic-programming algorithms: Floyd-Warshall and Matrix Chain Multiplication."""
INF = float("inf")


def floyd_warshall(dist, ctr):
    """All-pairs shortest paths. dist = V x V matrix (INF = no edge, 0 diagonal). Theta(V^3) time, Theta(V^2) space."""
    n = len(dist)
    d = [row[:] for row in dist]
    inner = improved = 0
    for k in range(n):
        dk = d[k]
        for i in range(n):
            di, dik = d[i], d[i][k]
            for j in range(n):
                inner += 1
                nd = dik + dk[j]
                if nd < di[j]:
                    di[j] = nd
                    improved += 1
    ctr.inc("inner_iterations", inner)
    ctr.inc("improvements", improved)
    return d


def matrix_chain(dims, ctr):
    """Minimum scalar multiplications for a chain; matrix i has size dims[i] x dims[i+1].
    Theta(n^3) time, Theta(n^2) space. Returns (cost, parenthesisation string)."""
    n = len(dims) - 1
    if n <= 0:
        return 0, ""
    m = [[0] * n for _ in range(n)]
    s = [[0] * n for _ in range(n)]
    inner = 0
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            best, arg = INF, i
            for k in range(i, j):
                inner += 1
                c = m[i][k] + m[k + 1][j] + dims[i] * dims[k + 1] * dims[j + 1]
                if c < best:
                    best, arg = c, k
            m[i][j], s[i][j] = best, arg
    ctr.inc("inner_iterations", inner)

    def paren(i, j):
        if i == j:
            return f"A{i + 1}"
        return "(" + paren(i, s[i][j]) + paren(s[i][j] + 1, j) + ")"
    return m[0][n - 1], paren(0, n - 1)
