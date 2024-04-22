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

def main():
    video_path = "video2.mp4"
    audio_path = "output_audio.wav"
    output_srt_file = "output.srt"

    # Convert video to audio
    convert_video_to_audio(video_path, audio_path)

    # Transcribe audio and save the output in an .srt file
    transcribe_audio(audio_path, output_srt_file)

if __name__ == "__main__":
    main()
