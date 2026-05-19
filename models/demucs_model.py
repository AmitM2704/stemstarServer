import subprocess
import os


class DemucsSeparator:

    def separate(self, input_file):

        os.makedirs(
            "separated",
            exist_ok=True
        )

        cmd = [

"demucs",

"--name",
"mdx_extra_q",

"--segment",
"2",

"--jobs",
"1",

"--shifts",
"1",

"--device",
"cpu",

input_file
]
        subprocess.run(
            cmd,
            check=True
        )

        return {
            "status": "done"
        }