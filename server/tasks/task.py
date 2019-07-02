class Task:
    def __init__(self, **kwargs):
        for field in ('id', 'name', 'status'):
            setattr(self, field, kwargs.get(field, None))