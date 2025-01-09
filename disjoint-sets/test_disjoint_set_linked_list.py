import unittest

from disjoint_set_linked_list import DisjointSetLinkedList


class TestDisjointSetLinkedList(unittest.TestCase):

    def test_initialize_set(self):
        disjoint_set = DisjointSetLinkedList([1, 2, 3])

        # Test that each element is in its own subset
        self.assertEqual(disjoint_set.find_set(1), 1)
        self.assertEqual(disjoint_set.find_set(2), 2)
        self.assertEqual(disjoint_set.find_set(3), 3)
        self.assertFalse(disjoint_set.same_set(1, 2) )
        self.assertFalse(disjoint_set.same_set(1, 3))
        self.assertFalse(disjoint_set.same_set(2, 3))
        self.assertCountEqual(disjoint_set.subsets(), [{1}, {2}, {3}])

    def test_add_set(self):
        disjoint_set = DisjointSetLinkedList([1])
        self.assertTrue(disjoint_set.make_set(2))
        self.assertFalse(disjoint_set.same_set(1, 2) )
        self.assertCountEqual(disjoint_set.subsets(), [{1}, {2}])

    def test_union_equal_size_subsets(self):
        disjoint_set = DisjointSetLinkedList([1, 2])

        self.assertEqual(disjoint_set.union(1, 2), 1)
        self.assertTrue(disjoint_set.same_set(1, 2) )
        self.assertFalse(disjoint_set.same_set(1, 3))
        self.assertCountEqual(disjoint_set.subsets(), [{1, 2}])

    def test_union_unequal_size_subsets(self):
        disjoint_set = DisjointSetLinkedList([1, 2])
        disjoint_set.union(1, 2)
        disjoint_set.make_set(3)

        # Union a bigger subset with a smaller subset, resulting set
        # inherits representative from the bigger subset
        self.assertEqual(disjoint_set.union(3, 1), 1)
        self.assertTrue(disjoint_set.same_set(1, 2) )
        self.assertTrue(disjoint_set.same_set(1, 3))
        self.assertTrue(disjoint_set.same_set(2, 3))
        self.assertCountEqual(disjoint_set.subsets(), [{1, 2, 3}])


if __name__ == "__main__":
    unittest.main()

