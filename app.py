from textual import on
from textual.app import App
from textual.containers import Horizontal, Vertical
from textual.message import Message
from textual.screen import ModalScreen
from textual.widgets import Button, Label, LoadingIndicator
from textual_plotext import PlotextPlot

from api import get_player


class GetPlayer(ModalScreen):
    def __init__(self, player_name):
        self.player_name = player_name
        super().__init__()

    def compose(self):
        with Vertical():
            yield Label(f'Loading {self.player_name}', id='loading-label')
            yield LoadingIndicator()

    def on_mount(self):
        self.run_worker(self.load(self.player_name))

    class Loaded(Message):
        def __init__(self, player):
            self.player = player
            super().__init__()

    async def load(self, player_name):
        player = await get_player(player_name)
        self.post_message(self.Loaded(player))
        self.app.pop_screen()


class PlayerPlot(PlotextPlot):
    def player_levels(self, skills):
        plt = self.plt
        plt.clear_data()
        plt.clear_figure()
        plt.bar(skills.names[::-1],
                skills.levels[::-1],
                orientation='horizontal',
                width=0.01)
        plt.xlim(0, 99)
        plt.title('Player Levels')

        self.refresh()

    def player_xp(self, skills):
        plt = self.plt
        plt.clear_data()
        plt.clear_figure()
        plt.bar(skills.names[::-1],
                skills.xp[::-1],
                orientation='horizontal',
                width=0.01)
        plt.title('Player XP')

        self.refresh()


class RunescapeApp(App):
    CSS = """
    Horizontal {
        height: 3;
    }

    GetPlayer {
        align: center middle;
    }

    Vertical {
        height: 10;
        width: 40;
        border: thick $background 80%;
        background: $surface;
    }

    #loading-label {
        content-align: center middle;
        width: 1fr;
        height: 3;
    }

    LoadingIndicator {
        padding: 0 0 3 0;
    }
    """
    def compose(self):
        with Horizontal():
            yield Button('Levels', id='show-levels')
            yield Button('Xp', id='show-xp')

        yield PlayerPlot()

    def on_mount(self):
        self.push_screen(GetPlayer('Salvsis2'))

    @on(Button.Pressed, '#show-levels')
    def switch_plot_to_levels(self):
        player_plot = self.query_one(PlayerPlot)
        player_plot.player_levels(self.player.skills)

    @on(Button.Pressed, '#show-xp')
    def switch_plot_to_xp(self):
        player_plot = self.query_one(PlayerPlot)
        player_plot.player_xp(self.player.skills)

    def on_get_player_loaded(self, message):
        self.player = message.player
        skills = self.player.skills
        player_plot = self.query_one(PlayerPlot)
        player_plot.player_levels(skills)
