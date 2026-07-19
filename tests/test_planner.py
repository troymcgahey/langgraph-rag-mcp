import json
from unittest.mock import Mock, patch

import pytest

from rag_mcp_agent.graph import plan_route, choose_route


@pytest.mark.parametrize(
    ("question", "planner_output", "expected"),
    [
        (
            "What travel tip do you have for Paris?",
            {
                "use_rag": False,
                "use_mcp": True,
                "destination": "paris",
                "reason": "A travel tip requires the MCP tool.",
            },
            {
                "use_rag": False,
                "use_mcp": True,
                "destination": "paris",
            },
        ),
        (
            "Use my documents and give me advice for visiting Pompeii.",
            {
                "use_rag": True,
                "use_mcp": True,
                "destination": "naples",
                "reason": "This needs documents and a travel tip.",
            },
            {
                "use_rag": True,
                "use_mcp": True,
                "destination": "naples",
            },
        ),
        # TODO: Add the Naples RAG-only case.
        # TODO: Add the Rome MCP-only case.
    ],
)
@patch("rag_mcp_agent.graph.ChatOllama")
def test_plan_route(
    mock_chat_ollama,
    question,
    planner_output,
    expected,
):
    mock_llm = Mock()
    mock_llm.invoke.return_value.content = json.dumps(planner_output)
    mock_chat_ollama.return_value = mock_llm

    state = {
        "question": question,
        "documents": [],
        "mcp_result": "",
        "answer": "",
        "use_rag": False,
        "use_mcp": False,
        "route": "",
        "plan_reason": "",
        "destination": "",
    }

    result = plan_route(state)

    assert result["use_rag"] is expected["use_rag"]
    assert result["use_mcp"] is expected["use_mcp"]
    assert result["destination"] == expected["destination"]
    assert result["plan_reason"]

@pytest.mark.parametrize(
    ("use_rag", "use_mcp", "expected_route"),
    [
        (True, False, "rag"),
        (False, True, "mcp"),
        (True, True, "both"),
        (False, False, "rag"),
    ],
)
def test_choose_route(use_rag, use_mcp, expected_route):
    state = {
        "use_rag": use_rag,
        "use_mcp": use_mcp,
    }

    assert choose_route(state) == expected_route
