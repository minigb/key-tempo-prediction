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
    out_dir = args.out_dir if args.out_dir else os.path.abspath(f'{in_dir}/../gtzan-label')

    if os.path.exists(out_dir) and not args.force:
        print(f'Result already exists at {out_dir}')
        return
    
    if os.path.exists(out_dir):
        shutil.rmtree(out_dir)
    os.makedirs(out_dir, exist_ok = True)
    
    # Get all the audio files in the directory
    for root, _, files in os.walk(in_dir):
        wav_files = []
        for file_name in files:
            if file_name.lower().endswith('.wav'):
                file_path = os.path.join(root, file_name)
                wav_files.append(file_path)

        if not len(wav_files):
            continue

        # Run executable files
        for exec in [KEY_EXEC, TEMPO_EXEC]:
            command = [exec, 'batch'] + wav_files + ['-o', out_dir]
            subprocess.run(command)

if __name__ == "__main__":
    main()