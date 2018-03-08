import base.singleton as sn
import business_logic.message_routing.message_router as message_router
import business_logic.data_processing.my_data as my_data
import business_logic.data_processing.world_data as world_data
import datetime
import business_logic.data_tags as tags


class SubscriptionChecker(sn.Singleton):
    def __init__(self):
        self.my_data = my_data.MyData.get_instance()
        self.check_period_seconds = 60 * 15
        self.single_subscription_period_seconds = 60 * 60
        self.message_router: message_router.MessageRouter = message_router.MessageRouter.get_instance()
        self.world_data: world_data.WorldData = world_data.WorldData.get_instance()
        self.subscriptions = self.my_data.get_subscriptions()
        for sub in self.subscriptions:
            sub["last_time_triggered"] = datetime.datetime.now()

    def check_all(self):
        subscriptions = self.my_data.get_subscribtions()
        for sub in subscriptions:
            self.check_one(sub)

    def check_one(self, sub):
        if sub["type"] == tags.SubType.industry:
            self.check_industry(sub)
        else:
            self.check_stock(sub)

    def check_industry(self, sub):
        ticker = sub["tickers"]
        time_now = datetime.datetime.now()
        last_time_triggered = sub["last_time_triggered"]
        old_price = self.world_data.get_price()

    def check_stock(self, sub):
        pass
