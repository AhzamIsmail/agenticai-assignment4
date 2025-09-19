
# tests/test_bot.py
import pytest
from customer_support_bot.agents import BotAgent
from customer_support_bot.sdk import ModelSettings

@pytest.fixture
def bot():
    return BotAgent()

def test_faq_return_policy(bot):
    ms = ModelSettings(metadata={})
    resp = bot.handle("Tell me about return policy", ms)
    assert "return" in resp["message"].lower()

def test_order_found(bot):
    ms = ModelSettings(metadata={"order_id": "1001"})
    resp = bot.handle("Where is my order?", ms)
    assert "1001" in resp["message"]

def test_order_not_found(bot):
    ms = ModelSettings(metadata={"order_id": "9999"})
    resp = bot.handle("Check my order", ms)
    assert "error" in resp

def test_negative_sentiment(bot):
    ms = ModelSettings(metadata={})
    resp = bot.handle("I am very angry", ms)
    assert resp["guardrail"] == "negative"

def test_offensive(bot):
    ms = ModelSettings(metadata={})
    resp = bot.handle("You are stupid", ms)
    assert resp["guardrail"] == "offensive"
