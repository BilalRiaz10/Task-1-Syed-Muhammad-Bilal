# 🤖 DecodeLabs AI Track — Project 1: Rule-Based AI Chatbot & Logic Engine

[![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![Architecture](https://img.shields.io/badge/Architecture-IPO%20Model%20%7C%20O(1)%20Hash%20Map-brightgreen.svg)]()
[![Tests](https://img.shields.io/badge/Tests-8%2F8%20Passing-success.svg)]()

> *"Before you can manage the chaos of a probability engine, you must master the precision of a logic engine."*

## 📌 Overview

This project implements the foundational **Project 1 Milestone** for the **DecodeLabs Artificial Intelligence Industrial Training (Batch 2026)**.

While modern AI is dominated by probabilistic Large Language Models (LLMs), production systems require **deterministic guardrails** ("White Box" architecture) for absolute traceability, zero hallucination risk, and regulatory compliance. This system serves as the high-precision logic skeleton and control layer, powered by continuous data normalization and constant-time $O(1)$ dictionary lookups.

---

## 🏗️ Architectural Principles

- **IPO Model (Input $\to$ Process $\to$ Output)**:
  - **Input Sanitization**: Normalizes inputs by trimming whitespace and lowercasing (`.lower().strip()`).
  - **Process (Logic Skeleton)**: Eliminates the fragile $O(n)$ `if-elif` ladder anti-pattern in favor of direct $O(1)$ Hash Map dispatching.
  - **Output Generation**: Delivers atomic response retrieval with default fallback handling via `.get()`.
- **Heartbeat Infinite Loop**: Interactive CLI `while True:` cycle with graceful kill/exit command handling (`exit`, `quit`, `bye`, `close`).
- **Dataset Intelligence Layer**: In-memory indexing of 1,200 transaction records across 14 dimensions from `Dataset for Data Analytics.xlsx`.

---

## ⚡ Features & Capabilities

1. **Conversational Intents**: Instant responses for greetings, help, about, system capabilities, and promotional campaigns.
2. **Order Tracking**: Constant-time $O(1)$ lookup for orders by **Order ID** (e.g., `ORD200000`) or **Tracking Number** (e.g., `TRK37947903`).
3. **Product Intelligence**: Catalog metrics, pricing ranges, and units sold across 7 product categories.
4. **Executive Analytics**: Real-time aggregation of total revenue ($1.26M+), fulfillment statuses, and marketing referral channels.
5. **Zero Hallucination Guardrails**: Deterministic fallback responses for unmapped or out-of-domain queries.

---

## 📂 Project Structure

```
Decode_Project_1/
├── Artificial intelligence P1.pdf      # Industrial Training Kit specification
├── Dataset for Data Analytics.xlsx     # 1,200 record e-commerce dataset
├── data_engine.py                      # O(1) hash map indexing & analytics engine
├── chatbot.py                          # Main interactive chatbot & logic engine
├── test_chatbot.py                     # Comprehensive unit test suite
└── README.md                           # Project documentation
```

---

## 🚀 Quickstart & Setup

### 1. Prerequisites
- Python 3.8 or higher
- `pandas` and `openpyxl`

### 2. Installation
```bash
git clone https://github.com/YOUR_USERNAME/Decode_Project_1.git
cd Decode_Project_1
pip install pandas openpyxl
```

### 3. Running the Chatbot
```bash
python chatbot.py
```

### 4. Running Unit Tests
```bash
python test_chatbot.py
```

---

## 💡 Example Queries

| Intent / Category | Sample Input | Expected Output |
| :--- | :--- | :--- |
| **Greeting** | `hello`, `hi` | Welcome message & assistant intro |
| **Order Tracking** | `track ORD200000` | Full status, customer ID, item, and delivery details |
| **Tracking Number** | `where is TRK91186779` | Order status and shipping info |
| **Product Query** | `product laptop` | Unit price, total sales, and revenue generated |
| **Business Analytics**| `sales summary` | Total revenue, units sold, and average order value |
| **Marketing Channels**| `referrals` | Breakdown of orders across social & search channels |
| **Exit Command** | `exit`, `quit` | Clean loop termination |

---

## 🧪 Verification & Quality Standard

The implementation is verified via `unittest` covering:
- ✅ Input sanitization & case-insensitivity
- ✅ Static $O(1)$ knowledge base intent retrieval
- ✅ Dynamic Order ID & Tracking Number queries
- ✅ Aggregate sales and business metric computations
- ✅ Atomic fallback execution for unknown inputs
- ✅ Clean loop exit commands

---

## 👨‍💻 Author
- **DecodeLabs AI Trainee (Batch 2026)**
