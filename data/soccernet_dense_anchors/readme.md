# Copy source files and config files
    
    rsync -abviuzP paddlevideo/ $PADDLEVIDEO_SOURCE_FOLDER/

    rsync config or data files

# Prepare training with class and event time labels

Generate label_mapping.txt (for category to category index map) and dense.list files.

    python data/soccernet_dense_anchors/generate_dense_anchors_labels.py \
    --clips_folder /mnt/storage/gait-0/xin/dataset/soccernet_456x256 \
    --output_folder ./

Split into train, val, test

    python data/soccernet/split_annotation_into_train_val_test.py \
    --annotation_file dense.list \
    --clips_folder ./ \
    --mode json

# Inference on whole video files

## Convert video input into lower resolution

This generates a sample script that converts all of the Soccernet videos.

    python data/soccernet_inference/convert_video_to_lower_resolution_for_inference.py \
    --input_folder /mnt/big/multimodal_sports/SoccerNet_HQ/raw_data \
    --output_folder /mnt/storage/gait-0/xin/dataset/soccernet_456x256_inference > \
    data/soccernet_inference/convert_video_to_lower_resolution_for_inference.sh

## Parallelize resolution conversion

Each 45 min video files takes about 10 min to convert to lower resolution. So we parallelize to 100 such jobs.

    for i in {0..99};
    do
    sed -n ${i}~100p data/soccernet_inference/convert_video_to_lower_resolution_for_inference.sh > data/soccernet_inference/convert_video_to_lower_resolution_for_inference_parallel/${i}.sh;
    done

Run the parallel jobs on a cluster, slurm based for example.

    for i in {0..99};
    do
    sbatch -p 1080Ti,2080Ti,TitanXx8  --gres=gpu:1 --cpus-per-task 4 -n 1 --wrap \
    "echo no | bash data/soccernet_inference/convert_video_to_lower_resolution_for_inference_parallel/${i}.sh" \
    --output="data/soccernet_inference/convert_video_to_lower_resolution_for_inference_parallel/${i}.log"
    done

# Train command

    python -u -B -m paddle.distributed.launch --gpus="0,1,2,3,4,5,6,7" --log_dir=logs/soccernet_videoswin_k400_dense_lr_0.001_sgd_60 main.py --validate -c data/soccernet/experiments/soccernet_videoswin_k400_dense_lr_0.001_sgd_60.yaml -w pretrained_weights/swin_base_patch4_window7_224.pdparams

## Generate inference json job files

    python data/soccernet_dense_anchors/generate_whole_video_inference_jsons.py \
    --videos_folder /mnt/storage/gait-0/xin/dataset/soccernet_456x256_inference \
    --output_folder /mnt/storage/gait-0/xin/dataset/soccernet_456x256_inference_json_lists

## Sample inference command

    INFERENCE_WEIGHT_FILE=output/ppTimeSformer_dense_event_lr_100/ppTimeSformer_dense_event_lr_100_epoch_00007.pdparams
    INFERENCE_JSON_CONFIG=/mnt/storage/gait-0/xin/dataset/soccernet_456x256_inference_json_lists/spain_laliga.2016-2017.2017-05-21_-_21-00_Malaga_0_-_2_Real_Madrid.2_LQ.mkv
    INFERENCE_DIR_ROOT=/mnt/storage/gait-0/xin/soccernet_features
    SHORTNAME=`basename "$INFERENCE_JSON_CONFIG" .mkv`
    INFERENCE_DIR=$INFERENCE_DIR_ROOT/$SHORTNAME
    echo $INFERENCE_DIR

    mkdir $INFERENCE_DIR

    python3.7 -B -m paddle.distributed.launch --gpus="0" --log_dir=log_videoswin_test  main.py  --test -c data/soccernet_inference/soccernet_pptimesformer_k400_videos_dense_event_lr_50_one_file_inference.yaml -w $INFERENCE_WEIGHT_FILE -o inference_dir=$INFERENCE_DIR -o DATASET.test.file_path=$INFERENCE_JSON_CONFIG 

# List of changed files and corresponding changes.

- Label files processing are changed and labels of category and event_times are composed into dicts to send into the pipeline. Class names are added into the init.
    
        paddlevideo/loader/dataset/video_dense_anchors.py

        paddlevideo/loader/dataset/__init__.py

    Added temporal coordinate embedding to inputs. Removed event time loss for background class. Added parser for one video file list.

        paddlevideo/loader/dataset/video_dense_anchors_one_file_inference.py

