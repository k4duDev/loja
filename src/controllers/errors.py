from flask.views import MethodView



class NotFoundController(MethodView):
    def get(self, error):
        return f"Pagina não encontrada {error}"