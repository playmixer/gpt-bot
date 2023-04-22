import replicate


class Replicate:

    def __init__(self, api_token=''):
        rep = replicate.Client(api_token=api_token)
        model = rep.models.get("stability-ai/stable-diffusion")
        self.version = model.versions.get("db21e45d3f7023abc2a46ee38a23973f6dce16bb082a930b0c49861f96d1e5bf")

    def paint(self, prompt: str) -> str:
        return self.version.predict(prompt=prompt)[0]
