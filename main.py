import os
import moviepy.editor as mp
import whisper

def convert_video_to_audio(video_path, audio_path):
    """Converts video to audio."""
    video_clip = mp.VideoFileClip(video_path)
    audio_clip = video_clip.audio
    audio_clip.write_audiofile(audio_path)
    audio_clip.close()
    video_clip.close()

def transcribe_audio(audio_path, output_srt_file):
    """Transcribes audio and saves the output in an .srt file."""
    audio = whisper.load_audio(audio_path)
    model = whisper.load_model("base")
    result = whisper.transcribe(model, audio, language="en")

    with open(output_srt_file, "w") as f:
        for i, segment in enumerate(result['segments'], start=1):
            start_time = f"00:00:{str(int(segment['start'])).replace('.', ',')}"
            end_time = f"00:00:{str(int(segment['end'])).replace('.', ',')}"
            text = segment['text'].strip()
            f.write(f"{i}\n{start_time} --> {end_time}\n{text}\n\n")

def process_video(video_file, audio_output_folder, srt_output_folder):
    """Process a single video file."""
    video_name = os.path.splitext(os.path.basename(video_file))[0]
    audio_path = os.path.join(audio_output_folder, f"{video_name}.wav")
    output_srt_file = os.path.join(srt_output_folder, f"{video_name}.srt")

    # Convert video to audio
    convert_video_to_audio(video_file, audio_path)

    # Transcribe audio and save the output in an .srt file
    transcribe_audio(audio_path, output_srt_file)

def main():
    input_folder = "input_files"
    audio_output_folder = "audio_outputs"
    srt_output_folder = "srt_outputs"

    # Create output folders if they don't exist
    os.makedirs(audio_output_folder, exist_ok=True)
    os.makedirs(srt_output_folder, exist_ok=True)

    # Iterate over all .mp4 files in the input folder
    for filename in os.listdir(input_folder):
        if filename.endswith(".mp4"):
            video_file = os.path.join(input_folder, filename)
            process_video(video_file, audio_output_folder, srt_output_folder)

if __name__ == "__main__":
    main()
