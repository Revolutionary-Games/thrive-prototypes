import matplotlib.pyplot as plt
import numpy as np

def plot_compound_in_patches(patches, repartition_snapshots):
    num_steps = repartition_snapshots.shape[0] - 1

    # Plot snapshots
    fig, axes = plt.subplots(ncols = len(patches), sharey = True)

    for i in range(len(patches)):
        axes[i].set_title("{0} level in patch {1} over time".format(patches[i].compound_name, patches[i].name))
        axes[i].plot(range(num_steps+1), repartition_snapshots[:,i])
        axes[i].axhline(0, color='black')
    plt.show()

def plot_repartitions(patches, repartition_snapshots):
    # Plot repartitions
    fig, axes = plt.subplots(ncols = 2)

    plot_absolute_repartitions(axes[0], patches, repartition_snapshots)
    plot_relative_repartitions(axes[1], patches, repartition_snapshots, add_legend=True)

    # Show graphic
    plt.show()

def plot_absolute_repartitions(axis, patches, repartition_snapshots, add_legend=False, bar_width=0.85, colors=["blue", "green", "orange", "red", "purple"]):
    num_steps = repartition_snapshots.shape[0] - 1

    bar_values = np.zeros(num_steps+1)
    old_values = np.zeros(num_steps+1)

    for i in range(len(patches)):
        old_values += bar_values
        bar_values = repartition_snapshots[:,i]
        axis.bar(range(num_steps+1), bar_values, bottom=old_values, color=colors[i%len(colors)], edgecolor='white', width=bar_width)

    # Custom x axis
    axis.set_xticks(range(num_steps+1))
    axis.set_xlabel("Generations")
    axis.set_ylabel("{} amount".format(patches[0].compound_name))
    axis.set_title("Amount of {} over time".format(patches[0].compound_name))

    if add_legend:
        axis.legend(loc='upper left', bbox_to_anchor=(1,1), ncol=1)

def plot_relative_repartitions(axis, patches, repartition_snapshots, add_legend=False, bar_width=0.85, colors=["blue", "green", "orange", "red", "purple"]):
    num_steps = repartition_snapshots.shape[0] - 1

    # Avoiding null totals
    total_per_snapshot = np.sum(repartition_snapshots, axis = 1)
    total_per_snapshot = [1 if x==0 else x for x in total_per_snapshot]

    bar_values = np.zeros(num_steps+1)
    old_values = np.zeros(num_steps+1)

    for i in range(len(patches)):
        old_values += bar_values
        bar_values = repartition_snapshots[:,i]/total_per_snapshot[:]
        axis.bar(range(num_steps+1), bar_values, bottom=old_values, color=colors[i%len(colors)], edgecolor='white', width=bar_width, label = "Patch "+ patches[i].name)

    axis.set_xticks(range(num_steps+1))
    axis.set_xlabel("Generations")
    axis.set_ylabel("% of total {}".format(patches[0].compound_name))
    axis.set_title("Repartition of {} over time".format(patches[0].compound_name))

    if add_legend:
        axis.legend(loc='upper left', bbox_to_anchor=(1,1), ncol=1)
