#!/usr/bin/env python3

import unittest

from pr_review_threads import DEFAULT_AI_AUTHORS, author_matches, filtered_threads, parse_pr_ref


class ReviewThreadTests(unittest.TestCase):
    def test_refs_and_ai_filter(self) -> None:
        self.assertEqual(("acme", "app", 42), parse_pr_ref("acme/app#42"))
        ai_thread = {"id": "ai", "isResolved": False, "comments": {"nodes": [{"author": {"login": "cursor[bot]"}}]}}
        human_thread = {"id": "human", "isResolved": False, "comments": {"nodes": [{"author": {"login": "alice"}}]}}
        payload = {"review_threads": [ai_thread, human_thread]}
        self.assertTrue(author_matches(ai_thread, DEFAULT_AI_AUTHORS))
        self.assertEqual([ai_thread], filtered_threads(payload, DEFAULT_AI_AUTHORS, False, False))
        self.assertEqual([ai_thread, human_thread], filtered_threads(payload, DEFAULT_AI_AUTHORS, False, True))


if __name__ == "__main__":
    unittest.main()
