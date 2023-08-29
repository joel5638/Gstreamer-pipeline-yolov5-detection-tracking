"""
File : gstreamer_decoder.py
Description : Class is responsible to Gstreamer Pipline and Processe frame decoding.
Created on : 
Author :
E-mail :

"""
from src.common.inference import Watcher
from src.constant.global_data import GlobalData
from src.exception.base_exception import GstreamerDecoderException, PipelineException
from src.constant.project_constant import Constant as constant
from src.common.handling_metadata import MetaDataHandler
import sys
import gi
gi.require_version(constant.GSTREAMER, constant.GST_VERSION)
from gi.repository import Gst, GLib
from threading import Thread
import time

import cv2
import numpy as np

##waowza login : - diboje8093@avidapro.com
#pwd: India@12345
# rtsp://9aa6be958977.entrypoint.cloud.wowza.com:1935/app-45260S6Q/ac9b55a0
class VideoProcessing(object):

    def __init__(self, stream) -> None:
        Gst.init()
        self.stream = stream
        self.main_loop = GLib.MainLoop()
        GlobalData.gst_main_thread = Thread(target=self.main_loop.run)
        GlobalData.gst_main_thread.start()
        self.running = True
        self.detections = []
        self.counter = 0
        self.inference = Watcher()

    def _create_pipeline(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        try:
            active_camera = GlobalData.camera_metadata[constant.ACTIVE_CAMERA]
            camera_configs = GlobalData.camera_metadata[constant.CAMERAS]

            active_camera_pipeline = (camera_configs[active_camera][constant.CAMERA_SOURCE])
            self.pipeline = Gst.parse_launch(active_camera_pipeline)
            
            appsink = self.pipeline.get_by_name(constant.GST_SINK)
            appsink.set_property(constant.GST_EMIT_SIGNAL, True)
            appsink.set_property(constant.GST_MAX_BUFFER, 1)
            appsink.connect(constant.GST_NEW_SAMPLE, self.on_new_sample)
            
            self.pipeline.set_state(Gst.State.PLAYING)
            return True
        except Exception as e:
            return False

    def run(self):
        """_summary_
        """
        GlobalData.metadata_handling = MetaDataHandler()
        GlobalData.metadata_handling.read_camera_config()
        
        if self._create_pipeline():
            try:
                while self.running:
                    time.sleep(0.1)
            except KeyboardInterrupt:
                pass
            self.pipeline.set_state(Gst.State.NULL)
            self.main_loop.quit()
            GlobalData.gst_main_thread.join()
        else:
            print('Exception occurred while creating Pipeline')
            self.main_loop.quit()
            GlobalData.gst_main_thread.join()
            

    def stop(self):
        self.running = False

    def on_new_sample(self, appsink):
        """_summary_
        Args:
            appsink (_type_): _description_
        Returns:
            _type_: _description_
        """
        sample = appsink.emit("pull-sample")
        if sample:
            buffer = sample.get_buffer()
            caps = sample.get_caps()
            width = caps.get_structure(0).get_value(constant.FRAME_BUFFER_WIDTH)
            height = caps.get_structure(0).get_value(constant.FRAME_BUFFER_HEIGHT)
            np_array = np.frombuffer(buffer.extract_dup(0, buffer.get_size()), dtype=np.uint8)
            frame = np_array.reshape((height, width, 3))
            
            #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            self.counter +=1
            inference_status = self.inference.frame_processing(frame, self.counter)
            if not inference_status:
                self.stop()
                self.main_loop.quit()
                GlobalData.gst_main_thread.join()
                sys.exit(0)
 
        cv2.destroyAllWindows()         
        return Gst.FlowReturn.OK


