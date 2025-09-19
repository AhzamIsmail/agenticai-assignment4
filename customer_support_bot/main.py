
# customer_support_bot/main.py
from .agents import BotAgent
from .sdk import ModelSettings

def run_demo():
    bot = BotAgent()

    scenarios = [
        ("Tell me about your return policy", {"customer_id": "cust_abc"}),
        ("Check my order", {"order_id": "1001"}),
        ("Check order", {"order_id": "9999"}),
        ("I am very angry", {}),
        ("You are stupid", {}),
    ]

    for text, metadata in scenarios:
        ms = ModelSettings(tool_choice="auto", metadata=metadata)
        print("\nUser:", text)
        print("Bot:", bot.handle(text, ms))

if __name__ == "__main__":
    run_demo()


