#!/usr/bin/env python3

import unittest
import stories


class TemplateTest(unittest.TestCase):
    def testFindFields(self):
        text = "My {rumpus} ate my {bearclaw}."
        correct = {'{rumpus}', '{bearclaw}'}
        fields = stories.StoryTemplate(text).fields
        self.assertEqual(fields, correct)

    def testFindFieldAtStart(self):
        text = "{name} likes {name}'s name, which is '{name}'."
        correct = {'{name}'}
        fields = stories.StoryTemplate(text).fields
        self.assertEqual(fields, correct)

    def testEmptyField(self):
        test = "This has a {} empty field."
        with self.assertRaises(stories.ParseError):
            stories.StoryTemplate(test)

    def testUnclosedField(self):
        test = "This has an {unclosed."
        with self.assertRaises(stories.ParseError):
            stories.StoryTemplate(test)

    def testUnopenedField(self):
        test = "This has a } busted field."
        with self.assertRaises(stories.ParseError):
            stories.StoryTemplate(test)

    def testReplace(self):
        test = "These words {verb} no sense."
        fields = {'{verb}': 'balloon'}
        self.assertEqual("These words balloon no sense.",
                         stories.StoryTemplate(test).Populate(fields))

    def testHTMLForm(self):
        text = "My dog ate my {bearclaw}."
        st = stories.StoryTemplate(text)
        html = st.HTMLForm(hidden='<input type=hidden name=test value=test>')
        self.assertEqual(html, (
            '<!DOCTYPE html>\n'
            '<title>Story</title>\n'
            '<form method=POST>\n'
            '<label>bearclaw: <input type=text name="bearclaw"></label><br>\n'
            '<input type=hidden name=test value=test>\n'
            '<button type=submit>Tell me a story!</button>\n'
            '</form>'))



if __name__ == '__main__':
    unittest.main()
