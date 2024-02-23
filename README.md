# GE slice time

There is a C source code `slicetime.cpp` to calculate the slice timing for GE scanner.
This python script accomplishes the same task.

For more information, please see https://github.com/rordenlab/dcm2niix/issues/635.

## prerequisite
- [numpy](https://numpy.org/)
- [python-fire](https://github.com/google/python-fire)

## usage
```python
python GE_slicetime.py MB DIM3 TR
```

The time for each slice will be printed and a slspec.txt file will be saved in current folder, which can be used in FSL's eddy.

For detailed information, run:
```python
python GE_slicetime.py
```
