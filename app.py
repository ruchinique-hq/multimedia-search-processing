from containers import Container
from logger import logger


class MultimodalSearchProcessing:

    def __int__(self):
        pass

    def run(self):
        print('')

if __name__ == '__main__':
    container = Container()
    container.init_resources()
    container.wire(modules=[__name__])

    worker = MultimodalSearchProcessing()
    worker.run()

