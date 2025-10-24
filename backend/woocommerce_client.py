"""
WooCommerce API asynchronous client using httpx.

Features:
- Environment-based configuration for base URL, consumer key, and consumer secret
- Fully async methods for common WooCommerce operations
- Robust error handling and helpful exceptions
- Type hints and detailed English docstrings

Environment variables:
- WOOCOMMERCE_BASE_URL: Base URL of your WooCommerce store (e.g., https://example.com)
- WOOCOMMERCE_CONSUMER_KEY: WooCommerce REST API consumer key
- WOOCOMMERCE_CONSUMER_SECRET: WooCommerce REST API consumer secret

Note: For self-hosted WordPress behind proxies/CDNs, ensure HTTPS and REST API accessibility.
"""
from __future__ import annotations

import os
from typing import Any, Dict, List, Optional, Union, Mapping

import httpx


class WooCommerceError(RuntimeError):
    """Custom exception representing WooCommerce API errors."""

    def __init__(self, message: str, status_code: Optional[int] = None, details: Optional[Any] = None):
        super().__init__(message)
        self.status_code = status_code
        self.details = details

    def __str__(self) -> str:
        base = super().__str__()
        if self.status_code is not None:
            base += f" (status={self.status_code})"
        if self.details is not None:
            base += f" details={self.details!r}"
        return base


