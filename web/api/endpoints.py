class Healthcheck:
    def on_get(self, _, resp):
        resp.media = {"success": True}
