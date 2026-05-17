import os


class DemucsSeparator:

    def separate(self, input_file):

        command = (
            f"demucs --two-stems=vocals {input_file}"
        )

        os.system(command)