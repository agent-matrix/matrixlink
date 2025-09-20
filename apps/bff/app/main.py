import json, datetime, os
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from .db import Base, engine, SessionLocal
from .models import Agent, Run
from .auth import require_auth
from .observability import setup_logging, RequestIdMiddleware
from .clients import mcp, agents as agent_client

setup_logging()
app = FastAPI(title="MatrixHub Front Door (BFF)", version="1.0.0")
app.add_middleware(RequestIdMiddleware)
Base.metadata.create_all(bind=engine)

class ToolIn(BaseModel):
    name: str
    description: str | None = None
    url: str
    request_type: str = "SSE"
    integration_type: str = "MCP"

class ServerIn(BaseModel):
    name: str
    description: str | None = None
    associated_tools: list[str] = []
    associated_resources: list[str] = []
    associated_prompts: list[str] = []

class AgentIn(BaseModel):
    name: str
    type: str = "app"
    image: str = ""
    tenant_id: str = "default"

class BindIn(BaseModel):
    server_id: str

class RunIn(BaseModel):
    task: str | None = None
    input: dict = {}
    options: dict = {}

@app.get("/api/health")
def api_health():
    return {"ok": True, "component": "bff"}

@app.get("/api/ready")
def api_ready():
    return {"ready": True, "mcp": mcp.health()}

# MCP proxy (admin plane)
@app.get("/api/mcp/servers", dependencies=[Depends(require_auth)])
def api_mcp_servers():
    return mcp.list_servers()

@app.get("/api/mcp/tools", dependencies=[Depends(require_auth)])
def api_mcp_tools():
    return mcp.list_tools()

@app.post("/api/mcp/servers", dependencies=[Depends(require_auth)])
def api_mcp_create_server(body: ServerIn):
    return mcp.create_server(body.model_dump())

@app.get("/healthz")
def healthz():
    return {"ok": True}

# Agents CRUD-ish
@app.get("/api/admin/agents", dependencies=[Depends(require_auth)])
def list_agents():
    with SessionLocal() as db:
        rows = db.execute(select(Agent)).scalars().all()
        return [
            dict(id=a.id, name=a.name, type=a.type, image=a.image, catalog_url=a.catalog_url, tenant_id=a.tenant_id)
            for a in rows
        ]

@app.post("/api/admin/agents", dependencies=[Depends(require_auth)])
def create_agent(body: AgentIn):
    with SessionLocal() as db:
        a = Agent(name=body.name, type=body.type, image=body.image, tenant_id=body.tenant_id)
        db.add(a); db.commit(); db.refresh(a)
        return dict(id=a.id, name=a.name, type=a.type, image=a.image, tenant_id=a.tenant_id)

@app.post("/api/admin/agents/{agent_id}/bind", dependencies=[Depends(require_auth)])
def bind_agent(agent_id: str, body: BindIn):
    catalog = mcp.assert_server(body.server_id)
    with SessionLocal() as db:
        a = db.get(Agent, agent_id)
        if not a: raise HTTPException(404, "Agent not found")
        a.catalog_url = catalog
        db.commit()
        return {"id": a.id, "catalog_url": a.catalog_url}

@app.post("/api/admin/agents/{agent_id}/run", dependencies=[Depends(require_auth)])
def run_agent(agent_id: str, body: RunIn):
    with SessionLocal() as db:
        a = db.get(Agent, agent_id)
        if not a: raise HTTPException(404, "Agent not found")
        if not a.catalog_url: raise HTTPException(400, "Agent not bound to server")
        run = Run(agent_id=a.id, status="running", request_json=json.dumps(body.model_dump()))
        db.add(run); db.commit(); db.refresh(run)
        url = agent_client.agent_invoke_url(a.name)
        payload = {"task": body.task or "default", "input": body.input, "context": {"catalog_url": a.catalog_url}, "options": body.options or {}}
        try:
            result = agent_client.call_agent_http(url, payload)
            run.status = result.get("status", "succeeded")
            run.result_json = json.dumps(result)
        except Exception as e:
            run.status = "failed"
            run.result_json = json.dumps({"status":"failed","error":{"code":"AGENT_INVOCATION_ERROR", "message":str(e)}})
        finally:
            run.finished_at = datetime.datetime.utcnow()
            db.commit()
        return {"run_id": run.id, **json.loads(run.result_json or "{}")}
