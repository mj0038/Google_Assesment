import os
import shutil
from pydub import AudioSegment

# Base and output directory 
audio_files_dir = 'audio_files'
output_dir = 'organized_audio_files'

os.makedirs(output_dir, exist_ok=True)

# Parse the file name and extract genre and artifact status
def parse_file_name(file_name):
    parts = file_name.split('_')
    if len(parts) < 5:
        raise ValueError(f"Invalid file name format: {file_name}")
    
    genre = parts[3]  # Extract genre (e.g., "pianomusic")
    artifact_status = parts[4].split('.')[0]  # Extract artifact status
    return genre, artifact_status

# Function to determine the duration category
def get_duration_category(duration):
    if duration < 30:
        return 'short'
    elif 30 <= duration <= 180:
        return 'medium'
    else:
        return 'long'

# Iterate over all files 
for file_name in os.listdir(audio_files_dir):
    if file_name.endswith('.wav'):
        file_path = os.path.join(audio_files_dir, file_name)
        
        try:
            # Parse the file name to get genre and artifact status
            genre, artifact_status = parse_file_name(file_name)
            
            # Load the audio file and calculate its duration in seconds
            audio = AudioSegment.from_wav(file_path)
            duration = len(audio) / 1000  # milliseconds to seconds
            
            # Determine the duration category
            duration_category = get_duration_category(duration)
            
            # Create the target directory and copy it
            target_dir = os.path.join(output_dir, genre, artifact_status, duration_category)
            os.makedirs(target_dir, exist_ok=True)
            shutil.copy(file_path, os.path.join(target_dir, file_name))
            
            print(f"Organized: {file_name} -> {target_dir}")
        except Exception as e:
            print(f"Error processing {file_name}: {e}")

print("Organization complete!")
