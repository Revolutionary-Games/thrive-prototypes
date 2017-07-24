
#include <iostream>
#include <math.h>
#include <random>

using namespace std;

//for normalising vectors in 2d
float norm(float a, float b){
    if (a != 0 && b!= 0){
        return pow(pow(a,2) + pow(b,2),0.5);
    }
    else{
        return 1;
    }
}

//for each point in a 100x100 grid make a 2d normalised vector pointing in a random direction
void initialise_grid(float grid[100][100][2]){
    for (int i = 0; i < 100; i++){
        for (int j = 0; j < 100; j++){
            grid[i][j][0]  = static_cast <float> (rand()) / static_cast <float> (RAND_MAX);
            grid[i][j][1]  = static_cast <float> (rand()) / static_cast <float> (RAND_MAX);
            float normalise = norm(grid[i][j][0], grid[i][j][1]);
            grid[i][j][0] = grid[i][j][0] / normalise;
            grid[i][j][1] = grid[i][j][1] / normalise;
        }
    }
}

//for each point in the grid move the vector a little
void update_grid(float grid[100][100][2]){
    for (int i = 0; i < 100; i++){
        for (int j = 0; j < 100; j++){
            grid[i][j][0]  += 0.1*static_cast <float> (rand()) / static_cast <float> (RAND_MAX);
            grid[i][j][1]  += 0.1*static_cast <float> (rand()) / static_cast <float> (RAND_MAX);
            float normalise = norm(grid[i][j][0], grid[i][j][1]);
            grid[i][j][0] = grid[i][j][0] / normalise;
            grid[i][j][1] = grid[i][j][1] / normalise;

        }
    }

}

//interpolate
float lerp(float a, float b, float c){
	return (1 - c)*a + c*b;
}

//Computes the dot product of the distance and gradient vectors.
float dotGridGradient(int ix, int iy, float x, float y, float grid[100][100][2]){
    //Precomputed (or otherwise) gradient vectors at each grid node
	float grad_x = grid[min(99,iy)][min(99,ix)][0];
	float grad_y = grid[min(99,iy)][min(99,ix)][1];
	//Compute the distance vector
	float dx = x - (float)ix;
	float dy = y - (float)iy;
	//Compute the dot-product
	return (dx*grad_x + dy*grad_y);

}

//Compute Perlin noise at coordinates x, y
float perlin(float x, float y, float grid[100][100][2]){
	//Determine grid cell coordinates
	int x0 = (int)floor(x);
	int x1 = (int)x0 + 1;
	int y0 = (int)floor(y);
	int y1 = (int)y0 + 1;
	//Determine interpolation weights
	//Could also use higher order polynomial/s-curve here
	float sx = x - (float)x0;
	float sy = y - (float)y0;
	//Interpolate between grid point gradients
	float n0 = dotGridGradient(x0, y0, x, y, grid);
	float n1 = dotGridGradient(x1, y0, x, y, grid);
	float ix0 = lerp(n0, n1, sx);
	n0 = dotGridGradient(x0, y1, x, y, grid);
	n1 = dotGridGradient(x1, y1, x, y, grid);
	float ix1 = lerp(n0, n1, sx);
	float value = lerp(ix0, ix1, sy);
	return value;
}


int main(){

    cout << "Perlin noise generator" << endl;

    //initialise the perlin grid
    float grid[100][100][2];
    initialise_grid(grid);
    //call update grid every time you want to time-evolve the noise
    update_grid(grid);

    for (int i = 0; i < 50; i++){
        cout << perlin(10 + 0.1*i,33.2,grid) << endl;
    }



}
