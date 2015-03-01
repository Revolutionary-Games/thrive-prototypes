
class GridLayers
{
    ArrayList<Grid> layers;
    ArrayList<String> names;
    ArrayList<Color> colors;
    
    GridLayers()
    {
      layers = new ArrayList<Grid>();
      names = new ArrayList<String>();
      colors = new ArrayList<Color>();
    }
  
    void Add(Grid g, color c)
    {
      layers.add(g);
      colors.add(new Color(c));
    }
    
    Grid get(int i)
    {
      return layers.get(i);
    }
    
    int length()
    {
      return layers.size();
    }
    
    void Diffuse(Arr2d mask)
    {
      for(int i = 0; i < length(); i++)
        layers.get(i).Diffuse(mask);
    }
    
    
    void Display()
    {
      for(int i = 0; i < length(); i++)
        layers.get(i).Display(colors.get(i).data);
    }
    
    void DisplayEdges()
    {
      for(int i = 0; i < length(); i++)
        layers.get(i).DisplayEdges(colors.get(i).data);
    }

}
