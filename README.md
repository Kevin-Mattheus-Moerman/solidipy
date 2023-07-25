# SolidiPy
This is a simple Python project to help export `Minecraft-pi` builds for 3D printing. 

## Getting started
To use this script do the following: 
1. On your Raspberry pi, simply run `Minecraft-pi`
2. Create or open a world
3. Open your Python IDE (e.g. Thonny) and open and run the Python script called: `SolidiPy_grow.py`. This will create a cubic build space in your world. 
4. Build your structure on the build plate and within the build space (while keeping in mind the 3D printing constraints your printer might have, e.g. concerning overhangs and the need for support). You can use any solid block type(s) you like. Note only the boundary of the shape is exported, color or texture is not stored/exported at the moment. 
5. Once you are done making your structure select the sword and hit the structure using *right-click*. This will trigger the selection of this structure for conversion to the STL file. You will then see the structure slowly "turning to gold" as it is loaded to a 3D Python matrix which is then converted to an STL file. 

## Contributing
If you have any suggestions or are experiencing any problems, please post an issue here. 

To contribute please fork this repository, make changes, and submit a pull request. We welcome any contributions such as improvements to the code, examples, and documentation. 

## License
This project is licensed under the [MIT license](/LICENSE). 