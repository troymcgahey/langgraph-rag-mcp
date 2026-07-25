import pytest

from rag_mcp_agent.graph import plan_route

@pytest.mark.integration
def test_real_planner_routes_paris_tip_to_mcp():
    state = {
        "question": "What travel tip do you have for Paris?",
        "documents": [],
        "mcp_results": "",
        "answer:" "",
        "use_rag": False,
        "use_mcp": False,
        "route": "",
        "plan_reason": "",
        "destination": "",
    }

    result = plan_route(state)

    # TODO: Assert the following:
    # - MCP is enabled.
    # - The route is "mcp".
    # - The destination is Paris, allowing for capitalization differences.
    # - The planner provides a nonempty reason.
