from datasets import load_dataset
import pandas as pd
import os
import argparse


# helper function
def get_trackid_and_value(root, file_name):
    # Get track_id
    parts = file_name.split('.')
    track_id = '.'.join(parts[:2])

    # Get information saved in file
    with open(os.path.join(root, file_name), 'r') as f:
        text = f.readline().strip()
    
    return track_id, text


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input_dir", required = True, help = "Path to the directory to save labeling result")
    parser.add_argument("-o", "--output_dir", required = True, help = "Path to the directory to save labeling result")
    args = parser.parse_args()

    # input dir
    input_dir = args.input_dir
    assert os.path.exists(input_dir), f'{input_dir} does not exist'

    # output dir
    output_dir = args.output_dir

    # Get base gtzan-bind
    dataset = load_dataset(f'../dataset/seungheondoh/gtzan-bind') # TODO(minigb): Better way to handle this?
    assert len(dataset.keys()) == 1, f'Only one dataframe is needed'
    base_df = pd.DataFrame.from_dict(list(dataset.values())[0])

    # Create new dataframe for key and tempo
    key_tempo_df = pd.DataFrame(columns = ['track_id', 'base_key', 'pseudo_key', 'base_tempo', 'pseudo_tempo'])
    key_tempo_df['track_id'] = base_df['track_id']
    key_tempo_df['base_key'] = base_df['key']
    key_tempo_df['base_tempo'] = base_df['tempo_mean']

    for root, _, files in os.walk(input_dir):
        for file_name in files:
            if file_name.lower().endswith('key.txt'): # key
                track_id, key = get_trackid_and_value(root, file_name)
                key_tempo_df.loc[key_tempo_df['track_id'] == track_id, 'pseudo_key'] = key
                
            elif file_name.lower().endswith('bpm.txt'): # tempo
                track_id, tempo = get_trackid_and_value(root, file_name)
                key_tempo_df.loc[key_tempo_df['track_id'] == track_id, 'pseudo_tempo'] = float(tempo)

    key_tempo_df.to_csv(f'{output_dir}/gtzan_key_tempo_labeled.csv', index = False)

if __name__ == "__main__":
    main()