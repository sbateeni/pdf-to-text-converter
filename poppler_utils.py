import os
import requests
import zipfile
import stat
import shutil
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

def is_poppler_installed():
    """Check if poppler is already in PATH."""
    return shutil.which('pdfinfo') is not None

def get_latest_poppler_release():
    try:
        url = "https://api.github.com/repos/oschwartz10612/poppler-windows/releases/latest"
        response = requests.get(url, timeout=10)
        latest_release = response.json()
        version = latest_release['tag_name']
        for asset in latest_release['assets']:
            if asset['name'].endswith(".zip"):
                download_url = asset['browser_download_url']
                return version, download_url
        raise Exception("No zip file found in the latest release")
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to get latest Poppler release: {str(e)}")
        # Fallback to a known working version
        version = "v24.02.0-0"
        download_url = f"https://github.com/oschwartz10612/poppler-windows/releases/download/{version}/Release-{version}.zip"
        return version, download_url

def download_and_extract_poppler(download_url, extract_to='.'):
    try:
        if not os.path.exists(extract_to):
            os.makedirs(extract_to)

        zip_file = os.path.join(extract_to, download_url.split('/')[-1])
        extracted_dir = os.path.join(extract_to, Path(zip_file).stem)

        # If already extracted, return the path
        if os.path.exists(extracted_dir):
            return extracted_dir

        if not os.path.exists(zip_file):
            logger.info("Downloading Poppler...")
            response = requests.get(download_url, stream=True, timeout=30)
            with open(zip_file, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

        logger.info("Extracting Poppler...")
        with zipfile.ZipFile(zip_file, 'r') as zip_ref:
            zip_ref.extractall(extract_to)

        return extracted_dir
    except Exception as e:
        logger.error(f"Error downloading/extracting Poppler: {str(e)}")
        raise

def setup_poppler():
    """Set up Poppler and add it to PATH if not already available."""
    if is_poppler_installed():
        logger.info("Poppler is already installed and in PATH")
        return True

    try:
        extract_to = './poppler'
        poppler_dir = None

        # Check if Poppler is already downloaded and extracted
        if os.path.exists(extract_to):
            for root, dirs, files in os.walk(extract_to):
                for dir_name in dirs:
                    if dir_name.startswith("Release-"):
                        poppler_dir = os.path.join(root, dir_name)
                        break

        # If Poppler is not found, download and extract it
        if not poppler_dir:
            version, download_url = get_latest_poppler_release()
            poppler_dir = download_and_extract_poppler(download_url, extract_to)

        poppler_bin_path = os.path.join(poppler_dir, "Library", "bin")

        # Ensure all files in poppler_path have the correct permissions
        for root, dirs, files in os.walk(poppler_bin_path):
            for file in files:
                file_path = os.path.join(root, file)
                os.chmod(file_path, stat.S_IEXEC | stat.S_IREAD)

        # Add poppler_path to system PATH
        os.environ['PATH'] += os.pathsep + os.path.abspath(poppler_bin_path)
        logger.info(f"Poppler setup completed. Path added: {poppler_bin_path}")
        return True

    except Exception as e:
        logger.error(f"Failed to setup Poppler: {str(e)}")
        return False
