# Copyright (c) 2020  PaddlePaddle Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from .anet_pipeline import GetMatchMap, GetVideoLabel, LoadFeat
from .augmentations import (CenterCrop, ColorJitter, GroupRandomFlip,
                            GroupResize, Image2Array, JitterScale, MultiCrop,
                            Normalization, PackOutput, RandomCrop, RandomFlip,
                            RandomResizedCrop, Scale, TenCrop, ToArray,
                            UniformCrop, RandomGamma, MultiCenterCrop,
                            RandomBrightness, RandomHue, RandomSaturation)
from .augmentations_ava import *
from .compose import Compose
from .decode import FeatureDecoder, FrameDecoder, VideoDecoder, ActionFeatureDecoder
from .decode_image import ImageDecoder
from .decode_sampler import DecodeSampler
from .mix import Cutmix, Mixup, VideoMix
from .multimodal import FeaturePadding, RandomCap, RandomMask, Tokenize
from .sample import Sampler, SamplerPkl, EventSampler
from .sample_one_file import OneFileSampler
from .sample_ava import *
from .segmentation import MultiNorm, MultiRestrictSize
from .skeleton_pipeline import AutoPadding, Iden, SkeletonNorm
from .skeleton_pipeline import SketeonCropSample, SketeonModalityTransform, RandomRotation
from .skeleton_pipeline import (UniformSampleFrames, PoseDecode, PoseCompact,
                                RandomResizedCrop_V2, Flip_V2, CenterCrop_V2,
                                GeneratePoseTarget, FormatShape, Collect)
from .decode_sampler_MRI import SFMRI_DecodeSampler
from .segmentation_pipline import SegmentationSampler

__all__ = [
    'ImageDecoder', 'RandomMask', 'UniformCrop', 'SkeletonNorm', 'Tokenize',
    'Sampler', 'EventSampler', 'OneFileSampler', 'FeatureDecoder', 'DecodeSampler', 'TenCrop', 'Compose',
    'AutoPadding', 'Normalization', 'Mixup', 'Image2Array', 'Scale',
    'GroupResize', 'VideoDecoder', 'FrameDecoder', 'PackOutput',
    'ActionFeatureDecoder', 'GetVideoLabel', 'Cutmix', 'CenterCrop',
    'RandomCrop', 'LoadFeat', 'RandomCap', 'JitterScale', 'Iden', 'VideoMix',
    'ColorJitter', 'RandomFlip', 'ToArray', 'FeaturePadding', 'GetMatchMap',
    'GroupRandomFlip', 'MultiCrop', 'SFMRI_DecodeSampler', 'MultiRestrictSize',
    'MultiNorm', 'RandomResizedCrop', 'SamplerPkl', 'SegmentationSampler',
    'SketeonCropSample', 'SketeonModalityTransform', 'RandomRotation',
    'RandomGamma', 'MultiCenterCrop', 'RandomBrightness', 'RandomHue',
    'RandomSaturation', 'UniformSampleFrames', 'PoseDecode', 'PoseCompact',
    'Resize', 'RandomResizedCrop_V2', 'Flip_V2', 'GeneratePoseTarget',
    'FormatShape', 'Collect'
]
