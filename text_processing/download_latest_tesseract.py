import os
import requests

def download_latest_tesseract():
    url = "https://github.com/UB-Mannheim/tesseract/releases/latest"
    response = requests.get(url)
    if response.status_code == 200:
        print("GitHub API response:", response.text)
        latest_version = response.url.split("/")[-1]
        print("Latest version:", latest_version)
        download_url = f"https://github.com/UB-Mannheim/tesseract/releases/download/{latest_version}/Tesseract-OCR-{latest_version}-exe.zip"
        print("Download URL:", download_url)
        response = requests.get(download_url, stream=True)
        if response.status_code == 200:
            print("Download started")
            folder_name = "Tesseract at UB Mannheim"
            if not os.path.exists(folder_name):
                os.makedirs(folder_name)
            file_path = os.path.join(folder_name, f"Tesseract-OCR-{latest_version}-exe.zip")
            with open(file_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
            print("Download completed")
        else:
            print("Failed to download the latest version:", response.status_code)
    else:
        print("Failed to retrieve the latest version information:", response.status_code)

download_latest_tesseract()