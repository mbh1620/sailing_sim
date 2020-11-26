
# Sailing Simulator

The aim is to have a boat automatically plot a route from A to B depending on where the wind is coming from. This boat will 
then be able to sail from A to B in the fastest possible way adjusting its sails in the process.

When travelling upwind the boat cannot sail directly into the wind, so the boat will have to work out a zig zagged approach to going upwind.
This will also mean that it will have to know when the best time to tack is.

# Improvements to be made:

So far I have the boats travelling around a course, however there still needs to be some improvements. 

When going upwind and downwind the sails need 
to be on the correct side of the boat. 

I also need to add the zig zagged approach to going upwind.

After this I then need to add more specific points of sail such as beam reach etc.

To be used on a real boat a PID control loop would need to be used to keep the steering constant.

Also a moving average filter could be applied to a wind vane sensor so that the wind direction can be accurately sensed. This would then 
allow the sail to be set at the correct position.

<html>
<iframe width="560" height="315" src="https://www.youtube.com/embed/z4esDaaClTE" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
</html>

[![IMAGE ALT TEXT](https://www.youtube.com/embed/z4esDaaClTE)](https://www.youtube.com/embed/z4esDaaClTE "Sailing fleet")

![photo2](https://github.com/mbh1620/sailing_sim/blob/master/sailing.gif)

![photo3](https://safe-skipper.com/wp-content/uploads/2019/06/36.1_Points-of-sail-1.jpg)

Link to some common race courses (https://www.fisherrowyachtclub.com/index.php/racing/courses-dinghy)
