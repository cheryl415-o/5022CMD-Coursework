"""Generic hash table using open addressing with linear probing.

The table is not tied to any domain class: keys can be any hashable value
(int or str) and values can be any object, so it can be reused elsewhere.
"""

from typing import Any, Optional


class Slot:
    """One slot (bucket) of the hash table.

    A slot is in one of three states:
      EMPTY    - never used; a search can stop here
      OCCUPIED - holds a key/value pair
      DELETED  - tombstone left by a removal; searches must keep probing
    """

    EMPTY = 0
    OCCUPIED = 1
    DELETED = 2

    __slots__ = ("key", "value", "state")

    def __init__(self) -> None:
        self.key: Any = None
        self.value: Any = None
        self.state: int = Slot.EMPTY


class HashTable:
    """Open-addressing hash table with linear probing.

    index = (hash(key) + i) % capacity   for i = 0, 1, 2, ...
    """

    def __init__(self, capacity: int = 31) -> None:
        if capacity < 1:
            raise ValueError("capacity must be at least 1")
        self._capacity = capacity
        self._slots = [Slot() for _ in range(capacity)]
        self._size = 0

    # ---------- helpers ----------
    def _hash(self, key: Any) -> int:
        """Hash function. Integers use a simple modulo; other keys use hash()."""
        if isinstance(key, int):
            return key % self._capacity
        return hash(key) % self._capacity

    def __len__(self) -> int:
        return self._size

    @property
    def capacity(self) -> int:
        return self._capacity

    def load_factor(self) -> float:
        return self._size / self._capacity

    # ---------- operations ----------
    def insert(self, key: Any, value: Any) -> int:
        """Insert (or update) a key. Returns the slot index used.

        Raises OverflowError if the table is full.
        """
        start = self._hash(key)
        first_free: Optional[int] = None

        for i in range(self._capacity):
            idx = (start + i) % self._capacity
            slot = self._slots[idx]

            if slot.state == Slot.OCCUPIED:
                if slot.key == key:          # duplicate key -> update value
                    slot.value = value
                    return idx
            elif slot.state == Slot.DELETED:
                if first_free is None:       # remember first reusable tombstone
                    first_free = idx
            else:                            # EMPTY: key is definitely absent
                if first_free is None:
                    first_free = idx
                break

        if first_free is None:
            raise OverflowError("Hash table is full")

        slot = self._slots[first_free]
        slot.key, slot.value, slot.state = key, value, Slot.OCCUPIED
        self._size += 1
        return first_free

    def search(self, key: Any) -> Optional[Any]:
        """Return the value stored for key, or None if not found."""
        idx = self._find_index(key)
        return None if idx is None else self._slots[idx].value

    def _find_index(self, key: Any) -> Optional[int]:
        start = self._hash(key)
        for i in range(self._capacity):
            idx = (start + i) % self._capacity
            slot = self._slots[idx]
            if slot.state == Slot.EMPTY:
                return None
            if slot.state == Slot.OCCUPIED and slot.key == key:
                return idx
        return None

    def delete(self, key: Any) -> bool:
        """Remove a key (leaves a tombstone). Returns True if it existed."""
        idx = self._find_index(key)
        if idx is None:
            return False
        slot = self._slots[idx]
        slot.key, slot.value, slot.state = None, None, Slot.DELETED
        self._size -= 1
        return True

    def values(self):
        """Yield all stored values (in slot order)."""
        for slot in self._slots:
            if slot.state == Slot.OCCUPIED:
                yield slot.value

    def __contains__(self, key: Any) -> bool:
        return self._find_index(key) is not None
