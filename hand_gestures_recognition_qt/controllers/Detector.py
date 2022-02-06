from PyQt5.QtCore import QObject
import numpy as np
from hand_gestures_recognition.mediapipe.MPGestureRecognition import MPGestureRecognition
from multiprocessing import Process, Queue


def recognition_process(queue: Queue):
    recognition = MPGestureRecognition()
    alive = True

    while alive:
        if not queue.empty():
            msg = queue.get()





class Detector(QObject):
    def __init__(self):
        super().__init__()
        self._recognition = MPGestureRecognition()
        self._available = True
        self._process = Process(target=self._recognition_loop)
        self._process.start()

    def recogniseImage(self, img: np.ndarray):
        if self._available:
            self._available = False
            rec = self._recognizeImage(img)
            self._available = True
            return rec

        return None


    def _recognizeImage(self, img: np.ndarray):
        rec = self._recognition.recognize(img, get_image_output=False)

        if rec:
            rec_dict = rec
            rec_dict = {lab: prob for lab, prob in rec_dict.items() if prob > 0.4}
            if rec_dict:
                lab = max(rec_dict, key=rec_dict.get)
                return lab

        return None

    def available(self):
        return self._available

    def flush(self):
        pass


from PyQt5 import QtCore

# Runner lives on the runner thread


class Runner(QtCore.QObject):
    """
    Runs a job in a separate process and forwards messages from the job to the
    main thread through a pyqtSignal.

    """

    msg_from_job = QtCore.pyqtSignal(object)

    def __init__(self, start_signal):
        """
        :param start_signal: the pyqtSignal that starts the job

        """
        super(Runner, self).__init__()
        self.job_input = None
        start_signal.connect(self._run)

    def _run(self):
        queue = Queue()
        p = Process(target=job_function, args=(queue, self.job_input))
        p.start()
        while True:
            msg = queue.get()
            self.msg_from_job.emit(msg)
            if msg == 'done':
                break


# Things below live on the main thread

def run_job(input):
    """ Call this to start a new job """
    runner.job_input = input
    runner_thread.start()


def handle_msg(msg):
    print(msg)
    if msg == 'done':
        runner_thread.quit()
        runner_thread.wait()


# Setup the OQ listener thread and move the OQ runner object to it
runner_thread = QtCore.QThread()
runner = Runner(start_signal=runner_thread.started)
runner.msg_from_job.connect(handle_msg)
runner.moveToThread(runner_thread)

