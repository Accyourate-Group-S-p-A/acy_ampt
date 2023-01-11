from pick import pick

def main():

    resample = False
    pan_to_use = 0
    pan = False

    title = 'Please choose which Dataset you would like to run: '
    options = ['A1', 'A2', 'B1', 'B2', 'C', 'D']

    option, index = pick(options, title, indicator='=>', default_index=0)

    title_resample = 'Do you want to resample to 200 Hz the traces? '
    options_resample = ['Yes', 'No']

    options_resample, index_resample = pick(options_resample, title_resample, indicator='=>', default_index=0)

    if index_resample == 0:
        resample = True
    else:
        resample = False

    title_select_algorhythm = 'Which Algorhythm do you want to use? '
    options_select_algorhythm = ['AMPT', 'PICKUS']

    options_select_algorhythm, index_select_algorhythm = pick(options_select_algorhythm, title_select_algorhythm, indicator='=>', default_index=0)

    if index_select_algorhythm == 0:
        pan = False
    if index_select_algorhythm == 1:
        pan = True
        pan_to_use = 1
    if index_select_algorhythm == 2:
        pan = True
        pan_to_use = 2

    if index == 0:
        """ A1 """
        from runners.run_mit_resample import main
        path = "ECG DBs/A - Physionet Challange 2014/A1 - High Quality - SET-P/"

        fs = 250
        main(path, fs, "results/A1/", pan=pan, plot=False, pan_to_use=pan_to_use, resample_ecg=resample)

    if index == 1:
        """ A2 """
        from runners.run_mit_resample import main
        path = "ECG DBs/A - Physionet Challange 2014/A2 - Low Quality - Training/"

        fs = 360 
        main(path, fs, "results/A2/", pan=pan, plot=False, pan_to_use=pan_to_use, resample_ecg=resample)

    if index == 2:
        """ B1 """
        from runners.run_mit_resample import main
        path = "ECG DBs/B - MIT-BIH NSR & ARRHYTHMIA/B1 - NSR DB 1.0.0/"

        fs = 128
        main(path, fs, "results/B1/", pan=pan, plot=False, pan_to_use=pan_to_use, resample_ecg=resample)

    if index == 3:
        """ B2 """
        from runners.run_mit_resample import main
        path = "ECG DBs/B - MIT-BIH NSR & ARRHYTHMIA/B2 - ARRHYTHMIA DB 1.0.0/"

        fs = 360
        main(path, fs, "results/B2/", pan=pan, plot=False, pan_to_use=pan_to_use, resample_ecg=resample)

    if index == 4:
        """ C """
        from runners.run_mit_resample import main
        path = "ECG DBs/C - MIT-BIH Pacemaker Rhythm - part of ARRHYT DB/"

        fs = 360
        main(path, fs, "results/C/", pan=pan, plot=False, pan_to_use=pan_to_use, resample_ecg=resample)

    if index == 5:
        """ D """
        from runners.run_mit_d_new import main
        path = "ECG DBs/D - Harvard Telehealth DB/"

        fs = 500
        main(path, fs, "results/D/", pan=pan, plot=False, pan_to_use=pan_to_use, resample_ecg=resample)

main()