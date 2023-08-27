import argparse
import subprocess
import os
import shutil

# TODO(minigb): Create an additional file for constants
EXEC = {'key' : 'KeyRecognition',
        'tempo' : 'TCNTempoDetector'}
AUDIO_FILE_TYPE = ['wav', 'mp3', 'flac']

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input_dir", required = True, help = "Path to the directory with audio files")
    parser.add_argument("-o", "--output_dir", required = True, help = "Path to the directory to save labeling result")
    parser.add_argument("-t", "--target_list", nargs = '+', default = None, help = "Things to estimate")
    parser.add_argument('-f', '--force', action = 'store_true', help = "Whether to force the execution even if the result exists")
    args = parser.parse_args()

    # input dir
    input_dir = args.input_dir
    assert os.path.exists(input_dir), f'{input_dir} does not exist'

    # output dir
    output_dir = args.output_dir

    # targets
    target_list = args.target_list if args.target_list else list(EXEC.keys())
    for target in target_list:
        assert target in EXEC.keys(), f'Unable to predict {target}. Only {list(EXEC.keys())} are available'

    # Get all of the audio files in the input directory
    audio_files = []
    for root, _, files in os.walk(input_dir):
        for file_name in files:
            for file_type in AUDIO_FILE_TYPE:
                if file_name.lower().endswith(f'.{file_type}'):
                    file_path = os.path.join(root, file_name)
                    audio_files.append(file_path)
    print(f'Found {len(audio_files)} audio files')

    if not len(audio_files):
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
        command = [EXEC[target], 'batch'] + audio_files + ['-o', target_dir]
        subprocess.run(command)
        print('Done')

if __name__ == "__main__":
    main()