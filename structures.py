"""Advanced data structures with operation counters:
Binomial Heap, Fibonacci Heap, Red-Black Tree, B-Tree (+ a naive BST baseline)."""
from metrics import Counter


# ----------------------------------------------------------------- Binomial heap
class BinNode:
    __slots__ = ("key", "degree", "child", "sibling", "parent")

    def __init__(self, key):
        self.key, self.degree = key, 0
        self.child = self.sibling = self.parent = None


class BinomialHeap:
    """Min-heap. insert/extract-min/merge/decrease-key are all O(log n)."""

    def __init__(self, ctr=None):
        self.head, self.size, self.ctr = None, 0, ctr or Counter()

    def _link(self, y, z):  # y becomes the leftmost child of z
        y.parent, y.sibling = z, z.child
        z.child = y
        z.degree += 1
        self.ctr.inc("links")

    @staticmethod
    def _merge_roots(a, b):
        dummy = BinNode(None)
        t = dummy
        while a and b:
            if a.degree <= b.degree:
                t.sibling, a = a, a.sibling
            else:
                t.sibling, b = b, b.sibling
            t = t.sibling
        t.sibling = a or b
        return dummy.sibling

    def _union(self, other_head):
        head = self._merge_roots(self.head, other_head)
        if head is None:
            self.head = None
            return
        prev, x = None, head
        nxt = x.sibling
        while nxt:
            if x.degree != nxt.degree or (nxt.sibling and nxt.sibling.degree == x.degree):
                prev, x = x, nxt
            else:
                self.ctr.inc("comparisons")
                if x.key <= nxt.key:
                    x.sibling = nxt.sibling
                    self._link(nxt, x)
                else:
                    if prev is None:
                        head = nxt
                    else:
                        prev.sibling = nxt
                    self._link(x, nxt)
                    x = nxt
            nxt = x.sibling
        self.head = head

    def insert(self, key):
        self.ctr.inc("insert_calls")
        node = BinNode(key)
        self._union(node)
        self.size += 1
        return node

    def merge(self, other):
        self.ctr.inc("merge_calls")
        self._union(other.head)
        self.size += other.size
        other.head, other.size = None, 0

    def find_min(self):
        best, x = None, self.head
        while x:
            if best is None or x.key < best.key:
                best = x
            x = x.sibling
        return None if best is None else best.key

    def extract_min(self):
        self.ctr.inc("extract_min_calls")
        if self.head is None:
            return None
        best, bprev, prev, x = self.head, None, None, self.head
        while x:
            self.ctr.inc("comparisons")
            if x.key < best.key:
                best, bprev = x, prev
            prev, x = x, x.sibling
        if bprev:
            bprev.sibling = best.sibling
        else:
            self.head = best.sibling
        rev, child = None, best.child
        while child:  # children are in decreasing degree: reverse them
            nxt = child.sibling
            child.sibling, child.parent = rev, None
            rev, child = child, nxt
        self._union(rev)
        self.size -= 1
        return best.key

    def decrease_key(self, node, new_key):
        self.ctr.inc("decrease_key_calls")
        if new_key > node.key:
            raise ValueError("new key is larger")
        node.key = new_key
        while node.parent is not None and node.key < node.parent.key:
            node.key, node.parent.key = node.parent.key, node.key  # swap payload upward
            self.ctr.inc("swaps")
            node = node.parent


# --------------------------------------------------------------- Fibonacci heap
class FibNode:
    __slots__ = ("key", "degree", "parent", "child", "left", "right", "mark")

    def __init__(self, key):
        self.key, self.degree, self.mark = key, 0, False
        self.parent = self.child = None
        self.left = self.right = self