- Added EventSampler

        paddlevideo/loader/pipelines/sample.py

        paddlevideo/loader/pipelines/__init__.py

    Added sampling one whole video file.

        paddlevideo/loader/pipelines/sample_one_file.py
    
    Added decoder for just one file 

        paddlevideo/loader/pipelines/decode.py

- Multitask losses.

        paddlevideo/modeling/losses/dense_anchor_loss.py
        
        paddlevideo/modeling/losses/__init__.py

- Changed head output. Class and event times.

        paddlevideo/modeling/heads/i3d_anchor_head.py

        paddlevideo/modeling/heads/pptimesformer_anchor_head.py

        paddlevideo/modeling/heads/__init__.py

- Input and output format in train_step, val step etc.

        paddlevideo/modeling/framework/recognizers/recognizer_transformer_features_inference.py

        paddlevideo/modeling/framework/recognizers/recognizer_transformer_dense_anchors.py
        
        paddlevideo/modeling/framework/recognizers/__init__.py

- Add a new mode to log both class loss and event time loss.

        paddlevideo/utils/record.py

- Added MODEL.head.name and MODEL.head.output_mode branch to process outputs of class scores and event_times. Also unified feature inference with simple classification mode.

        paddlevideo/tasks/test.py

- Lower generate lower resolution script.

        data/soccernet_inference/convert_video_to_lower_resolution_for_inference.py

- Balanced samples do not seem necessary 
    
        data/soccernet_dense_anchors/balance_class_samples.py

- Collate file to replace the current library file

        /mnt/home/xin/.conda/envs/paddle_soccernet_feature_extraction/lib/python3.7/site-packages/paddle/fluid/dataloader/collate.py

- Config files

        data/soccernet/soccernet_videoswin_k400_dense_one_file_inference.yaml

- Updated to support dense anchors

        data/soccernet/split_annotation_into_train_val_test.py

# Comments

1. TODO paddlevideo/loader/dataset/video_dense_anchors_one_file_inference.py can inherit from paddlevideo/loader/dataset/video_dense_anchors.py





paddlevideo/loader/pipelines/decode.py




/mnt/home/xin/.conda/envs/paddle_soccernet_feature_extraction/bin/python -u -B -m paddle.distributed.launch --gpus="0" --log_dir=logs/dense_anchors main.py --validate -c data/soccernet/soccernet_videoswin_k400_dense.yaml -w pretrained_weights/swin_base_patch4_window7_224.pdparams


python -u -B -m paddle.distributed.launch --gpus="0" --log_dir=logs/dense_anchors main.py --validate -c data/soccernet/soccernet_videoswin_k400_dense.yaml -w pretrained_weights/swin_base_patch4_window7_224.pdparams



python -u -B -m paddle.distributed.launch --gpus="0,1,2,3,4,5,6,7" --log_dir=logs/dense_anchors_1 main.py --validate -c data/soccernet/soccernet_videoswin_k400_dense.yaml -w pretrained_weights/swin_base_patch4_window7_224.pdparams 2>&1 | tee -a logs/dense_anchors_1.log

sbatch -p V100_GAIT --nodelist=asimov-228 --account=gait -t 30-00:00:00 --gres=gpu:8 --cpus-per-task 40 -n 1  \
--wrap "python -u -B -m paddle.distributed.launch --gpus="0,1,2,3,4,5,6,7" --log_dir=logs/dense_anchors_1 main.py --validate -c data/soccernet/soccernet_videoswin_k400_dense.yaml -w pretrained_weights/swin_base_patch4_window7_224.pdparams" \
--output="/mnt/storage/gait-0/xin//logs/soccernet_videoswin_21_dense_lr_0.001.log"

sbatch -p V100_GAIT --nodelist=asimov-230 --account=gait -t 30-00:00:00 --gres=gpu:8 --cpus-per-task 40 -n 1  \
--wrap "python -u -B -m paddle.distributed.launch --gpus="0,1,2,3,4,5,6,7" --log_dir=logs/dense_anchors_2 main.py --validate -c data/soccernet/experiments/soccernet_videoswin_k400_dense_lr_0.01.yaml -w pretrained_weights/swin_base_patch4_window7_224.pdparams" \
--output="/mnt/storage/gait-0/xin//logs/soccernet_videoswin_20_dense_lr_0.01.log"


sbatch -p V100_GAIT --nodelist=asimov-228 --account=gait -t 30-00:00:00 --gres=gpu:8 --cpus-per-task 40 -n 1  \
--wrap "python -u -B -m paddle.distributed.launch --gpus="0,1,2,3,4,5,6,7" --log_dir=logs/dense_anchors_2_lr_0.001 main.py --validate -c data/soccernet/experiments/soccernet_videoswin_k400_dense_lr_0.001.yaml -w pretrained_weights/swin_base_patch4_window7_224.pdparams" \
--output="/mnt/storage/gait-0/xin//logs/soccernet_videoswin_21_dense_adamW_lr_0.001.log"

