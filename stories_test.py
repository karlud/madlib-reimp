#!/usr/bin/env python3

import unittest
import stories


class TemplateTest(unittest.TestCase):
    def testFindFields(self):
        text = "My {rumpus} ate my {bearclaw}."
        correct = {'{rumpus}', '{bearclaw}'}
        fields = stories.FindFields(text)
        self.assertEqual(fields, correct)

    def testFindFieldAtStart(self):
        text = "{name} likes {name}'s name, which is '{name}'."
        correct = {'{name}'}
        fields = stories.FindFields(text)
        self.assertEqual(fields, correct)

    def testEmptyField(self):
        test = "This has a {} empty field."
        with self.assertRaises(stories.ParseError):
            stories.FindFields(test)

    def testUnclosedField(self):
        test = "This has an {unclosed."
        with self.assertRaises(stories.ParseError):
            stories.FindFields(test)

    def testUnopenedField(self):
        test = "This has a } busted field."
        with self.assertRaises(stories.ParseError):
            stories.FindFields(test)

    def testReplace(self):
        test = "These words {verb} no sense."
        fields = {'{verb}': 'balloon'}
        self.assertEqual("These words balloon no sense.",
                         stories.Replace(test, fields))


if __name__ == '__main__':
    unittest.main()
