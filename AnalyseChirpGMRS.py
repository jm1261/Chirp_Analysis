import time
import logging
import Functions as func

config_filepath = './CPR_configuration.ini'
log_filepath = 'ChirpAnalysis.log'
log_level = logging.DEBUG
logger = func.setup_logger(log_filepath, log_level)

params = func.get_simulation_params(logger, config_filepath)
params['log_filepath'] = log_filepath
params['log_level'] = log_level

roi_array = None

filenames_old = list()
while True:
    image_files = func.get_image_filenames(logger, params, filenames_old)
    filenames_old.extend(image_files)

    if image_files:  # Check if there are images ready to be processed
        print(f'{len(image_files)} files will now be processed')
        logger.info(f'{len(image_files)} files processed')
        if not roi_array:
            roi_array = func.register_ROIs(logger, params, image_files)
        func.process_images(logger, params, image_files, roi_array)
        func.save_data(logger, params, roi_array)
        func.plot_data(params, filenames_old, roi_array)
        break

    if params['sleep_time'] > 0:
        print(f"Waiting for {params['sleep_time']} minutes")
        logger.info(f"...Sleeping for {params['sleep_time']} minutes")
        time.sleep(params['sleep_time'] * 60)
