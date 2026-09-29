from dataclasses import dataclass, field
from typing import Any
import uuid

@dataclass
class AgentResult:
    agent: str
    summary: str
    evidence: list[dict[str, Any]] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class RunContext:
    decision_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    trace: list[dict[str, Any]] = field(default_factory=list)
    state: dict[str, Any] = field(default_factory=dict)

    def record(self, agent, action, payload=None):
        self.trace.append({"agent": agent, "action": action, "payload": payload or {}})
