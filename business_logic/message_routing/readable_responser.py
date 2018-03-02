import base.singleton as sn


class ReadableResponser(sn.Singleton):
    def get_readable_response_for_news(self, request, data):

        print(request)
        print(data)
        print(data[0])
        return None #return meaningful string here

    def get_readable_response_for_public_opinion(self, request, data):
        print(request)
        print(data.keys())
        print(data)
        return None