class FibonacciHeap:
    """Min-heap. insert/merge/decrease-key are O(1) amortised, extract-min O(log n) amortised."""

    def __init__(self, ctr=None):
        self.min, self.size, self.ctr = None, 0, ctr or Counter()

    @staticmethod
    def _iter(start):
        out = []
        if start is None:
            return out
        x = start
        while True:
            out.append(x)
            x = x.right
            if x is start:
                break
        return out

    @staticmethod
    def _splice_after(anchor, node):  # put node right of anchor in a circular list
        node.left, node.right = anchor, anchor.right
        anchor.right.left = node
        anchor.right = node

    def _add_root(self, node):
        node.parent, node.mark = None, False
        if self.min is None:
            node.left = node.right = node
            self.min = node
        else:
            self._splice_after(self.min, node)
            self.ctr.inc("comparisons")
            if node.key < self.min.key:
                self.min = node

    def insert(self, key):
        self.ctr.inc("insert_calls")
        node = FibNode(key)
        self._add_root(node)
        self.size += 1
        return node

    def merge(self, other):
        self.ctr.inc("merge_calls")
        self.ctr.inc("splices")
        if other.min is None:
            return
        if self.min is None:
            self.min = other.min
        else:
            a, b = self.min, other.min
            a_right, b_left = a.right, b.left
            a.right, b.left = b, a
            a_right.left, b_left.right = b_left, a_right
            self.ctr.inc("comparisons")
            if other.min.key < self.min.key:
                self.min = other.min
        self.size += other.size
        other.min, other.size = None, 0

    def _link(self, y, x):  # y becomes a child of x
        y.parent, y.mark = x, False
        if x.child is None:
            x.child = y
            y.left = y.right = y
        else:
            self._splice_after(x.child, y)
        x.degree += 1
        self.ctr.inc("links")

    def _consolidate(self):
        table = {}
        for w in self._iter(self.min):
            x, d = w, w.degree
            while d in table:
                y = table.pop(d)
                self.ctr.inc("comparisons")
                if x.key > y.key:
                    x, y = y, x
                self._link(y, x)
                d = x.degree
            table[d] = x
        self.min = None
        for x in table.values():
            x.left = x.right = x
            x.parent = None
            if self.min is None:
                self.min = x
            else:
                self._splice_after(self.min, x)
                self.ctr.inc("comparisons")
                if x.key < self.min.key:
                    self.min = x

    def extract_min(self):
        self.ctr.inc("extract_min_calls")
        z = self.min
        if z is None:
            return None
        for c in self._iter(z.child):
            c.parent, c.mark = None, False
            self._splice_after(z, c)
        z.child, z.degree = None, 0
        if z.right is z:
            self.min = None
        else:
            z.left.right, z.right.left = z.right, z.left
            self.min = z.right
            self._consolidate()
        self.size -= 1
        return z.key

    def _cut(self, x, y):
        if y.child is x:
            y.child = x.right if x.right is not x else None
        x.left.right, x.right.left = x.right, x.left
        y.degree -= 1
        self._add_root(x)
        self.ctr.inc("cuts")

    def _cascade(self, y):
        z = y.parent
        while z is not None:
            if not y.mark:
                y.mark = True
                return
            self._cut(y, z)
            y, z = z, z.parent

    def decrease_key(self, node, new_key):
        self.ctr.inc("decrease_key_calls")
        if new_key > node.key:
            raise ValueError("new key is larger")
        node.key = new_key
        y = node.parent
        if y is not None and node.key < y.key:
            self._cut(node, y)
            self._cascade(y)
        self.ctr.inc("comparisons")
        if node.key < self.min.key:
            self.min = node


# --------------------------------------------------------------- Red-Black tree
RED, BLACK = 0, 1


class RBNode:
    __slots__ = ("key", "color", "left", "right", "parent")

    def __init__(self, key, color):
        self.key, self.color = key, color
        self.left = self.right = self.parent = None


class RedBlackTree:
    """Self-balancing BST: height <= 2*log2(n+1). Counts comparisons, rotations, recolours."""

    def __init__(self, ctr=None):
        self.ctr = ctr or Counter()
        self.NIL = RBNode(None, BLACK)
        self.NIL.left = self.NIL.right = self.NIL.parent = self.NIL
        self.root, self.size = self.NIL, 0

    def _rot_left(self, x):
        self.ctr.inc("rotations")
        y = x.right
        x.right = y.left
        if y.left is not self.NIL:
            y.left.parent = x
        y.parent = x.parent
        if x.parent is self.NIL:
            self.root = y
        elif x is x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left, x.parent = x, y

    def _rot_right(self, x):
        self.ctr.inc("rotations")
        y = x.left
        x.left = y.right
        if y.right is not self.NIL:
            y.right.parent = x
        y.parent = x.parent
        if x.parent is self.NIL:
            self.root = y
        elif x is x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y
        y.right, x.parent = x, y

    def insert(self, key):
        self.ctr.inc("insert_calls")
        z = RBNode(key, RED)
        z.left = z.right = self.NIL
        y, x = self.NIL, self.root
        while x is not self.NIL:
            y = x
            self.ctr.inc("comparisons")
            x = x.left if key < x.key else x.right
        z.parent = y
        if y is self.NIL:
            self.root = z
        elif key < y.key:
            y.left = z
        else:
            y.right = z
        self._fix(z)
        self.size += 1

    def _fix(self, z):
        while z.parent.color == RED:
            g = z.parent.parent
            if z.parent is g.left:
                u = g.right
                if u.color == RED:
                    z.parent.color = u.color = BLACK
                    g.color = RED
                    self.ctr.inc("recolors")
                    z = g
                else:
                    if z is z.parent.right:
                        z = z.parent
                        self._rot_left(z)
                    z.parent.color, z.parent.parent.color = BLACK, RED
                    self._rot_right(z.parent.parent)
            else:
                u = g.left
                if u.color == RED:
                    z.parent.color = u.color = BLACK
                    g.color = RED
                    self.ctr.inc("recolors")
                    z = g
                else:
                    if z is z.parent.left:
                        z = z.parent
                        self._rot_right(z)
                    z.parent.color, z.parent.parent.color = BLACK, RED
                    self._rot_left(z.parent.parent)
        self.root.color = BLACK

    def search(self, key):
        self.ctr.inc("search_calls")
        x = self.root
        while x is not self.NIL:
            self.ctr.inc("search_comparisons")
            if key == x.key:
                return True
            x = x.left if key < x.key else x.right
        return False

    def height(self):
        best, stack = 0, [(self.root, 1)]
        while stack:
            n, d = stack.pop()
            if n is self.NIL:
                continue
            best = max(best, d)
            stack += [(n.left, d + 1), (n.right, d + 1)]
        return best

    def inorder(self):
        out, stack, x = [], [], self.root
        while stack or x is not self.NIL:
            while x is not self.NIL:
                stack.append(x)
                x = x.left
            x = stack.pop()
            out.append(x.key)
            x = x.right
        return out

    def check_invariants(self):
        if self.root.color != BLACK:
            return False

        def walk(n):  # returns black-height or -1 on violation
            if n is self.NIL:
                return 1
            if n.color == RED and (n.left.color == RED or n.right.color == RED):
                return -1
            a, b = walk(n.left), walk(n.right)
            if a == -1 or b == -1 or a != b:
                return -1
            return a + (1 if n.color == BLACK else 0)
        return walk(self.root) != -1


