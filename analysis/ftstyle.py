import matplotlib.pyplot as plt
import matplotlib.patheffects as path_effects
import numpy as np
import cycler

class FtStyle:
    small_font = 26
    large_font = 32
    line_width = 5

    def set_plt_rc(self, plot: plt) -> plt:
        """Takes a plot and applies a style as rc params"""

        ft_background = "#FFF1E5"
        ft_democrat_blue = "#0F56B5"
        ft_republican_red = "#EF4647"
        ft_pink = "#E95D8C"
        ft_darkred = "#7D062E"
        ft_darkblue = "#065296"
        ft_blue = "#2591CE"
        ft_lightblue = "#72D9E7"
        ft_greenish = "#A2BC5D"
        ft_maybe_grey = "#716962"
        ft_golden = "#B89E17"

        plot.rcParams['figure.facecolor'] = ft_background
        plot.rcParams['axes.facecolor']= ft_background
        plot.rcParams['text.color']= ft_maybe_grey
        plot.rcParams['xtick.color']= ft_maybe_grey
        plot.rcParams['ytick.color']= ft_maybe_grey
        plot.rcParams['axes.labelcolor']= ft_maybe_grey

        #plot.rcParams["axes.grid.axis"] ="y"
        #plot.rcParams["axes.grid"] = True
        plot.rcParams['axes.spines.left'] = True
        plot.rcParams['axes.spines.right'] = False
        plot.rcParams['axes.spines.top'] = False
        plot.rcParams['axes.spines.bottom'] = True
        #plot.rcParams['figure.figsize'] = (20,12)

        #plot.rcParams['lines.linewidth'] = self.line_width

        #plot.rcParams['axes.titlesize'] = self.large_font
        #plot.rcParams['font.size'] = self.small_font
        #plot.rcParams['xtick.labelsize'] = self.small_font
        #plot.rcParams['ytick.labelsize'] = self.small_font
        #plot.rcParams['axes.labelsize']  = self.small_font
        #plot.rcParams['ytick.labelsize'] = self.small_font
        plot.rcParams['xtick.major.size'] = 10
        plot.rcParams['xtick.major.pad'] = 10
        plot.rcParams['ytick.major.size'] = 0
        plot.rcParams['ytick.major.pad'] = 10
        plot.rcParams['figure.constrained_layout.use'] = True

        plot.rc('axes', prop_cycle=(cycler.cycler('color', [ft_darkblue,
                                                           ft_blue,
                                                           ft_lightblue,
                                                           ft_pink,
                                                           ft_darkred,
                                                           ft_greenish])))
        return plot

    def test_plot(self):

        np.random.seed(1)
        n,m = 200,6
        x = np.arange(n)
        y = np.cumsum(np.random.randn(m,n)*0.1,axis = 1)

        myplot=self.set_plt_rc(plt)

        fig, ax = myplot.subplots(constrained_layout = True)
        for i in range(m):
            ax.plot(x,y[i,:], lw = self.line_width+1, c="w") # White outline of line
            p = ax.plot(x,y[i,:])
            color = p[-1].get_color() # Match text color with line color
            text = ax.text(x[-1]+1,y[i,-1]*1.05,  f"   Category {i+1}",fontsize = self.small_font, va ="center", color = color)
            text.set_path_effects([path_effects.Stroke(linewidth=1, foreground='white'), path_effects.Normal()]) # White outline of text
        ax.set_ylim(-3,3)


        left = -0.06
        ax.text(left, 1.18,'The main title',
            ha='left',va='center', transform = ax.transAxes,
            fontsize = self.large_font,color ="k")

        ax.text(left, 1.1,'And this is a smaller title',
            ha='left',va='center', transform = ax.transAxes)

        ax.text(left,-0.15,"Here is a footnote.",
            ha='left',va='center', transform = ax.transAxes)

        ax.set_xlabel("This is the x-label")
        ax.set_ylabel("This is the y-label")

        #plt.show()
        plt.savefig("sampleplot.png", dpi=100)






