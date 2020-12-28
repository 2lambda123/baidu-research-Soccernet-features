#  Copyright (c) 2020 PaddlePaddle Authors. All Rights Reserve.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import cv2

from ..registry import PIPELINES
import sys
from reader_utils import DataReader
try:
    import cPickle as pickle
    from cStringIO import StringIO
except ImportError:
    import pickle
    from io import BytesIO
import numpy as np
import random

python_ver = sys.version_info
max_len = 512




@PIPELINES.register()
class VideoDecoder(object):
    """
    Decode mp4 file to frames.
    Args:
        filepath: the file path of mp4 file
    """

    def __init__(self):
        pass

    def __call__(self, results):
        """
        Perform mp4 decode operations.
        return:
            List where each item is a numpy array after decoder.
        """
        #XXX get info from results!!!
        file_path = results['filename']
        cap = cv2.VideoCapture(file_path)
        videolen = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        sampledFrames = []
        for i in range(videolen):
            ret, frame = cap.read()
            # maybe first frame is empty
            if ret == False:
                continue
            img = frame[:, :, ::-1]
            sampledFrames.append(img)
        results['frames'] = sampledFrames
        results['frames_len'] = len(sampledFrames)
        results['format'] = 'video'
        return results

@PIPELINES.register()
class FrameDecoder(object):
    """just parse results
    """
    def __init__(self):
        pass
    def __call__(self, results):
        results['format'] = 'frame'
        return results

@PIPELINES.register()
class FeatureDecoder(object):
    """
        Perform feature decode operations.e.g.youtube8m
    """
    def __init__(self, num_classes, mode):
        self.num_classes = num_classes
        self.mode = mode
    def __call__(self, results):
        """
        Perform feature decode operations.
        return:
            List where each item is a numpy array after decoder.
        """
        #1. load pkl
        #2. parse to rgb/audio/
        #3. padding

        filepath = results['filename']
        data = pickle.load(open(filepath, 'rb'), encoding='bytes')

        record = data
        nframes = record[b'nframes']
        rgb = record[b'feature'].astype(float)
        audio = record[b'audio'].astype(float)
        if self.mode != 'infer':
            label = record[b'label']
            one_hot_label = make_one_hot(label, self.num_classes)
        video = record[b'video']

        rgb = rgb[0:nframes, :]
        audio = audio[0:nframes, :]

        rgb = dequantize(
            rgb,
            max_quantized_value=2.,
            min_quantized_value=-2.)
        audio = dequantize(
            audio,
            max_quantized_value=2,
            min_quantized_value=-2)

        if self.mode != 'infer':
            feature_out = (rgb, audio, one_hot_label)
        else:
            feature_out = (rgb, audio, video)

        feat_pad_list = []
        feat_len_list = []
        mask_list = []
        vitem = [rgb, audio]
        for vi in range(2): #rgb and audio
            feat = vitem[vi]
            feat_len_list.append(feat.shape[0])
            ###feat pad step 1. padding
            feat_add = np.zeros((max_len - feat.shape[0], feat.shape[1]), dtype=np.float32)
            feat_pad = np.concatenate( (feat, feat_add), axis=0 )
            feat_pad_list.append(feat_pad)
            ###feat pad step 2. mask
            feat_mask_origin = np.ones(feat.shape, dtype=np.float32)
            feat_mask_add = feat_add
            feat_mask = np.concatenate( (feat_mask_origin, feat_mask_add), axis=0 )
            mask_list.append(feat_mask)

        return [feat_pad_list[0], feat_pad_list[1],
                       feat_len_list[0], feat_len_list[1],
                       mask_list[0], mask_list[1],
                       feature_out[2]]

    def dequantize(feat_vector, max_quantized_value=2., min_quantized_value=-2.):
        """
        Dequantize the feature from the byte format to the float format
        """
    
        assert max_quantized_value > min_quantized_value
        quantized_range = max_quantized_value - min_quantized_value
        scalar = quantized_range / 255.0
        bias = (quantized_range / 512.0) + min_quantized_value
    
        return feat_vector * scalar + bias
    
    
    def make_one_hot(label, dim=3862):
        one_hot_label = np.zeros(dim)
        one_hot_label = one_hot_label.astype(float)
        for ind in label:
            one_hot_label[int(ind)] = 1
        return one_hot_label
