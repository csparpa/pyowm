#!/usr/bin/env python

"""
Test case for linkedlist.py module.
"""

import unittest
from pyowm.commons.frontlinkedlist import FrontLinkedList


class TestFrontLinkedList(unittest.TestCase):

    def test_add(self):
        instance = FrontLinkedList()
        self.assertEqual(0, instance.size())
        instance.add("test1")
        self.assertEqual(1, instance.size())
        instance.add("test2")
        self.assertEqual(2, instance.size())

    def test_remove(self):
        instance = FrontLinkedList()
        for i in range(1, 6):
            instance.add(i)
        self.assertEqual(5, instance.size())
        instance.remove(3)
        self.assertEqual(4, instance.size())
        for item in instance:
            self.assertNotEqual(3, item.data())

    def test_remove_deletes_the_first_occurrence_from_the_front(self):
        instance = FrontLinkedList()
        instance.add("4")
        instance.add("3")
        instance.add("2")
        instance.add("1")
        instance.add("4")
        instance.add("0")
        instance.remove("4")
        counter = 0
        next_item = None
        for item in instance:
            if item.data() == "4":
                counter += 1
                next_item = item.next()
        self.assertEqual(1, counter)
        self.assertFalse(next_item)

    def test_contains(self):
        instance = FrontLinkedList()
        instance.add(12)
        instance.add(3)
        instance.add(456)
        self.assertTrue(instance.contains(3))
        self.assertFalse(instance.contains("test"))

    def test_index_of(self):
        instance = FrontLinkedList()
        instance.add("first")
        instance.add("middle")
        instance.add("last")
        self.assertEqual(2, instance.index_of("first"))
        self.assertEqual(1, instance.index_of("middle"))
        self.assertEqual(0, instance.index_of("last"))

    def test_pop(self):
        instance = FrontLinkedList()
        expected = "popped"
        instance.add(expected)
        instance.add(4)
        instance.add(3)
        instance.add(2)
        instance.add(1)
        result = instance.pop()
        self.assertFalse(instance.contains("popped"))
        self.assertEqual(expected, result)
