# # customer_support_bot/agents.py
# from .sdk import guardrail, ModelSettings, FUNCTION_REGISTRY
# from .tools import get_order_status
# from .logging_utils import log


# class Agent:
#     def __init__(self, name: str):
#         self.name = name
#     def handle(self, query: str, model_settings: ModelSettings):
#         raise NotImplementedError


# class HumanAgent(Agent):
#      def __init__(self):
#         super().__init__("HumanAgent")
#      def handle(self, query: str, model_settings: ModelSettings):
#          return {"agent": self.name, "message": "Human agent will assist you shortly."}


# class BotAgent(Agent):
#     def __init__(self):
#        super().__init__("BotAgent")
#        self.human = HumanAgent()


# @guardrail
# def handle(self, query: str, model_settings: ModelSettings):
#     q = query.lower()
#     if "return policy" in q:
#         return {"agent": self.name, "message": "You can return within 30 days."}


#     if "shipping" in q:
#        return {"agent": self.name, "message": "We offer standard and express shipping."}

# tool = FUNCTION_REGISTRY.get("get_order_status")
# if tool and (not tool["is_enabled"] or tool["is_enabled"](query, model_settings.metadata)):
#     order_id = model_settings.metadata.get("order_id")
#     if order_id:
#        result = get_order_status(order_id=order_id)
#        if "error" in result:
#            return result
#         return {"agent": self.name, "message": f"Order {order_id} is {result['status']} (ETA: {result['eta']})."}
#     return {"agent": self.name, "message": "Please provide your order ID."}


#  


# customer_support_bot/agents.py
from .sdk import guardrail, ModelSettings, FUNCTION_REGISTRY
from .tools import get_order_status

class Agent:
    def __init__(self, name: str):
        self.name = name
    def handle(self, query: str, model_settings: ModelSettings):
        raise NotImplementedError

class HumanAgent(Agent):
    def __init__(self):
        super().__init__("HumanAgent")
    def handle(self, query: str, model_settings: ModelSettings):
        return {"agent": self.name, "message": "Human agent will assist you shortly."}

class BotAgent(Agent):
    def __init__(self):
        super().__init__("BotAgent")
        self.human = HumanAgent()

    @guardrail
    def handle(self, query: str, model_settings: ModelSettings):
        q = query.lower()

        if "return policy" in q:
            return {"agent": self.name, "message": "You can return within 30 days."}

        if "shipping" in q:
            return {"agent": self.name, "message": "We offer standard and express shipping."}

        tool = FUNCTION_REGISTRY.get("get_order_status")
        if tool and (not tool["is_enabled"] or tool["is_enabled"](query, model_settings.metadata)):
            order_id = model_settings.metadata.get("order_id")
            if order_id:
                result = get_order_status(order_id=order_id)
                if "error" in result:
                    return result
                return {"agent": self.name, "message": f"Order {order_id} is {result['status']} (ETA: {result['eta']})."}
            return {"agent": self.name, "message": "Please provide your order ID."}

        return self.human.handle(query, model_settings)


