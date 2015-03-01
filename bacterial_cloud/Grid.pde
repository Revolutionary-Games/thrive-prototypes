

class Grid {

  Arr2d data;
  int _xs, _ys;
  int _w; // display size

  Grid(int xs, int ys, int w)
  {
    _xs = xs;
    _ys = ys;
    _w = w;

    data = new Arr2d(xs,ys,0);
  }
  
  Grid(Arr2d clone, int w)
  {
    _xs = clone._xs;
    _ys = clone._ys;
    _w = w;
    data = new Arr2d(clone);
  }

  void AddAt(PVector target, float val)
  {
    int x = constrain(floor(target.x / _w), 0, _xs-1);
    int y = constrain(floor(target.y / _w), 0, _ys-1);
    data.data[x][y] += val;
  }
  
  PVector GradAt(PVector target)
  {
    int x = constrain(floor(target.x / _w), 0, _xs-1);
    int y = constrain(floor(target.y / _w), 0, _ys-1);
    
    float xg = 0;
    float yg = 0;
    
    for(int i = -1; i <= 1; i++)
    for(int j = -1; j <= 1; j++)
    if(x + i >= 0 && x + i < _xs && y + j >= 0 && y + j < _ys)
      {
        xg += i * data.data[x+i][y+j];
        yg += j * data.data[x+i][y+j];
      }
    return new PVector(xg,yg);
  }
  
  void Diffuse(Arr2d mask)
  {
    Arr2d temp = new Arr2d(data.data);
    data.Conv(mask);
    data.Add(temp);
    data.Clamp(0,10);
  }
  
  void React(Grid in1, Grid in2, Grid out)
  {
    Arr2d growth = new Arr2d(data.data);
    growth.Mult(in1.data);
    growth.Mult(in2.data);
//    PrintArr2d(growth.data);
    
    Arr2d mg = new Arr2d(growth.data);
    mg.Mult(0.5);
    data.Add(mg);
//    data.Sub(.01);
    data.Mult(0.99);
    data.Clamp(0, 10);
    
    growth.Mult(0.2);
    in2.data.Sub(growth);
    in1.data.Sub(growth);
    out.data.Add(growth);
  }

  void Display()
  {
    this.Display(color(1,1,1));
  }

  void Display(color c) {
    for (int x = 0; x < _xs; x++)
      for (int y = 0; y < _ys; y++)
      {
        int f = floor(constrain(data.data[x][y],0,1) * 255);
        fill((c & 0x00FFFFFF) | (f << 24));
        noStroke();
        rect(x*_w, y*_w, _w, _w);
      }
  }
  
  void DisplayEdges(color c)
  {
    for (int x = 0; x < _xs; x++)
      for (int y = 0; y < _ys; y++)
      {
        int f = floor(constrain(data.data[x][y],0,1) * 255);
        stroke((c & 0x00FFFFFF) | (f << 24));
        noFill();
        rect(x*_w, y*_w, _w, _w);
      }
  }
}

