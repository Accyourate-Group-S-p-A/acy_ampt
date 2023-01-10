# AMTP - RUN AND COMPARE

Accyourate Modified Pam Tompkins Algorhythm.
A tool to run and compare AMTP with the Pam Tompkins build algorhythm by
- PIKUS;

## Installation

You can clone this project by running in yout Terminal:
```
git clone https://github.com/Accyourate-Group-S-p-A/acy_ampt
```

To install dependencies in your Terminal use:
```
pip3 install -r requirements.txt 
```

## Dataset Download
The Dataset downoad is mandatory.
You can download a .zip file containing the datasets ready to be processed by our tool from the following link:
https://mega.nz/file/Q1lDRaBK#LgtQ3YkLoN-h7Zc6B5Bg-uFI0stfI1SNP2FIUm3VzDQ

After the download exctract the zip contents and place the "ECG DBs" folder into the main directory of this project.

## Included datasets

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

## Contributing
- [Antonio Augello](https://www.linkedin.com/in/antonio-augello-aba83911a/)
- [Luca Neri](https://www.linkedin.com/in/lucaneri-/)
- Matt T. Oberdier

## Credits
- [Sarah Pickus - Reprodution of Pam Tompkins](https://github.com/pickus91/HRV)


## License

[MIT](https://choosealicense.com/licenses/mit/)
