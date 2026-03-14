"""
Design Pattern #3: Factory Pattern
────────────────────────────────────
The ElectionFactory centralises the creation of Election model instances.
Callers pass a plain dict (or keyword args) and the factory decides which
"flavour" of Election to build based on the `type` field (federal vs provincial).

Benefits
--------
* Object creation logic is decoupled from the service layer.
* Adding a new election type (e.g., "local") requires a change in ONE place.
* Keeps the service layer thin and readable.
"""

from datetime import datetime
from app.models.election import Election


class ElectionFactory:
    """Creates Election ORM objects; the caller never calls Election() directly."""

    """
    This is a dictionary that defines the valid election types and their default values. Right now all three types share the same default status ("upcoming"), but this is where you'd add type-specific behaviour in the future. For example if federal elections needed extra fields, you'd add them here in one place.
    
    """
    # Registry maps election type → any extra defaults that type needs
    _DEFAULTS: dict = {
        "federal":    {"status": "upcoming"},
        "provincial": {"status": "upcoming"},
        "local":      {"status": "upcoming"},
    }

    @classmethod
    def create(
        cls,
        name: str,
        election_type: str,
        start_date: datetime,
        end_date: datetime,
        status: str = "upcoming",
    ) -> Election:
        """
        Build and return an Election instance without persisting it.
        The service/repository is responsible for adding it to the DB session.
        """
        election_type = election_type.lower()
        if election_type not in cls._DEFAULTS:
            raise ValueError(
                f"Unknown election type '{election_type}'. "
                f"Valid types: {list(cls._DEFAULTS.keys())}"
            )

        defaults = cls._DEFAULTS[election_type].copy()
        # Explicit status overrides the per-type default
        defaults["status"] = status

        return Election(
            name=name,
            type=election_type,
            start_date=start_date,
            end_date=end_date,
            **defaults,
        )