sbatch -p V100_GAIT --nodelist=asimov-230 --account=gait -t 30-00:00:00 --gres=gpu:8 --cpus-per-task 40 -n 1  \
--wrap "python -u -B -m paddle.distributed.launch --gpus="0,1,2,3,4,5,6,7" --log_dir=logs/dense_anchors_2_lr_0.0001 main.py --validate -c data/soccernet/experiments/soccernet_videoswin_k400_dense_lr_0.0001.yaml -w pretrained_weights/swin_base_patch4_window7_224.pdparams" \
--output="/mnt/storage/gait-0/xin//logs/soccernet_videoswin_21_dense_adamW_lr_0.0001.log"

sbatch -p V100x8 --gres=gpu:8 --cpus-per-task 40 -n 1  \
--wrap "python -u -B -m paddle.distributed.launch --gpus="0,1,2,3,4,5,6,7" --log_dir=logs/soccernet_videoswin_k400_dense_lr_0.001_no_warmup main.py --validate -c data/soccernet/experiments/soccernet_videoswin_k400_dense_lr_0.001_no_warmup.yaml -w pretrained_weights/swin_base_patch4_window7_224.pdparams" \
--output="/mnt/storage/gait-0/xin//logs/soccernet_videoswin_k400_dense_lr_0.001_no_warmup.log"


sbatch -p V100x8 --gres=gpu:8 --cpus-per-task 40 -n 1  \
--wrap "/mnt/home/xin/.conda/envs/paddle_soccernet_feature_extraction/bin/python -u -B -m paddle.distributed.launch --gpus="0,1,2,3,4,5,6,7" --log_dir=logs/soccernet_videoswin_k400_dense_lr_0.001_balanced main.py --validate -c data/soccernet/experiments/soccernet_videoswin_k400_dense_lr_0.001_balanced.yaml -w pretrained_weights/swin_base_patch4_window7_224.pdparams" \
--output="/mnt/storage/gait-0/xin//logs/soccernet_videoswin_k400_dense_lr_0.001_balanced.log"


sbatch -p V100x8 --gres=gpu:8 --cpus-per-task 40 -n 1  \
--wrap "/mnt/home/xin/.conda/envs/paddle_soccernet_feature_extraction/bin/python -u -B -m paddle.distributed.launch --gpus="0,1,2,3,4,5,6,7" --log_dir=logs/soccernet_videoswin_20_dense_lr_0.00001_adamW main.py --validate -c data/soccernet/experiments/soccernet_videoswin_k400_dense_lr_0.00001.yaml -w pretrained_weights/swin_base_patch4_window7_224.pdparams" \
--output="/mnt/storage/gait-0/xin//logs/soccernet_videoswin_20_dense_lr_0.00001_adamW.log"



sbatch -p V100x8 --gres=gpu:8 --cpus-per-task 40 -n 1  \
--wrap "/mnt/home/xin/.conda/envs/paddle_soccernet_feature_extraction/bin/python -u -B -m paddle.distributed.launch --gpus="0,1,2,3,4,5,6,7" --log_dir=logs/soccernet_videoswin_20_dense_lr_0.000001_adamW main.py --validate -c data/soccernet/experiments/soccernet_videoswin_k400_dense_lr_0.000001.yaml -w pretrained_weights/swin_base_patch4_window7_224.pdparams" \
--output="/mnt/storage/gait-0/xin//logs/soccernet_videoswin_20_dense_lr_0.000001_adamW.log"


sbatch -p V100_GAIT --nodelist=asimov-230 --account=gait -t 30-00:00:00 --gres=gpu:8 --cpus-per-task 40 -n 1  \
--wrap "python -u -B -m paddle.distributed.launch --gpus="0,1,2,3,4,5,6,7" --log_dir=logs/dense_anchors_2 main.py --validate -c data/soccernet/experiments/soccernet_videoswin_k400_dense_lr_0.00001.yaml -w pretrained_weights/swin_base_patch4_window7_224.pdparams" \
--output="/mnt/storage/gait-0/xin//logs/soccernet_videoswin_20_dense_lr_0.00001.log"


