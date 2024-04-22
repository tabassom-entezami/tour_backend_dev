import math
import shutil

from .convertor.libpano import Config, MetaData, Stitcher, utils
from .repositories import ProcessorRepository

import cv2 as cv
import os
import tempfile
import subprocess


class ProcessorService:
    def __init__(self, access_info, repo: ProcessorRepository):
        self.access_info = access_info
        self.repo = repo

    def get_start(self, access_info, image_folder_url):
        pass

    def process(self, images_folder, output_fn):
        meta = MetaData.MetaData(images_folder)

        # non-processed rows
        if meta.metrics.N_v == 4:
            other_rows = [0, 3]
        elif meta.metrics.N_v == 5:
            other_rows = [0, 1, 4]
        elif meta.metrics.N_v == 6:
            other_rows = [0, 1, 4, 5]
        elif meta.metrics.N_v == 7:
            other_rows = [0, 1, 5, 6]
        elif meta.metrics.N_v == 8:
            other_rows = [0, 1, 6, 7]
        elif meta.metrics.N_v == 9:
            other_rows = [0, 1, 2, 7, 8]
        else:
            print("\nERROR: number of rows should be in 4 ~ 9.\n")
            return -1

        temp_folder = tempfile.mkdtemp()
        meta_string = meta.meta_to_string()
        meta_file_name = os.path.join(temp_folder, Config.meta_data_name)
        f = open(meta_file_name, "w")
        f.write(meta_string)
        f.close()

        scale = math.sqrt(Config.internal_panorama_width / meta.metrics.PW)

        return_code = subprocess.call(
            ['processor/convertor/utils/pano-register',
             '--folder', images_folder,
             '--temp-folder', temp_folder,
             '--meta', meta_file_name,
             '--scale', str(scale)]
        )

        if return_code != 0:
            print("Error in registering frame images.")
            return -1

        if Config.mainframe_first:
            print("- Composing.....")
            return_code = subprocess.call(
                ['processor/convertor/utils/pano-composer',
                 '--folder', temp_folder,
                 '--config', Config.register_result_name,
                 '--mode', 'frame',
                 '--output', os.path.join(temp_folder, 'frame.jpg')]
            )

            if return_code != 0:
                print("Error in composing frame images.")
                return -1

        ############################################
        # Transforming other rows(not-mainframe rows)
        ############################################

        # Calculate the scale done by prestitcher
        # psr_name = os.path.join(temp_folder, Config.register_result_name)
        # psr_df = pd.read_csv(psr_name, header=0, delimiter=' ', names=['row', 'col' 'x', 'y', 'width', 'height'])

        # resizing, warping, and rotating
        stitcher = Stitcher.Stitcher(images_folder, temp_folder, meta)

        timer = utils.Timer()
        print('\n- Load and preprocess images.....', end='', flush=True)
        stitcher.load_and_preprocess(1.0, other_rows)
        print('{:.3f} seconds'.format(timer.end()))

        print('- Positioning images.....', end='')
        timer.begin()
        stitcher.position_frames(other_rows)
        print('{:.3f} seconds'.format(timer.end()))

        if Config.mainframe_first:
            print("- Composing.....")
            raw_output_name = os.path.join(temp_folder, 'panorama.jpg')
            return_code = subprocess.call(
                ['processor/convertor/utils/pano-composer',
                 '--folder', temp_folder,
                 '--config', Config.compose_config_name,
                 '--mode', 'full',
                 '--output', raw_output_name]
            )

            if return_code != 0:
                print("Error in composing frame images.")
                return -1

            output = cv.imread(raw_output_name)

        else:
            # Now, we don't need frames any more
            stitcher.frames = []

            # seam finding
            print('- Finding seams.....', end='', flush=True)
            timer.begin()
            stitcher.seam_find()
            print('{:.3f} seconds'.format(timer.end()))

            # blending images
            print('- Blending images.....', end='', flush=True)
            timer.begin()
            output = stitcher.blend_frames()
            print('{:.3f} seconds'.format(timer.end()))

        ############################################
        # Cropping, saving, removing temporary folder
        ############################################
        print('- Cropping and resizing.....', end='')
        timer.begin()

        height, width = output.shape[0], output.shape[1]
        cy = height // 2

        gray = cv.cvtColor(output, cv.COLOR_BGR2GRAY)
        middle_line = gray[cy, :]

        left = 0
        while middle_line[left] == 0:
            left += 1

        right = width - 1
        while middle_line[right] == 0:
            right -= 1

        roi_width = right - left
        roi_height = roi_width // 2 - 200
        top = (height - roi_height) // 2

        cropped = output[top:(top + roi_height), left:(left + roi_width), :]
        output = cv.resize(cropped, (4096, 2048), 0, 0, cv.INTER_LINEAR_EXACT)

        cv.imwrite(output_fn, output)

        try:
            shutil.rmtree(temp_folder)
        except OSError:
            pass

