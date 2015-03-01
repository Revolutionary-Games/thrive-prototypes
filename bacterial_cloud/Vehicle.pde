// The Nature of Code
// Daniel Shiffman
// http://natureofcode.com

// The "Vehicle" class (for wandering)

class Vehicle {

  PVector location;
  PVector velocity;
  PVector acceleration;
  float r;
  float maxforce;    // Maximum steering force
  float maxspeed;    // Maximum speed

  Wander_Steering ws;
  Gradient_Steering gs;
  
  Vehicle(float x, float y, Grid g) {
    acceleration = new PVector(0,0);
    velocity = new PVector(0,0);
    location = new PVector(x,y);
    r = 6;
    maxspeed = 2;
    maxforce = 0.05;
	
	ws = new Wander_Steering(0);
	gs = new Gradient_Steering(g);
  }

  void run() {
    
    PVector g = gs.CalcTarget(location, velocity, acceleration);
    PVector w = ws.CalcTarget(location, velocity, acceleration);
    
//    g.mult(5);
    g.normalize();
    w.normalize();
    g.mult(0.5);
    
    PVector targ = PVector.add(g,w); //gs.CalcTarget(location, velocity, acceleration), ws.CalcTarget(location, velocity, acceleration));
    targ.add(location);

    print("l : ", location, "| g : ", g, " | w : ", w, "| t : ", targ, "\n");

    seek(targ);
    
    ws.DisplayDebug();
    gs.DisplayDebug();

    update();
    borders();
    display();
  }

  // Method to update location
  void update() {
    // Update velocity
    velocity.add(acceleration);
    // Limit speed
    velocity.limit(maxspeed);
    location.add(velocity);
    // Reset accelertion to 0 each cycle
    acceleration.mult(0);
  }

  void applyForce(PVector force) {
    // We could add mass here if we want A = F / M
    acceleration.add(force);
  }


  // A method that calculates and applies a steering force towards a target
  // STEER = DESIRED MINUS VELOCITY
  void seek(PVector target) {
    PVector desired = PVector.sub(target,location);  // A vector pointing from the location to the target

    // Normalize desired and scale to maximum speed
    desired.normalize();
    desired.mult(maxspeed);
    // Steering = Desired minus Velocity
    PVector steer = PVector.sub(desired,velocity);
    steer.limit(maxforce);  // Limit to maximum steering force

    applyForce(steer);
  }

  void display() {
    // Draw a triangle rotated in the direction of velocity
    float theta = velocity.heading2D() + radians(90);
    fill(1);
    stroke(0);
    pushMatrix();
    translate(location.x,location.y);
    rotate(theta);
    beginShape(TRIANGLES);
    vertex(0, -r*2);
    vertex(-r, r*2);
    vertex(r, r*2);
    endShape();
    popMatrix();
  }

  // Wraparound
  void borders() {
    if (location.x < -r) location.x = width+r;
    if (location.y < -r) location.y = height+r;
    if (location.x > width+r) location.x = -r;
    if (location.y > height+r) location.y = -r;
  }
}
