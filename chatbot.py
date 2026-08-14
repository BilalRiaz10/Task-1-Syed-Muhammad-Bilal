"""
Rule-Based AI Chatbot - Industrial Training Kit (Project 1)
Powered by DecodeLabs Architecture Principles:
- IPO (Input -> Process -> Output) Model
- O(1) Hash Map / Dictionary Lookups (Eliminating O(n) if-elif anti-pattern)
- Atomic .get() response retrieval with fallback
- Input Sanitization & Normalization (.lower().strip())
- Interactive Heartbeat Infinite Loop with Clean Kill Command
"""

import sys
import re
from typing import Dict, Tuple, Optional
from data_engine import DataEngine


class RuleBasedAIChatbot:
    def __init__(self):
        # Initialize the underlying data engine with indexed dataset
        self.data_engine = DataEngine()
        
        # Static Knowledge Base (O(1) Dictionary Lookup)
        # Maps canonical normalized intents to response generation functions or static text
        self.static_responses: Dict[str, str] = {
            "hello": "Hello! I am your AI Assistant from DecodeLabs. How can I help you today?",
            "hi": "Hi there! Welcome to DecodeLabs AI. How may I assist you?",
            "hey": "Hey! Great to see you. Feel free to ask about orders, products, or analytics.",
            "greetings": "Greetings! I am ready to assist with your queries.",
            "who are you": "I am a deterministic, rule-based AI Chatbot engineered for high-precision query processing and zero-hallucination guardrails.",
            "about": "DecodeLabs AI Rule-Based System (Project 1):\nA deterministic logic engine operating on O(1) hash tables with zero hallucination risk.",
            "help": (
                "Here are some commands and queries you can try:\n"
                "  • Greetings: 'hello', 'hi', 'hey'\n"
                "  • General: 'help', 'about', 'who are you', 'capabilities'\n"
                "  • Order Tracking: 'track ORD200000', 'order ORD200004', 'track TRK37947903'\n"
                "  • Product Lookup: 'product laptop', 'price monitor', 'product phone'\n"
                "  • Analytics: 'sales summary', 'status breakdown', 'referrals', 'coupons'\n"
                "  • Exit: 'exit', 'quit', 'bye', 'close'"
            ),
            "capabilities": (
                "My capabilities include:\n"
                "  1. Order & tracking lookups across 1,200 transactions.\n"
                "  2. Product catalog pricing and aggregate sales summaries.\n"
                "  3. Executive financial analytics and channel breakdown.\n"
                "  4. Instant O(1) deterministic response generation."
            ),
            "coupons": (
                "Active promotional campaigns in our dataset:\n"
                f"  • FREESHIP: {self.data_engine.get_coupon_info('freeship')} redemptions\n"
                f"  • WINTER15: {self.data_engine.get_coupon_info('winter15')} redemptions\n"
                f"  • SAVE10:   {self.data_engine.get_coupon_info('save10')} redemptions"
            ),
        }

        # Kill/Exit command set for clean termination
        self.exit_commands = {"exit", "quit", "bye", "close", "stop", "terminate", "kill"}

        # Fallback response for unmapped / out-of-domain queries
        self.fallback_message = (
            "I'm sorry, I could not recognize that command. "
            "Type 'help' to see all available commands, order queries, or product lookups."
        )

    def sanitize_input(self, raw_input: str) -> str:
        """
        Phase 1: Input & Sanitization (IPO Model)
        Normalizes text by lowercasing and trimming excessive whitespace.
        """
        if not raw_input:
            return ""
        return raw_input.lower().strip()

    def handle_sales_summary(self) -> str:
        """Generates executive sales and revenue metrics response."""
        m = self.data_engine.get_metrics()
        return (
            "📊 Executive Business Summary:\n"
            f"  • Total Revenue:       ${m['total_revenue']:,.2f}\n"
            f"  • Total Orders:        {m['total_orders']:,}\n"
            f"  • Units Sold:          {m['total_units_sold']:,}\n"
            f"  • Average Order Value: ${m['avg_order_value']:,.2f}\n"
            f"  • Unique Customers:    {m['unique_customers']:,}\n"
            f"  • Active Period:       {m['date_range']}"
        )

    def handle_status_breakdown(self) -> str:
        """Generates order fulfillment status distribution."""
        sc = self.data_engine.status_counts
        total = self.data_engine.metrics["total_orders"]
        lines = ["📦 Order Fulfillment Breakdown:"]
        for status, count in sorted(sc.items(), key=lambda x: x[1], reverse=True):
            pct = (count / total) * 100
            lines.append(f"  • {status.capitalize():<12}: {count:>4} orders ({pct:>5.1f}%)")
        return "\n".join(lines)

    def handle_referral_breakdown(self) -> str:
        """Generates referral channel breakdown."""
        rc = self.data_engine.referral_counts
        total = self.data_engine.metrics["total_orders"]
        lines = ["🌐 Marketing Referral Channels:"]
        for channel, count in sorted(rc.items(), key=lambda x: x[1], reverse=True):
            pct = (count / total) * 100
            lines.append(f"  • {channel.capitalize():<12}: {count:>4} visits ({pct:>5.1f}%)")
        return "\n".join(lines)

    def handle_order_lookup(self, identifier: str) -> str:
        """Handles O(1) order tracking and details lookup."""
        order = self.data_engine.get_order(identifier)
        if not order:
            return f"❌ No order found matching Order ID or Tracking Number: '{identifier}'."
        
        return (
            f"📦 Order Details [{order['OrderID']}]:\n"
            f"  • Order Status:    {order['OrderStatus']}\n"
            f"  • Tracking Number: {order['TrackingNumber']}\n"
            f"  • Order Date:      {order['Date']}\n"
            f"  • Customer ID:     {order['CustomerID']}\n"
            f"  • Product:         {order['Product']} (Qty: {order['Quantity']})\n"
            f"  • Unit Price:      ${order['UnitPrice']:,.2f}\n"
            f"  • Total Price:     ${order['TotalPrice']:,.2f}\n"
            f"  • Payment Method:  {order['PaymentMethod']}\n"
            f"  • Coupon Applied:  {order['CouponCode']}\n"
            f"  • Shipping To:     {order['ShippingAddress']}"
        )

    def handle_product_lookup(self, prod_query: str) -> str:
        """Handles O(1) product performance and catalog lookup."""
        prod = self.data_engine.get_product(prod_query)
        if not prod:
            available = ", ".join([p.capitalize() for p in self.data_engine.products.keys()])
            return f"❌ Product '{prod_query}' not found. Available products: {available}"
        
        return (
            f"🏷️ Product Intelligence [{prod['name']}]:\n"
            f"  • Total Orders:    {prod['total_orders']:,}\n"
            f"  • Total Units Sold:{prod['total_units']:,}\n"
            f"  • Total Revenue:   ${prod['total_revenue']:,.2f}\n"
            f"  • Average Price:   ${prod['avg_price']:,.2f}\n"
            f"  • Price Range:     ${prod['min_price']:,.2f} - ${prod['max_price']:,.2f}"
        )

    def process_query(self, raw_input: str) -> Tuple[str, bool]:
        """
        Phase 2: Process (The Logic Skeleton)
        Evaluates the input using O(1) hash maps and rule patterns.
        Returns: (Response string, is_exit_flag)
        """
        clean_input = self.sanitize_input(raw_input)

        if not clean_input:
            return "Please type a question or command. Type 'help' for examples.", False

        # 1. Kill / Exit command verification
        if clean_input in self.exit_commands:
            return "Goodbye! Thank you for using DecodeLabs AI Chatbot.", True

        # 2. Static Knowledge Base Direct Lookup (O(1))
        if clean_input in self.static_responses:
            return self.static_responses[clean_input], False

        # 3. Dynamic Analytics Direct Commands (O(1))
        if clean_input in {"sales", "sales summary", "analytics", "revenue", "metrics"}:
            return self.handle_sales_summary(), False
        if clean_input in {"status", "order status", "status breakdown", "fulfillment"}:
            return self.handle_status_breakdown(), False
        if clean_input in {"referrals", "marketing", "referral channels", "traffic"}:
            return self.handle_referral_breakdown(), False
        if clean_input in {"products", "product list", "catalog"}:
            prods = ", ".join([p.capitalize() for p in self.data_engine.products.keys()])
            return f"Available Products in Catalog: {prods}\nQuery any product details with 'product <name>'.", False

        # 4. Pattern / Entity Extraction Queries
        # Order Tracking patterns (e.g. 'track ORD200000', 'order ORD200000', 'ORD200000', 'TRK37947903')
        order_match = re.search(r"\b(ord\d+|trk\d+)\b", clean_input)
        if order_match:
            return self.handle_order_lookup(order_match.group(1)), False

        # Product queries (e.g. 'product laptop', 'price monitor', 'laptop')
        for prod_key in self.data_engine.products.keys():
            if re.search(rf"\b{re.escape(prod_key)}\b", clean_input):
                return self.handle_product_lookup(prod_key), False

        # 5. Atomic Fallback Execution
        return self.fallback_message, False

    def run(self) -> None:
        """
        The Heartbeat: Continuous Infinite Loop
        Keeps running until user issues a kill command.
        """
        print("=" * 65)
        print("🤖 DecodeLabs Rule-Based AI Chatbot (Project 1 - Batch 2026)")
        print("   Deterministic Logic Engine | O(1) Hash Map Architecture")
        print("=" * 65)
        print("Chatbot initialized and ready. Type 'help' for options, or 'exit' to quit.\n")

        while True:
            try:
                user_input = input("You: ")
                response, should_exit = self.process_query(user_input)
                print(f"Bot: {response}\n")
                if should_exit:
                    break
            except (KeyboardInterrupt, EOFError):
                print("\nBot: Session terminated. Goodbye!")
                break


if __name__ == "__main__":
    bot = RuleBasedAIChatbot()
    bot.run()
