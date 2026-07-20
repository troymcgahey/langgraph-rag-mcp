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
        (
            "Use my documents for travel information for Rome.",
            {
                "use_rag": True,
                "use_mcp": False,
                "destination": "rome",
                "reason": "This needs documents",
            },
            {
                "use_rag": True,
                "use_mcp": False,
                "destination": "rome",
            },
        ),
        (
            "What travel tip do you have for Rome?",
            {
                "use_rag": False,
                "use_mcp": True,
                "destination": "rome",
                "reason": "A travel tip requires an mcp tool",
            },
            {
                "use_rag": False,
                "use_mcp": True,
                "destination": "rome"
            },
        )
    ],
)
@patch("rag_mcp_agent.graph.ChatOllama")
def test_plan_route_parses_llm_decision(
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

@patch("rag_mcp_agent.graph.ChatOllama")
def test_plan_route_defaults_to_rag_when_llm_returns_invalid_json(
    mock_chat_ollama,
):
    mock_llm = Mock()
    mock_llm.invoke.return_value.content = "This is not valid JSON"
    mock_chat_ollama.return_value = mock_llm

    state = {
        "question": "Tell me about Naples",
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

    assert result["use_rag"] is  True
    assert result["use_mcp"] is False
    assert result["destination"] == ""
    assert "invalid json" in result["plan_reason"].lower()
