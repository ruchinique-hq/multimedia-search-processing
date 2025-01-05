import os
import subprocess

from services.amazon_service import AmazonService
from services.asset_service import AssetService
from logger import logger

class FileService:
    def __init__(self, amazon_service: AmazonService, asset_service: AssetService):
        self.amazon_service = amazon_service
        self.asset_service = asset_service

    def process(self, key: str):
        try:

            logger.debug(f"processing file {key} to convert into frames")

            current_directory = os.getcwd()
            file_path = current_directory + "/temp.mp4"

            self.amazon_service.download_file(key, file_path)
            logger.info(f"downloaded file into {file_path}")

            frames_path = current_directory + "/frames"
            self.video_to_frames(file_path, frames_path)

            self.amazon_service.upload_directory_to_s3(frames_path, key)
            

        except Exception as err:
            logger.error(f"failed to process file {key} {err.__str__()}")

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

            result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            logger.info(f"video converted to frames successfully {output_path}")

        except Exception as e:
            logger.error(f'failed to convert to frames {video_path} {e.__str__()}')