class NaiveBST:
    """Unbalanced BST baseline: degenerates to a linked list on sorted input (O(n^2) total)."""

    def __init__(self, ctr=None):
        self.ctr, self.root, self.size = ctr or Counter(), None, 0

    def insert(self, key):
        self.ctr.inc("insert_calls")
        node = [key, None, None]
        self.size += 1
        if self.root is None:
            self.root = node
            return
        x, comps = self.root, 0
        while True:
            comps += 1
            i = 1 if key < x[0] else 2
            if x[i] is None:
                x[i] = node
                break
            x = x[i]
        self.ctr.inc("comparisons", comps)

    def height(self):
        best, stack = 0, [(self.root, 1)] if self.root else []
        while stack:
            n, d = stack.pop()
            best = max(best, d)
            for c in (n[1], n[2]):
                if c is not None:
                    stack.append((c, d + 1))
        return best


# ------------------------------------------------------------------------ B-Tree
class BTNode:
    __slots__ = ("keys", "children", "leaf")

    def __init__(self, leaf):
        self.keys, self.children, self.leaf = [], [], leaf


class BTree:
    """B-Tree of minimum degree t (each node holds t-1 .. 2t-1 keys). Counts splits, node accesses
    (a proxy for disk reads) and key comparisons."""

    def __init__(self, t=2, ctr=None):
        if t < 2:
            raise ValueError("minimum degree t must be >= 2")
        self.t, self.ctr, self.root, self.size = t, ctr or Counter(), BTNode(True), 0

    def _split_child(self, x, i):
        t = self.t
        y = x.children[i]
        z = BTNode(y.leaf)
        mid = y.keys[t - 1]
        z.keys, y.keys = y.keys[t:], y.keys[:t - 1]
        if not y.leaf:
            z.children, y.children = y.children[t:], y.children[:t]
        x.children.insert(i + 1, z)
        x.keys.insert(i, mid)
        self.ctr.inc("splits")

    def insert(self, key):
        self.ctr.inc("insert_calls")
        t = self.t
        if len(self.root.keys) == 2 * t - 1:
            s = BTNode(False)
            s.children = [self.root]
            self.root = s
            self._split_child(s, 0)
        x = self.root
        while True:
            self.ctr.inc("node_accesses")
            i = len(x.keys) - 1
            comps = 0
            while i >= 0:
                comps += 1
                if key < x.keys[i]:
                    i -= 1
                else:
                    break
            self.ctr.inc("comparisons", comps)
            if x.leaf:
                x.keys.insert(i + 1, key)
                break
            i += 1
            if len(x.children[i].keys) == 2 * t - 1:
                self._split_child(x, i)
                if key > x.keys[i]:
                    i += 1
            x = x.children[i]
        self.size += 1

    def search(self, key):
        self.ctr.inc("search_calls")
        x = self.root
        while True:
            self.ctr.inc("search_node_accesses")
            i = 0
            while i < len(x.keys) and key > x.keys[i]:
                i += 1
                self.ctr.inc("search_comparisons")
            if i < len(x.keys) and key == x.keys[i]:
                return True
            if x.leaf:
                return False
            x = x.children[i]

    def height(self):
        h, x = 1, self.root
        while not x.leaf:
            x, h = x.children[0], h + 1
        return h

    def inorder(self):
        out = []

        def walk(n):
            for i, k in enumerate(n.keys):
                if not n.leaf:
                    walk(n.children[i])
                out.append(k)
            if not n.leaf:
                walk(n.children[-1])
        walk(self.root)
        return out

    def check_invariants(self):
        t = self.t
        depths = set()

        def walk(n, depth, is_root):
            if len(n.keys) > 2 * t - 1 or (not is_root and len(n.keys) < t - 1):
                return False
            if n.keys != sorted(n.keys):
                return False
            if n.leaf:
                depths.add(depth)
                return True
            if len(n.children) != len(n.keys) + 1:
                return False
            return all(walk(c, depth + 1, False) for c in n.children)
        return walk(self.root, 0, True) and len(depths) <= 1
