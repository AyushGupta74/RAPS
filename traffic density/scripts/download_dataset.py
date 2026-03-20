import kagglehub

def download():
    path = kagglehub.dataset_download("bratjay/ua-detrac-orig")
    print("Dataset downloaded at:", path)
    return path

if __name__ == "__main__":
    download()