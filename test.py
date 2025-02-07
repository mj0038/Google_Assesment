import os
from pydub import AudioSegment
from collections import defaultdict

# Define directories
base_dir = "organized_audio_files"
expected_artifacts = {"gap", "clean", "glitch", "noise", "static"}
expected_durations = {"short", "medium", "long"}

# Summary storage
summary = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))
errors = []

# Function to check duration category
def get_expected_duration_category(duration):
    if duration < 30:
        return "short"
    elif 30 <= duration <= 180:
        return "medium"
    else:
        return "long"

# Walk through organized files
for genre in os.listdir(base_dir):
    genre_path = os.path.join(base_dir, genre)
    
    if not os.path.isdir(genre_path):
        continue  # Skip non-directory files
    
    found_artifacts = set()
    
    for artifact in os.listdir(genre_path):
        artifact_path = os.path.join(genre_path, artifact)
        
        if not os.path.isdir(artifact_path):
            continue
        
        found_artifacts.add(artifact)
        found_durations = set()
        
        for duration_category in os.listdir(artifact_path):
            duration_path = os.path.join(artifact_path, duration_category)
            
            if not os.path.isdir(duration_path):
                continue
            
            found_durations.add(duration_category)

            # Verify each file's duration
            for file_name in os.listdir(duration_path):
                if file_name.endswith(".wav"):
                    file_path = os.path.join(duration_path, file_name)
                    
                    try:
                        # Load audio file to check duration
                        audio = AudioSegment.from_wav(file_path)
                        actual_duration = len(audio) / 1000  # Convert ms to sec
                        expected_category = get_expected_duration_category(actual_duration)

                        if expected_category != duration_category:
                            errors.append(
                                f"Misplaced file: {file_name} (Actual: {actual_duration}s, Expected: {expected_category}, Found: {duration_category})"
                            )

                        # Update summary
                        summary[genre][artifact][duration_category] += 1

                    except Exception as e:
                        errors.append(f"Error processing {file_name}: {e}")

        # Check if all duration categories exist under each artifact
        missing_durations = expected_durations - found_durations
        if missing_durations:
            errors.append(f"Missing duration categories in {genre}/{artifact}: {missing_durations}")

    # Check if all artifact types exist under each genre
    missing_artifacts = expected_artifacts - found_artifacts
    if missing_artifacts:
        errors.append(f"Missing artifact categories in {genre}: {missing_artifacts}")

# Print summary
print("\nAudio File Organization Summary:")
for genre, artifacts in summary.items():
    print(f"\n{genre}:")
    for artifact, durations in artifacts.items():
        print(f"  {artifact}:")
        for duration, count in durations.items():
            print(f"    {duration}: {count} files")

# Print errors if any
if errors:
    print("\nErrors Found:")
    for err in errors:
        print(f"  - {err}")
else:
    print("\nAll files are correctly organized.")

print("\nValidation Complete.")
