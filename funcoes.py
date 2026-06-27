class Funcoes:
    def __init__(self, view):
        self.view = view
        self.repo = self.view.controles['var_repo'].get()
        self.version = self.view.controles['var_version'].get()
        self.programa_title = self.view.controles['var_title'].get()

        # O controlador se adapta automaticamente baseando-se em qual janela o chamou
        if hasattr(view, 'nome_janela'):
            if view.nome_janela == "novo-programa":
                self._vincular_janela_principal()

    def _vincular_janela_principal(self):
        pass