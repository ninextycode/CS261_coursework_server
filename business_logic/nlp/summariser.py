import data_providers.external_apis.textsummarization_net_api as tsz_api
import data_providers.external_apis.summarisation_with_sumy as sumy_api
import base.singleton as sn


class Summariser(sn.Singleton):
    def __init__(self):
        self.sum_apis = [
            # too expensive to run TextsummarizationNetApi (sad)
            # tsz_api.TextsummarizationNetApi.get_instance()
            sumy_api.SummarisationWithSumy.get_instance()
            # potentially add more
        ]
        self.no_summary_response = 'Unfortunately no summary available.'

    def summarise_url(self, url):
        for api in self.sum_apis:
            summary = api.summarise_url(url)
            if summary is not None:
                return summary

        return self.no_summary_response
