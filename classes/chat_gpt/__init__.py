import openai
from enum import Enum


class Logger:
    def info(self, text: str):
        pass

    def error(self, text: str):
        pass


class GPTModels(Enum):
    GPT3_5TURBO = 'gpt-3.5-turbo'
    ADA = 'ada'


class ChatGPT:
    ai = None
    user_messages = dict()
    log = None
    MODELS = GPTModels

    def __init__(self, api_key, log: Logger = None):
        self.ai = openai
        self.ai.api_key = api_key
        self.log = log

    def _info(self, text: str):
        if self.log is not None:
            self.log.info(text)
        else:
            print(text)

    def _error(self, text: str):
        if self.log is not None:
            self.log.error(text)
        else:
            print(text)

    def chat(self, model=MODELS.GPT3_5TURBO, *args, **kwargs) -> str:
        if model == self.MODELS.ADA:
            return self.input_ada(*args, **kwargs)
        else:
            return self.input_gpt35turbo(*args, **kwargs)

    def input_gpt35turbo(self, id: int, text: str) -> str:
        if self.user_messages.get(id) is None:
            self.user_messages[id] = list()

        self.user_messages[id].append({"role": "user", "content": text})
        self.user_messages[id] = self.user_messages[id][-20:]

        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=self.user_messages[id],
        )
        self._info(f"completion: {completion}")

        chat_response = completion.choices[0].message.content
        self.user_messages[id].append({"role": "assistant", "content": chat_response})
        return chat_response

    def input_ada(self, id: int, text: str) -> str:

        completion = openai.Completion.create(
            engine="davinci",
            prompt=text,
            max_tokens=100,
            # n=1,
            stop=None,
            temperature=0.5,
        )
        self._info(f"completion: {completion}")

        chat_response = ' '.join(m.text.strip() for m in completion.choices)
        return chat_response
