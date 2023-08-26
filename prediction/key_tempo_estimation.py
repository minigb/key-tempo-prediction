import argparse
import subprocess
import os
import shutil

# TODO(minigb): Create an additional file for constants
# TODO(minigb): This is assuming that you are in the same directory with this file
DATASET_PATH = os.path.abspath('../dataset')
GTZAN_AUDIO_PATH = f'{DATASET_PATH}/gtzan-audio'
GTZAN_LABEL_PATH = os.path.abspath('../gtzan-label')
EXEC = {'key' : 'KeyRecognition',
        'tempo' : 'TCNTempoDetector'}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input_dir", default = None, help = "Path to the directory with audio files")
    parser.add_argument("-o", "--output_dir", default = None, help = "Path to the directory to save labeling result")
    parser.add_argument("-t", "--target_list", nargs = '+', default = None, help = "Things to estimate")
    parser.add_argument('-f', '--force', action = 'store_true', help = "Whether to force the execution even if the result exists")
    args = parser.parse_args()

    # input dir
    input_dir = args.input_dir if args.input_dir else GTZAN_AUDIO_PATH
    assert os.path.exists(input_dir), f'{input_dir} does not exist'

    # output dir
    output_dir = args.output_dir if args.output_dir else GTZAN_LABEL_PATH

    # targets
    target_list = args.target_list if args.target_list else list(EXEC.keys())
    for target in target_list:
        assert target in EXEC.keys(), f'Unable to predict {target}. Only {list(EXEC.keys())} are available'

    # Get all of the audio files in the input directory
    wav_files = []
    for root, _, files in os.walk(input_dir):
        for file_name in files:
            if file_name.lower().endswith('.wav'):
                file_path = os.path.join(root, file_name)
                wav_files.append(file_path)
    if not len(wav_files):
        return

    # Run executable files to predict
    for target in target_list:
        print('-' * 10)
        print(target)

        target_dir = f'{output_dir}/{target}'
        if os.path.exists(target_dir):
            if args.force:
                shutil.rmtree(target_dir) # remove existing directory
            else:
                print(f'Result already exists in {target_dir}')
                continue

        os.makedirs(target_dir)
        command = [EXEC[target], 'batch'] + wav_files + ['-o', target_dir]
        subprocess.run(command)
        print('Done')

if __name__ == "__main__":
    main()