sbatch -p V100_GAIT --nodelist=asimov-230 --account=gait -t 30-00:00:00 --gres=gpu:8 --cpus-per-task 40 -n 1  \
--wrap "python -u -B -m paddle.distributed.launch --gpus="0,1,2,3,4,5,6,7" --log_dir=logs/soccernet_videoswin_k400_dense_lr_0.001_sgd_60 main.py --validate -c data/soccernet/experiments/soccernet_videoswin_k400_dense_lr_0.001_sgd_60.yaml -w pretrained_weights/swin_base_patch4_window7_224.pdparams" \
--output="/mnt/storage/gait-0/xin//logs/soccernet_videoswin_k400_dense_lr_0.001_sgd_60.log"


sbatch -p V100_GAIT --nodelist=asimov-228 --account=gait -t 30-00:00:00 --gres=gpu:8 --cpus-per-task 40 -n 1  \
--wrap "python -u -B -m paddle.distributed.launch --gpus="0,1,2,3,4,5,6,7" --log_dir=logs/soccernet_videoswin_k400_dense_lr_0.0001_sgd_60 main.py --validate -c data/soccernet/experiments/soccernet_videoswin_k400_dense_lr_0.0001_sgd_60.yaml -w pretrained_weights/swin_base_patch4_window7_224.pdparams" \
--output="/mnt/storage/gait-0/xin//logs/soccernet_videoswin_k400_dense_lr_0.0001_sgd_60.log"


sbatch -p V100x8 --gres=gpu:8 --cpus-per-task 40 -n 1  \
--wrap "python -u -B -m paddle.distributed.launch --gpus="0,1,2,3,4,5,6,7" --log_dir=logs/dense_anchors_lr_0.1 main.py --validate -c data/soccernet/experiments/soccernet_videoswin_k400_dense_lr_0.1.yaml -w pretrained_weights/swin_base_patch4_window7_224.pdparams" \
--output="/mnt/storage/gait-0/xin//logs/soccernet_videoswin_21_dense_lr_0.1.log"


sbatch -p V100x8_mlong --gres=gpu:8 --cpus-per-task 40 -n 1  \
--wrap "python -u -B -m paddle.distributed.launch --gpus="0,1,2,3,4,5,6,7" --log_dir=logs/soccernet_videoswin_k400_dense_lr_0.001_sgd_60_randomization main.py --validate -c data/soccernet/experiments/soccernet_videoswin_k400_dense_lr_0.001_sgd_60_pptimesformer_randomization.yaml -w pretrained_weights/swin_base_patch4_window7_224.pdparams" \
--output="/mnt/storage/gait-0/xin//logs/soccernet_videoswin_k400_dense_lr_0.001_sgd_60_randomization.log"

sbatch -p V100x8 --gres=gpu:8 --cpus-per-task 40 -n 1  \
--wrap "python -u -B -m paddle.distributed.launch --gpus="0,1,2,3,4,5,6,7" --log_dir=logs/soccernet_videoswin_k400_dense_lr_0.001_sgd_60_random_scale_adamW main.py --validate -c data/soccernet/experiments/soccernet_videoswin_k400_dense_lr_0.001_sgd_60_random_scale_adamW.yaml -w pretrained_weights/swin_base_patch4_window7_224.pdparams" \
--output="/mnt/storage/gait-0/xin//logs/soccernet_videoswin_k400_dense_lr_0.001_sgd_60_random_scale_adamW.log"


sbatch -p V100x8 --gres=gpu:8 --cpus-per-task 40 -n 1  \
--wrap "python -u -B -m paddle.distributed.launch --gpus="0,1,2,3,4,5,6,7" --log_dir=logs/soccernet_videoswin_k400_dense_lr_0.0001_sgd_60_random_scale_adamW main.py --validate -c data/soccernet/experiments/soccernet_videoswin_k400_dense_lr_0.0001_sgd_60_random_scale_adamW.yaml -w pretrained_weights/swin_base_patch4_window7_224.pdparams" \
--output="/mnt/storage/gait-0/xin//logs/soccernet_videoswin_k400_dense_lr_0.0001_sgd_60_random_scale_adamW.log"


sbatch -p V100x8 --gres=gpu:8 --cpus-per-task 40 -n 1  \
--wrap "python -u -B -m paddle.distributed.launch --gpus="0,1,2,3,4,5,6,7" --log_dir=logs/soccernet_videoswin_k400_dense_lr_0.00001_sgd_60_random_scale_adamW main.py --validate -c data/soccernet/experiments/soccernet_videoswin_k400_dense_lr_0.00001_sgd_60_random_scale_adamW.yaml -w pretrained_weights/swin_base_patch4_window7_224.pdparams" \
--output="/mnt/storage/gait-0/xin//logs/soccernet_videoswin_k400_dense_lr_0.00001_sgd_60_random_scale_adamW.log"


