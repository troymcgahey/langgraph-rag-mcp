import pytest

from rag_mcp_agent.graph import plan_route

@pytest.mark.integration
def test_real_planner_routes_paris_tip_to_mcp():
    state = {
        "question": "What travel tip do you have for Paris?",
        "documents": [],
        "mcp_results": "",
        "answer": "",
        "use_rag": False,
        "use_mcp": False,
        "route": "",
        "plan_reason": "",
        "destination": "",
    }

    result = plan_route(state)

    assert result["use_mcp"] is True
    assert result["route"] == "mcp"
    assert result["destination"].lower() == "paris"
    assert result["plan_reason"].strip()
