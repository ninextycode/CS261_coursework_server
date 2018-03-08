import base.singleton as sn
import business_logic.message_routing.message_router as message_router
import business_logic.data_processing.my_data as my_data


class Subscriber(sn.Singleton):
    def __init__(self):
        self.my_data = my_data.MyData.get_instance()
        self.check_period_seconds = 60 * 15
        self.message_router: message_router.MessageRouter = message_router.MessageRouter.get_instance()

    def check_all(self):
        subscriptions = self.my_data.get_subscribtions()
        for sub in subscriptions:
            self.check_one(sub)

    def check_one(self, subscriptions):
        data = self.message_router.response_to_formal_request(subscriptions["request"])
        