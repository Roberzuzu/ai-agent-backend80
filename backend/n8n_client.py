"""
Async n8n API client for managing and executing workflows.

- Uses environment variables:
  - N8N_BASE_URL: Base URL to the n8n API (default: https://n8n.cloud/api/v1)
  - N8N_API_KEY: API key for authentication

All methods are asynchronous and use httpx.AsyncClient under the hood.
"""
from __future__ import annotations

import os
from typing import Any, Dict, List, Optional, TypedDict, Union

import httpx


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
    """Asynchronous client for the n8n REST API.

    This client authenticates using an API key via the header `X-N8N-API-KEY`.

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

    async def list_workflows(self) -> List[Workflow]:
        """Retrieve all workflows available in the n8n instance.

        Returns:
            A list of workflow metadata dictionaries.
        """
        async with self._client() as client:
            resp = await client.get("/workflows")
            self._raise_for_status(resp)
            data = resp.json()
            if not isinstance(data, list):
                raise N8nAPIResponseError(resp.status_code, "Unexpected response format for workflows list", url=str(resp.request.url))
            return data  # type: ignore[return-value]

    async def get_workflow(self, workflow_id: Union[str, int]) -> Workflow:
        """Get details for a specific workflow by ID.

        Args:
            workflow_id: The workflow identifier.
        Returns:
            The workflow object.
        """
        async with self._client() as client:
            resp = await client.get(f"/workflows/{workflow_id}")
            self._raise_for_status(resp)
            data = resp.json()
            if not isinstance(data, dict):
                raise N8nAPIResponseError(resp.status_code, "Unexpected response format for workflow", url=str(resp.request.url))
            return data  # type: ignore[return-value]

    async def execute_workflow(self, workflow_id: Union[str, int], data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Trigger execution of a workflow with optional input data.

        Args:
            workflow_id: The workflow identifier.
            data: Optional payload passed to the workflow's start node.
        Returns:
            Execution trigger response containing execution id or result.
        """
        payload = data or {}
        async with self._client() as client:
            resp = await client.post(f"/workflows/{workflow_id}/run", json=payload)
            self._raise_for_status(resp)
            result = resp.json()
            if not isinstance(result, dict):
                raise N8nAPIResponseError(resp.status_code, "Unexpected response format for execution", url=str(resp.request.url))
            return result

    async def get_executions(self, workflow_id: Union[str, int], *, limit: Optional[int] = None, last_id: Optional[str] = None) -> List[Execution]:
        """List executions for a workflow.

        Args:
            workflow_id: The workflow identifier.
            limit: Optional maximum number of executions to return.
            last_id: Optional cursor for pagination.
        Returns:
            A list of execution records.
        """
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
                return data["results"]  # type: ignore[return-value]
            if isinstance(data, list):
                return data  # type: ignore[return-value]
            raise N8nAPIResponseError(resp.status_code, "Unexpected response format for executions list", url=str(resp.request.url))

    async def get_execution_status(self, execution_id: Union[str, int]) -> Execution:
        """Get the status/details for an execution by ID.

        Args:
            execution_id: The execution identifier.
        Returns:
            An execution record with status and metadata.
        """
        async with self._client() as client:
            resp = await client.get(f"/executions/{execution_id}")
            self._raise_for_status(resp)
            data = resp.json()
            if not isinstance(data, dict):
                raise N8nAPIResponseError(resp.status_code, "Unexpected response format for execution status", url=str(resp.request.url))
            return data  # type: ignore[return-value]

    async def activate_workflow(self, workflow_id: Union[str, int]) -> Workflow:
        """Activate a workflow so that triggers and schedules run automatically.

        Args:
            workflow_id: The workflow identifier.
        Returns:
            The updated workflow object reflecting active state.
        """
        async with self._client() as client:
            resp = await client.post(f"/workflows/{workflow_id}/activate")
            self._raise_for_status(resp)
            data = resp.json()
            if not isinstance(data, dict):
                raise N8nAPIResponseError(resp.status_code, "Unexpected response format for activate", url=str(resp.request.url))
            return data  # type: ignore[return-value]

    async def deactivate_workflow(self, workflow_id: Union[str, int]) -> Workflow:
        """Deactivate a workflow to stop automatic triggers and schedules.

        Args:
            workflow_id: The workflow identifier.
        Returns:
            The updated workflow object reflecting inactive state.
        """
        async with self._client() as client:
            resp = await client.post(f"/workflows/{workflow_id}/deactivate")
            self._raise_for_status(resp)
            data = resp.json()
            if not isinstance(data, dict):
                raise N8nAPIResponseError(resp.status_code, "Unexpected response format for deactivate", url=str(resp.request.url))
            return data  # type: ignore[return-value]


__all__ = [
    "N8nClient",
    "N8nClientError",
    "N8nAuthError",
    "N8nAPIResponseError",
    "Execution",
    "Workflow",
]
