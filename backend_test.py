#!/usr/bin/env python3
"""
FinanceTracker Backend API Test Suite
Tests all backend functionality including auth, transactions, budgets, goals, stats, and AI advice
"""

import requests
import json
from datetime import datetime, timedelta
import sys
import os

# Get backend URL from environment
BACKEND_URL = "https://expo-finance-1.preview.emergentagent.com/api"

class FinanceTrackerTester:
    def __init__(self):
        self.base_url = BACKEND_URL
        self.token = None
        self.user_id = None
        self.test_results = {
            "auth": {"passed": 0, "failed": 0, "errors": []},
            "transactions": {"passed": 0, "failed": 0, "errors": []},
            "budgets": {"passed": 0, "failed": 0, "errors": []},
            "goals": {"passed": 0, "failed": 0, "errors": []},
            "stats": {"passed": 0, "failed": 0, "errors": []},
            "advice": {"passed": 0, "failed": 0, "errors": []}
        }
        self.created_items = {
            "transactions": [],
            "budgets": [],
            "goals": []
        }

    def log_result(self, category, test_name, success, message="", response=None):
        """Log test result"""
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {category.upper()}: {test_name}")
        if message:
            print(f"   {message}")
        if response and not success:
            print(f"   Response: {response.status_code} - {response.text[:200]}")
        
        if success:
            self.test_results[category]["passed"] += 1
        else:
            self.test_results[category]["failed"] += 1
            self.test_results[category]["errors"].append(f"{test_name}: {message}")
        print()

    def get_headers(self, include_auth=True):
        """Get request headers"""
        headers = {"Content-Type": "application/json"}
        if include_auth and self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        return headers

    def test_auth(self):
        """Test authentication endpoints"""
        print("🔐 TESTING AUTHENTICATION")
        print("=" * 50)
        
        # Test user registration
        register_data = {
            "email": "marco.rossi@email.com",
            "password": "SecurePass123!",
            "name": "Marco Rossi"
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/auth/register",
                json=register_data,
                headers=self.get_headers(include_auth=False)
            )
            
            if response.status_code == 201 or response.status_code == 200:
                data = response.json()
                if "token" in data and "id" in data:
                    self.token = data["token"]
                    self.user_id = data["id"]
                    self.log_result("auth", "User Registration", True, 
                                  f"User registered successfully with ID: {self.user_id}")
                else:
                    self.log_result("auth", "User Registration", False, 
                                  "Missing token or ID in response", response)
            else:
                # User might already exist, try login instead
                if response.status_code == 400 and "already registered" in response.text:
                    self.log_result("auth", "User Registration", True, 
                                  "User already exists (expected for repeated tests)")
                else:
                    self.log_result("auth", "User Registration", False, 
                                  f"Unexpected status code: {response.status_code}", response)
        except Exception as e:
            self.log_result("auth", "User Registration", False, f"Exception: {str(e)}")

        # Test user login
        login_data = {
            "email": "marco.rossi@email.com",
            "password": "SecurePass123!"
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/auth/login",
                json=login_data,
                headers=self.get_headers(include_auth=False)
            )
            
            if response.status_code == 200:
                data = response.json()
                if "token" in data and "id" in data:
                    self.token = data["token"]
                    self.user_id = data["id"]
                    self.log_result("auth", "User Login", True, 
                                  f"Login successful, token received")
                else:
                    self.log_result("auth", "User Login", False, 
                                  "Missing token or ID in response", response)
            else:
                self.log_result("auth", "User Login", False, 
                              f"Login failed with status: {response.status_code}", response)
        except Exception as e:
            self.log_result("auth", "User Login", False, f"Exception: {str(e)}")

        # Test invalid login
        try:
            invalid_login = {
                "email": "marco.rossi@email.com",
                "password": "WrongPassword"
            }
            response = requests.post(
                f"{self.base_url}/auth/login",
                json=invalid_login,
                headers=self.get_headers(include_auth=False)
            )
            
            if response.status_code == 401:
                self.log_result("auth", "Invalid Login Rejection", True, 
                              "Invalid credentials properly rejected")
            else:
                self.log_result("auth", "Invalid Login Rejection", False, 
                              f"Expected 401, got {response.status_code}", response)
        except Exception as e:
            self.log_result("auth", "Invalid Login Rejection", False, f"Exception: {str(e)}")

    def test_transactions(self):
        """Test transaction endpoints"""
        print("💰 TESTING TRANSACTIONS")
        print("=" * 50)
        
        if not self.token:
            self.log_result("transactions", "All Transaction Tests", False, 
                          "No authentication token available")
            return

        # Test creating transactions
        test_transactions = [
            {
                "type": "income",
                "amount": 3500.00,
                "category": "Stipendio",
                "description": "Stipendio mensile gennaio",
                "date": datetime.now().isoformat()
            },
            {
                "type": "expense",
                "amount": 1200.00,
                "category": "Affitto",
                "description": "Affitto appartamento gennaio",
                "date": datetime.now().isoformat()
            },
            {
                "type": "expense",
                "amount": 350.00,
                "category": "Alimentari",
                "description": "Spesa settimanale supermercato",
                "date": (datetime.now() - timedelta(days=2)).isoformat()
            },
            {
                "type": "expense",
                "amount": 80.00,
                "category": "Trasporti",
                "description": "Abbonamento mezzi pubblici",
                "date": (datetime.now() - timedelta(days=1)).isoformat()
            }
        ]

        for i, transaction_data in enumerate(test_transactions):
            try:
                response = requests.post(
                    f"{self.base_url}/transactions",
                    json=transaction_data,
                    headers=self.get_headers()
                )
                
                if response.status_code in [200, 201]:
                    data = response.json()
                    if "id" in data:
                        self.created_items["transactions"].append(data["id"])
                        self.log_result("transactions", f"Create Transaction {i+1}", True, 
                                      f"Transaction created: {transaction_data['description']}")
                    else:
                        self.log_result("transactions", f"Create Transaction {i+1}", False, 
                                      "No ID in response", response)
                else:
                    self.log_result("transactions", f"Create Transaction {i+1}", False, 
                                  f"Status: {response.status_code}", response)
            except Exception as e:
                self.log_result("transactions", f"Create Transaction {i+1}", False, f"Exception: {str(e)}")

        # Test getting transactions
        try:
            response = requests.get(
                f"{self.base_url}/transactions",
                headers=self.get_headers()
            )
            
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list) and len(data) > 0:
                    self.log_result("transactions", "Get Transactions", True, 
                                  f"Retrieved {len(data)} transactions")
                else:
                    self.log_result("transactions", "Get Transactions", False, 
                                  "No transactions returned or invalid format", response)
            else:
                self.log_result("transactions", "Get Transactions", False, 
                              f"Status: {response.status_code}", response)
        except Exception as e:
            self.log_result("transactions", "Get Transactions", False, f"Exception: {str(e)}")

        # Test deleting a transaction
        if self.created_items["transactions"]:
            transaction_id = self.created_items["transactions"][0]
            try:
                response = requests.delete(
                    f"{self.base_url}/transactions/{transaction_id}",
                    headers=self.get_headers()
                )
                
                if response.status_code == 200:
                    self.log_result("transactions", "Delete Transaction", True, 
                                  f"Transaction {transaction_id} deleted")
                    self.created_items["transactions"].remove(transaction_id)
                else:
                    self.log_result("transactions", "Delete Transaction", False, 
                                  f"Status: {response.status_code}", response)
            except Exception as e:
                self.log_result("transactions", "Delete Transaction", False, f"Exception: {str(e)}")

        # Test unauthorized access
        try:
            response = requests.get(
                f"{self.base_url}/transactions",
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 401 or response.status_code == 403:
                self.log_result("transactions", "Unauthorized Access Block", True, 
                              "Unauthorized access properly blocked")
            else:
                self.log_result("transactions", "Unauthorized Access Block", False, 
                              f"Expected 401/403, got {response.status_code}", response)
        except Exception as e:
            self.log_result("transactions", "Unauthorized Access Block", False, f"Exception: {str(e)}")

    def test_budgets(self):
        """Test budget endpoints"""
        print("📊 TESTING BUDGETS")
        print("=" * 50)
        
        if not self.token:
            self.log_result("budgets", "All Budget Tests", False, 
                          "No authentication token available")
            return

        # Test creating budgets
        test_budgets = [
            {
                "category": "Alimentari",
                "limit": 500.00,
                "period": "monthly"
            },
            {
                "category": "Trasporti",
                "limit": 150.00,
                "period": "monthly"
            },
            {
                "category": "Intrattenimento",
                "limit": 200.00,
                "period": "monthly"
            }
        ]

        for i, budget_data in enumerate(test_budgets):
            try:
                response = requests.post(
                    f"{self.base_url}/budgets",
                    json=budget_data,
                    headers=self.get_headers()
                )
                
                if response.status_code in [200, 201]:
                    data = response.json()
                    if "id" in data:
                        self.created_items["budgets"].append(data["id"])
                        self.log_result("budgets", f"Create Budget {i+1}", True, 
                                      f"Budget created for {budget_data['category']}: €{budget_data['limit']}")
                    else:
                        self.log_result("budgets", f"Create Budget {i+1}", False, 
                                      "No ID in response", response)
                else:
                    self.log_result("budgets", f"Create Budget {i+1}", False, 
                                  f"Status: {response.status_code}", response)
            except Exception as e:
                self.log_result("budgets", f"Create Budget {i+1}", False, f"Exception: {str(e)}")

        # Test getting budgets
        try:
            response = requests.get(
                f"{self.base_url}/budgets",
                headers=self.get_headers()
            )
            
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list):
                    self.log_result("budgets", "Get Budgets", True, 
                                  f"Retrieved {len(data)} budgets")
                else:
                    self.log_result("budgets", "Get Budgets", False, 
                                  "Invalid response format", response)
            else:
                self.log_result("budgets", "Get Budgets", False, 
                              f"Status: {response.status_code}", response)
        except Exception as e:
            self.log_result("budgets", "Get Budgets", False, f"Exception: {str(e)}")

        # Test updating a budget
        if self.created_items["budgets"]:
            budget_id = self.created_items["budgets"][0]
            update_data = {
                "category": "Alimentari",
                "limit": 600.00,
                "period": "monthly"
            }
            
            try:
                response = requests.put(
                    f"{self.base_url}/budgets/{budget_id}",
                    json=update_data,
                    headers=self.get_headers()
                )
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get("limit") == 600.00:
                        self.log_result("budgets", "Update Budget", True, 
                                      f"Budget updated to €{update_data['limit']}")
                    else:
                        self.log_result("budgets", "Update Budget", False, 
                                      "Budget not properly updated", response)
                else:
                    self.log_result("budgets", "Update Budget", False, 
                                  f"Status: {response.status_code}", response)
            except Exception as e:
                self.log_result("budgets", "Update Budget", False, f"Exception: {str(e)}")

        # Test deleting a budget
        if self.created_items["budgets"]:
            budget_id = self.created_items["budgets"][-1]
            try:
                response = requests.delete(
                    f"{self.base_url}/budgets/{budget_id}",
                    headers=self.get_headers()
                )
                
                if response.status_code == 200:
                    self.log_result("budgets", "Delete Budget", True, 
                                  f"Budget {budget_id} deleted")
                    self.created_items["budgets"].remove(budget_id)
                else:
                    self.log_result("budgets", "Delete Budget", False, 
                                  f"Status: {response.status_code}", response)
            except Exception as e:
                self.log_result("budgets", "Delete Budget", False, f"Exception: {str(e)}")

    def test_goals(self):
        """Test goal endpoints"""
        print("🎯 TESTING GOALS")
        print("=" * 50)
        
        if not self.token:
            self.log_result("goals", "All Goal Tests", False, 
                          "No authentication token available")
            return

        # Test creating goals
        test_goals = [
            {
                "name": "Fondo Emergenza",
                "target_amount": 5000.00,
                "deadline": (datetime.now() + timedelta(days=365)).isoformat()
            },
            {
                "name": "Vacanze Estive",
                "target_amount": 2000.00,
                "deadline": (datetime.now() + timedelta(days=180)).isoformat()
            }
        ]

        for i, goal_data in enumerate(test_goals):
            try:
                response = requests.post(
                    f"{self.base_url}/goals",
                    json=goal_data,
                    headers=self.get_headers()
                )
                
                if response.status_code in [200, 201]:
                    data = response.json()
                    if "id" in data:
                        self.created_items["goals"].append(data["id"])
                        self.log_result("goals", f"Create Goal {i+1}", True, 
                                      f"Goal created: {goal_data['name']} - €{goal_data['target_amount']}")
                    else:
                        self.log_result("goals", f"Create Goal {i+1}", False, 
                                      "No ID in response", response)
                else:
                    self.log_result("goals", f"Create Goal {i+1}", False, 
                                  f"Status: {response.status_code}", response)
            except Exception as e:
                self.log_result("goals", f"Create Goal {i+1}", False, f"Exception: {str(e)}")

        # Test getting goals
        try:
            response = requests.get(
                f"{self.base_url}/goals",
                headers=self.get_headers()
            )
            
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list):
                    self.log_result("goals", "Get Goals", True, 
                                  f"Retrieved {len(data)} goals")
                else:
                    self.log_result("goals", "Get Goals", False, 
                                  "Invalid response format", response)
            else:
                self.log_result("goals", "Get Goals", False, 
                              f"Status: {response.status_code}", response)
        except Exception as e:
            self.log_result("goals", "Get Goals", False, f"Exception: {str(e)}")

        # Test contributing to a goal
        if self.created_items["goals"]:
            goal_id = self.created_items["goals"][0]
            try:
                response = requests.put(
                    f"{self.base_url}/goals/{goal_id}/contribute?amount=100",
                    headers=self.get_headers()
                )
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get("current_amount", 0) >= 100:
                        self.log_result("goals", "Contribute to Goal", True, 
                                      f"€100 contributed to goal")
                    else:
                        self.log_result("goals", "Contribute to Goal", False, 
                                      "Contribution not reflected in current_amount", response)
                else:
                    self.log_result("goals", "Contribute to Goal", False, 
                                  f"Status: {response.status_code}", response)
            except Exception as e:
                self.log_result("goals", "Contribute to Goal", False, f"Exception: {str(e)}")

        # Test deleting a goal
        if self.created_items["goals"]:
            goal_id = self.created_items["goals"][-1]
            try:
                response = requests.delete(
                    f"{self.base_url}/goals/{goal_id}",
                    headers=self.get_headers()
                )
                
                if response.status_code == 200:
                    self.log_result("goals", "Delete Goal", True, 
                                  f"Goal {goal_id} deleted")
                    self.created_items["goals"].remove(goal_id)
                else:
                    self.log_result("goals", "Delete Goal", False, 
                                  f"Status: {response.status_code}", response)
            except Exception as e:
                self.log_result("goals", "Delete Goal", False, f"Exception: {str(e)}")

    def test_stats(self):
        """Test statistics endpoint"""
        print("📈 TESTING STATISTICS")
        print("=" * 50)
        
        if not self.token:
            self.log_result("stats", "Statistics Test", False, 
                          "No authentication token available")
            return

        try:
            response = requests.get(
                f"{self.base_url}/stats",
                headers=self.get_headers()
            )
            
            if response.status_code == 200:
                data = response.json()
                required_fields = ["total_income", "total_expenses", "balance", 
                                 "category_expenses", "recent_income", "recent_expenses", 
                                 "transaction_count"]
                
                missing_fields = [field for field in required_fields if field not in data]
                
                if not missing_fields:
                    self.log_result("stats", "Get Statistics", True, 
                                  f"Statistics retrieved with all required fields")
                    print(f"   Balance: €{data.get('balance', 0):.2f}")
                    print(f"   Total Income: €{data.get('total_income', 0):.2f}")
                    print(f"   Total Expenses: €{data.get('total_expenses', 0):.2f}")
                    print(f"   Transaction Count: {data.get('transaction_count', 0)}")
                else:
                    self.log_result("stats", "Get Statistics", False, 
                                  f"Missing fields: {missing_fields}", response)
            else:
                self.log_result("stats", "Get Statistics", False, 
                              f"Status: {response.status_code}", response)
        except Exception as e:
            self.log_result("stats", "Get Statistics", False, f"Exception: {str(e)}")

    def test_advice(self):
        """Test AI advice endpoint"""
        print("🤖 TESTING AI ADVICE")
        print("=" * 50)
        
        if not self.token:
            self.log_result("advice", "AI Advice Test", False, 
                          "No authentication token available")
            return

        advice_request = {
            "context": "Come posso risparmiare di più ogni mese? Ho difficoltà a mettere da parte soldi."
        }

        try:
            response = requests.post(
                f"{self.base_url}/advice",
                json=advice_request,
                headers=self.get_headers()
            )
            
            if response.status_code == 200:
                data = response.json()
                if "advice" in data and data["advice"]:
                    advice_text = data["advice"]
                    if len(advice_text) > 50:  # Reasonable advice length
                        self.log_result("advice", "Get AI Advice", True, 
                                      f"AI advice received ({len(advice_text)} characters)")
                        print(f"   Advice preview: {advice_text[:100]}...")
                    else:
                        self.log_result("advice", "Get AI Advice", False, 
                                      "Advice too short or generic", response)
                else:
                    self.log_result("advice", "Get AI Advice", False, 
                                  "No advice field in response", response)
            else:
                self.log_result("advice", "Get AI Advice", False, 
                              f"Status: {response.status_code}", response)
        except Exception as e:
            self.log_result("advice", "Get AI Advice", False, f"Exception: {str(e)}")

    def test_error_scenarios(self):
        """Test error handling scenarios"""
        print("⚠️  TESTING ERROR SCENARIOS")
        print("=" * 50)
        
        # Test accessing non-existent transaction
        try:
            response = requests.get(
                f"{self.base_url}/transactions/nonexistent123",
                headers=self.get_headers()
            )
            # This endpoint doesn't exist, should get 404 or 405
            if response.status_code in [404, 405]:
                self.log_result("transactions", "Non-existent Endpoint", True, 
                              "Non-existent endpoint properly handled")
            else:
                self.log_result("transactions", "Non-existent Endpoint", False, 
                              f"Unexpected status: {response.status_code}", response)
        except Exception as e:
            self.log_result("transactions", "Non-existent Endpoint", False, f"Exception: {str(e)}")

        # Test deleting non-existent transaction
        try:
            response = requests.delete(
                f"{self.base_url}/transactions/507f1f77bcf86cd799439011",  # Valid ObjectId format
                headers=self.get_headers()
            )
            
            if response.status_code == 404:
                self.log_result("transactions", "Delete Non-existent Transaction", True, 
                              "Non-existent transaction deletion properly handled")
            else:
                self.log_result("transactions", "Delete Non-existent Transaction", False, 
                              f"Expected 404, got {response.status_code}", response)
        except Exception as e:
            self.log_result("transactions", "Delete Non-existent Transaction", False, f"Exception: {str(e)}")

    def print_summary(self):
        """Print test summary"""
        print("\n" + "=" * 60)
        print("🏁 TEST SUMMARY")
        print("=" * 60)
        
        total_passed = 0
        total_failed = 0
        
        for category, results in self.test_results.items():
            passed = results["passed"]
            failed = results["failed"]
            total_passed += passed
            total_failed += failed
            
            status = "✅" if failed == 0 else "❌"
            print(f"{status} {category.upper()}: {passed} passed, {failed} failed")
            
            if results["errors"]:
                for error in results["errors"]:
                    print(f"   - {error}")
        
        print(f"\n🎯 OVERALL: {total_passed} passed, {total_failed} failed")
        
        if total_failed == 0:
            print("🎉 ALL TESTS PASSED!")
        else:
            print(f"⚠️  {total_failed} TESTS FAILED - See details above")
        
        return total_failed == 0

def main():
    """Main test execution"""
    print("🚀 Starting FinanceTracker Backend API Tests")
    print(f"🌐 Backend URL: {BACKEND_URL}")
    print("=" * 60)
    
    tester = FinanceTrackerTester()
    
    # Run all tests
    tester.test_auth()
    tester.test_transactions()
    tester.test_budgets()
    tester.test_goals()
    tester.test_stats()
    tester.test_advice()
    tester.test_error_scenarios()
    
    # Print summary
    success = tester.print_summary()
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()