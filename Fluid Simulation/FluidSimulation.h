//Project: fluid_sim
//File: FluidSimulation.h
//Programmer: Nathan Hock

#pragma once

class FluidSimulation
{
	const float DT;
	const float DIFFUSION;
	const float VISCOSITY;
	float* u_prev;
	float* v_prev;
	float* dens_prev;

	void set_bnd(int N, int b, float * x);
	void diffuse(int N, int b, float * x, float * x0, float diff, float dt);
	void advect(int N, int b, float * d, float * d0, float * u, float *v, float dt);
	void project(int N, float * u, float * v, float * p, float * div);

public:
	const int N;	//Number of cells on a side within the boundary
	float* u;
	float* v;
	float* dens;

	FluidSimulation();
	~FluidSimulation();
	void dens_step();
	void vel_step();
};