class WooCommerceClient:
    """Asynchronous WooCommerce REST API client using httpx.

    This client wraps common endpoints of the WooCommerce REST API and handles
    authentication, request building, and error handling. All methods are async
    and safe to use within asyncio applications or async frameworks (e.g., FastAPI).

    Credentials are loaded from environment variables by default:
    - WOOCOMMERCE_BASE_URL
    - WOOCOMMERCE_CONSUMER_KEY
    - WOOCOMMERCE_CONSUMER_SECRET

    You can also pass them explicitly to the constructor to override env values.

    Parameters
    - base_url: Base URL to your WooCommerce site (e.g., https://store.example.com)
    - consumer_key: WooCommerce REST API consumer key
    - consumer_secret: WooCommerce REST API consumer secret
    - timeout: Optional request timeout in seconds (default: 30.0)
    - verify_ssl: Whether to verify SSL certificates (default: True)

    Usage
        async with WooCommerceClient() as wc:
            products = await wc.get_products(per_page=20)
    """

    def __init__(
        self,
        base_url: Optional[str] = None,
        consumer_key: Optional[str] = None,
        consumer_secret: Optional[str] = None,
        *,
        timeout: Union[float, httpx.Timeout] = 30.0,
        verify_ssl: bool = True,
        additional_headers: Optional[Mapping[str, str]] = None,
    ) -> None:
        self.base_url = (base_url or os.getenv("WOOCOMMERCE_BASE_URL") or "").rstrip("/")
        self.consumer_key = consumer_key or os.getenv("WOOCOMMERCE_CONSUMER_KEY")
        self.consumer_secret = consumer_secret or os.getenv("WOOCOMMERCE_CONSUMER_SECRET")
        self.timeout = timeout
        self.verify_ssl = verify_ssl
        self._client: Optional[httpx.AsyncClient] = None
        self._headers: Dict[str, str] = {"Accept": "application/json"}
        if additional_headers:
            self._headers.update(dict(additional_headers))

        if not self.base_url:
            raise WooCommerceError("WOOCOMMERCE_BASE_URL is not configured")
        if not self.consumer_key or not self.consumer_secret:
            raise WooCommerceError("WooCommerce API credentials are not configured")

        # WooCommerce REST namespace
        self.api_prefix = "/wp-json/wc/v3"

    async def __aenter__(self) -> "WooCommerceClient":
        await self._ensure_client()
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        await self.aclose()

    async def _ensure_client(self) -> None:
        """Initialize the underlying httpx.AsyncClient if not already created."""
        if self._client is None:
            self._client = httpx.AsyncClient(
                base_url=self.base_url,
                timeout=self.timeout,
                verify=self.verify_ssl,
                headers=self._headers,
                auth=httpx.BasicAuth(self.consumer_key or "", self.consumer_secret or ""),
            )

    async def aclose(self) -> None:
        """Close the underlying HTTP client."""
        if self._client is not None:
            await self._client.aclose()
            self._client = None

    # --------------- Internal helpers ---------------
    async def _request(
        self,
        method: str,
        path: str,
        *,
        params: Optional[Dict[str, Any]] = None,
        json: Optional[Any] = None,
    ) -> Any:
        """Perform an HTTP request and handle common WooCommerce errors.

        Raises WooCommerceError on non-2xx responses.
        """
        await self._ensure_client()
        assert self._client is not None

        url = f"{self.api_prefix}{path}"
        try:
            resp = await self._client.request(method, url, params=params, json=json)
        except httpx.HTTPError as e:
            raise WooCommerceError(f"HTTP error while requesting {method} {url}: {e}") from e

        if resp.status_code >= 400:
            try:
                details = resp.json()
            except Exception:
                details = resp.text
            message = details.get("message") if isinstance(details, dict) else str(details)
            raise WooCommerceError(message or "WooCommerce API error", status_code=resp.status_code, details=details)

        # Try to parse JSON; some endpoints may return empty body (204)
        if resp.status_code == 204 or not resp.content:
            return None
        try:
            return resp.json()
        except ValueError:
            return resp.text

    # --------------- Public API methods ---------------
    async def get_products(self, page: int = 1, per_page: int = 10, status: Optional[str] = None) -> List[Dict[str, Any]]:
        """Retrieve a paginated list of products.

        Parameters
        - page: Page number (1-based)
        - per_page: Items per page (max typically 100)
        - status: Optional product status filter (e.g., 'publish', 'draft')
        """
        params: Dict[str, Any] = {"page": page, "per_page": per_page}
        if status:
            params["status"] = status
        data = await self._request("GET", "/products", params=params)
        return list(data or [])

    async def search_products(self, search: str, page: int = 1, per_page: int = 10) -> List[Dict[str, Any]]:
        """Search products by a query string."""
        params = {"search": search, "page": page, "per_page": per_page}
        data = await self._request("GET", "/products", params=params)
        return list(data or [])

    async def create_product(self, product: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new product.

        Example product payload:
        {
            "name": "T-Shirt",
            "type": "simple",
            "regular_price": "19.99",
            "description": "A great shirt",
            "categories": [{"id": 12}],
            "images": [{"src": "https://.../image.jpg"}]
        }
        """
        data = await self._request("POST", "/products", json=product)
        return dict(data or {})

    async def update_product(self, product_id: int, updates: Dict[str, Any]) -> Dict[str, Any]:
        """Update an existing product by ID."""
        data = await self._request("PUT", f"/products/{product_id}", json=updates)
        return dict(data or {})

    async def delete_product(self, product_id: int, force: bool = True) -> Dict[str, Any]:
        """Delete a product by ID.

        Parameters
        - force: If True, permanently delete (bypass trash). Default True.
        """
        params = {"force": str(force).lower()}
        data = await self._request("DELETE", f"/products/{product_id}", params=params)
        return dict(data or {})

    async def get_orders(self, page: int = 1, per_page: int = 10, status: Optional[str] = None) -> List[Dict[str, Any]]:
        """Retrieve a paginated list of orders."""
        params: Dict[str, Any] = {"page": page, "per_page": per_page}
        if status:
            params["status"] = status
        data = await self._request("GET", "/orders", params=params)
        return list(data or [])

    async def get_order_by_id(self, order_id: int) -> Dict[str, Any]:
        """Retrieve order details by ID."""
        data = await self._request("GET", f"/orders/{order_id}")
        return dict(data or {})

    async def update_order_status(self, order_id: int, status: str) -> Dict[str, Any]:
        """Update the status of an order.

        Common statuses include: pending, processing, on-hold, completed, cancelled, refunded, failed.
        """
        payload = {"status": status}
        data = await self._request("PUT", f"/orders/{order_id}", json=payload)
        return dict(data or {})

    async def get_categories(self, page: int = 1, per_page: int = 10, hide_empty: Optional[bool] = None) -> List[Dict[str, Any]]:
        """Retrieve product categories."""
        params: Dict[str, Any] = {"page": page, "per_page": per_page}
        if hide_empty is not None:
            params["hide_empty"] = str(hide_empty).lower()
        data = await self._request("GET", "/products/categories", params=params)
        return list(data or [])


# Convenience function if needed by external modules
async def get_woocommerce_client(**kwargs: Any) -> WooCommerceClient:
    """Factory that returns a WooCommerceClient instance using environment defaults."""
    return WooCommerceClient(**kwargs)
