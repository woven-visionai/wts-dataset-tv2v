<div id="top" align="center">

<p align="center">
  <img src="assets/images/overview.png">
</p>

**WTS:A Pedestrian-Centric Traffic Video Dataset for Fine-grained Spatial-Temporal Understanding**

**TV2V subset served as official source for AI City Challenge Track 5**

</div>

<div id="top" align="center">
  
[![License](https://img.shields.io/badge/License-wts_terms%20-blue)](#licenseandcitation)
[![](https://img.shields.io/badge/Latest%20release-v1.0-yellow)](#datastructure)
[![Project](https://img.shields.io/badge/Project-website%20-green)](https://woven-visionai.github.io/wts-dataset-homepage/)
</div>

## Update List

- [ ] Release test datasets
- [ ] Release submission instructions and evaluation scripts

## WTS Dataset <a name="introduction"></a>

The [Woven Traffic Safety (WTS) Dataset](https://woven-visionai.github.io/wts-dataset-homepage/) from [Woven by Toyota, Inc.](https://woven.toyota/en/), is designed to emphasize detailed behaviors of both vehicles and pedestrians within a variety of staged traffic events including accidents.
Comprising over 1.2k video events across over 130 distinct traffic scenarios, WTS integrates diverse perspectives from vehicle ego and fixed overhead cameras in a vehicle-infrastructure cooperative environment. Each event in WTS is enriched with comprehensive textual descriptions of the observed behaviors and contexts. An overview of the contents of the data and the annotation pipeline is shown as below.

<p align="center">
    <img width="896" alt="image" src="https://github.com/user-attachments/assets/63fa5f89-662c-455c-ac6a-9f06223d009c" />
</p>

This repo contains a subset of the main WTS dataset with relevant descriptions and scripts for [`AI City Challenge Track 5`](https://github.com/woven-visionai/wts-dataset-tv2v) (Generative Video Forecasting). More details about the main dataset can be found in the [main repo](https://github.com/woven-visionai/wts-dataset).

## Dataset Download <a name="download"></a>

1. Please **submit request** through [Google Form](https://forms.gle/szQPk1TMR8JXzm327) first.
2. You will get a DropBox link and a Google Drive link. They have identical content, so you can choose **either one**.
3. For the Google Drive, in case you do not have access, **request on Google Drive** and it will be approved manually as long as you have completed Step 1.


## Data Structure
This challenge defines the task of generating future video frames conditioned on history frames and textutal descriptions for the future. For the purpose of this task, we provide two types of data:

- Videos
- Captions for pedestrian and vehicle perspectives

The structure of each type of the data is described in below:

### Video Data

All collected WTS video data are stored under the `videos` folder. 
Some scenarios have multiple-view videos.

```
videos
├── train
│   ├── 20230707_12_SN17_T1  ##scenario index
│   │   ├── overhead_view    ##different overhead views of the scenario
│   │   │   ├── 20230707_12_SN17_T1_Camera1_0.mp4
│   │   │   ├── 20230707_12_SN17_T1_Camera2_3.mp4
│   │   │   ├── 20230707_12_SN17_T1_Camera3_1.mp4
│   │   │   └── 20230707_12_SN17_T1_Camera4_2.mp4
│   │   └── vehicle_view  ##vehicle ego-views of the scenario
│   │       └── 20230707_12_SN17_T1_vehicle_view.mp4
│   ├── 20230707_15_SY4_T1
│   │   ├── overhead_view
│   │   │   ├── 20230707_15_SY4_T1_Camera1_0.mp4
│   │   │   ├── 20230707_15_SY4_T1_Camera2_1.mp4
│   │   │   └── 20230707_15_SY4_T1_Camera3_2.mp4
│   │   └── vehicle_view
│   │       └── 20230707_15_SY4_T1_vehicle_view.mp4
...
```
All pedestrian-related videos from BDD are stored under `external` folder:
```
external/
└── BDD_PC_5K
    ├── videos
    │   ├── train
        │   ├── video1004.mp4
        │   ├── video1006.mp4
        │   ├── video1009.mp4
        │   ├── video100.mp4
        │   ├── video1015.mp4
...
```

### Caption Data

Note that the videos from overhead_view and vehicle_view in the same scenario folder will share the same caption.

```
annotations
├──caption/
  ├── train
  │   ├── 20230707_12_SN17_T1 ##scenario index
  │   │   ├── overhead_view   
  │   │   │   └── 20230707_12_SN17_T1_caption.json   ##captions are shared by multiple views
  │   │   └── vehicle_view   
  │   │       └── 20230707_12_SN17_T1_caption.json   ##captions are the same as overhead view. Only timestamp may be different, in order to find the same phase in the vehicle view video.
  │   ├── 20230707_15_SY4_T1
  │   │   ├── overhead_view
  │   │   │   └── 20230707_15_SY4_T1_caption.json
  │   │   └── vehicle_view
  │   │       └── 20230707_15_SY4_T1_caption.json
...
```
Caption JSON format:
```
{
    "id": 722,
    "overhead_videos": [ ## caption related videos
        "20230707_8_SN46_T1_Camera1_0.mp4",
        "20230707_8_SN46_T1_Camera2_1.mp4",
        "20230707_8_SN46_T1_Camera2_2.mp4",
        "20230707_8_SN46_T1_Camera3_3.mp4"
    ],
    "event_phase": [
        {
            "labels": [
                "4"  ##segment number
            ],
            "caption_pedestrian": "The pedestrian stands still on the left side behind the vehicle, ...",  ##caption for pedestrian during the segment
            "caption_vehicle": "The vehicle was positioned diagonally to ...",  ##caption for vehicle during the segment
            "start_time": "39.395",  ##start time of the segment in seconds, 0.0 is the starting time of the given video.
            "end_time": "44.663"     ##end time of the segment in seconds
        },
...
```


## Data Preparation

We provide an example script to extract a video segment and its corresponding text descriptions via:

```
python script/data_sample.py
```

Note that:

- To reduce the required resources, all videos are downscaled into a resolution of `1280 x 720`.

- Users are free to partition video segment into condition history frames and target future frames to maximize data diversity and model performance. For evaluation, we will explicitly provide condition history frames and specify the expected number of target future frames to be generated.

- By default we seperately extract text descriptions for vehicles and pedestrians. However users are free to combine or augment the text descriptions for more effective text prompts.

## Data Split
The split of train/val/test part is provided in below:

### Train/Val Split
  - Main dataset
    - [Video](https://drive.google.com/drive/folders/1cl7oHj_v10yOzgS4kJS6lcfYkQBlq1r7?usp=drive_link)
    - [Caption](https://drive.google.com/drive/folders/1pjtUdOJR01OMY12C9FmOr3UNiSeNhAvk?usp=drive_link)
      
  - External dataset (BDD_PC_5K)
    - [Video](https://drive.google.com/file/d/1EJgLslKvyKMUyPC-aWR8YpzNZRBUu-gg/view?usp=drive_link)
    - [Caption](https://drive.google.com/file/d/1rzExQcjkuV3_C4WtDBRWHBwBiRnBzxtO/view?usp=drive_link)

### Test Split
 - To be released.

## Evaluation
To be released.

## License and Citation <a name="licenseandcitation"></a>
Please refer to our license from WTS dataset [homepage](https://woven-visionai.github.io/wts-dataset-homepage/)

Please consider citing our paper if you find WTS dataset is helpful for your works.
```BibTeX
@misc{kong2024wtspedestriancentrictrafficvideo,
      title={WTS: A Pedestrian-Centric Traffic Video Dataset for Fine-grained Spatial-Temporal Understanding}, 
      author={Quan Kong and Yuki Kawana and Rajat Saini and Ashutosh Kumar and Jingjing Pan and Ta Gu and Yohei Ozao and Balazs Opra and David C. Anastasiu and Yoichi Sato and Norimasa Kobori},
      year={2024},
      eprint={2407.15350},
      archivePrefix={arXiv},
      primaryClass={cs.CV},
      url={https://arxiv.org/abs/2407.15350}, 
}
```
