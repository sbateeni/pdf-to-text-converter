import os
import requests
import zipfile
import stat

def get_latest_poppler_release():
    url = "https://api.github.com/repos/oschwartz10612/poppler-windows/releases/latest"
    response = requests.get(url)
    latest_release = response.json()
    version = latest_release['tag_name']
    for asset in latest_release['assets']:
        if asset['name'].endswith(".zip"):
            download_url = asset['browser_download_url']
            return version, download_url
    raise Exception("No zip file found in the latest release")

def download_and_extract_poppler(download_url, extract_to='.'):
    if not os.path.exists(extract_to):
        os.makedirs(extract_to)

    zip_file = os.path.join(extract_to, download_url.split('/')[-1])

    if not os.path.exists(zip_file):
        response = requests.get(download_url, stream=True)
        with open(zip_file, "wb") as f:
            for chunk in response.iter_content(chunk_size=1024):
                f.write(chunk)

    extracted_dir = os.path.join(extract_to, zip_file.replace(".zip", ""))
    if not os.path.exists(extracted_dir):
        with zipfile.ZipFile(zip_file, 'r') as zip_ref:
            zip_ref.extractall(extract_to)

    return extracted_dir

def setup_poppler():
    extract_to = './poppler'
    poppler_dir = None

    # Check if Poppler is already downloaded and extracted
    for root, dirs, files in os.walk(extract_to):
        for dir_name in dirs:
            if dir_name.startswith("poppler-"):
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
    print(f"Poppler setup completed. Path added: {poppler_bin_path}")

setup_poppler()
