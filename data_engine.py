"""
Data Engine Module for Project 1: Rule-Based AI Chatbot
Loads and indexes 'Dataset for Data Analytics.xlsx' into hash tables (dictionaries)
for O(1) constant-time query resolution.
"""

import os
import pandas as pd
from typing import Dict, Any, Optional

DATASET_PATH = os.path.join(os.path.dirname(__file__), "Dataset for Data Analytics.xlsx")


class DataEngine:
    def __init__(self, file_path: str = DATASET_PATH):
        self.file_path = file_path
        self.df: Optional[pd.DataFrame] = None
        
        # O(1) Index lookup tables
        self.orders_by_id: Dict[str, Dict[str, Any]] = {}
        self.orders_by_tracking: Dict[str, Dict[str, Any]] = {}
        self.products: Dict[str, Dict[str, Any]] = {}
        self.coupons: Dict[str, int] = {}
        self.metrics: Dict[str, Any] = {}
        self.status_counts: Dict[str, int] = {}
        self.referral_counts: Dict[str, int] = {}
        
        self.load_data()

    def load_data(self) -> None:
        """Loads Excel dataset and builds O(1) dictionary indices."""
        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f"Dataset file not found at: {self.file_path}")

        self.df = pd.read_excel(self.file_path)

        # 1. Build Order ID and Tracking Number indices (normalized lowercase keys)
        for _, row in self.df.iterrows():
            order_data = {
                "OrderID": str(row["OrderID"]),
                "Date": str(row["Date"])[:10] if pd.notnull(row["Date"]) else "N/A",
                "CustomerID": str(row["CustomerID"]),
                "Product": str(row["Product"]),
                "Quantity": int(row["Quantity"]),
                "UnitPrice": float(row["UnitPrice"]),
                "TotalPrice": float(row["TotalPrice"]),
                "OrderStatus": str(row["OrderStatus"]),
                "PaymentMethod": str(row["PaymentMethod"]),
                "ShippingAddress": str(row["ShippingAddress"]),
                "TrackingNumber": str(row["TrackingNumber"]),
                "CouponCode": str(row["CouponCode"]) if pd.notnull(row["CouponCode"]) else "None",
                "ReferralSource": str(row["ReferralSource"]),
            }
            # Index by lowercased OrderID and TrackingNumber for constant-time lookup
            self.orders_by_id[str(row["OrderID"]).strip().lower()] = order_data
            self.orders_by_tracking[str(row["TrackingNumber"]).strip().lower()] = order_data

        # 2. Build Product Performance and Pricing Index
        prod_grp = self.df.groupby("Product").agg(
            total_orders=("OrderID", "count"),
            total_units=("Quantity", "sum"),
            total_revenue=("TotalPrice", "sum"),
            avg_unit_price=("UnitPrice", "mean"),
            min_price=("UnitPrice", "min"),
            max_price=("UnitPrice", "max"),
        ).reset_index()

        for _, row in prod_grp.iterrows():
            prod_name = str(row["Product"]).strip().lower()
            self.products[prod_name] = {
                "name": str(row["Product"]),
                "total_orders": int(row["total_orders"]),
                "total_units": int(row["total_units"]),
                "total_revenue": round(float(row["total_revenue"]), 2),
                "avg_price": round(float(row["avg_unit_price"]), 2),
                "min_price": round(float(row["min_price"]), 2),
                "max_price": round(float(row["max_price"]), 2),
            }

        # 3. Build Coupons Index
        coupon_series = self.df["CouponCode"].dropna().value_counts()
        for coupon, count in coupon_series.items():
            self.coupons[str(coupon).strip().lower()] = int(count)

        # 4. Status and Referral distributions
        status_series = self.df["OrderStatus"].value_counts()
        for status, count in status_series.items():
            self.status_counts[str(status).strip().lower()] = int(count)

        ref_series = self.df["ReferralSource"].value_counts()
        for ref, count in ref_series.items():
            self.referral_counts[str(ref).strip().lower()] = int(count)

        # 5. Global Business Metrics
        self.metrics = {
            "total_orders": len(self.df),
            "total_revenue": round(float(self.df["TotalPrice"].sum()), 2),
            "avg_order_value": round(float(self.df["TotalPrice"].mean()), 2),
            "total_units_sold": int(self.df["Quantity"].sum()),
            "date_range": f"{str(self.df['Date'].min())[:10]} to {str(self.df['Date'].max())[:10]}",
            "unique_customers": int(self.df["CustomerID"].nunique()),
        }

    def get_order(self, order_id_or_tracking: str) -> Optional[Dict[str, Any]]:
        """O(1) lookup for an order by OrderID or TrackingNumber."""
        key = order_id_or_tracking.strip().lower()
        if key in self.orders_by_id:
            return self.orders_by_id[key]
        if key in self.orders_by_tracking:
            return self.orders_by_tracking[key]
        return None

    def get_product(self, product_name: str) -> Optional[Dict[str, Any]]:
        """O(1) lookup for product analytics and details."""
        return self.products.get(product_name.strip().lower())

    def get_coupon_info(self, coupon_code: str) -> Optional[int]:
        """O(1) lookup for coupon usage count."""
        return self.coupons.get(coupon_code.strip().lower())

    def get_metrics(self) -> Dict[str, Any]:
        """Returns the pre-calculated global dataset metrics."""
        return self.metrics
