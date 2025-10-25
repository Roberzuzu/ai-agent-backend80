# ai_integrations_complete.py
# Complete AI Router implementation with integrations and fallback logic

from __future__ import annotations

import logging
import json
import time
from typing import Any, Dict, List, Optional, Tuple, Callable

# Local imports (existing project modules)
from .ai_router import AIRouterBase
from .llm_client import OpenAIClient, PerplexityClient, ClaudeClient
from .n8n_client import N8nClient
from .woocommerce_client import WooCommerceClient
from .wordpress_integration import WordPressIntegration
from .integraciones_sociales import SocialIntegrations
from .ai_integrations import FALClient, AbacusClient, OpenAIToolsClient

logger = logging.getLogger(__name__)


class AIRouter(AIRouterBase):
    """
    Complete AI Router using Perplexity as primary coordinator and OpenAI as backup.
    Provides handler methods for woocommerce, n8n, social media, wordpress, FAL, perplexity,
    abacus, openai tools, and claude. Implements complete detect_intent with fallbacks.
    """

    def __init__(
        self,
        openai_client: Optional[OpenAIClient] = None,
        perplexity_client: Optional[PerplexityClient] = None,
        claude_client: Optional[ClaudeClient] = None,
        n8n_client: Optional[N8nClient] = None,
        woocommerce_client: Optional[WooCommerceClient] = None,
        wordpress_integration: Optional[WordPressIntegration] = None,
        social_integrations: Optional[SocialIntegrations] = None,
        fal_client: Optional[FALClient] = None,
        abacus_client: Optional[AbacusClient] = None,
        openai_tools_client: Optional[OpenAIToolsClient] = None,
        config: Optional[Dict[str, Any]] = None,
    ) -> None:
        super().__init__(config=config)

        # Clients
        self.openai = openai_client or OpenAIClient(config=config)
        self.perplexity = perplexity_client or PerplexityClient(config=config)
        self.claude = claude_client or ClaudeClient(config=config)
        self.n8n = n8n_client or N8nClient(config=config)
        self.wc = woocommerce_client or WooCommerceClient(config=config)
        self.wp = wordpress_integration or WordPressIntegration(config=config)
        self.social = social_integrations or SocialIntegrations(config=config)
        self.fal = fal_client or FALClient(config=config)
        self.abacus = abacus_client or AbacusClient(config=config)
        self.openai_tools = openai_tools_client or OpenAIToolsClient(config=config)

        logger.debug("AIRouter initialized with all integrations.")

    # ------------------------ Coordinator Logic ------------------------
    def detect_intent(
        self,
        user_input: str,
        context: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Use Perplexity as primary to detect intent and routing. Fallback to OpenAI, then Claude.
        Returns a dict with keys: intent, confidence, route, tool, arguments, notes.
        """
        context = context or {}

        def _safe_parse(resp: Any) -> Dict[str, Any]:
            if isinstance(resp, dict):
                return resp
            try:
                return json.loads(resp)
            except Exception:
                return {
                    "intent": "unknown",
                    "confidence": 0.0,
                    "route": "none",
                    "tool": None,
                    "arguments": {},
                    "notes": str(resp)[:500],
                }

        # Attempt 1: Perplexity as primary coordinator
        try:
            logger.info("Detecting intent with Perplexity...")
            pxy_prompt = self._build_coordinator_prompt(user_input, context)
            pxy_resp = self.perplexity.detect_intent(pxy_prompt)
            parsed = _safe_parse(pxy_resp)
            if parsed.get("intent") and parsed.get("route"):
                logger.debug("Perplexity intent parsed: %s", parsed)
                return parsed
        except Exception as e:
            logger.warning("Perplexity detect_intent failed: %s", e)

        # Attempt 2: OpenAI backup
        try:
            logger.info("Detecting intent with OpenAI backup...")
            oai_prompt = self._build_coordinator_prompt(user_input, context)
            oai_resp = self.openai.detect_intent(oai_prompt)
            parsed = _safe_parse(oai_resp)
            if parsed.get("intent") and parsed.get("route"):
                logger.debug("OpenAI intent parsed: %s", parsed)
                return parsed
        except Exception as e:
            logger.warning("OpenAI detect_intent failed: %s", e)

        # Attempt 3: Claude final fallback
        try:
            logger.info("Detecting intent with Claude fallback...")
            claude_prompt = self._build_coordinator_prompt(user_input, context)
            cl_resp = self.claude.detect_intent(claude_prompt)
            parsed = _safe_parse(cl_resp)
            logger.debug("Claude intent parsed: %s", parsed)
            return parsed
        except Exception as e:
            logger.error("Claude detect_intent failed: %s", e)

        # Absolute fallback
        return {
            "intent": "unknown",
            "confidence": 0.0,
            "route": "none",
            "tool": None,
            "arguments": {},
            "notes": "All providers failed",
        }

    def _build_coordinator_prompt(self, user_input: str, context: Dict[str, Any]) -> str:
        schema_hint = (
            "Return strict JSON with keys: intent, confidence, route, tool, arguments, notes."
        )
        routes = [
            "woocommerce", "n8n", "social", "wordpress", "fal", "perplexity",
            "abacus", "openai_tools", "claude", "analysis_only"
        ]
        return (
            f"User: {user_input}\n"
            f"Context: {json.dumps(context)[:2000]}\n"
            f"Decide best route from {routes}. {schema_hint}"
        )

    # ------------------------ Public Routing ------------------------
    def route(self, user_input: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        context = context or {}
        intent = self.detect_intent(user_input, context)
        route = intent.get("route")
        args = intent.get("arguments", {}) or {}
        tool = intent.get("tool")
        result: Dict[str, Any]

        try:
            if route == "woocommerce":
                result = self.handle_woocommerce(tool, args, context)
            elif route == "n8n":
                result = self.handle_n8n(tool, args, context)
            elif route == "social":
                result = self.handle_social(tool, args, context)
            elif route == "wordpress":
                result = self.handle_wordpress(tool, args, context)
            elif route == "fal":
                result = self.handle_fal(tool, args, context)
            elif route == "perplexity":
                result = self.handle_perplexity(tool, args, context)
            elif route == "abacus":
                result = self.handle_abacus(tool, args, context)
            elif route == "openai_tools":
                result = self.handle_openai_tools(tool, args, context)
            elif route == "claude":
                result = self.handle_claude(tool, args, context)
            else:
                # Default to analysis with Perplexity then OpenAI
                result = self.handle_perplexity("answer", {"query": user_input}, context)
        except Exception as e:
            logger.exception("Routing error: %s", e)
            result = {"ok": False, "error": str(e)}

        return {"intent": intent, "result": result}

    # ------------------------ Handlers ------------------------
    def handle_woocommerce(self, tool: Optional[str], args: Dict[str, Any], ctx: Dict[str, Any]) -> Dict[str, Any]:
        try:
            action = tool or args.get("action")
            if action == "list_products":
                return self.wc.list_products(**args)
            if action == "get_product":
                return self.wc.get_product(args.get("product_id"))
            if action == "create_product":
                return self.wc.create_product(args.get("data", {}))
            if action == "update_product":
                return self.wc.update_product(args.get("product_id"), args.get("data", {}))
            if action == "orders_list":
                return self.wc.list_orders(**args)
            if action == "order_get":
                return self.wc.get_order(args.get("order_id"))
            return {"ok": False, "error": f"Unknown WooCommerce action: {action}"}
        except Exception as e:
            logger.exception("WooCommerce handler error: %s", e)
            return {"ok": False, "error": str(e)}

    def handle_n8n(self, tool: Optional[str], args: Dict[str, Any], ctx: Dict[str, Any]) -> Dict[str, Any]:
        try:
            workflow = args.get("workflow") or tool
            payload = args.get("payload", {})
            return self.n8n.trigger_workflow(workflow, payload)
        except Exception as e:
            logger.exception("n8n handler error: %s", e)
            return {"ok": False, "error": str(e)}

    def handle_social(self, tool: Optional[str], args: Dict[str, Any], ctx: Dict[str, Any]) -> Dict[str, Any]:
        try:
            platform = args.get("platform")
            action = tool or args.get("action")
            if action == "post":
                return self.social.post(platform, args.get("content"), **args)
            if action == "schedule":
                return self.social.schedule(platform, args.get("content"), args.get("when"), **args)
            if action == "insights":
                return self.social.insights(platform, **args)
            return {"ok": False, "error": f"Unknown Social action: {action}"}
        except Exception as e:
            logger.exception("Social handler error: %s", e)
            return {"ok": False, "error": str(e)}

    def handle_wordpress(self, tool: Optional[str], args: Dict[str, Any], ctx: Dict[str, Any]) -> Dict[str, Any]:
        try:
            action = tool or args.get("action")
            if action == "create_post":
                return self.wp.create_post(args.get("title"), args.get("content"), **args)
            if action == "update_post":
                return self.wp.update_post(args.get("post_id"), args.get("data", {}))
            if action == "list_posts":
                return self.wp.list_posts(**args)
            if action == "media_upload":
                return self.wp.upload_media(args.get("file_path"), **args)
            return {"ok": False, "error": f"Unknown WordPress action: {action}"}
        except Exception as e:
            logger.exception("WordPress handler error: %s", e)
            return {"ok": False, "error": str(e)}

    def handle_fal(self, tool: Optional[str], args: Dict[str, Any], ctx: Dict[str, Any]) -> Dict[str, Any]:
        try:
            action = tool or args.get("action")
            if action == "image_generate":
                return self.fal.image_generate(**args)
            if action == "image_variation":
                return self.fal.image_variation(**args)
            return {"ok": False, "error": f"Unknown FAL action: {action}"}
        except Exception as e:
            logger.exception("FAL handler error: %s", e)
            return {"ok": False, "error": str(e)}

    def handle_perplexity(self, tool: Optional[str], args: Dict[str, Any], ctx: Dict[str, Any]) -> Dict[str, Any]:
        try:
            action = tool or args.get("action") or "answer"
            if action == "answer":
                return self.perplexity.answer(args.get("query"))
            if action == "search":
                return self.perplexity.search(args.get("query"), **args)
            return {"ok": False, "error": f"Unknown Perplexity action: {action}"}
        except Exception as e:
            logger.exception("Perplexity handler error: %s", e)
            # Fallback to OpenAI answering
            try:
                return self.openai.answer(args.get("query"))
            except Exception as e2:
                logger.exception("OpenAI backup failed: %s", e2)
                return {"ok": False, "error": str(e)}

    def handle_abacus(self, tool: Optional[str], args: Dict[str, Any], ctx: Dict[str, Any]) -> Dict[str, Any]:
        try:
            action = tool or args.get("action")
            if action == "metrics":
                return self.abacus.metrics(**args)
            if action == "log_event":
                return self.abacus.log_event(**args)
            return {"ok": False, "error": f"Unknown Abacus action: {action}"}
        except Exception as e:
            logger.exception("Abacus handler error: %s", e)
            return {"ok": False, "error": str(e)}

    def handle_openai_tools(self, tool: Optional[str], args: Dict[str, Any], ctx: Dict[str, Any]) -> Dict[str, Any]:
        try:
            action = tool or args.get("action")
            if action == "function_call":
                return self.openai_tools.function_call(args.get("name"), args.get("arguments", {}))
            if action == "embedding":
                return self.openai_tools.embedding(args.get("text"), **args)
            if action == "moderation":
                return self.openai_tools.moderation(args.get("text"))
            return {"ok": False, "error": f"Unknown OpenAI Tools action: {action}"}
        except Exception as e:
            logger.exception("OpenAI Tools handler error: %s", e)
            return {"ok": False, "error": str(e)}

    def handle_claude(self, tool: Optional[str], args: Dict[str, Any], ctx: Dict[str, Any]) -> Dict[str, Any]:
        try:
            action = tool or args.get("action") or "answer"
            if action == "answer":
                return self.claude.answer(args.get("query"))
            if action == "tool_use":
                return self.claude.tool_use(args.get("tool"), args.get("arguments", {}))
            return {"ok": False, "error": f"Unknown Claude action: {action}"}
        except Exception as e:
            logger.exception("Claude handler error: %s", e)
            return {"ok": False, "error": str(e)}


# If directly executed, perform a quick sanity check (non-fatal if dependencies not configured)
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    router = AIRouter()
    sample = router.route("List WooCommerce products", {"prefer": "woocommerce"})
    print(json.dumps(sample, indent=2, default=str))
