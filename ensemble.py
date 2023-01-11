import mdllearn

class Ensemble:

    def __init__(self, models):
        self.models = models

    def get_preferred_extension(self, instance):
        best_s = None
        best_i = None
        for m in self.models:
            i = m.get_preferred_extension(instance)
            s = mdllearn.get_data_MDL_one_instance(m, i)
            if best_s is None or s < best_s:
                best_s = s
                best_i = i
        return best_i