sbatch -p V100x8 --gres=gpu:8 --cpus-per-task 40 -n 1  \
--wrap "python -u -B -m paddle.distributed.launch --gpus="0,1,2,3,4,5,6,7" --log_dir=logs/soccernet_videoswin_k400_dense_lr_0.00001_sgd_60_random_scale main.py --validate -c data/soccernet/experiments/soccernet_videoswin_k400_dense_lr_0.00001_sgd_60_random_scale.yaml -w pretrained_weights/swin_base_patch4_window7_224.pdparams" \
--output="/mnt/storage/gait-0/xin//logs/soccernet_videoswin_k400_dense_lr_0.00001_sgd_60_random_scale.log"

sbatch -p V100x8 --gres=gpu:8 --cpus-per-task 40 -n 1  \
--wrap "python -u -B -m paddle.distributed.launch --gpus="0,1,2,3,4,5,6,7" --log_dir=logs/soccernet_videoswin_k400_dense_lr_0.0001_sgd_60_random_scale main.py --validate -c data/soccernet/experiments/soccernet_videoswin_k400_dense_lr_0.0001_sgd_60_random_scale.yaml -w pretrained_weights/swin_base_patch4_window7_224.pdparams" \
--output="/mnt/storage/gait-0/xin//logs/soccernet_videoswin_k400_dense_lr_0.0001_sgd_60_random_scale.log"


sbatch -p V100x8_mlong --gres=gpu:8 --cpus-per-task 40 -n 1  \
--wrap "python -u -B -m paddle.distributed.launch --gpus="0,1,2,3,4,5,6,7" --log_dir=logs/soccernet_videoswin_k400_dense_lr_0.001_sgd_60_random_scale main.py --validate -c data/soccernet/experiments/soccernet_videoswin_k400_dense_lr_0.001_sgd_60_random_scale.yaml -w pretrained_weights/swin_base_patch4_window7_224.pdparams" \
--output="/mnt/storage/gait-0/xin//logs/soccernet_videoswin_k400_dense_lr_0.001_sgd_60_random_scale.log"



sbatch -p V100x8_mlong --gres=gpu:8 --cpus-per-task 40 -n 1  \
--wrap "python -u -B -m paddle.distributed.launch --gpus="0,1,2,3,4,5,6,7" --log_dir=logs/soccernet_pptimesformer_k400_videos_dense main.py --validate -c data/soccernet/experiments/pptimesformer/soccernet_pptimesformer_k400_videos_dense.yaml -w pretrained_weights/ppTimeSformer_k400_16f_distill.pdparams" \
--output="/mnt/storage/gait-0/xin//logs/soccernet_pptimesformer_k400_videos_dense.log"


sbatch -p V100x8 --gres=gpu:8 --cpus-per-task 40 -n 1  \
--wrap "python -u -B -m paddle.distributed.launch --gpus="0,1,2,3,4,5,6,7" --log_dir=logs/soccernet_pptimesformer_k400_videos_dense_lr_1e-4 main.py --validate -c data/soccernet/experiments/pptimesformer/soccernet_pptimesformer_k400_videos_dense_lr_1e-4.yaml -w pretrained_weights/ppTimeSformer_k400_16f_distill.pdparams" \
--output="/mnt/storage/gait-0/xin//logs/soccernet_pptimesformer_k400_videos_dense_lr_1e-4.log"


sbatch -p V100x8 --gres=gpu:8 --cpus-per-task 40 -n 1  \
--wrap "python -u -B -m paddle.distributed.launch --gpus="0,1,2,3,4,5,6,7" --log_dir=logs/soccernet_pptimesformer_k400_videos_dense_lr_1e-5 main.py --validate -c data/soccernet/experiments/pptimesformer/soccernet_pptimesformer_k400_videos_dense_lr_1e-5.yaml -w pretrained_weights/ppTimeSformer_k400_16f_distill.pdparams" \
--output="/mnt/storage/gait-0/xin//logs/soccernet_pptimesformer_k400_videos_dense_lr_1e-5.log"


sbatch -p V100x8_mlong  --exclude asimov-231 --gres=gpu:8 --cpus-per-task 40 -n 1  \
--wrap "python -u -B -m paddle.distributed.launch --gpus="0,1,2,3,4,5,6,7" --log_dir=logs/soccernet_videoswin_k400_dense_lr_0.001_sgd_60_random_scale_event_lr_50_warmup main.py --validate -c data/soccernet/experiments/soccernet_videoswin_k400_dense_lr_0.001_sgd_60_random_scale_event_lr_50_warmup.yaml -w pretrained_weights/ppTimeSformer_k400_16f_distill.pdparams" \
--output="/mnt/storage/gait-0/xin//logs/soccernet_videoswin_k400_dense_lr_0.001_sgd_60_random_scale_event_lr_50_warmup.log"



