from horizon_fastapi_template.utils import BaseAPI

class TykApi:
    def __init__(
            self,
            api: BaseAPI,
            base_uri: str = "/api",
    ):
        self.api = api
        self.base_uri = base_uri
        
class TykDashboardApi(TykApi):
    def __init__(self, api: BaseAPI, base_uri: str = "/api"):
        super().__init__(api, base_uri=base_uri)

class TykDashboardAdminApi(TykApi):
    def __init__(self, api: BaseAPI, base_uri: str = "/admin"):
        super().__init__(api, base_uri=base_uri)