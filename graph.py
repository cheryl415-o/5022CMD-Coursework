"""Generic unweighted directed graph (adjacency lists).

Vertices can be any hashable object, so the class has no knowledge of any
specific domain (e.g. Course) and can be reused in other contexts.

For every vertex we keep two adjacency lists:
  _out[v] - vertices that v points to        (v -> x)
  _in[v]  - vertices that point to v         (x -> v)
Keeping the incoming list makes listIncomingAdjacentVertex O(deg-in) instead
of scanning the whole graph.
"""

from typing import Dict, Generic, Hashable, List, TypeVar

V = TypeVar("V", bound=Hashable)


class DirectedGraph(Generic[V]):
    def __init__(self) -> None:
        self._out: Dict[V, List[V]] = {}
        self._in: Dict[V, List[V]] = {}

    # ---------- required methods ----------
    def addVertex(self, vertex: V) -> bool:
        """Add a vertex. Returns False if it already exists."""
        if vertex in self._out:
            return False
        self._out[vertex] = []
        self._in[vertex] = []
        return True

    def addEdge(self, source: V, target: V) -> bool:
        """Add a directed edge source -> target.

        Returns False if either vertex is missing, the edge already exists,
        or it would be a self-loop.
        """
        if source not in self._out or target not in self._out:
            return False
        if source == target or target in self._out[source]:
            return False
        self._out[source].append(target)
        self._in[target].append(source)
        return True

    def listIncomingAdjacentVertex(self, vertex: V) -> List[V]:
        """All vertices that have an edge pointing INTO vertex."""
        return list(self._in.get(vertex, []))

    # ---------- extra helpers ----------
    def listOutgoingAdjacentVertex(self, vertex: V) -> List[V]:
        """All vertices that vertex points TO."""
        return list(self._out.get(vertex, []))

    def removeEdge(self, source: V, target: V) -> bool:
        if source not in self._out or target not in self._out[source]:
            return False
        self._out[source].remove(target)
        self._in[target].remove(source)
        return True

    def hasVertex(self, vertex: V) -> bool:
        return vertex in self._out

    def hasEdge(self, source: V, target: V) -> bool:
        return source in self._out and target in self._out[source]

    def vertices(self) -> List[V]:
        return list(self._out)

    def wouldCreateCycle(self, source: V, target: V) -> bool:
        """True if adding source -> target would create a cycle,
        i.e. if source is already reachable from target."""
        stack, seen = [target], set()
        while stack:
            cur = stack.pop()
            if cur == source:
                return True
            if cur in seen:
                continue
            seen.add(cur)
            stack.extend(self._out[cur])
        return False
