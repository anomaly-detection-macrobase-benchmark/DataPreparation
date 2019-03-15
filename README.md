Scripts for benchmark data preparation and benchmark results evaluation 

https://github.com/anomaly-detection-macrobase-benchmark/macrobase/tree/alexp-vmu/alexp/src/main/java/alexp/macrobase

https://www.draw.io/?lightbox=1&highlight=0000ff&edit=_blank&layers=1&nav=1&title=benchmark.xml#Uhttps%3A%2F%2Fdrive.google.com%2Fuc%3Fid%3D1680K8Opv09O7BPfbhmxHNfp9c3wMeriC%26export%3Ddownload

# Usage

Requirements:

- Python 3.7+
- [pipenv](https://pipenv.readthedocs.io/en/latest/)

Install dependencies by executing `pipenv install`. Use `pipenv shell` or `pipenv run` to run scripts (or use PyCharm, it should detect pipenv)

Example:

`cd preparation`

`pipenv run python describe.py original_datasets/shuttle-unsupervised-ad.csv --label is_anomaly`

Run scripts without arguments to get description and usage info (or look at the source code).
 
