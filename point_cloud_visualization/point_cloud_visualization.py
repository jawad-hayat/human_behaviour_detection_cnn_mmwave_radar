import numpy as np
from matplotlib import pyplot as plt
import matplotlib.animation as animation
import pandas as pd
import argparse

# path = '../../../data/raw/person_1/a/ti_mmwave-radar_scan.csv'
# type = 'point_id'
# # type = 'time'
extract_path = './src/exploratory-data-analysis/visuals/'
parser = argparse.ArgumentParser("give the file path and on which bases you want to make frames point_id or time")
parser.add_argument('path', help="give the path of csv")
parser.add_argument('type', help='give point_id or time')
args = parser.parse_args()

def point_cloud_visualization(path,type):
    def update_graph(num):
        data=df[df['time']==num]
        graph._offsets3d = (data.x, data.y, data.z)
        title.set_text('3D Test, time={}'.format(num))
        return graph, title

    dataframe = pd.read_csv(path)
    a = np.array(dataframe[['x','y','z']])
    time = []
    frame_no = 0

    if(type=='point_id'):
        for index, row in dataframe.iterrows():
            if row["point_id"] == 0 :
                frame_no+=1
            time.append(frame_no)
        t = np.array(time)
    elif(type=='time'):
        abc = np.array(dataframe['Time'])
        abc = abc.astype(int)
        n = abc.shape[0]
        for i in range(n):
            time.append(frame_no)
            try:
                if (abc[i + 1] > abc[i]):
                    frame_no = frame_no + 1
            except:
                pass
        t = np.array(time)

    df = pd.DataFrame({"time": t ,"x" : a[:,0], "y" : a[:,1], "z" : a[:,2]})
    xyz = np.array(df['time'])
    xyz = xyz.astype(int)
    frames = xyz[-1]
    fig = plt.figure()
    ax = fig.add_subplot(221, projection='3d')
    ax2 = fig.add_subplot(222, projection='3d')
    title = ax.set_title('3D Test')
    ax.scatter(df.x, df.y, df.z)

    data=df[df['time']==1]
    graph = ax2.scatter(data.x, data.y, data.z)
    
    ax2.set_xlim(ax.get_xlim())
    ax2.set_ylim(ax.get_ylim())
    ax2.set_zlim(ax.get_zlim())

    ani = animation.FuncAnimation(fig, update_graph, frames,
                                       interval=1, blit=False)
    ani.save(extract_path + "falling.gif", writer="Pillow")
    plt.show()

if __name__ == '__main__':
    point_cloud_visualization(args.path,args.type)