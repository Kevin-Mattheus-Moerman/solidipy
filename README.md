# SolidiPy

Please cite this work  using: [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.10552104.svg)](https://doi.org/10.5281/zenodo.10552104)



![](/assets/getStarted_03.jpg)

This is a simple Python project to help export `Minecraft-pi` builds for 3D printing. 

## Getting started
To use this script do the following: 
1. On your Raspberry pi, simply run `Minecraft-pi`
2. Create or open a world
3. Open your Python IDE (e.g. Thonny) and open and run the Python script called: `SolidiPy_grow.py`. This will create a cubic build space in your world. 
4. Build your structure on the build plate and within the build space (while keeping in mind the 3D printing constraints your printer might have, e.g. concerning overhangs and the need for support). You can use any solid block type(s) you like. Note only the boundary of the shape is exported, color or texture is not stored/exported at the moment. 
5. Once you are done making your structure select the sword and hit the structure using *right-click*. This will trigger the selection of this structure for conversion to the STL file. You will then see the structure slowly "turning to gold" as it is loaded to a 3D Python matrix which is then converted to an STL file. 
6. Finally you could slice your model and send it to the 3D printer

Notes on units. This code converts each solid minecraft block to a 1x1x1 cube in the 3D mesh. So if you import your model to a slicer for 3D printing, and the units are set to mm, then each block is 1 mm cubed. However, 3D printer slicer software allows you to rescale the models too if you like. 

## Contributing
If you have any suggestions or are experiencing any problems, please post an issue here. 

To contribute please fork this repository, make changes, and submit a pull request. We welcome any contributions such as improvements to the code, examples, and documentation. 

## License
This project is licensed under the [MIT license](/LICENSE). 