sbatch -p V100_GAIT --nodelist=asimov-230 --account=gait -t 30-00:00:00 --gres=gpu:8 --cpus-per-task 40 -n 1  \
--wrap "python -u -B -m paddle.distributed.launch --gpus="0,1,2,3,4,5,6,7" --log_dir=logs/soccernet_videoswin_k400_dense_lr_0.001_sgd_60_random_scale_event_lr main.py --validate -c data/soccernet/experiments/soccernet_videoswin_k400_dense_lr_0.001_sgd_60_random_scale_event_lr.yaml -w pretrained_weights/ppTimeSformer_k400_16f_distill.pdparams" \
--output="/mnt/storage/gait-0/xin//logs/soccernet_videoswin_k400_dense_lr_0.001_sgd_60_random_scale_event_lr.log"


sbatch -p V100_GAIT --nodelist=asimov-228 --account=gait -t 30-00:00:00 --gres=gpu:8 --cpus-per-task 40 -n 1  \
--wrap "python -u -B -m paddle.distributed.launch --gpus="0,1,2,3,4,5,6,7" --log_dir=logs/soccernet_pptimesformer_k400_videos_dense_event_lr_100 main.py --validate -c data/soccernet/experiments/pptimesformer/soccernet_pptimesformer_k400_videos_dense_event_lr_100.yaml -w pretrained_weights/ppTimeSformer_k400_16f_distill.pdparams" \
--output="/mnt/storage/gait-0/xin//logs/soccernet_pptimesformer_k400_videos_dense_event_lr_100.log"


sbatch -p V100_GAIT --nodelist=asimov-230 --account=gait -t 30-00:00:00 --gres=gpu:8 --cpus-per-task 40 -n 1  \
--wrap "python -u -B -m paddle.distributed.launch --gpus="0,1,2,3,4,5,6,7" --log_dir=logs/soccernet_pptimesformer_k400_videos_dense_event_lr_50 main.py --validate -c data/soccernet/experiments/pptimesformer/soccernet_pptimesformer_k400_videos_dense_event_lr_50.yaml -w pretrained_weights/ppTimeSformer_k400_16f_distill.pdparams" \
--output="/mnt/storage/gait-0/xin//logs/soccernet_pptimesformer_k400_videos_dense_event_lr_50.log"



python -u -B -m paddle.distributed.launch --gpus="0" --log_dir=logs/soccernet_videoswin_k400_dense_lr_0.001_sgd_60_randomization main.py --validate -c data/soccernet/experiments/soccernet_videoswin_k400_dense_lr_0.001_sgd_60_pptimesformer_randomization.yaml -w pretrained_weights/swin_base_patch4_window7_224.pdparams

some augmentation error

在add_coordinates_embedding_to_imgs的时候pyav得到的是tensor， decord是np array? pyav decode完就是paddle.tensor了？

'decord'
ipdb> type(imgs)
<class 'numpy.ndarray'>
ipdb> imgs.shape
(3, 16, 256, 456)


python -u -B -m paddle.distributed.launch --gpus="0" --log_dir=logs/soccernet_pptimesformer_k400_videos_dense main.py --validate -c data/soccernet/soccernet_pptimesformer_k400_videos_dense.yaml -w pretrained_weights/ppTimeSformer_k400_16f_distill.pdparams

python -u -B -m paddle.distributed.launch --gpus="0" --log_dir=logs/soccernet_pptimesformer_k400_videos_dense main.py --validate -c data/soccernet/soccernet_videoswin_k400_dense.yaml -w pretrained_weights/ppTimeSformer_k400_16f_distill.pdparams



TODO:
Test one video inference, test on longer video


git filter-branch --index-filter \
    'git rm -rf --cached --ignore-unmatch data/soccernet/generate_training_short_clips.sh' HEAD

ffmpeg -i "/mnt/big/multimodal_sports/SoccerNet_HQ/raw_data/england_epl/2015-2016/2015-08-29 - 17-00 Manchester City 2 - 0 Watford/1_HQ.mkv" -vf scale=456x256 -map 0:v -avoid_negative_ts make_zero -c:v libx264 -c:a aac "/mnt/storage/gait-0/xin/dataset/soccernet_456x256_inference/england_epl.2015-2016.2015-08-29_-_17-00_Manchester_City_2_-_0_Watford.1_LQ.mkv" -max_muxing_queue_size 9999



for i in {0..28};
do
sed -n ${i}~29p data/soccernet_inference/convert_video_rerun.sh > data/soccernet_inference/convert_video_rerun_parallel/${i}.sh;
done



