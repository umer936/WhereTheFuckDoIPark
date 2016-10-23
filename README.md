# SpotASpot

Frustrated with current parking procedures, we decided parking lots could be smarter. So we originally wanted to make an app and/or webapp to color where cars are and aren't to help a driver find a spot. However, as we were working, we realized that humans can see a picture just fine and that this technology would work much better for autonomous vehicles that cannot easily recognize objects. 

So, we used OpenCV to write a python script that takes an image of a parking lot and tells which spots are empty and which are not. This gives valuable information to all parties. 

The autonomous vehicle gets: 
- Current data on the closest parking spot (which means it will not be driving around until it finds one) 
- To the spot quicker (saving fuel [whether electric, gas, etc.])

The business owner gets: 
- Data regarding how full a lot section is
- Customers spending less time in the lot and more time in the store 

The best part: 
- It can potentially use existing CCTV/security cameras already installed in the lot for the data feed
- Cost is very little considering this can run on a RaspberryPi0

The future: 
- Once autonomous vehicles are more popular, this will encourage parking lots to be smarter. This means a car may be able to get data from multiple lots and pick the best one to park in based on spot availability and factor in parking lot prices. 
- Less movement in a parking lot means less chances for accidents (Hack-cidents?) 
- Humans getting where they need to be quicker 


## Installation & Usage

1. Clone repository using `https://github.com/umer936/spotAspot.git`
2. Install python and opencv
3. Run `python CarsByRows.py`

## Contributing

1. Fork it!
2. Create your feature branch: `git checkout -b my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin my-new-feature`
5. Submit a pull request :D

## Credits

Umer Salman
Jorge Rivero
Valeria Jara

## License

MIT License

## References

- http://tutorial.simplecv.org/en/latest/examples/parking.html
- http://tutorial.simplecv.org/en/latest/examples/display.html
- http://simplecv.readthedocs.io/en/1.1/cookbook/#colors-and-levels
- http://stackoverflow.com/questions/35447293/how-do-you-count-cars-in-opencv-with-python
