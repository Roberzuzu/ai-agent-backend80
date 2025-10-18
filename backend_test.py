#!/usr/bin/env python3
"""
Comprehensive Backend Testing for Payment and Monetization System
Tests all payment endpoints, subscription plans, analytics, and checkout functionality
"""

import requests
import json
import time
from datetime import datetime
from typing import Dict, Any, List

# Configuration
BASE_URL = "https://agente90-cont.preview.emergentagent.com/api"
TEST_EMAIL = "usuario.test@example.com"
ORIGIN_URL = "https://agente90-cont.preview.emergentagent.com"

class PaymentSystemTester:
    def __init__(self):
        self.session = requests.Session()
        self.test_results = []
        self.products = []
        
    def log_test(self, test_name: str, success: bool, details: str = "", response_data: Any = None):
        """Log test results"""
        result = {
            "test": test_name,
            "success": success,
            "details": details,
            "timestamp": datetime.now().isoformat(),
            "response_data": response_data
        }
        self.test_results.append(result)
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} - {test_name}")
        if details:
            print(f"    Details: {details}")
        if not success and response_data:
            print(f"    Response: {response_data}")
        print()

    def test_subscription_plans(self):
        """Test GET /api/subscriptions/plans"""
        print("🔍 Testing Subscription Plans...")
        try:
            response = self.session.get(f"{BASE_URL}/subscriptions/plans")
            
            if response.status_code == 200:
                plans = response.json()
                
                # Verify we have 3 plans
                if len(plans) != 3:
                    self.log_test("Subscription Plans Count", False, f"Expected 3 plans, got {len(plans)}", plans)
                    return False
                
                # Verify plan structure and prices
                expected_plans = {
                    "basic": {"price": 9.99, "name": "Plan Básico"},
                    "pro": {"price": 29.99, "name": "Plan Pro"},
                    "enterprise": {"price": 99.99, "name": "Plan Empresa"}
                }
                
                plans_by_id = {plan["id"]: plan for plan in plans}
                
                for plan_id, expected in expected_plans.items():
                    if plan_id not in plans_by_id:
                        self.log_test("Subscription Plans Structure", False, f"Missing plan: {plan_id}", plans)
                        return False
                    
                    plan = plans_by_id[plan_id]
                    if plan["price"] != expected["price"]:
                        self.log_test("Subscription Plans Prices", False, 
                                    f"Plan {plan_id}: expected ${expected['price']}, got ${plan['price']}", plan)
                        return False
                    
                    if plan["name"] != expected["name"]:
                        self.log_test("Subscription Plans Names", False,
                                    f"Plan {plan_id}: expected '{expected['name']}', got '{plan['name']}'", plan)
                        return False
                
                self.log_test("Subscription Plans", True, "All 3 plans verified with correct prices and names", plans)
                return True
            else:
                self.log_test("Subscription Plans", False, f"HTTP {response.status_code}", response.text)
                return False
                
        except Exception as e:
            self.log_test("Subscription Plans", False, f"Exception: {str(e)}")
            return False

    def get_products(self):
        """Get products for testing checkout"""
        print("🔍 Getting Products for Checkout Testing...")
        try:
            response = self.session.get(f"{BASE_URL}/products")
            
            if response.status_code == 200:
                products = response.json()
                if products:
                    self.products = products
                    self.log_test("Get Products", True, f"Retrieved {len(products)} products", len(products))
                    return True
                else:
                    self.log_test("Get Products", False, "No products found for testing")
                    return False
            else:
                self.log_test("Get Products", False, f"HTTP {response.status_code}", response.text)
                return False
                
        except Exception as e:
            self.log_test("Get Products", False, f"Exception: {str(e)}")
            return False

    def test_product_checkout(self):
        """Test POST /api/payments/checkout/session for product"""
        print("🔍 Testing Product Checkout...")
        
        if not self.products:
            self.log_test("Product Checkout", False, "No products available for testing")
            return False
            
        try:
            product = self.products[0]  # Use first product
            
            checkout_data = {
                "payment_type": "product",
                "product_id": product["id"],
                "user_email": TEST_EMAIL,
                "origin_url": ORIGIN_URL
            }
            
            response = self.session.post(
                f"{BASE_URL}/payments/checkout/session",
                json=checkout_data,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                result = response.json()
                
                # Verify response structure
                if "url" not in result or "session_id" not in result:
                    self.log_test("Product Checkout Response", False, "Missing url or session_id in response", result)
                    return False
                
                # Verify URL contains Stripe
                if "stripe" not in result["url"].lower():
                    self.log_test("Product Checkout URL", False, "URL doesn't appear to be a Stripe URL", result["url"])
                    return False
                
                self.log_test("Product Checkout", True, 
                            f"Checkout session created for product '{product['name']}' (${product['price']})", 
                            {"session_id": result["session_id"], "has_stripe_url": True})
                return True
            else:
                self.log_test("Product Checkout", False, f"HTTP {response.status_code}", response.text)
                return False
                
        except Exception as e:
            self.log_test("Product Checkout", False, f"Exception: {str(e)}")
            return False

    def test_subscription_checkout(self):
        """Test POST /api/payments/checkout/session for subscription"""
        print("🔍 Testing Subscription Checkout...")
        try:
            checkout_data = {
                "payment_type": "subscription",
                "plan_id": "basic",
                "user_email": TEST_EMAIL,
                "origin_url": ORIGIN_URL
            }
            
            response = self.session.post(
                f"{BASE_URL}/payments/checkout/session",
                json=checkout_data,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                result = response.json()
                
                # Verify response structure
                if "url" not in result or "session_id" not in result:
                    self.log_test("Subscription Checkout Response", False, "Missing url or session_id in response", result)
                    return False
                
                # Verify URL contains Stripe
                if "stripe" not in result["url"].lower():
                    self.log_test("Subscription Checkout URL", False, "URL doesn't appear to be a Stripe URL", result["url"])
                    return False
                
                self.log_test("Subscription Checkout", True, 
                            "Checkout session created for basic plan ($9.99/month)", 
                            {"session_id": result["session_id"], "has_stripe_url": True})
                return True
            else:
                self.log_test("Subscription Checkout", False, f"HTTP {response.status_code}", response.text)
                return False
                
        except Exception as e:
            self.log_test("Subscription Checkout", False, f"Exception: {str(e)}")
            return False

    def test_revenue_analytics(self):
        """Test GET /api/analytics/revenue"""
        print("🔍 Testing Revenue Analytics...")
        try:
            response = self.session.get(f"{BASE_URL}/analytics/revenue")
            
            if response.status_code == 200:
                analytics = response.json()
                
                # Verify required fields
                required_fields = [
                    "total_revenue", "product_revenue", "subscription_revenue", 
                    "total_transactions", "product_sales", "subscription_sales",
                    "active_subscriptions", "mrr", "discount_code_tracking", "currency"
                ]
                
                missing_fields = [field for field in required_fields if field not in analytics]
                if missing_fields:
                    self.log_test("Revenue Analytics Structure", False, 
                                f"Missing fields: {missing_fields}", analytics)
                    return False
                
                # Verify data types
                numeric_fields = ["total_revenue", "product_revenue", "subscription_revenue", "mrr"]
                for field in numeric_fields:
                    if not isinstance(analytics[field], (int, float)):
                        self.log_test("Revenue Analytics Data Types", False,
                                    f"Field {field} should be numeric, got {type(analytics[field])}", analytics[field])
                        return False
                
                self.log_test("Revenue Analytics", True, 
                            f"Total Revenue: ${analytics['total_revenue']}, MRR: ${analytics['mrr']}", 
                            {k: v for k, v in analytics.items() if k != "discount_code_tracking"})
                return True
            else:
                self.log_test("Revenue Analytics", False, f"HTTP {response.status_code}", response.text)
                return False
                
        except Exception as e:
            self.log_test("Revenue Analytics", False, f"Exception: {str(e)}")
            return False

    def test_campaign_roi(self):
        """Test GET /api/analytics/campaign-roi"""
        print("🔍 Testing Campaign ROI Analytics...")
        try:
            response = self.session.get(f"{BASE_URL}/analytics/campaign-roi")
            
            if response.status_code == 200:
                roi_data = response.json()
                
                # Verify required fields
                required_fields = ["campaigns", "total_ad_spend", "total_revenue", "average_roi"]
                missing_fields = [field for field in required_fields if field not in roi_data]
                if missing_fields:
                    self.log_test("Campaign ROI Structure", False, 
                                f"Missing fields: {missing_fields}", roi_data)
                    return False
                
                # Verify campaigns is array
                if not isinstance(roi_data["campaigns"], list):
                    self.log_test("Campaign ROI Data Type", False, 
                                "campaigns should be an array", type(roi_data["campaigns"]))
                    return False
                
                # If there are campaigns, verify structure
                if roi_data["campaigns"]:
                    campaign = roi_data["campaigns"][0]
                    campaign_fields = ["campaign_id", "campaign_name", "platform", "budget", "revenue", "roi", "status"]
                    missing_campaign_fields = [field for field in campaign_fields if field not in campaign]
                    if missing_campaign_fields:
                        self.log_test("Campaign ROI Campaign Structure", False,
                                    f"Missing campaign fields: {missing_campaign_fields}", campaign)
                        return False
                
                self.log_test("Campaign ROI", True, 
                            f"Found {len(roi_data['campaigns'])} campaigns, Average ROI: {roi_data['average_roi']}%", 
                            {k: v for k, v in roi_data.items() if k != "campaigns"})
                return True
            else:
                self.log_test("Campaign ROI", False, f"HTTP {response.status_code}", response.text)
                return False
                
        except Exception as e:
            self.log_test("Campaign ROI", False, f"Exception: {str(e)}")
            return False

    def test_affiliate_commissions(self):
        """Test GET /api/analytics/affiliate-commissions"""
        print("🔍 Testing Affiliate Commissions...")
        try:
            response = self.session.get(f"{BASE_URL}/analytics/affiliate-commissions")
            
            if response.status_code == 200:
                commissions = response.json()
                
                # Verify required fields
                required_fields = ["total_commissions", "commission_rate", "affiliate_products", "commissions", "currency"]
                missing_fields = [field for field in required_fields if field not in commissions]
                if missing_fields:
                    self.log_test("Affiliate Commissions Structure", False, 
                                f"Missing fields: {missing_fields}", commissions)
                    return False
                
                # Verify commissions is array
                if not isinstance(commissions["commissions"], list):
                    self.log_test("Affiliate Commissions Data Type", False, 
                                "commissions should be an array", type(commissions["commissions"]))
                    return False
                
                # If there are commissions, verify structure
                if commissions["commissions"]:
                    commission = commissions["commissions"][0]
                    commission_fields = ["product_id", "product_name", "affiliate_link", "sales_count", "revenue", "commission_earned"]
                    missing_commission_fields = [field for field in commission_fields if field not in commission]
                    if missing_commission_fields:
                        self.log_test("Affiliate Commission Item Structure", False,
                                    f"Missing commission fields: {missing_commission_fields}", commission)
                        return False
                
                self.log_test("Affiliate Commissions", True, 
                            f"Total Commissions: ${commissions['total_commissions']}, Rate: {commissions['commission_rate']}%", 
                            {k: v for k, v in commissions.items() if k != "commissions"})
                return True
            else:
                self.log_test("Affiliate Commissions", False, f"HTTP {response.status_code}", response.text)
                return False
                
        except Exception as e:
            self.log_test("Affiliate Commissions", False, f"Exception: {str(e)}")
            return False

    def test_advanced_dashboard(self):
        """Test GET /api/analytics/dashboard-advanced"""
        print("🔍 Testing Advanced Dashboard...")
        try:
            response = self.session.get(f"{BASE_URL}/analytics/dashboard-advanced")
            
            if response.status_code == 200:
                dashboard = response.json()
                
                # Verify required sections
                required_sections = ["overview", "revenue", "campaign_roi", "affiliate_commissions", "generated_at"]
                missing_sections = [section for section in required_sections if section not in dashboard]
                if missing_sections:
                    self.log_test("Advanced Dashboard Structure", False, 
                                f"Missing sections: {missing_sections}", list(dashboard.keys()))
                    return False
                
                # Verify overview section
                overview_fields = ["products", "trends", "content", "social_posts", "campaigns"]
                missing_overview = [field for field in overview_fields if field not in dashboard["overview"]]
                if missing_overview:
                    self.log_test("Advanced Dashboard Overview", False,
                                f"Missing overview fields: {missing_overview}", dashboard["overview"])
                    return False
                
                self.log_test("Advanced Dashboard", True, 
                            f"Complete dashboard with all sections: {list(dashboard.keys())}", 
                            dashboard["overview"])
                return True
            else:
                self.log_test("Advanced Dashboard", False, f"HTTP {response.status_code}", response.text)
                return False
                
        except Exception as e:
            self.log_test("Advanced Dashboard", False, f"Exception: {str(e)}")
            return False

    def test_payment_history(self):
        """Test GET /api/payments/history"""
        print("🔍 Testing Payment History...")
        try:
            response = self.session.get(f"{BASE_URL}/payments/history")
            
            if response.status_code == 200:
                history = response.json()
                
                # Verify it's an array
                if not isinstance(history, list):
                    self.log_test("Payment History Data Type", False, 
                                "Payment history should be an array", type(history))
                    return False
                
                # If there are transactions, verify structure
                if history:
                    transaction = history[0]
                    required_fields = ["id", "session_id", "amount", "currency", "payment_type", "payment_status", "status", "created_at"]
                    missing_fields = [field for field in required_fields if field not in transaction]
                    if missing_fields:
                        self.log_test("Payment History Transaction Structure", False,
                                    f"Missing transaction fields: {missing_fields}", transaction)
                        return False
                
                self.log_test("Payment History", True, 
                            f"Retrieved {len(history)} payment transactions", 
                            {"transaction_count": len(history)})
                return True
            else:
                self.log_test("Payment History", False, f"HTTP {response.status_code}", response.text)
                return False
                
        except Exception as e:
            self.log_test("Payment History", False, f"Exception: {str(e)}")
            return False

    def test_database_info(self):
        """Test GET /api/database/info"""
        print("🔍 Testing Database Info...")
        try:
            response = self.session.get(f"{BASE_URL}/database/info")
            
            if response.status_code == 200:
                db_info = response.json()
                
                # Verify required fields
                required_fields = ["database_name", "collections_count", "collections", "migrations_applied", "last_migration"]
                missing_fields = [field for field in required_fields if field not in db_info]
                if missing_fields:
                    self.log_test("Database Info Structure", False, 
                                f"Missing fields: {missing_fields}", db_info)
                    return False
                
                # Verify collections is array
                if not isinstance(db_info["collections"], list):
                    self.log_test("Database Info Collections Type", False, 
                                "collections should be an array", type(db_info["collections"]))
                    return False
                
                # Check main collections have indexes (> 1 means more than just _id index)
                main_collections = ["users", "products", "payment_transactions", "subscriptions", "affiliates", "notifications"]
                collections_dict = {col["name"]: col for col in db_info["collections"]}
                
                for col_name in main_collections:
                    if col_name in collections_dict:
                        indexes = collections_dict[col_name].get("indexes", 0)
                        if indexes <= 1:
                            self.log_test("Database Indexes Check", False, 
                                        f"Collection {col_name} has only {indexes} indexes (should have > 1)", 
                                        collections_dict[col_name])
                            return False
                
                self.log_test("Database Info", True, 
                            f"Database: {db_info['database_name']}, Collections: {db_info['collections_count']}, Migrations: {db_info['migrations_applied']}", 
                            {"collections_with_indexes": len([c for c in db_info["collections"] if c.get("indexes", 0) > 1])})
                return True
            else:
                self.log_test("Database Info", False, f"HTTP {response.status_code}", response.text)
                return False
                
        except Exception as e:
            self.log_test("Database Info", False, f"Exception: {str(e)}")
            return False

    def test_database_backups_list(self):
        """Test GET /api/database/backups"""
        print("🔍 Testing Database Backups List...")
        try:
            response = self.session.get(f"{BASE_URL}/database/backups")
            
            if response.status_code == 200:
                backups_data = response.json()
                
                # Verify required fields
                required_fields = ["count", "backups"]
                missing_fields = [field for field in required_fields if field not in backups_data]
                if missing_fields:
                    self.log_test("Database Backups Structure", False, 
                                f"Missing fields: {missing_fields}", backups_data)
                    return False
                
                # Verify backups is array
                if not isinstance(backups_data["backups"], list):
                    self.log_test("Database Backups Array Type", False, 
                                "backups should be an array", type(backups_data["backups"]))
                    return False
                
                # If there are backups, verify structure
                if backups_data["backups"]:
                    backup = backups_data["backups"][0]
                    backup_fields = ["path", "name", "size_mb", "modified"]
                    missing_backup_fields = [field for field in backup_fields if field not in backup]
                    if missing_backup_fields:
                        self.log_test("Database Backup Item Structure", False,
                                    f"Missing backup fields: {missing_backup_fields}", backup)
                        return False
                
                self.log_test("Database Backups List", True, 
                            f"Found {backups_data['count']} backups available", 
                            {"backup_count": backups_data["count"]})
                return True
            else:
                self.log_test("Database Backups List", False, f"HTTP {response.status_code}", response.text)
                return False
                
        except Exception as e:
            self.log_test("Database Backups List", False, f"Exception: {str(e)}")
            return False

    def test_database_backup_create(self):
        """Test POST /api/database/backup"""
        print("🔍 Testing Database Backup Creation...")
        try:
            response = self.session.post(f"{BASE_URL}/database/backup")
            
            if response.status_code == 200:
                backup_result = response.json()
                
                # Verify required fields
                required_fields = ["message", "status"]
                missing_fields = [field for field in required_fields if field not in backup_result]
                if missing_fields:
                    self.log_test("Database Backup Create Structure", False, 
                                f"Missing fields: {missing_fields}", backup_result)
                    return False
                
                # Verify status is "processing"
                if backup_result["status"] != "processing":
                    self.log_test("Database Backup Status", False, 
                                f"Expected status 'processing', got '{backup_result['status']}'", backup_result)
                    return False
                
                self.log_test("Database Backup Create", True, 
                            f"Backup initiated with status: {backup_result['status']}", 
                            backup_result)
                return True
            else:
                self.log_test("Database Backup Create", False, f"HTTP {response.status_code}", response.text)
                return False
                
        except Exception as e:
            self.log_test("Database Backup Create", False, f"Exception: {str(e)}")
            return False

    def test_database_indexes_payment_transactions(self):
        """Test GET /api/database/indexes/payment_transactions"""
        print("🔍 Testing Payment Transactions Indexes...")
        try:
            response = self.session.get(f"{BASE_URL}/database/indexes/payment_transactions")
            
            if response.status_code == 200:
                indexes_data = response.json()
                
                # Verify required fields
                required_fields = ["collection", "indexes"]
                missing_fields = [field for field in required_fields if field not in indexes_data]
                if missing_fields:
                    self.log_test("Payment Transactions Indexes Structure", False, 
                                f"Missing fields: {missing_fields}", indexes_data)
                    return False
                
                # Verify collection name
                if indexes_data["collection"] != "payment_transactions":
                    self.log_test("Payment Transactions Collection Name", False, 
                                f"Expected collection 'payment_transactions', got '{indexes_data['collection']}'", indexes_data)
                    return False
                
                # Verify indexes is array
                if not isinstance(indexes_data["indexes"], list):
                    self.log_test("Payment Transactions Indexes Array", False, 
                                "indexes should be an array", type(indexes_data["indexes"]))
                    return False
                
                # Check for specific expected indexes
                expected_indexes = ["user_email", "payment_status", "session_id_unique", "user_status", "created_at_desc", "type_status"]
                index_names = [idx.get("name", "") for idx in indexes_data["indexes"]]
                
                missing_indexes = []
                for expected_idx in expected_indexes:
                    if not any(expected_idx in name for name in index_names):
                        missing_indexes.append(expected_idx)
                
                if missing_indexes:
                    self.log_test("Payment Transactions Expected Indexes", False, 
                                f"Missing expected indexes: {missing_indexes}", index_names)
                    return False
                
                self.log_test("Payment Transactions Indexes", True, 
                            f"Found {len(indexes_data['indexes'])} indexes including expected ones", 
                            {"total_indexes": len(indexes_data["indexes"]), "expected_found": len(expected_indexes) - len(missing_indexes)})
                return True
            else:
                self.log_test("Payment Transactions Indexes", False, f"HTTP {response.status_code}", response.text)
                return False
                
        except Exception as e:
            self.log_test("Payment Transactions Indexes", False, f"Exception: {str(e)}")
            return False

    def test_database_indexes_notifications(self):
        """Test GET /api/database/indexes/notifications"""
        print("🔍 Testing Notifications Indexes...")
        try:
            response = self.session.get(f"{BASE_URL}/database/indexes/notifications")
            
            if response.status_code == 200:
                indexes_data = response.json()
                
                # Verify required fields
                required_fields = ["collection", "indexes"]
                missing_fields = [field for field in required_fields if field not in indexes_data]
                if missing_fields:
                    self.log_test("Notifications Indexes Structure", False, 
                                f"Missing fields: {missing_fields}", indexes_data)
                    return False
                
                # Verify collection name
                if indexes_data["collection"] != "notifications":
                    self.log_test("Notifications Collection Name", False, 
                                f"Expected collection 'notifications', got '{indexes_data['collection']}'", indexes_data)
                    return False
                
                # Verify indexes is array
                if not isinstance(indexes_data["indexes"], list):
                    self.log_test("Notifications Indexes Array", False, 
                                "indexes should be an array", type(indexes_data["indexes"]))
                    return False
                
                # Check for specific expected indexes
                expected_indexes = ["user_email", "is_read", "user_read", "user_created", "type", "created_at_desc"]
                index_names = [idx.get("name", "") for idx in indexes_data["indexes"]]
                
                missing_indexes = []
                for expected_idx in expected_indexes:
                    if not any(expected_idx in name for name in index_names):
                        missing_indexes.append(expected_idx)
                
                if missing_indexes:
                    self.log_test("Notifications Expected Indexes", False, 
                                f"Missing expected indexes: {missing_indexes}", index_names)
                    return False
                
                self.log_test("Notifications Indexes", True, 
                            f"Found {len(indexes_data['indexes'])} indexes including expected ones", 
                            {"total_indexes": len(indexes_data["indexes"]), "expected_found": len(expected_indexes) - len(missing_indexes)})
                return True
            else:
                self.log_test("Notifications Indexes", False, f"HTTP {response.status_code}", response.text)
                return False
                
        except Exception as e:
            self.log_test("Notifications Indexes", False, f"Exception: {str(e)}")
            return False

    def run_all_tests(self):
        """Run all payment system tests"""
        print("🚀 Starting Comprehensive Payment System Testing")
        print("=" * 60)
        
        # Test sequence
        tests = [
            ("Subscription Plans", self.test_subscription_plans),
            ("Get Products", self.get_products),
            ("Product Checkout", self.test_product_checkout),
            ("Subscription Checkout", self.test_subscription_checkout),
            ("Revenue Analytics", self.test_revenue_analytics),
            ("Campaign ROI", self.test_campaign_roi),
            ("Affiliate Commissions", self.test_affiliate_commissions),
            ("Advanced Dashboard", self.test_advanced_dashboard),
            ("Payment History", self.test_payment_history)
        ]
        
        passed = 0
        total = len(tests)
        
        for test_name, test_func in tests:
            try:
                if test_func():
                    passed += 1
            except Exception as e:
                self.log_test(test_name, False, f"Unexpected error: {str(e)}")
        
        print("=" * 60)
        print(f"🏁 TESTING COMPLETE: {passed}/{total} tests passed")
        
        if passed == total:
            print("🎉 ALL TESTS PASSED! Payment system is working correctly.")
        else:
            print("⚠️  Some tests failed. Check details above.")
        
        return passed, total, self.test_results

def main():
    """Main testing function"""
    tester = PaymentSystemTester()
    passed, total, results = tester.run_all_tests()
    
    # Save detailed results
    with open("/app/payment_test_results.json", "w") as f:
        json.dump({
            "summary": {
                "passed": passed,
                "total": total,
                "success_rate": f"{(passed/total)*100:.1f}%",
                "timestamp": datetime.now().isoformat()
            },
            "detailed_results": results
        }, f, indent=2)
    
    print(f"\n📄 Detailed results saved to: /app/payment_test_results.json")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)