import time
from yaspin import yaspin

with yaspin(text="Downloading images", color="cyan") as sp:
    # task 1
    time.sleep(10)
    sp.write("> image 1 download complete")

    # task 2
    time.sleep(2)
    sp.write("> image 2 download complete")

    # finalize
    sp.ok("✔")