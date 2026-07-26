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

@pytest.mark.integration
def test_real_planner_routes_naples_to_rag():
    state = {
        "question": "Use my documents to tell me about Naples.",
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

    assert result["use_rag"] is True
    assert result["route"] == "rag"
    assert result["destination"].lower() == "naples"
    assert result["plan_reason"].strip()

@pytest.mark.integration
def test_real_planner_routes_naples_using_rag_and_mcp():
    state = {
        "question": "Use my documents and give me a travel tip for Naples.",
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

    assert result["use_rag"] is True
    assert result["use_mcp"] is True
    assert result["destination"].lower() == "naples"
    assert result["plan_reason"].strip()
