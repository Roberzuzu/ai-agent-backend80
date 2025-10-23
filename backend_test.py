#!/usr/bin/env python3
"""
Comprehensive Backend Testing for AI Agent System (Cerebro AI)
Tests the AI Agent endpoints as requested in the review
Priority: HIGH - Testing the new AI Agent system with Claude 3.5 Sonnet
"""

import requests
import json
import time
from datetime import datetime
from typing import Dict, Any, List

# Configuration
BASE_URL = "https://railway-port-config.preview.emergentagent.com/api"
TEST_USER_ID = "test_user_backend"
ORIGIN_URL = "https://railway-port-config.preview.emergentagent.com"

class AIAgentTester:
    def __init__(self):
        self.session = requests.Session()
        self.test_results = []
        
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

    def test_agent_status(self):
        """Test GET /api/agent/status - Verificar estado del agente"""
        print("🔍 Testing Agent Status...")
        try:
            response = self.session.get(f"{BASE_URL}/agent/status")
            
            if response.status_code == 200:
                status = response.json()
                
                # Verificar campos requeridos
                required_fields = ["success", "agente_activo", "herramientas_disponibles", "caracteristicas"]
                missing_fields = [field for field in required_fields if field not in status]
                if missing_fields:
                    self.log_test("Agent Status Structure", False, f"Missing fields: {missing_fields}", status)
                    return False
                
                # Verificar valores específicos
                if not status.get("success"):
                    self.log_test("Agent Status Success", False, "success should be true", status)
                    return False
                
                if not status.get("agente_activo"):
                    self.log_test("Agent Status Active", False, "agente_activo should be true", status)
                    return False
                
                if status.get("herramientas_disponibles") != 22:
                    self.log_test("Agent Status Tools", False, f"Expected 22 tools, got {status.get('herramientas_disponibles')}", status)
                    return False
                
                # Verificar características
                caracteristicas = status.get("caracteristicas", {})
                if not caracteristicas.get("memoria_persistente"):
                    self.log_test("Agent Status Memory", False, "memoria_persistente should be true", caracteristicas)
                    return False
                
                if not caracteristicas.get("rag_enabled"):
                    self.log_test("Agent Status RAG", False, "rag_enabled should be true", caracteristicas)
                    return False
                
                self.log_test("Agent Status", True, 
                            f"Agent active with {status['herramientas_disponibles']} tools, memory and RAG enabled", 
                            {k: v for k, v in status.items() if k != "caracteristicas"})
                return True
            else:
                self.log_test("Agent Status", False, f"HTTP {response.status_code}", response.text)
                return False
                
        except Exception as e:
            self.log_test("Agent Status", False, f"Exception: {str(e)}")
            return False

    def test_agent_execute_simple(self):
        """Test POST /api/agent/execute - Ejecutar comando simple"""
        print("🔍 Testing Agent Execute Simple Command...")
        try:
            command_data = {
                "command": "Dame las estadísticas del sitio",
                "user_id": TEST_USER_ID
            }
            
            response = self.session.post(
                f"{BASE_URL}/agent/execute",
                json=command_data,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                result = response.json()
                
                # Verificar campos requeridos
                required_fields = ["success", "mensaje", "plan", "resultados"]
                missing_fields = [field for field in required_fields if field not in result]
                if missing_fields:
                    self.log_test("Agent Execute Structure", False, f"Missing fields: {missing_fields}", result)
                    return False
                
                # Verificar success
                if not result.get("success"):
                    self.log_test("Agent Execute Success", False, "success should be true", result)
                    return False
                
                # Verificar que hay mensaje
                if not result.get("mensaje"):
                    self.log_test("Agent Execute Message", False, "mensaje should not be empty", result)
                    return False
                
                # Verificar que hay plan
                if not result.get("plan"):
                    self.log_test("Agent Execute Plan", False, "plan should not be empty", result)
                    return False
                
                # Verificar que hay resultados (array con al menos 1 resultado)
                resultados = result.get("resultados", [])
                if not isinstance(resultados, list) or len(resultados) < 1:
                    self.log_test("Agent Execute Results", False, "resultados should be array with at least 1 result", resultados)
                    return False
                
                self.log_test("Agent Execute Simple", True, 
                            f"Command executed successfully with {len(resultados)} results", 
                            {"has_message": bool(result.get("mensaje")), "has_plan": bool(result.get("plan")), "results_count": len(resultados)})
                return True
            else:
                self.log_test("Agent Execute Simple", False, f"HTTP {response.status_code}", response.text)
                return False
                
        except Exception as e:
            self.log_test("Agent Execute Simple", False, f"Exception: {str(e)}")
            return False

    def test_agent_memory_get(self):
        """Test GET /api/agent/memory/{user_id} - Verificar memoria guardada"""
        print("🔍 Testing Agent Memory Retrieval...")
        try:
            response = self.session.get(f"{BASE_URL}/agent/memory/{TEST_USER_ID}?limit=5")
            
            if response.status_code == 200:
                memory_data = response.json()
                
                # Verificar campos requeridos
                required_fields = ["success", "user_id", "total", "memories"]
                missing_fields = [field for field in required_fields if field not in memory_data]
                if missing_fields:
                    self.log_test("Agent Memory Structure", False, f"Missing fields: {missing_fields}", memory_data)
                    return False
                
                # Verificar success
                if not memory_data.get("success"):
                    self.log_test("Agent Memory Success", False, "success should be true", memory_data)
                    return False
                
                # Verificar user_id
                if memory_data.get("user_id") != TEST_USER_ID:
                    self.log_test("Agent Memory User ID", False, f"Expected user_id {TEST_USER_ID}, got {memory_data.get('user_id')}", memory_data)
                    return False
                
                # Verificar memories es array
                if not isinstance(memory_data.get("memories"), list):
                    self.log_test("Agent Memory Array", False, "memories should be an array", type(memory_data.get("memories")))
                    return False
                
                # Si hay memorias, verificar estructura
                memories = memory_data.get("memories", [])
                if memories:
                    memory = memories[0]
                    memory_fields = ["command", "response", "timestamp"]
                    missing_memory_fields = [field for field in memory_fields if field not in memory]
                    if missing_memory_fields:
                        self.log_test("Agent Memory Item Structure", False,
                                    f"Missing memory fields: {missing_memory_fields}", memory)
                        return False
                
                self.log_test("Agent Memory Get", True, 
                            f"Retrieved {len(memories)} memories for user {TEST_USER_ID}", 
                            {"total": memory_data.get("total"), "memories_count": len(memories)})
                return True
            else:
                self.log_test("Agent Memory Get", False, f"HTTP {response.status_code}", response.text)
                return False
                
        except Exception as e:
            self.log_test("Agent Memory Get", False, f"Exception: {str(e)}")
            return False

    def test_agent_chat(self):
        """Test POST /api/agent/chat - Chat sin ejecución"""
        print("🔍 Testing Agent Chat...")
        try:
            chat_data = {
                "command": "¿Qué herramientas tienes disponibles?",
                "user_id": TEST_USER_ID
            }
            
            response = self.session.post(
                f"{BASE_URL}/agent/chat",
                json=chat_data,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                result = response.json()
                
                # Verificar campos requeridos
                required_fields = ["success", "respuesta", "plan", "acciones_sugeridas"]
                missing_fields = [field for field in required_fields if field not in result]
                if missing_fields:
                    self.log_test("Agent Chat Structure", False, f"Missing fields: {missing_fields}", result)
                    return False
                
                # Verificar success
                if not result.get("success"):
                    self.log_test("Agent Chat Success", False, "success should be true", result)
                    return False
                
                # Verificar que hay respuesta
                if not result.get("respuesta"):
                    self.log_test("Agent Chat Response", False, "respuesta should not be empty", result)
                    return False
                
                # Verificar que acciones_sugeridas es array
                if not isinstance(result.get("acciones_sugeridas"), list):
                    self.log_test("Agent Chat Actions", False, "acciones_sugeridas should be an array", type(result.get("acciones_sugeridas")))
                    return False
                
                self.log_test("Agent Chat", True, 
                            f"Chat response received with {len(result.get('acciones_sugeridas', []))} suggested actions", 
                            {"has_response": bool(result.get("respuesta")), "has_plan": bool(result.get("plan"))})
                return True
            else:
                self.log_test("Agent Chat", False, f"HTTP {response.status_code}", response.text)
                return False
                
        except Exception as e:
            self.log_test("Agent Chat", False, f"Exception: {str(e)}")
            return False

    def test_agent_search_memory(self):
        """Test POST /api/agent/search-memory - Búsqueda semántica"""
        print("🔍 Testing Agent Search Memory...")
        try:
            search_data = {
                "command": "estadísticas",
                "user_id": TEST_USER_ID
            }
            
            response = self.session.post(
                f"{BASE_URL}/agent/search-memory",
                json=search_data,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                result = response.json()
                
                # Verificar campos requeridos
                required_fields = ["success", "query", "resultados", "memories"]
                missing_fields = [field for field in required_fields if field not in result]
                if missing_fields:
                    self.log_test("Agent Search Memory Structure", False, f"Missing fields: {missing_fields}", result)
                    return False
                
                # Verificar success
                if not result.get("success"):
                    self.log_test("Agent Search Memory Success", False, "success should be true", result)
                    return False
                
                # Verificar query
                if result.get("query") != "estadísticas":
                    self.log_test("Agent Search Memory Query", False, f"Expected query 'estadísticas', got '{result.get('query')}'", result)
                    return False
                
                # Verificar memories es array
                if not isinstance(result.get("memories"), list):
                    self.log_test("Agent Search Memory Array", False, "memories should be an array", type(result.get("memories")))
                    return False
                
                # Verificar resultados count
                memories = result.get("memories", [])
                if result.get("resultados") != len(memories):
                    self.log_test("Agent Search Memory Count", False, f"resultados count {result.get('resultados')} doesn't match memories length {len(memories)}", result)
                    return False
                
                # Si hay memorias, verificar estructura
                if memories:
                    memory = memories[0]
                    memory_fields = ["command", "response", "timestamp", "similarity"]
                    missing_memory_fields = [field for field in memory_fields if field not in memory]
                    if missing_memory_fields:
                        self.log_test("Agent Search Memory Item Structure", False,
                                    f"Missing memory fields: {missing_memory_fields}", memory)
                        return False
                
                self.log_test("Agent Search Memory", True, 
                            f"Search returned {len(memories)} similar memories for query 'estadísticas'", 
                            {"query": result.get("query"), "results_count": len(memories)})
                return True
            else:
                self.log_test("Agent Search Memory", False, f"HTTP {response.status_code}", response.text)
                return False
                
        except Exception as e:
            self.log_test("Agent Search Memory", False, f"Exception: {str(e)}")
            return False

    # Additional test methods can be added here if needed

    def run_all_tests(self):
        """Run all AI Agent system tests"""
        print("🚀 Starting AI Agent System Testing (Cerebro AI)")
        print("=" * 80)
        
        # Test sequence - AI Agent tests as requested
        tests = [
            # AI Agent Core Tests (Priority: HIGH)
            ("Agent Status", self.test_agent_status),
            ("Agent Execute Simple", self.test_agent_execute_simple),
            ("Agent Memory Get", self.test_agent_memory_get),
            ("Agent Chat", self.test_agent_chat),
            ("Agent Search Memory", self.test_agent_search_memory)
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
            print("🎉 ALL TESTS PASSED! AI Agent system is working correctly.")
        else:
            print("⚠️  Some tests failed. Check details above.")
        
        return passed, total, self.test_results

def main():
    """Main testing function"""
    tester = AIAgentTester()
    passed, total, results = tester.run_all_tests()
    
    # Save detailed results
    with open("/app/ai_agent_test_results.json", "w") as f:
        json.dump({
            "summary": {
                "passed": passed,
                "total": total,
                "success_rate": f"{(passed/total)*100:.1f}%",
                "timestamp": datetime.now().isoformat()
            },
            "detailed_results": results
        }, f, indent=2)
    
    print(f"\n📄 Detailed results saved to: /app/ai_agent_test_results.json")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)