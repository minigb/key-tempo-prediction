import argparse
import subprocess
import os
import shutil

KEY_EXEC = 'TCNTempoDetector'
TEMPO_EXEC = 'KeyRecognition'

def main():
    # Get file directory
    parser = argparse.ArgumentParser()
    parser.add_argument("in_dir", help = "Path to the directory with audio files")
    parser.add_argument("-o", "--out_dir", type = str, default = None, help = "Path to the directory to save labeling result")
    parser.add_argument('-f', '--force', action = 'store_true')
    args = parser.parse_args()

    in_dir = args.in_dir
    if not args.out_dir:
        args.out_dir = os.path.abspath(f'{in_dir}/../gtzan-label')

    if args.force and os.path.exists(args.out_dir):
        shutil.rmtree(args.out_dir)

    if not os.path.exists(args.out_dir):
        # Get all the audio files in the directory
        for root, _, files in os.walk(in_dir):
            dir_name = os.path.basename(root)
            wav_files = []
            for file_name in files:
                if file_name.lower().endswith('.wav'):
                    file_path = os.path.join(root, file_name)
                    wav_files.append(file_path)

            if not len(wav_files):
                continue

            result_dir = f'{args.out_dir}/{dir_name}'
            os.makedirs(result_dir, exist_ok = True)
            if len(wav_files):
                # Run executable files
                for exec in [KEY_EXEC, TEMPO_EXEC]:
                    command = [exec, 'batch'] + wav_files + ['-o', result_dir]
                    subprocess.run(command)

if __name__ == "__main__":
    main()