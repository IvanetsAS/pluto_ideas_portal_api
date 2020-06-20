import json


class BaseResponse:
    def __init__(self, success, data):
        self.success = success
        self.data = data

    def serialize(self):
        return '{"result": ' + str(self.success).lower() + ', "data": ' + json.dumps(self.data.__dict__, ensure_ascii=False) + '}'
