from dependency_injector.wiring import Provide

from services.amazon_service import AmazonService

from containers import Container
from logger import logger


class MultimodalSearchProcessing:
    def __init__(self, processing_queue: str, amazon_service: AmazonService):
        self.processing_queue = processing_queue
        self.amazon_service = amazon_service

    def run(self):
        queue = self.amazon_service.get_queue_by_name(self.processing_queue)

        while True:
            messages = self.amazon_service.receive_message(queue['QueueUrl'])
            for message in messages:
                self.process_message(queue, message)

    def process_message(self, queue, message):
        try:
            logger.debug(f"processing message {message['MessageId']}")

            body = message['Body']

            logger.info(f"{body}")
        except Exception as err:
            logger.error(f"failed to process message {message['MessageId']} {err.__str__()}")
        finally:
            self.amazon_service.delete_message(queue['QueueUrl'], message['ReceiptHandle'])


if __name__ == '__main__':
    container = Container()
    container.init_resources()
    container.wire(modules=[__name__])

    queue_name = container.config.aws.queue_name
    amazon_service = container.amazon_service()

    worker = MultimodalSearchProcessing(queue_name, amazon_service)
    worker.run()

