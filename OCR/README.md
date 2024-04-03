# Optical Character Recogition Usage

The map images consist of either Discrete Legends or Colour Bars, each of them having a certain value corresponding to a distinct colour.
In order to gain insights into the contents of the map image, we leveraged the use of OCR models to extract relevant information regarding the values present in the image.

We tried several different models for this task before settling on using **PaddleOCR**.

The models we tried are mentioned as separate folders and the Jupyter Notebooks we used for each are listed in the folders respectively. Each notebook has certain updates and hence there are multiple variations of the same. An example output is also provided for each of these models' outputs.

## Models Used

- KerasOCR
- TesseractOCR
- PaddleOCR
