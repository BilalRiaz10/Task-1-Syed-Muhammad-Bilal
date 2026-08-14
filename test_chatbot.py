"""
Automated Test Suite for Project 1: Rule-Based AI Chatbot
Validates:
1. Input Sanitization & Normalization
2. O(1) Static Knowledge Base Retrieval
3. Dynamic Dataset Lookups (Order ID & Tracking Number)
4. Product Catalog and Business Analytics
5. Atomic Fallback Execution
6. Exit/Kill Command Termination
"""

import unittest
from chatbot import RuleBasedAIChatbot


class TestRuleBasedAIChatbot(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.bot = RuleBasedAIChatbot()

    def test_01_sanitization(self):
        """Test that inputs are lowercased and stripped of leading/trailing spaces."""
        self.assertEqual(self.bot.sanitize_input("  HELLO  "), "hello")
        self.assertEqual(self.bot.sanitize_input("\tWhAt Is ThIs \n"), "what is this")
        self.assertEqual(self.bot.sanitize_input(""), "")

    def test_02_static_greetings_and_intents(self):
        """Test static 5+ intent responses in knowledge base."""
        # Greeting intent
        resp, should_exit = self.bot.process_query("  HeLLo  ")
        self.assertIn("DecodeLabs", resp)
        self.assertFalse(should_exit)

        # Help intent
        resp, should_exit = self.bot.process_query("HELP")
        self.assertIn("Order Tracking", resp)
        self.assertFalse(should_exit)

        # About intent
        resp, should_exit = self.bot.process_query("about")
        self.assertIn("Project 1", resp)
        self.assertFalse(should_exit)

        # Capabilities intent
        resp, should_exit = self.bot.process_query("capabilities")
        self.assertIn("1,200 transactions", resp)
        self.assertFalse(should_exit)

        # Coupons intent
        resp, should_exit = self.bot.process_query("coupons")
        self.assertIn("FREESHIP", resp)
        self.assertFalse(should_exit)

    def test_03_order_lookup_by_id(self):
        """Test O(1) order lookup using OrderID from dataset."""
        resp, should_exit = self.bot.process_query("track ORD200000")
        self.assertIn("ORD200000", resp)
        self.assertIn("Monitor", resp)
        self.assertIn("TRK37947903", resp)
        self.assertFalse(should_exit)

    def test_04_order_lookup_by_tracking(self):
        """Test O(1) order lookup using TrackingNumber from dataset."""
        resp, should_exit = self.bot.process_query("where is TRK91186779")
        self.assertIn("ORD200001", resp)
        self.assertIn("Phone", resp)
        self.assertFalse(should_exit)

    def test_05_product_intelligence(self):
        """Test product analytics lookup."""
        resp, should_exit = self.bot.process_query("product laptop")
        self.assertIn("Product Intelligence [Laptop]", resp)
        self.assertIn("Total Revenue", resp)
        self.assertFalse(should_exit)

    def test_06_business_analytics(self):
        """Test aggregate sales and analytics reports."""
        resp, should_exit = self.bot.process_query("sales summary")
        self.assertIn("Executive Business Summary", resp)
        self.assertIn("1,200", resp)

        resp_status, _ = self.bot.process_query("status breakdown")
        self.assertIn("Order Fulfillment Breakdown", resp_status)

        resp_ref, _ = self.bot.process_query("referrals")
        self.assertIn("Marketing Referral Channels", resp_ref)

    def test_07_atomic_fallback(self):
        """Test default fallback response for unknown / out-of-domain inputs."""
        resp, should_exit = self.bot.process_query("asdkjhasd random unmapped question")
        self.assertIn("could not recognize", resp)
        self.assertFalse(should_exit)

    def test_08_exit_commands(self):
        """Test graceful kill commands for loop termination."""
        for cmd in ["exit", "quit", "bye", "close"]:
            resp, should_exit = self.bot.process_query(f"  {cmd.upper()}  ")
            self.assertIn("Goodbye", resp)
            self.assertTrue(should_exit)


if __name__ == "__main__":
    unittest.main()
