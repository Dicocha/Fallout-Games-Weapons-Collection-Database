import kagglehub


class Extractor:
    def __init__(self):
        self.handle = "wassimouledmohamed/fallout-new-vegas-weapons-dataset"
        self.local_path = "./archive"

    def download(self):
        # This downloads the dataset and returns the local path to the folder
        kagglehub.dataset_download(self.handle, output_dir=self.local_path)
        print("Download complete. Dataset is available at:", self.local_path)