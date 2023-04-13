import requests

download_file = "earthshine_brdf_fitting/cars_download_list.txt"
with open(download_file, 'r') as file:
    download_urls = file.read().splitlines()

with requests.Session() as session:

    for i, URL in enumerate(download_urls[::5]):
        result = session.get(URL)
        filename = "earthshine_brdf_fitting/cars_data/" + URL.split("/")[-1]
        try:
            result.raise_for_status()
            with open(filename, 'wb') as file:
                file.write(result.content)
            
            print(f'Contents of URL written to {filename}')
            print(f"{i}/{len(download_urls)}")
        except:
            print(f'Download failed, error code: {result.status_code}')