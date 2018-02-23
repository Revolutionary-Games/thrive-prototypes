//Project: fluid_sim
//File: FluidSimulation.cpp
//Programmer: Nathan Hock

#include "FluidSimulation.h"

#define IX(i,j) ((i)+(N+2)*(j))
#define SWAP(x0, x) {float *tmp = x0; x0 = x; x = tmp;}

FluidSimulation::FluidSimulation()
	:N(100),DT(1),DIFFUSION(0.00001),VISCOSITY(0.0001)
{
	u_prev = new float[(N + 2) * (N + 2)];
	v_prev = new float[(N + 2) * (N + 2)];
	dens_prev = new float[(N + 2) * (N + 2)];
	u = new float[(N + 2) * (N + 2)];
	v = new float[(N + 2) * (N + 2)];
	dens = new float[(N + 2) * (N + 2)];
	for (int i = 0; i < (N + 2) * (N + 2); i++)
	{
		u_prev[i] = 0;
		v_prev[i] = 0;
		dens_prev[i] = 0;
		u[i] = 0;
		v[i] = 0;
		dens[i] = 0;
	}
}

FluidSimulation::~FluidSimulation()
{
	delete[] u_prev;
	delete[] v_prev;
	delete[] dens_prev;
	delete[] u;
	delete[] v;
	delete[] dens;
}

void FluidSimulation::set_bnd(int N, int b, float * x)
{
	int i;
	for (i = 1; i <= N; i++) {
		x[IX(0, i)] = b == 1 ? -x[IX(1, i)] : x[IX(1, i)];
		x[IX(N + 1, i)] = b == 1 ? -x[IX(N, i)] : x[IX(N, i)];
		x[IX(i, 0)] = b == 2 ? -x[IX(i, 1)] : x[IX(i, 1)];
		x[IX(i, N + 1)] = b == 2 ? -x[IX(i, N)] : x[IX(i, N)];
	}
	x[IX(0, 0)] = 0.5*(x[IX(1, 0)] + x[IX(0, 1)]);
	x[IX(0, N + 1)] = 0.5*(x[IX(1, N + 1)] + x[IX(0, N)]);
	x[IX(N + 1, 0)] = 0.5*(x[IX(N, 0)] + x[IX(N + 1, 1)]);
	x[IX(N + 1, N + 1)] = 0.5*(x[IX(N, N + 1)] + x[IX(N + 1, N)]);
	return;
}

void FluidSimulation::diffuse(int N, int b, float * x, float * x0, float diff, float dt)
{
	int i, j, k;
	float a = dt * diff*N*N;
	for (k = 0; k<20; k++) {
		for (i = 1; i <= N; i++) {
			for (j = 1; j <= N; j++) {
				x[IX(i, j)] = (x0[IX(i, j)] + a * (x[IX(i - 1, j)] + x[IX(i + 1, j)] +
					x[IX(i, j - 1)] + x[IX(i, j + 1)])) / (1 + 4 * a);
			}
		}
		set_bnd(N, b, x);
	}
	return;
}

void FluidSimulation::advect(int N, int b, float * d, float * d0, float * u, float *v, float dt)
{
	int i, j, i0, j0, i1, j1;
	float x, y, s0, t0, s1, t1, dt0;
	dt0 = dt * N;
	for (i = 1; i <= N; i++) {
		for (j = 1; j <= N; j++) {
			x = i - dt0 * u[IX(i, j)]; y = j - dt0 * v[IX(i, j)];
			if (x<0.5) x = 0.5; if (x>N + 0.5) x = N + 0.5; i0 = (int)x; i1 = i0 + 1;
			if (y<0.5) y = 0.5; if (y>N + 0.5) y = N + 0.5; j0 = (int)y; j1 = j0 + 1;
			s1 = x - i0; s0 = 1 - s1; t1 = y - j0; t0 = 1 - t1;
			d[IX(i, j)] = s0 * (t0*d0[IX(i0, j0)] + t1 * d0[IX(i0, j1)]) +
				s1 * (t0*d0[IX(i1, j0)] + t1 * d0[IX(i1, j1)]);
		}
	}
	set_bnd(N, b, d);
	return;
}

void FluidSimulation::project(int N, float * u, float * v, float * p, float * div)
{
	int i, j, k;
	float h;
	h = 1.0 / N;
	for (i = 1; i <= N; i++) {
		for (j = 1; j <= N; j++) {
			div[IX(i, j)] = -0.5*h*(u[IX(i + 1, j)] - u[IX(i - 1, j)] + v[IX(i, j + 1)] - v[IX(i, j - 1)]);
			p[IX(i, j)] = 0;
		}
	}
	set_bnd(N, 0, div);
	set_bnd(N, 0, p);
	for (k = 0; k<20; k++) {
		for (i = 1; i <= N; i++) {
			for (j = 1; j <= N; j++) {
				p[IX(i, j)] = (div[IX(i, j)] + p[IX(i - 1, j)] + p[IX(i + 1, j)] + p[IX(i, j - 1)] + p[IX(i, j + 1)]) / 4;
			}
		}
		set_bnd(N, 0, p);
	}
	for (i = 1; i <= N; i++) {
		for (j = 1; j <= N; j++) {
			u[IX(i, j)] -= 0.5*(p[IX(i + 1, j)] - p[IX(i - 1, j)]) / h;
			v[IX(i, j)] -= 0.5*(p[IX(i, j + 1)] - p[IX(i, j - 1)]) / h;
		}
	}
	set_bnd(N, 1, u); set_bnd(N, 2, v);
	return;
}

void FluidSimulation::dens_step()
{
	SWAP(this->dens_prev, this->dens); this->diffuse(this->N, 0, this->dens, this->dens_prev, this->DIFFUSION, this->DT);
	SWAP(this->dens_prev, this->dens); this->advect(this->N, 0, this->dens, this->dens_prev, this->u, this->v, this->DT);
	return;
}

void FluidSimulation::vel_step()
{

	SWAP(this->u_prev, this->u); diffuse(this->N, 1, this->u, this->u_prev, this->VISCOSITY, this->DT);
	SWAP(this->v_prev, this->v); diffuse(this->N, 2, this->v, this->v_prev, this->VISCOSITY, this->DT);
	project(this->N, this->u, this->v, this->u_prev, this->v_prev);
	SWAP(this->u_prev, this->u); SWAP(this->v_prev, this->v);
	advect(this->N, 1, this->u, this->u_prev, this->u_prev, this->v_prev, this->DT); 
	advect(this->N, 2, this->v, this->v_prev, this->u_prev, this->v_prev, this->DT);
	project(this->N, this->u, this->v, this->u_prev, this->v_prev);
	return;
}