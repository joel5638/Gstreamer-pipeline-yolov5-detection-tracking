"""
File : infernce.py
Description : Class is responsible for custom exception handling
Created on : 
Author :
E-mail :

"""

from src.common.gstreamer_decoder import VideoProcessing
from src.constant.project_constant import Constant as constant
from src.common.config_manager import cfg
from src.utils.logger import Logger
from src.constant.global_data import GlobalData


if __name__ == "__main__":
    try:
        stream = 'person.mp4'
        processor = VideoProcessing(stream)
        processor.run()
        GlobalData.gst_main_thread.join()
    except Exception as e:
        print("Exception:", e)

        