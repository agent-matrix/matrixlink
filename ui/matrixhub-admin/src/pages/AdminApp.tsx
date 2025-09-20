import React, { useEffect, useState } from "react";

async function api(base: string, path: string, init: RequestInit, auth?: string) {
    const headers: Record<string, string> = { "Content-Type": "application/json", ...(init.headers as any || {}) };
    if (auth) headers["Authorization"] = auth;
    const url = new URL(path.replace(/^\//, ""), base).toString();
    const res = await fetch(url, { ...init, headers });
    if (!res.ok) {
        throw new Error(`${res.status} ${res.statusText}: ${await res.text()}`);
    }
    return res.json();
}

const LS = "matrixhub-admin";
function useCfg() {
    const [cfg, setCfg] = useState<any>(() => {
        try { return JSON.parse(localStorage.getItem(LS) || 'null'); } catch { return null; }
    });
    useEffect(() => {
        if (!cfg) {
            setCfg({ base: "http://localhost:8080/api/", auth: "Bearer changeme-admin-bearer-token" });
        }
    }, [cfg]);
    useEffect(() => {
        if (cfg) {
            localStorage.setItem(LS, JSON.stringify(cfg));
        }
    }, [cfg]);
    return [cfg || { base: "http://localhost:8080/api/", auth: "" }, setCfg] as const;
}

type Agent = { id: string; name: string; type: string; catalog_url?: string };
type ServerDef = { id: string; name: string; description?: string };
type Tool = { id: string; name: string; description?: string };

export default function AdminApp() {
    const [cfg, setCfg] = useCfg();
    const [agents, setAgents] = useState<Agent[]>([]);
    const [servers, setServers] = useState<ServerDef[]>([]);
    const [tools, setTools] = useState<Tool[]>([]);
    const base = cfg.base.endsWith('/') ? cfg.base : cfg.base + '/';

    async function refresh() {
        const [a, s, t] = await Promise.all([
            api(base, "admin/agents", { method: "GET" }, cfg.auth),
            api(base, "mcp/servers", { method: "GET" }, cfg.auth),
            api(base, "mcp/tools", { method: "GET" }, cfg.auth),
        ]);
        setAgents(a); setServers(s); setTools(t);
    }

    useEffect(() => { refresh().catch(console.error); }, [cfg.base, cfg.auth]);

    return (
        <div style={{ padding: 24, fontFamily: "Inter, system-ui, sans-serif" }}>
            <header style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 16 }}>
                <h2 style={{ margin: 0 }}>MatrixHub Admin</h2>
                <button onClick={() => refresh()}>Refresh</button>
            </header>

            <section style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 16 }}>
                <div style={{ border: "1px solid #ddd", borderRadius: 12, padding: 16 }}>
                    <h3>Servers</h3>
                    {servers.length === 0 ? <div>No servers.</div> : servers.map(s => (
                        <div key={s.id} style={{ padding: 8, borderBottom: "1px solid #eee" }}>
                            <div style={{ fontWeight: 600 }}>{s.name}</div>
                            <div style={{ fontSize: 12, color: "#666" }}>{s.description || "—"}</div>
                        </div>
                    ))}
                </div>
                <div style={{ border: "1px solid #ddd", borderRadius: 12, padding: 16 }}>
                    <h3>Agents</h3>
                    {agents.length === 0 ? <div>No agents.</div> : agents.map(a => (
                        <div key={a.id} style={{ padding: 8, borderBottom: "1px solid #eee" }}>
                            <div style={{ fontWeight: 600 }}>{a.name}</div>
                            <div style={{ fontSize: 12, color: "#666" }}>{a.type}</div>
                            <div style={{ fontSize: 12, color: "#666", wordBreak: 'break-all' }}>Catalog: {a.catalog_url || "—"}</div>
                        </div>
                    ))}
                </div>
            </section>

            <section style={{ marginTop: 16, border: "1px solid #ddd", borderRadius: 12, padding: 16 }}>
                <h3>Settings</h3>
                <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 12 }}>
                    <label>
                        Base URL
                        <input style={{ width: "100%", boxSizing: 'border-box' }} value={cfg.base} onChange={e => setCfg((c: any) => ({ ...c, base: e.target.value }))} />
                    </label>
                    <label>
                        Authorization
                        <input style={{ width: "100%", boxSizing: 'border-box' }} value={cfg.auth} onChange={e => setCfg((c: any) => ({ ...c, auth: e.target.value }))} placeholder="Bearer <token>" />
                    </label>
                </div>
            </section>

            <footer style={{ marginTop: 24, fontSize: 12, color: "#666" }}>MatrixHub • MCP Gateway + A2A catalog</footer>
        </div>
    );
}
