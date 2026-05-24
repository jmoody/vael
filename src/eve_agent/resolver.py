"""
Name / ID resolution with ESI fallback.

The Fuzzwork SDE snapshot can lag the live game by many months. When CCP
introduces new items (e.g. Mobile Phase Anchor, new ship variants, new
modules), they exist on the live market and in ESI immediately, but
won't appear in the SDE until the next static publish.

These helpers transparently fall back to ESI when the SDE has no record:
  - resolve_type_id(name_or_id)   -> int | None
  - resolve_type_info(type_id)    -> dict | None  (same shape as sde.get_type)

Use these from async tools instead of calling sde.get_type / search_types
directly when the input might be a newly-added type.
"""

from __future__ import annotations

import logging
from typing import Optional

from eve_agent import sde
from eve_agent.esi_client import ESIClient, ESINotFoundError


log = logging.getLogger(__name__)


# In-process memoization. Name resolution is stable enough that we
# don't need to round-trip ESI more than once per type per session.
_NAME_TO_ID: dict[str, Optional[int]] = {}
_ID_TO_INFO: dict[int, Optional[dict]] = {}


async def resolve_type_id(name_or_id: str | int) -> Optional[int]:
    """
    Return the type ID for a name or numeric ID.

    Resolution order:
      1. Numeric input -> int passthrough.
      2. SDE search (case-insensitive, prefers exact match).
      3. ESI POST /universe/ids/ fallback.
    """
    if isinstance(name_or_id, int):
        return name_or_id
    s = str(name_or_id).strip()
    if not s:
        return None
    if s.isdigit():
        return int(s)

    key = s.lower()
    if key in _NAME_TO_ID:
        return _NAME_TO_ID[key]

    # Try SDE first
    matches = sde.search_types(s, limit=10)
    if matches:
        # Prefer exact case-insensitive match
        for m in matches:
            if m["name"].lower() == key:
                _NAME_TO_ID[key] = m["type_id"]
                return m["type_id"]
        chosen = matches[0]["type_id"]
        _NAME_TO_ID[key] = chosen
        return chosen

    # SDE miss — fall back to ESI name resolution
    try:
        async with ESIClient() as esi:
            data = await esi.post("/universe/ids/", json=[s])
    except Exception as e:
        log.warning("ESI name resolution failed for %r: %s", s, e)
        _NAME_TO_ID[key] = None
        return None

    type_id: Optional[int] = None
    for entry in (data or {}).get("inventory_types", []) or []:
        if entry.get("name", "").lower() == key:
            type_id = entry.get("id")
            break
    if type_id is None and (data or {}).get("inventory_types"):
        type_id = data["inventory_types"][0].get("id")

    if type_id is not None:
        log.info("Resolved %r -> type_id %d via ESI (not in SDE)", s, type_id)
    _NAME_TO_ID[key] = type_id
    return type_id


async def resolve_type_info(type_id: int) -> Optional[dict]:
    """
    Return type info dict (same keys as sde.get_type) for a type ID.

    Falls back to ESI /universe/types/{id}/ when the SDE has no record.
    The ESI response is mapped to the SDE shape so callers don't care
    where the data came from. category_name / group_name will be filled
    via additional ESI calls when possible.
    """
    if type_id in _ID_TO_INFO:
        return _ID_TO_INFO[type_id]

    # SDE first
    info = sde.get_type(type_id)
    if info is not None:
        _ID_TO_INFO[type_id] = info
        return info

    # ESI fallback
    try:
        async with ESIClient() as esi:
            t = await esi.get(f"/universe/types/{type_id}/", authenticated=False)
            group_id = t.get("group_id")
            group_name: Optional[str] = None
            category_id: Optional[int] = None
            category_name: Optional[str] = None
            if group_id:
                try:
                    g = await esi.get(f"/universe/groups/{group_id}/", authenticated=False)
                    group_name = g.get("name")
                    category_id = g.get("category_id")
                    if category_id:
                        c = await esi.get(
                            f"/universe/categories/{category_id}/",
                            authenticated=False,
                        )
                        category_name = c.get("name")
                except Exception as e:
                    log.debug("Group/category enrichment failed for type %d: %s", type_id, e)
    except ESINotFoundError:
        _ID_TO_INFO[type_id] = None
        return None
    except Exception as e:
        log.warning("ESI type lookup failed for %d: %s", type_id, e)
        _ID_TO_INFO[type_id] = None
        return None

    info = {
        "type_id": t.get("type_id", type_id),
        "name": t.get("name"),
        "description": t.get("description"),
        "group_id": group_id,
        "group_name": group_name,
        "category_id": category_id,
        "category_name": category_name,
        "mass": t.get("mass"),
        "volume": t.get("volume"),
        "capacity": t.get("capacity"),
        "published": 1 if t.get("published") else 0,
    }
    log.info("Resolved type_id %d -> %r via ESI (not in SDE)", type_id, info["name"])
    _ID_TO_INFO[type_id] = info
    return info


async def resolve_type_name(type_id: int) -> str:
    """Best-effort name for a type id, with ESI fallback."""
    info = await resolve_type_info(type_id)
    return info["name"] if info and info.get("name") else f"Unknown type ({type_id})"
