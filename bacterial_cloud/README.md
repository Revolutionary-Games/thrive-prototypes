Feature list/todo etc. coming soon... before that I should probably explain how to run this code.

It's written in processing, which is a simple graphics library/engine built on top of java.  It's good for quick and simple prototypes, but if this gets much more complicated I'll probably move it to something else.

- Download the processing IDE here: https://processing.org/download/?processing
- You'll also need java
- Launch the processing IDE, then open bacterial_cloud.pde within the bacterial_cloud folder
- Hit run in the top left
- Alternatively you can export (right-most button) for an executable file.

Quick explanation of whats happening:
- The three triangles are microbe agents, each 'leaks' a different compound.
- The red & green agents also consume the blue compound
- The red & green agents seek high concentrations of blue compound, the blue agent seeks high concentrations of red compound.
- The bacteria (represented by a cyan outline to grid squares) consumes red + green compounds to both grow, and produce blue compound.  It dies off if starved.  The cell the the left of the screen has a permanent bacteria population to prevent it going extinct.
- This is all very crude for now, I've just put the basic components together to make something that sort of works for now, more to come soon.