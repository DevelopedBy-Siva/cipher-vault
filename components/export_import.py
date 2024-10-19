from components.top_level import TopLevel


class ExportImport(TopLevel):

    __KEY = "export-import"

    def __init__(self, parent) -> None:
        super().__init__(parent, key=self.__KEY)
