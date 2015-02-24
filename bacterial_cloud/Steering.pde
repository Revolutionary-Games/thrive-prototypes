
class Steering
{
	PVector force;

	Steering()
	{
		force = new PVector(0,0);
	}
	
        PVector CalcTarget(PVector location, PVector velocity, PVector acceleration) 
        { return new PVector(0,0); }
	void calcForce(){}
}


class Wander_Steering extends Steering
{
	float wandertheta;
	
	Wander_Steering(float wanderTheta)
	{
		super();
		wandertheta = wanderTheta;
	}
	
	PVector CalcTarget(PVector location, PVector velocity, PVector acceleration) {
		float wanderR = 25;         // Radius for our "wander circle"
		float wanderD = 80;         // Distance for our "wander circle"
		float change = 0.3;
		wandertheta += random(-change,change);     // Randomly change wander theta

		// Now we have to calculate the new location to steer towards on the wander circle
		PVector circleloc = velocity.get();    // Start with velocity
		circleloc.normalize();            // Normalize to get heading
		circleloc.mult(wanderD);          // Multiply by distance
//		circleloc.add(location);               // Make it relative to boid's location
		
		float h = velocity.heading2D();        // We need to know the heading to offset wandertheta

		PVector circleOffSet = new PVector(wanderR*cos(wandertheta+h),wanderR*sin(wandertheta+h));
		PVector target = PVector.add(circleloc,circleOffSet);

		// Set debug drawing variables
		d_location = location;
		d_circle = PVector.add(circleloc, location); 
		d_target = PVector.add(target, location);
		d_rad = wanderR;
		
		return target;
	}  

	// Variables for drawing debug display
	PVector d_location;
	PVector d_circle;
	PVector d_target;
	float d_rad;
	
	void DisplayDebug()
	{
		stroke(1); 
		noFill();
		ellipseMode(CENTER);
		ellipse(d_circle.x,d_circle.y,d_rad*2,d_rad*2);
		ellipse(d_target.x,d_target.y,4,4);
		line(d_location.x,d_location.y,d_circle.x,d_circle.y);
		line(d_circle.x,d_circle.y,d_target.x,d_target.y);
	}
}

class Gradient_Steering extends Steering
{
	Grid target_field;
	
	Gradient_Steering(Grid target)
	{
		super();
		target_field = target;
	}
	
	PVector CalcTarget(PVector location, PVector velocity, PVector acceleration) 
	{
		PVector target = target_field.GradAt(location);

		d_location = location;
		d_target = new PVector(target.x, target.y);

//                target.add(location);        

                return target;
	}
	
	// Debug variables
	PVector d_location;
	PVector d_target;
	
	void DisplayDebug()
	{
		stroke(1);
		noFill();
                float ln = 10;
		line(d_location.x, d_location.y, d_location.x + (ln * d_target.x), d_location.y + (ln * d_target.y));
//                line(d_location.x, d_location.y, d_target.x, d_target.y);
	}
}
