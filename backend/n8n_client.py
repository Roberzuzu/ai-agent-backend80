"""
Async n8n API client for managing and executing workflows.

- Uses environment variables:
  - N8N_BASE_URL: Base URL to the n8n API (default: https://n8n.cloud/api/v1)
  - N8N_API_KEY: API key for authentication
  - AI_AGENT_BACKEND: Optional central backend URL (default: https://ai-agent-backend80.onrender.com)
All methods are asynchronous and use httpx.AsyncClient under the hood.
"""

from __future__ import annotations

import os
from typing import Any, Dict, List, Optional, TypedDict, Union
import httpx

# Configuración para backend central AI Agent (puedes usarla para logging, hooks y reporting)
AI_AGENT_BACKEND = os.getenv("AI_AGENT_BACKEND", "https://ai-agent-backend80.onrender.com")

class N8nClientError(Exception):
    """Base exception for n8n client errors."""

class N8nAuthError(N8nClientError):
    """Raised when authentication configuration is missing or invalid."""

class N8nAPIResponseError(N8nClientError):
    """Raised when the n8n API returns a non-successful response."""
    def __init__(self, status_code: int, message: str, *, url: str | None = None, details: Any | None = None) -> None:
        super().__init__(f"HTTP {status_code}: {message}")
        self.status_code = status_code
        self.url = url
        self.details = details

class Execution(TypedDict, total=False):
    id: str
    status: str
    startedAt: str
    stoppedAt: Optional[str]
    workflowId: str
    mode: str
    finished: Optional[bool]
    data: Dict[str, Any]

class Workflow(TypedDict, total=False):
    id: str
    name: str
    active: bool
    nodes: List[Dict[str, Any]]
    connections: Dict[str, Any]

