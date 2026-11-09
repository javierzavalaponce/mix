import pandas as pd
from textual.app import App, ComposeResult
from textual.widgets import DataTable, Footer, Header


class Explorador(App):
    TITLE = "Biblioteca DJ"

    def compose(self) -> ComposeResult:
        yield Header()
        yield DataTable()
        yield Footer()

    def on_mount(self) -> None:
        df = pd.read_csv("biblioteca.csv")
        tabla = self.query_one(DataTable)
        tabla.add_columns(*df.columns)
        for fila in df.itertuples(index=False):
            tabla.add_row(*fila)


if __name__ == "__main__":
    Explorador().run()
