ffmpeg -i "/mnt/big/multimodal_sports/SoccerNet_HQ/raw_data/england_epl/2015-2016/2015-12-28 - 20-30 Manchester United 0 - 0 Chelsea/2_HQ.mkv" -vf "scale=456x256,fps=5" -map 0:v -c:v libx264 "/mnt/storage/gait-0/xin/dataset/soccernet_456x256_inference_5fps/england_epl.2015-2016.2015-12-28_-_20-30_Manchester_United_0_-_0_Chelsea.2_LQ.mkv" -y
ffmpeg -i "/mnt/big/multimodal_sports/SoccerNet_HQ/raw_data/england_epl/2016-2017/2017-01-02 - 18-00 Sunderland 2 - 2 Liverpool/2_HQ.mkv" -vf "scale=456x256,fps=5" -map 0:v -c:v libx264 "/mnt/storage/gait-0/xin/dataset/soccernet_456x256_inference_5fps/england_epl.2016-2017.2017-01-02_-_18-00_Sunderland_2_-_2_Liverpool.2_LQ.mkv" -y
ffmpeg -i "/mnt/big/multimodal_sports/SoccerNet_HQ/raw_data/europe_uefa-champions-league/2015-2016/2015-09-15 - 21-45 Paris SG 2 - 0 Malmo FF/2_HQ.mkv" -vf "scale=456x256,fps=5" -map 0:v -c:v libx264 "/mnt/storage/gait-0/xin/dataset/soccernet_456x256_inference_5fps/europe_uefa-champions-league.2015-2016.2015-09-15_-_21-45_Paris_SG_2_-_0_Malmo_FF.2_LQ.mkv" -y
ffmpeg -i "/mnt/big/multimodal_sports/SoccerNet_HQ/raw_data/europe_uefa-champions-league/2016-2017/2016-11-23 - 22-45 Arsenal 2 - 2 Paris SG/2_HQ.mkv" -vf "scale=456x256,fps=5" -map 0:v -c:v libx264 "/mnt/storage/gait-0/xin/dataset/soccernet_456x256_inference_5fps/europe_uefa-champions-league.2016-2017.2016-11-23_-_22-45_Arsenal_2_-_2_Paris_SG.2_LQ.mkv" -y
ffmpeg -i "/mnt/big/multimodal_sports/SoccerNet_HQ/raw_data/germany_bundesliga/2014-2015/2015-04-11 - 16-30 Bayern Munich 3 - 0 Eintracht Frankfurt/2_HQ.mkv" -vf "scale=456x256,fps=5" -map 0:v -c:v libx264 "/mnt/storage/gait-0/xin/dataset/soccernet_456x256_inference_5fps/germany_bundesliga.2014-2015.2015-04-11_-_16-30_Bayern_Munich_3_-_0_Eintracht_Frankfurt.2_LQ.mkv" -y
ffmpeg -i "/mnt/big/multimodal_sports/SoccerNet_HQ/raw_data/germany_bundesliga/2016-2017/2017-02-11 - 18-00 Leipzig 0 - 3 Hamburger/2_HQ.mkv" -vf "scale=456x256,fps=5" -map 0:v -c:v libx264 "/mnt/storage/gait-0/xin/dataset/soccernet_456x256_inference_5fps/germany_bundesliga.2016-2017.2017-02-11_-_18-00_Leipzig_0_-_3_Hamburger.2_LQ.mkv" -y
ffmpeg -i "/mnt/big/multimodal_sports/SoccerNet_HQ/raw_data/italy_serie-a/2016-2017/2016-10-25 - 21-45 Genoa 3 - 0 AC Milan/2_HQ.mkv" -vf "scale=456x256,fps=5" -map 0:v -c:v libx264 "/mnt/storage/gait-0/xin/dataset/soccernet_456x256_inference_5fps/italy_serie-a.2016-2017.2016-10-25_-_21-45_Genoa_3_-_0_AC_Milan.2_LQ.mkv" -y
ffmpeg -i "/mnt/big/multimodal_sports/SoccerNet_HQ/raw_data/italy_serie-a/2016-2017/2017-05-14 - 16-00 Torino 0 - 5 Napoli/2_HQ.mkv" -vf "scale=456x256,fps=5" -map 0:v -c:v libx264 "/mnt/storage/gait-0/xin/dataset/soccernet_456x256_inference_5fps/italy_serie-a.2016-2017.2017-05-14_-_16-00_Torino_0_-_5_Napoli.2_LQ.mkv" -y
ffmpeg -i "/mnt/big/multimodal_sports/SoccerNet_HQ/raw_data/spain_laliga/2015-2016/2016-03-05 - 18-00 Real Madrid 7 - 1 Celta Vigo/2_HQ.mkv" -vf "scale=456x256,fps=5" -map 0:v -c:v libx264 "/mnt/storage/gait-0/xin/dataset/soccernet_456x256_inference_5fps/spain_laliga.2015-2016.2016-03-05_-_18-00_Real_Madrid_7_-_1_Celta_Vigo.2_LQ.mkv" -y
ffmpeg -i "/mnt/big/multimodal_sports/SoccerNet_HQ/raw_data/spain_laliga/2016-2017/2017-03-04 - 22-45 Barcelona 5 - 0 Celta Vigo/2_HQ.mkv" -vf "scale=456x256,fps=5" -map 0:v -c:v libx264 "/mnt/storage/gait-0/xin/dataset/soccernet_456x256_inference_5fps/spain_laliga.2016-2017.2017-03-04_-_22-45_Barcelona_5_-_0_Celta_Vigo.2_LQ.mkv" -y
