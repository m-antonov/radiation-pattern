from sys import argv, exit

from asyncio import sleep, get_event_loop, all_tasks, ProactorEventLoop, set_event_loop, CancelledError

from PyQt5 import uic
from PyQt5.QtGui import QPalette
from PyQt5.QtWidgets import QMainWindow, QApplication

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from pattern import RadiationPattern


async def _processing(application):
    """ Process all pending events - keep interface alive """
    while True:
        application.processEvents()
        await sleep(0)


class ApplicationUI(QMainWindow):
    """  """
    def __init__(self):
        super(ApplicationUI, self).__init__()
        uic.loadUi('application.ui', self)

        self._loop = get_event_loop()
        self._break = False

        self.sequence_btn.clicked.connect(self._seq_exec)

        self._pattern = RadiationPattern()
        self._pattern.phi = -60

        self._canvas = Canvas(self.plot)
        self.plot_lyt.addWidget(self._canvas)

        self._loop.create_task(self.__update_plot())

    async def __update_plot(self):
        """  """
        self.pattern_box.setTitle(f'Pattern [Φ = {self._pattern.phi}]')
        self._canvas.ax.cla()
        self._canvas.ax.plot(*self._pattern.get_theta_r())
        self._canvas.draw()

    async def __seq_exec(self):
        """  """
        for value in range(int(self.min.text()), int(self.max.text()) + 1):
            if self._break:
                return
            self._pattern.phi = value
            await self.__update_plot()
            await sleep(0.05)

        self._seq_break()

    def _seq_exec(self):
        """  """
        self._break = False

        self.sequence_btn.disconnect()
        self.sequence_btn.clicked.connect(self._seq_break)
        self.sequence_btn.setText('Break')

        self.min.setEnabled(False)
        self.max.setEnabled(False)

        self._loop.create_task(self.__seq_exec())

    def _seq_break(self):
        """  """
        self._break = True

        self.sequence_btn.disconnect()
        self.sequence_btn.clicked.connect(self._seq_exec)
        self.sequence_btn.setText('Sequence')

        self.min.setEnabled(True)
        self.max.setEnabled(True)

    def closeEvent(self, *args, **kwargs):
        """ Application main window close action """
        for queue in all_tasks():
            queue.cancel()


class Canvas(FigureCanvas):
    """  """
    def __init__(self, parent):
        fig = Figure()
        fig.patch.set_facecolor(parent.palette().color(QPalette.Background).name())

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        self.ax = self.figure.add_subplot(111, projection='polar')


if __name__ == '__main__':
    _application = QApplication(argv)

    _loop = ProactorEventLoop()
    set_event_loop(_loop)

    _ui = ApplicationUI()
    _ui.show()

    try:
        _loop.run_until_complete(_processing(_application))
    except CancelledError:
        exit(0)
