# AMTP - Accyourate Modified Pan-Tompkins

A tool to run and compare AMTP peak detection results with the Pan-Tompkins build algorhythm by Sara Pikus to compare accuracy and execution speed of the analysis.

## Installation

You can clone this project by running in your Terminal:
```
git clone https://github.com/Accyourate-Group-S-p-A/acy_ampt
```

To install dependencies in your Terminal use:
```
pip3 install -r requirements.txt 
```

### Depedencies:
- numpy;
- pandas;
- scipy;
- matplotlib;
- wfdb;

## How to download the Dataset
The Dataset downoad is mandatory.
You can download a .zip file containing the datasets ready to be processed by our tool from the following link:
https://mega.nz/file/Q1lDRaBK#LgtQ3YkLoN-h7Zc6B5Bg-uFI0stfI1SNP2FIUm3VzDQ

After the download exctract the zip contents and place the "ECG DBs" folder into the main directory of this project.

## Included datasets
- A1 - Physionet Challange 2014/A1 - High Quality - SET-P;
- A2 - Physionet Challange 2014/A2 - Low Quality - Training;
- B1 - MIT-BIH NSR & ARRHYTHMIA/B1 - NSR DB 1.0.0;
- B2 - MIT-BIH NSR & ARRHYTHMIA/B2 - ARRHYTHMIA DB 1.0.0;
- C - MIT-BIH Pacemaker Rhythm - part of ARRHYT DB;
- D - Harvard Telehealth DB;

## Usage
```
python3 run.py
```

1. Select the Dataset you would like to use;
2. Select if you want to resample the ECG to 200Hz;
3. Select which analysis algorhytjhm you want to use between:
    - AMTP;
    - PICKUS;


## Results
The results will be saved into "results" folder of this project directory as a .csv dataframe having as column:
- timing: the execution time in seconds;
- file: the name of the processed file;
- Our Peaks: peaks found by the choosen algorythm;
- Annotation Peaks: the peak count of the annotations;
- False Positive: the false positive;
- False Negative: the false negative;

## Authors
- [Antonio Augello](https://www.linkedin.com/in/antonio-augello-aba83911a/)
- [Luca Neri](https://www.linkedin.com/in/lucaneri-/)
- Matt T. Oberdier

## Credits
- [Sarah Pickus - Reprodution of Pam Tompkins](https://github.com/pickus91/HRV)

## License
[MIT](https://choosealicense.com/licenses/mit/)
