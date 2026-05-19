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

    "--overlap",
    "0.05",

    "--jobs",
    "1",

    "--shifts",
    "0",

    "--device",
    "cpu",

    input_file
]

        print(
            "Starting demucs"
        )

        subprocess.run(
            cmd,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE,
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