// Class for 2d arrays, including element wise math

class Arr2d
{
  float[][] data;
  int _xs, _ys;
  
  Arr2d(int xs, int ys)
  {
    this(xs,ys,0);
  }
  
  Arr2d(int xs, int ys, float val)
  {
    _xs = xs; _ys = ys;
    data = new float[_xs][_ys];
    Set(val);
  }
  
  Arr2d(float[][] val)
  {
    _xs = val.length;
    _ys = val[0].length;
    data = new float[_xs][_ys];
    Set(val);
  }
  
  Arr2d(Arr2d clone)
  {
    this(clone.data);
//    data = new float[clone._xs][clone._ys];
//    Set(clone);
  }
  
  void Set(float val)
  {
    for(int x = 0; x < _xs; x++)
    for(int y = 0; y < _ys; y++)
      data[x][y] = val;
  }
  
  void Set(float[][] val)
  {
    for(int x = 0; x < _xs; x++)
    for(int y = 0; y < _ys; y++)
      data[x][y] = val[x][y];

  }
  
  void Set(Arr2d val)
  {  Set(val.data); }
  
  void Mult(float val)
  {  
    for(int x = 0; x < _xs; x++)
    for(int y = 0; y < _ys; y++)
      data[x][y] *= val;
  }
  
  void Mult(Arr2d val)
  {    
    for(int x = 0; x < _xs; x++)
    for(int y = 0; y < _ys; y++)
      data[x][y] *= val.data[x][y];
  }
  
  void Add(float val)
  {  
    for(int x = 0; x < _xs; x++)
    for(int y = 0; y < _ys; y++)
      data[x][y] += val;
  }
  
  void Add(Arr2d val)
  {        
    for(int x = 0; x < _xs; x++)
    for(int y = 0; y < _ys; y++)
      data[x][y] += val.data[x][y];
  }
  
  void Sub(float val)
  { Add(-val); }
  
  void Sub(Arr2d val)
  {
    for(int x = 0; x < _xs; x++)
    for(int y = 0; y < _ys; y++)
      data[x][y] -= val.data[x][y];

  }
  
  void Conv(Arr2d mask)
  {    
    int mx = mask._xs; 
    int my = mask._ys;
    int mcx = mx/2;
    int mcy = my/2;
    
    float[][] out = new float[_xs][_ys];
    for (int x = 0; x < _xs; x++)
      for (int y = 0; y < _ys; y++)
        out[x][y] = 0;

    for (int x = 0; x < _xs; x++)
      for (int y = 0; y < _ys; y++)
        for (int i = 0 - mcx; i < (mx - mcx); i++)
          for (int j = 0 - mcy; j < (my - mcy); j++)
          {
            if ((x+i) < 0 || (x+i) >= _xs || (y+j) < 0 || (y+j) >= _ys)
              continue;
            else
            {
              out[x][y] += data[x + i][y + j] * mask.data[i+mcx][j+mcy];
            }
          }
    data = out;
  }
  
  float Sum()
  {
    float total = 0;
    for(int x = 0; x < _xs; x++)
    for(int y = 0; y < _ys; y++)
      total += data[x][y];
      
    return total;
  }
  
  void Clamp(float min, float max)
  {
    for(int x = 0; x < _xs; x++)
    for(int y = 0; y < _ys; y++)
      data[x][y] = constrain(data[x][y], min, max);
  }
}


