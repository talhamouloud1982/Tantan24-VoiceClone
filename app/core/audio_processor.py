import subprocess
import os


class AudioProcessor:

    def enhance(self, input_file, output_file):

        os.makedirs(os.path.dirname(output_file), exist_ok=True)

        command = [
            "ffmpeg",
            "-y",
            "-i", input_file,
            "-af",
            (
                "highpass=f=80,"
                "lowpass=f=12000,"
                "loudnorm,"
                "acompressor=threshold=-18dB:ratio=2:"
                "attack=20:release=250"
            ),
            output_file
        ]

        subprocess.run(command, check=True)

        return output_file