import matplotlib.pyplot as plt

from pymoo.model.callback import Callback


class AnimationCallback(Callback):

    def __init__(self,
                 do_show=False,
                 nth_gen=10,
                 fname=None,
                 dpi=None,
                 video=None,
                 exception_if_not_applicable=True):

        super().__init__()
        self.nth_gen = nth_gen
        self.do_show = do_show
        self.exception_if_not_applicable = exception_if_not_applicable

        self.video = video
        if self.video is None and fname is not None:
            try:
                from pyrecorder.recorders.file import File
                from pyrecorder.video import Video
                from pyrecorder.converters.matplotlib import Matplotlib
            except:
                print("Please install pyrecorder for animation support: pip install pyrecorder")
            self.video = Video(File(fname), converter=Matplotlib(dpi=dpi))

    def notify(self, algorithm):
        if algorithm.n_gen == 1 or algorithm.n_gen % self.nth_gen == 0:
            try:

                self.do(algorithm.problem, algorithm)

                if self.do_show:
                    plt.show()

                if self.video is not None:
                    self.video.record()

            except Exception as ex:
                if self.exception_if_not_applicable:
                    raise ex
