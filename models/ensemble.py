from app.models.demucs_model import DemucsSeparator
from app.models.mdx_model import MDXSeparator


class EnsembleSeparator:

    def __init__(self):
        self.demucs = DemucsSeparator()
        self.mdx = MDXSeparator()

    def process(self, input_file):

        self.demucs.separate(input_file)