class N8nClient:
    """
    Asynchronous client for the n8n REST API.
    - Authenticates via 'X-N8N-API-KEY' header.
    - Can be expanded to report, sync, or use the backend AI agent if required.
    Parameters:
      base_url: Base URL to the n8n API. Defaults to env N8N_BASE_URL or "https://n8n.cloud/api/v1".
      api_key: API key. Defaults to env N8N_API_KEY.
      timeout: Optional timeout for HTTP requests in seconds (default 30).
    """
    def __init__(
        self,
        base_url: Optional[str] = None,
        api_key: Optional[str] = None,
        *,
        timeout: Union[int, float] = 30,
    ) -> None:
        env_base = os.getenv("N8N_BASE_URL", "https://n8n.cloud/api/v1")
        env_key = os.getenv("N8N_API_KEY")
        self.base_url: str = (base_url or env_base).rstrip("/")
        self.api_key: Optional[str] = api_key or env_key
        if not self.api_key:
            raise N8nAuthError("N8N_API_KEY is not configured.")
        self._timeout = httpx.Timeout(timeout)
        self._headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "X-N8N-API-KEY": self.api_key,
        }

    def _client(self) -> httpx.AsyncClient:
        """Create a configured AsyncClient instance."""
        return httpx.AsyncClient(base_url=self.base_url, headers=self._headers, timeout=self._timeout)

    @staticmethod
    def _raise_for_status(resp: httpx.Response) -> None:
        """Raise a detailed error for non-2xx responses."""
        if 200 <= resp.status_code < 300:
            return
        try:
            payload = resp.json()
        except Exception:
            payload = {"text": resp.text}
        message = payload.get("message") if isinstance(payload, dict) else None
        raise N8nAPIResponseError(resp.status_code, message or "Request failed", url=str(resp.request.url) if resp.request else None, details=payload)

    # --- LISTAR WORKFLOWS ---
    async def list_workflows(self) -> List[Workflow]:
        """Retrieve all workflows available in the n8n instance."""
        async with self._client() as client:
            resp = await client.get("/workflows")
            self._raise_for_status(resp)
            data = resp.json()
            if not isinstance(data, list):
                raise N8nAPIResponseError(resp.status_code, "Unexpected response format for workflows list", url=str(resp.request.url))
            return data

    # --- DETALLES DE WORKFLOW ---
    async def get_workflow(self, workflow_id: Union[str, int]) -> Workflow:
        """Get details for a specific workflow by ID."""
        async with self._client() as client:
            resp = await client.get(f"/workflows/{workflow_id}")
            self._raise_for_status(resp)
            data = resp.json()
            if not isinstance(data, dict):
                raise N8nAPIResponseError(resp.status_code, "Unexpected response format for workflow", url=str(resp.request.url))
            return data

    # --- EJECUTAR WORKFLOW ---
    async def execute_workflow(self, workflow_id: Union[str, int], data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Trigger execution of a workflow with optional input data."""
        payload = data or {}
        async with self._client() as client:
            resp = await client.post(f"/workflows/{workflow_id}/run", json=payload)
            self._raise_for_status(resp)
            result = resp.json()
            if not isinstance(result, dict):
                raise N8nAPIResponseError(resp.status_code, "Unexpected response format for execution", url=str(resp.request.url))
            # Puedes enviar log/report de ejecución al backend AI si lo necesitas
            await self._report_to_backend({
                "action": "workflow_executed",
                "workflow_id": workflow_id,
                "result": result
            })
            return result

    # --- LISTAR EXECUTIONS ---
    async def get_executions(self, workflow_id: Union[str, int], *, limit: Optional[int] = None, last_id: Optional[str] = None) -> List[Execution]:
        """List executions for a workflow."""
        params: Dict[str, Any] = {}
        if limit is not None:
            params["limit"] = int(limit)
        if last_id is not None:
            params["lastId"] = str(last_id)
        async with self._client() as client:
            resp = await client.get(f"/workflows/{workflow_id}/executions", params=params or None)
            self._raise_for_status(resp)
            data = resp.json()
            # n8n may return {count, results: []} or an array depending on version; normalize
            if isinstance(data, dict) and "results" in data and isinstance(data["results"], list):
                return data["results"]
            if isinstance(data, list):
                return data
            raise N8nAPIResponseError(resp.status_code, "Unexpected response format for executions list", url=str(resp.request.url))

    # --- STATUS DE EJECUCIÓN ---
    async def get_execution_status(self, execution_id: Union[str, int]) -> Execution:
        """Get the status/details for an execution by ID."""
        async with self._client() as client:
            resp = await client.get(f"/executions/{execution_id}")
            self._raise_for_status(resp)
            data = resp.json()
            if not isinstance(data, dict):
                raise N8nAPIResponseError(resp.status_code, "Unexpected response format for execution status", url=str(resp.request.url))
            return data

    # --- ACTIVAR WORKFLOW ---
    async def activate_workflow(self, workflow_id: Union[str, int]) -> Workflow:
        """Activate a workflow so that triggers and schedules run automatically."""
        async with self._client() as client:
            resp = await client.post(f"/workflows/{workflow_id}/activate")
            self._raise_for_status(resp)
            data = resp.json()
            if not isinstance(data, dict):
                raise N8nAPIResponseError(resp.status_code, "Unexpected response format for activate", url=str(resp.request.url))
            # Si quieres, reporta activaciones al backend
            await self._report_to_backend({
                "action": "workflow_activated",
                "workflow_id": workflow_id,
                "data": data
            })
            return data

    # --- DESACTIVAR WORKFLOW ---
    async def deactivate_workflow(self, workflow_id: Union[str, int]) -> Workflow:
        """Deactivate a workflow to stop automatic triggers and schedules."""
        async with self._client() as client:
            resp = await client.post(f"/workflows/{workflow_id}/deactivate")
            self._raise_for_status(resp)
            data = resp.json()
            if not isinstance(data, dict):
                raise N8nAPIResponseError(resp.status_code, "Unexpected response format for deactivate", url=str(resp.request.url))
            await self._report_to_backend({
                "action": "workflow_deactivated",
                "workflow_id": workflow_id,
                "data": data
            })
            return data

    # --- REPORTAR AL BACKEND AI AGENT ---
    async def _report_to_backend(self, payload: Dict[str, Any]) -> None:
        """Opcional: Reporta log/resultados al backend central para monitoreo, analítica o triggers AI."""
        try:
            async with httpx.AsyncClient(timeout=20) as client:
                await client.post(f"{AI_AGENT_BACKEND}/api/n8n-events", json=payload)
        except Exception:
            # No falles nunca por logging externo
            pass

__all__ = [
    "N8nClient",
    "N8nClientError",
    "N8nAuthError",
    "N8nAPIResponseError",
    "Execution",
    "Workflow",
]
