// Includes

int time = 0;

// Grid setup
int xs = 50;
int ys = 30;
int w = 30;

Vehicle[] agents;
boolean debug = true;

Arr2d mask;
GridLayers compounds;
GridLayers bacteria;

void setup(){
  colorMode(RGB, 1);
  
  size(xs*w,ys*w);
  
  
  mask = new Arr2d(new float[][]{{0.707,1,0.707},{1,0,1},{0.707,1,0.707}});
  mask.Mult(0.01);
  mask.data[1][1] = -mask.Sum();

  compounds = new GridLayers();
  compounds.Add(new Grid(xs,ys,w), color(1,0,0));
  compounds.Add(new Grid(xs,ys,w), color(0,1,0));
  compounds.Add(new Grid(xs,ys,w), color(0,0,1));
  
  bacteria = new GridLayers();
  bacteria.Add(new Grid(xs,ys,w), color(0,1,1));
  
  agents = new Vehicle[3];
  agents[0] = new Vehicle(w * xs/2, (w * ys) * 1 / 4, compounds.get(2));
  agents[1] = new Vehicle(w * xs/2, (w * ys) * 2 / 4, compounds.get(2));
  agents[2] = new Vehicle(w * xs/2, (w * ys) * 3 / 4, compounds.get(0));
//  for(int i = 0; i < 3; i++)
//  if (i == 2)
//    agents[i] = new Vehicle(w * xs/2, (w * ys) * (i + 1) / 4, compounds.get(2));
//  else
//    agents[i] = new Vehicle(w * xs/2, (w * ys) * (i + 1) / 4, compounds.get(0));
          
//  PrintArr2d(mask.data);
//  Arr2d co = new Arr2d(mask.data);
//  PrintArr2d(co.data);
//  co.data[1][1] = 5;
//  PrintArr2d(co.data);
//  PrintArr2d(mask.data);
  
//  mask.Mult(mask);
//  print("\n");
//  PrintArr2d(mask.data);
}

int i = 0;

void draw(){
  if(millis() > time)
  { // update at most 20 times per second
//    time = millis() + 50;
    background(0);
    
    // Diffuse and display compounds
    compounds.Diffuse(mask);
    compounds.Display();
    
    // React, diffuse, and display bacteria
    bacteria.get(0).data.data[xs/4][ys/2] = 1; // Seed population
    bacteria.get(0).React(compounds.get(0), compounds.get(1), compounds.get(2));
    bacteria.Diffuse(mask);
    bacteria.DisplayEdges();

//    Arr2d temp = new Arr2d(compounds.get(0).data);
////    temp.Add(compounds.get(1).data);
//    Grid g = new Grid(temp, w);
//    g.DisplayEdges(color(1,1,1));

    // Move and display agents
    for(int i = 0; i < 3; i++)
      {
        agents[i].run();
        
        // Agents leak compounds
        compounds.get(i).AddAt(agents[i].location, .2);
        if( i < 2)
        compounds.get(2).AddAt(agents[i].location, -1);
        else
        compounds.get(0).AddAt(agents[i].location, -1);
      }
      
    // Test gradient at current mouse position
    PVector m = new PVector(mouseX, mouseY);
    PVector g = compounds.get(2).GradAt(m);
    
    noFill();
    stroke(1);
    line(m.x,m.y,m.x + (5* g.x), m.y + (5 * g.y));
  }
}

void PrintArr2d(float[][] data)
{
  for(int i = 0; i < data.length; i++)
  {
      print("\n");
  for(int j = 0; j < data[i].length; j++)
     if(j == 0)
       print(data[i][j]);
     else
       print(", ", data[i][j]);
  }
}

