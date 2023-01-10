# AMTP - RUN AND COMPARE

Accyourate Modified Pam Tompkins Algorhythm.
A tool to run and compare AMTP with the Pam Tompkins build algorhythm by
- PIKUS;

## Installation

You can clone this project by running in yout Terminal:
```
git clone ["name repo"]
```

To install dependencies in your Terminal use:
```
pip3 install -r requirements.txt 
```

## Dataset Download
https://mega.nz/file/Q1lDRaBK#LgtQ3YkLoN-h7Zc6B5Bg-uFI0stfI1SNP2FIUm3VzDQ

## Usage
```
python run.py
```

1. Select the Dataset you would like to use;
2. Select if you want to resample the ECG to 200Hz;
3. Select which analysis algorhytjhm you want to use between:
    - AMTP;
    - PICKUS;


## Results
The results will be saved into "results" folder of this project directory as a pandas dataframe having as column:
- timing: the execution time in seconds;
- file: the name of the processed file;
- Our Peaks: peaks found by the choosen algorythm;
- Annotation Peaks: the peak count of the annotations;
- False Positive: the false positive;
- False Negative: the false negative;

## Contributing
- [Antonio Augello](https://www.linkedin.com/in/antonio-augello-aba83911a/)
- [Luca Neri](https://www.linkedin.com/in/lucaneri-/)


## Credits
- [Sarah Pickus](https://github.com/pickus91/HRV)


## License

[MIT](https://choosealicense.com/licenses/mit/)