for i in {0..28};
do
sbatch -p 1080Ti,2080Ti,TitanXx8  --gres=gpu:1 --cpus-per-task 4 -n 1 --wrap \
"echo yes | bash data/soccernet_inference/convert_video_rerun_parallel/${i}.sh" \
--output="data/soccernet_inference/convert_video_rerun_parallel/${i}.log"
done



override weight, override jobs file

sbatch each line

weight file is always in the output folder. output/$model_name

for FILE in /mnt/storage/gait-0/xin/dataset/soccernet_456x256_inference_json_lists/*; do echo $FILE; done

INFERENCE_WEIGHT_FILE=output/ppTimeSformer_dense_event_lr_100/ppTimeSformer_dense_event_lr_100_epoch_00007.pdparams
INFERENCE_JSON_CONFIG=/mnt/storage/gait-0/xin/dataset/soccernet_456x256_inference_json_lists/spain_laliga.2016-2017.2017-05-21_-_21-00_Malaga_0_-_2_Real_Madrid.2_LQ.mkv
INFERENCE_DIR_ROOT=/mnt/storage/gait-0/xin/soccernet_features
SHORTNAME=`basename "$INFERENCE_JSON_CONFIG" .mkv`
INFERENCE_DIR=$INFERENCE_DIR_ROOT/$SHORTNAME
echo $INFERENCE_DIR

mkdir $INFERENCE_DIR

python3.7 -B -m paddle.distributed.launch --gpus="0" --log_dir=log_videoswin_test  main.py  --test -c data/soccernet_inference/soccernet_pptimesformer_k400_videos_dense_event_lr_50_one_file_inference.yaml -w $INFERENCE_WEIGHT_FILE -o inference_dir=$INFERENCE_DIR -o DATASET.test.file_path=$INFERENCE_JSON_CONFIG 


for FILE in /mnt/storage/gait-0/xin/dataset/soccernet_456x256_inference_json_lists/*; 


INFERENCE_WEIGHT_FILE=output/ppTimeSformer_dense_event_lr_100/ppTimeSformer_dense_event_lr_100_epoch_00012.pdparams
INFERENCE_DIR_ROOT=/mnt/storage/gait-0/xin/soccernet_features


for FILE in /mnt/storage/gait-0/xin/dataset/soccernet_456x256_inference_json_lists/*; 
do 
echo $FILE;
INFERENCE_JSON_CONFIG=$FILE
SHORTNAME=`basename "$INFERENCE_JSON_CONFIG" .mkv`
INFERENCE_DIR=$INFERENCE_DIR_ROOT/$SHORTNAME
mkdir $INFERENCE_DIR

sbatch -p 1080Ti,2080Ti --gres=gpu:1 --cpus-per-task 4 -n 1  \
--wrap "python3.7 -B -m paddle.distributed.launch --gpus='0' --log_dir=/mnt/storage/gait-0/xin//logs/$SHORTNAME  main.py  --test -c data/soccernet_inference/soccernet_pptimesformer_k400_videos_dense_event_lr_50_one_file_inference.yaml -w $INFERENCE_WEIGHT_FILE -o inference_dir=$INFERENCE_DIR -o DATASET.test.file_path=$INFERENCE_JSON_CONFIG" \
--output="/mnt/storage/gait-0/xin//logs/$SHORTNAME.log"

echo /mnt/storage/gait-0/xin//logs/$SHORTNAME.log

done



python -u -B -m paddle.distributed.launch --gpus="0" --log_dir=logs/soccernet_pptimesformer_k400_videos_dense_event_lr_50_compare main.py --validate -c data/soccernet_inference/soccernet_pptimesformer_k400_videos_dense_event_lr_50_compare.yaml -w pretrained_weights/ppTimeSformer_k400_16f_distill.pdparams

Timesformer does not have coordinate embedding



/mnt/storage/gait-0/xin/soccernet_features/spain_laliga.2016-2017.2017-05-21_-_21-00_Malaga_0_-_2_Real_Madrid.2_LQ/features.npy

a = np.load("/mnt/storage/gait-0/xin/soccernet_features/spain_laliga.2016-2017.2017-05-21_-_21-00_Malaga_0_-_2_Real_Madrid.2_LQ/features.npy", allow_pickle = True)

a
array({'features': array([[[-0.11292514, -0.1312699 ,  0.07413186, ..., -0.0345116 ,
          0.09101289,  0.06796468]],

       [[-0.07808004, -0.10946111, -0.09529223, ...,  0.01151106,
          0.09962937, -0.09179376]],

       [[-0.0843792 , -0.10908166, -0.09925203, ...,  0.00971421,
          0.09548534, -0.08486937]],

       [[-0.08389836, -0.10990171, -0.1055292 , ...,  0.00767103,
          0.08909672, -0.07665699]],

       [[-0.08546472, -0.10893059, -0.10001937, ...,  0.00777278,
          0.08489308, -0.07387131]]], dtype=float32)}, dtype=object)


/mnt/storage/gait-0/xin/soccernet_features



CONFIG_DIR=/mnt/storage/gait-0/xin/dataset/soccernet_456x256_inference_json_lists/
INFERENCE_WEIGHT_FILE=output/ppTimeSformer_dense_event_lr_100/ppTimeSformer_dense_event_lr_100_epoch_00028.pdparams
INFERENCE_DIR_ROOT=/mnt/storage/gait-0/xin/soccernet_features

for FILE in /mnt/storage/gait-0/xin/dataset/soccernet_456x256_inference_json_lists/*; 
do 
line=`basename "$FILE" .mkv`
INFERENCE_JSON_CONFIG=$CONFIG_DIR/$line.mkv
INFERENCE_DIR=$INFERENCE_DIR_ROOT/$line

echo "sbatch -p TitanXx8_mlong,TitanXx8_slong,2080Ti_mlong,1080Ti_slong,1080Ti_mlong,1080Ti,TitanXx8 --gres=gpu:1 --cpus-per-task 4 -n 1  \
--wrap \"python3.7 -B -m paddle.distributed.launch --gpus='0' --log_dir=/mnt/storage/gait-0/xin//logs/$line  main.py  --test -c data/soccernet_inference/soccernet_pptimesformer_k400_videos_dense_event_lr_50_one_file_inference.yaml -w $INFERENCE_WEIGHT_FILE -o inference_dir=$INFERENCE_DIR -o DATASET.test.file_path=$INFERENCE_JSON_CONFIG\" \
--output=\"/mnt/storage/gait-0/xin//logs/$line.log\" "
done



CONFIG_DIR=/mnt/storage/gait-0/xin/dataset/soccernet_456x256_inference_json_lists/
INFERENCE_WEIGHT_FILE=output/ppTimeSformer_dense_event_lr_100/ppTimeSformer_dense_event_lr_100_epoch_00028.pdparams
INFERENCE_DIR_ROOT=/mnt/storage/gait-0/xin/soccernet_features


cat inference_matches_todo.txt | while read line 
do 
INFERENCE_JSON_CONFIG=$CONFIG_DIR/$line.mkv
INFERENCE_DIR=$INFERENCE_DIR_ROOT/$line


echo "sbatch -p 1080Ti,TitanXx8 --gres=gpu:1 --cpus-per-task 4 -n 1  \
--wrap \"python3.7 -B -m paddle.distributed.launch --gpus='0' --log_dir=/mnt/storage/gait-0/xin//logs/$line  main.py  --test -c data/soccernet_inference/soccernet_pptimesformer_k400_videos_dense_event_lr_50_one_file_inference.yaml -w $INFERENCE_WEIGHT_FILE -o inference_dir=$INFERENCE_DIR -o DATASET.test.file_path=$INFERENCE_JSON_CONFIG\" \
--output=\"/mnt/storage/gait-0/xin//logs/$line.log\" "
done

1080Ti
watch tail -n 20 /mnt/storage/gait-0/xin//logs/germany_bundesliga.2016-2017.2016-10-22_-_16-30_Ingolstadt_3_-_3_Dortmund.2_LQ.log
watch tail -n 20 /mnt/storage/gait-0/xin//logs/germany_bundesliga.2016-2017.2016-10-22_-_16-30_Ingolstadt_3_-_3_Dortmund.2_LQ/workerlog.0

TitanXx8
watch tail -n 20 /mnt/storage/gait-0/xin//logs/spain_laliga.2016-2017.2016-11-27_-_22-45_Real_Sociedad_1_-_1_Barcelona.1_LQ.log
watch tail -n 20 /mnt/storage/gait-0/xin//logs/spain_laliga.2016-2017.2016-11-27_-_22-45_Real_Sociedad_1_-_1_Barcelona.1_LQ/workerlog.0


watch tail -n 20 /mnt/storage/gait-0/xin//logs/england_epl.2014-2015.2015-02-21_-_18-00_Chelsea_1_-_1_Burnley.1_LQ/workerlog.0
watch tail -n 20 /mnt/storage/gait-0/xin//logs/england_epl.2014-2015.2015-02-21_-_18-00_Chelsea_1_-_1_Burnley.2_LQ/workerlog.0

python data/soccernet_dense_anchors/check_unfinished_inference.py