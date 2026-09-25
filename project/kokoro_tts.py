import soundfile as sf
import sounddevice as sd
import numpy as np
from kokoro import KPipeline

def main():
    print("Loading Kokoro TTS model (English)...")
    # 'a' = American English, 'b' = British English, 'j' = Japanese, 'z' = Mandarin, etc.
    pipeline = KPipeline(lang_code='h')

    # Popular voice options: 'af_heart', 'af_bella', 'af_sarah', 'am_adam', 'am_michael'
    voice = 'hf_alpha'
    sample_rate = 24000

    print("Type your text below and press Enter to generate speech (Type 'exit' or 'q' to quit).\n")

    while True:
        try:
            text = input("Enter text: ").strip()
            if not text:
                continue
            if text.lower() in ('exit', 'q', 'quit'):
                print("Exiting...")
                break

            print("Generating speech...")
            # pipeline yields chunks of: (graphemes, phonemes, audio_array)
            generator = pipeline(text, voice=voice, speed=1.0)
            
            all_audio = []
            for _, _, audio in generator:
                all_audio.append(audio)

            if all_audio:
                full_audio = np.concatenate(all_audio)

                # 1. Play audio in real-time
                print("Playing audio...")
                sd.play(full_audio, samplerate=sample_rate)
                sd.wait()

                # 2. Save audio to WAV file
                # output_filename = "output.wav"
                # sf.write(output_filename, full_audio, sample_rate)
                # print(f"Saved speech to '{output_filename}'\n")

        except KeyboardInterrupt:
            print("\nSession ended.")
            break
        except Exception as e:
            print(f"Error: {e}\n")

if __name__ == "__main__":
    main()