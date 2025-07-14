import types, sys
models = types.ModuleType('models')
models.load_model = lambda *args, **kwargs: None
sys.modules[__name__ + '.models'] = models
