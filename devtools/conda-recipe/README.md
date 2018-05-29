## Instructions

```bash
conda config --set anaconda_upload no
conda build .
conda build . --output # If needed
anaconda login
anaconda upload --user uibcdf /path/to/conda-package.tar.bz2
conda build purge
anaconda logout
```

### Source
https://docs.anaconda.com/anaconda-cloud/user-guide/tasks/work-with-packages
