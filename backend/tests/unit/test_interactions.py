"""Unit tests for interaction filtering logic."""

from app.models.interaction import InteractionLog
from app.routers.interactions import _filter_by_item_id


def _make_log(id: int, learner_id: int, item_id: int) -> InteractionLog:
    return InteractionLog(id=id, learner_id=learner_id, item_id=item_id, kind="attempt")


def test_filter_returns_all_when_item_id_is_none() -> None:
    interactions = [_make_log(1, 1, 1), _make_log(2, 2, 2)]
    result = _filter_by_item_id(interactions, None)
    assert result == interactions


def test_filter_returns_empty_for_empty_input() -> None:
    result = _filter_by_item_id([], 1)
    assert result == []


def test_filter_returns_interaction_with_matching_ids() -> None:
    interactions = [_make_log(1, 1, 1), _make_log(2, 2, 2)]
    result = _filter_by_item_id(interactions, 1)
    assert len(result) == 1
    assert result[0].id == 1


def test_filter_excludes_interaction_with_different_learner_id():
    """Test that filtering by item_id excludes interactions with different learner_id"""
    # Import the InteractionLog class
    from app.models.interaction import InteractionLog

    # Create test data using proper objects
    interactions = [
        InteractionLog(
            id=1, item_id=1, learner_id=2, rating=5
        ),  # item_id=1, learner_id=2
        InteractionLog(
            id=2, item_id=2, learner_id=1, rating=3
        ),  # item_id=2, learner_id=1
    ]

    # Filter by item_id=1
    result = _filter_by_item_id(interactions, 1)

    # This should fail with AssertionError: assert 0 == 1
    # because the function currently filters by learner_id instead of item_id
    assert len(result) == 1
    assert result[0].item_id == 1


# KEEP - добавляем в test_interactions.py
def test_filter_with_zero_item_id() -> None:
    """Test filtering with item_id=0 (boundary value)."""
    interactions = [
        _make_log(1, 1, 0),
        _make_log(2, 2, 1),
        _make_log(3, 3, 0),
    ]
    result = _filter_by_item_id(interactions, 0)
    assert len(result) == 2
    assert all(log.item_id == 0 for log in result)


def test_filter_with_large_item_id() -> None:
    """Test filtering with a large item_id value (boundary - max 32-bit int)."""
    large_id = 2_147_483_647
    interactions = [
        _make_log(1, 1, large_id),
        _make_log(2, 2, 100),
        _make_log(3, 3, large_id),
    ]
    result = _filter_by_item_id(interactions, large_id)
    assert len(result) == 2
    assert all(log.item_id == large_id for log in result)


def test_filter_multiple_interactions_same_item_different_learners() -> None:
    """Test filtering when multiple interactions share the same item_id."""
    interactions = [
        _make_log(1, 1, 10),
        _make_log(2, 2, 10),
        _make_log(3, 3, 10),
        _make_log(4, 1, 20),
    ]
    result = _filter_by_item_id(interactions, 10)
    assert len(result) == 3
    assert all(log.item_id == 10 for log in result)
