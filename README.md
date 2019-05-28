# ISMI project

3D UNet  for segmentation of the liver and liver tumors on CT scans of the thorax.

**Start script:**

```console
#!/bin/bash
#SBATCH -t 5-00:00:00
#SBATCH -N 1 -c 16
#SBATCH -p gpu
module load IPython/5.8.0-foss-2017b-Python-3.6.3
module load cuDNN/7.4.2-CUDA-10.0.130
pip install tensorflow-gpu --user
pip install keras --user
pip install tqdm --user
pip install SimpleITK --user
pip install h5py --user
pip install ipywidgets --user

jupyter nbextension install --py widgetsnbextension --user
jupyter nbextension enable --py widgetsnbextension --user
```
