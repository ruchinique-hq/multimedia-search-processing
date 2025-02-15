import os
import subprocess

from transformers.content_transformer import ContentTransformer

from services.amazon_service import AmazonService

from logger import logger

class VideoTransformer(ContentTransformer):
    def __init__(self, amazon_service: AmazonService):  
        super().__init__(amazon_service)

    def transform(self, key: str, s3_content):

        current_directory = os.getcwd()
        file_path = current_directory + "/temp.mp4"

        with open(file_path, 'wb') as f:
            f.write(s3_content['Body'].read())

        frames_path = current_directory + "/frames"
        self.video_to_frames(file_path, frames_path)

        self.amazon_service.upload_directory_to_s3(frames_path, key)
    
    def video_to_frames(self, video_path, output_path):
        try:

            logger.debug(f"converting video {video_path} into frames")

            os.makedirs(output_path, exist_ok=True)

            command = [
                'ffmpeg',
                '-i', video_path,  # input video file
                '-q:v', '2',  # quality of the output frames (lower is better quality, 2 is a good balance)
                '-start_number', str(0),  # start numbering from
                os.path.join(output_path, '%05d.jpg')  # output path with filename pattern for frames
            ]

            subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            logger.info(f"video converted to frames successfully {output_path}")

        except Exception as e:
            logger.error(f'failed to convert to frames {video_path} {e.__str__()}')


