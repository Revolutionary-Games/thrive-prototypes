//Project: fluid_sim
//File: main.cpp
//Programmer: Nathan Hock
//Based on this paper by Jos Stam: http://www.dgp.toronto.edu/people/stam/reality/Research/pdf/GDC03.pdf

#include <SDL.h>
#include "FluidSimulation.h"

#define IX(i,j) ((i)+(simulation.N+2)*(j))

void render_FluidSimulation(SDL_Renderer* renderer, const FluidSimulation & simulation, const int screen_width, const int velocity_length)
{
	float ratio = static_cast<float>(screen_width) / simulation.N;
	int x;
	int y;
	float coloration;
	SDL_Rect cell = { 0, 0, ratio, ratio };

	for (int i = 0; i < simulation.N + 2; i++)
	{
		for (int j = 0; j < simulation.N + 2; j++)
		{
			cell.x = i * ratio;
			cell.y = j * ratio;
			SDL_SetRenderDrawColor(renderer, 0xFF * (1 - simulation.dens[IX(i, j)]), 0xFF, 0xFF * (1 - simulation.dens[IX(i, j)]), 0xFF);
			SDL_RenderFillRect(renderer, &cell);

			/*x = i * ratio;
			y = j * ratio;
			SDL_SetRenderDrawColor(renderer, 0xFF, 0x00, 0x00, 0xFF);
			SDL_RenderDrawLine(renderer, x, y, x + simulation.u[IX(i, j)] * velocity_length, y + simulation.v[IX(i, j)] * velocity_length);*/
		}
	}
	return;
}

int main(int argc, char* args[])
{
	//Constants
	const int SCREEN_WIDTH = 600;
	const int SCREEN_HEIGHT = 600;
	const float VELOCITY_LENGTH = 1000;

	//Variables
	bool quit = false;
	int i, j; //temp
	float u_source;
	float v_source;
	SDL_Window* window = NULL;
	SDL_Renderer* renderer = NULL;
	SDL_Event event;
	SDL_Point mouse;
	SDL_Point mouse_prev;
	FluidSimulation current_simulation;
	
	const float RATIO = static_cast<float>(SCREEN_WIDTH) / current_simulation.N;

	//Initialize SDL, the window, and the renderer.
	SDL_Init(SDL_INIT_VIDEO);
	window = SDL_CreateWindow("Fluid Sim", SDL_WINDOWPOS_UNDEFINED, SDL_WINDOWPOS_UNDEFINED, SCREEN_WIDTH, SCREEN_HEIGHT, SDL_WINDOW_SHOWN);
	renderer = SDL_CreateRenderer(window, -1, SDL_RENDERER_ACCELERATED);

	while (!quit)
	{
		while (SDL_PollEvent(&event) != 0)
		{
			if (event.type == SDL_QUIT)
			{
				quit = true;
			}
			else if (event.type == SDL_MOUSEBUTTONDOWN)
			{
				SDL_GetMouseState(&mouse.x, &mouse.y);
			}
		}
		//If left button pressed, add source density
		if (SDL_GetMouseState(NULL, NULL) & SDL_BUTTON(SDL_BUTTON_LEFT))
		{
			SDL_GetMouseState(&mouse.x, &mouse.y);
			i = mouse.x / RATIO;
			j = mouse.y / RATIO;
			current_simulation.dens[(i)+(current_simulation.N + 2)*(j)] = 1;
			current_simulation.dens[(i)+(current_simulation.N + 2)*(j+1)] = 1;
			current_simulation.dens[(i)+(current_simulation.N + 2)*(j-1)] = 1;
			current_simulation.dens[(i+1)+(current_simulation.N + 2)*(j)] = 1;
			current_simulation.dens[(i+1)+(current_simulation.N + 2)*(j+1)] = 1;
			current_simulation.dens[(i+1)+(current_simulation.N + 2)*(j-1)] = 1;
			current_simulation.dens[(i-1)+(current_simulation.N + 2)*(j)] = 1;
			current_simulation.dens[(i-1)+(current_simulation.N + 2)*(j+1)] = 1;
			current_simulation.dens[(i-1)+(current_simulation.N + 2)*(j-1)] = 1;
		} 
		//If right button pressed, get source velocity from the mouse
		else if (SDL_GetMouseState(NULL, NULL) & SDL_BUTTON(SDL_BUTTON_RIGHT))
		{
			mouse_prev = mouse;
			SDL_GetMouseState(&mouse.x, &mouse.y);
			u_source = mouse.x - mouse_prev.x;
			v_source = mouse.y - mouse_prev.y;
			i = mouse_prev.x / RATIO;
			j = mouse_prev.y / RATIO;
			current_simulation.u[(i)+(current_simulation.N + 2)*(j)] = u_source;
			current_simulation.v[(i)+(current_simulation.N + 2)*(j)] = v_source;
		}
		
		current_simulation.dens_step();
		current_simulation.vel_step();

		//Clear the renderer
		SDL_SetRenderDrawColor(renderer, 0xFF, 0xFF, 0xFF, 0xFF);
		SDL_RenderClear(renderer);

		render_FluidSimulation(renderer, current_simulation, SCREEN_WIDTH, VELOCITY_LENGTH);

		SDL_RenderPresent(renderer);

		SDL_Delay(100);
	}

	//Destroy renderer and window and quit SDL
	SDL_DestroyRenderer(renderer);
	renderer = NULL;
	SDL_DestroyWindow(window);
	window = NULL;
	SDL_Quit();

	return 0;
}