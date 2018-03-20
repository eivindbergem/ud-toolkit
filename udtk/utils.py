from urllib.request import urlopen

from tqdm import tqdm

def download_file(url, filename, block_size=2**13):
    with filename.open("wb") as local:
        with urlopen(url) as remote:
            size = int(remote.getheader("content-length"))

            with tqdm(total=size, unit="B", unit_scale=True) as bar:
                while True:
                    block = remote.read(block_size)
                    local.write(block)

                    n = len(block)
                    bar.update(n)

                    if not n:
                        break
