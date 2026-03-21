from textual.app import App
from textual.message import Message
from textual_plotext import PlotextPlot

from api import get_player


class GetPlayer(PlotextPlot):
    class Loaded(Message):
        def __init__(self, player):
            self.player = player
            super().__init__()

    async def load(self, player_name):
        player = await get_player(player_name)
        self.post_message(self.Loaded(player))


class RunescapeApp(App):
    CSS = """
    GetPlayer {
        padding: 4 0 0 0
    }
    """
    def compose(self):
        yield GetPlayer()

    def on_mount(self):
        self.run_worker(self.query_one(PlotextPlot).load('Salvsis2'))

    def on_get_player_loaded(self, message):
        self.notify('received player loaded message')

        skills = message.player.skills
        plot_widget = self.query_one(GetPlayer)
        plt = plot_widget.plt
        plt.clear_data()
        plt.clear_figure()
        plt.bar(skills.names[::-1],
                skills.levels[::-1],
                orientation='horizontal',
                width=0.01)
        plt.xlim(0, 99)
        plt.title('Player Levels')
        plot_widget.refresh()
