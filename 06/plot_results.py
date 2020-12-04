import matplotlib.pyplot as plt
import glob

file_list = glob.glob('./out/*')


def plot_file(x1,y1,x2,y2, name):
  plt.title(f'{name}')
  plt.plot(x1,y1, label="naive", color="red")
  plt.plot(x2,y2, label="smart")
  plt.xlabel("Matrix size")
  plt.ylabel("Average number of cache misses")
  plt.savefig(f'{name}-graph.png')
  plt.close()

def get_values(file_name):
  file = open(file_name, 'r')
  print("file name: ", file_name)
  
  x = []
  y = []

  for line in file:
    if (len(line) == 0):
      continue
    tokens = line.split()
    
    print("token-1: ",tokens[0], "token-2: ", tokens[1])
    x.append(float(tokens[0]))
    y.append(float(tokens[1]))
  
  file.close()

  return x, y



b16_naive = glob.glob('./out/t-sim-m1024-b16-naive')
b16_smart = glob.glob('./out/t-sim-m1024-b16-smart')
x1, y1 = get_values("./out/t-sim-m1024-b16-naive")
x2, y2 = get_values("./out/t-sim-m1024-b16-smart")
plot_file(x1,y1,x2,y2, "m1024b16")

b64_naive = glob.glob('./out/t-sim-m8192-b64-naive')
b64_smart = glob.glob('./out/t-sim-m8192-b64-smart')
x1, y1 = get_values("./out/t-sim-m8192-b64-naive")
x2, y2 = get_values("./out/t-sim-m8192-b64-smart")
plot_file(x1,y1,x2,y2, "m8192b64")

b256_naive = glob.glob('./out/t-sim-m65536-b256-naive')
b256_smart = glob.glob('./out/t-sim-m65536-b256-smart')
x1, y1 = get_values("./out/t-sim-m65536-b256-naive")
x2, y2 = get_values("./out/t-sim-m65536-b256-smart")
plot_file(x1,y1,x2,y2, "m65536b256")

b4096_naive = glob.glob('./out/t-sim-m65536-b4096-naive')
b4096_smart = glob.glob('./out/t-sim-m65536-b4096-smart')
x1, y1 = get_values("./out/t-sim-m65536-b4096-naive")
x2, y2 = get_values("./out/t-sim-m65536-b4096-smart")
plot_file(x1,y1,x2,y2, "m65536b4096")

