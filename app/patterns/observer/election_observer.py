"""
Design Pattern #5: Observer Pattern
─────────────────────────────────────
When an Election's status changes (upcoming → active → completed) the
ElectionEventManager notifies every registered listener automatically.

Participants
------------
* ElectionEvent        – data class carrying event payload
* ElectionObserver     – abstract base; concrete observers implement `update()`
* ElectionEventManager – subject that maintains the observer list and fires events

Concrete observers supplied here
---------------------------------
* LoggingObserver   – logs the event to stdout (swap for proper logging later)
* AuditObserver     – appends a row to an in-memory audit trail (demo only)

In production you would also add an EmailNotificationObserver,
a WebSocketBroadcastObserver, etc.
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import List, Dict


# ── Event ──────────────────────────────────────────────────────────────────

@dataclass
class ElectionEvent:
    election_id: int
    election_name: str
    old_status: str
    new_status: str
    occurred_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )


# ── Abstract Observer ──────────────────────────────────────────────────────

class ElectionObserver(ABC):
    @abstractmethod
    def update(self, event: ElectionEvent) -> None: ...


# ── Concrete Observers ─────────────────────────────────────────────────────

class LoggingObserver(ElectionObserver):
    """Prints a human-readable log line for every status change."""

    def update(self, event: ElectionEvent) -> None:
        print(
            f"[ELECTION LOG] {event.occurred_at} | "
            f"Election '{event.election_name}' (id={event.election_id}) "
            f"changed status: {event.old_status!r} → {event.new_status!r}"
        )


class AuditObserver(ElectionObserver):
    """Maintains an in-memory audit trail (replace with DB writes in production)."""

    def __init__(self) -> None:
        self._trail: List[Dict] = []

    def update(self, event: ElectionEvent) -> None:
        self._trail.append({
            "election_id": event.election_id,
            "event": f"status_change:{event.old_status}→{event.new_status}",
            "at": event.occurred_at,
        })

    @property
    def trail(self) -> List[Dict]:
        return list(self._trail)


# ── Event Manager (Subject) ────────────────────────────────────────────────

class ElectionEventManager:
    """
    Singleton-friendly event manager.  Call `get_instance()` to obtain the
    application-wide manager, or create a local instance in tests.
    """

    _instance: "ElectionEventManager | None" = None

    def __init__(self) -> None:
        self._observers: List[ElectionObserver] = []

    # ── Singleton accessor ─────────────────────────────────────────────────
    @classmethod
    def get_instance(cls) -> "ElectionEventManager":
        if cls._instance is None:
            manager = cls()
            manager.subscribe(LoggingObserver())
            manager.subscribe(AuditObserver())
            cls._instance = manager
        return cls._instance

    # ── Observer management ────────────────────────────────────────────────
    def subscribe(self, observer: ElectionObserver) -> None:
        self._observers.append(observer)

    def unsubscribe(self, observer: ElectionObserver) -> None:
        self._observers.remove(observer)

    # ── Notification ───────────────────────────────────────────────────────
    def notify(self, event: ElectionEvent) -> None:
        for observer in self._observers:
            observer.update(event)

    def status_changed(
        self,
        election_id: int,
        election_name: str,
        old_status: str,
        new_status: str,
    ) -> None:
        """Convenience wrapper used by the election service."""
        self.notify(ElectionEvent(election_id, election_name, old_status, new_status))
