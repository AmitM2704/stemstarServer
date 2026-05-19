import subprocess
import os


class DemucsSeparator:

    def separate(
        self,
        input_file
    ):

        cmd = [

            "demucs",

            "--name",
            "mdx_extra_q",

            "--segment",
            "1",

            "--jobs",
            "1",

            "--device",
            "cpu",

            input_file
        ]

        print(
            "Starting demucs"
        )

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=600
        )

        print(
            "STDOUT:",
            result.stdout
        )

        print(
            "STDERR:",
            result.stderr
        )

        if result.returncode != 0:

            raise Exception(
                result.stderr
            )

        print(
            "Demucs finished"
        )

        return {
            "stems":[]
        }