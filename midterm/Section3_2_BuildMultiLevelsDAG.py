class Node:
    def __init__(self, name):
        self.name = name #Xác định node
        self.children = [] #Đây là các node có cung đi vào node hiện tại
        #ở biến children này sẽ cho chúng ta thấy được sự phụ thuộc giữa các node
        self.struct = [] #chứa các sub-problem

    def add_child(self, child): #hàm này dùng để thêm các node có cung đi vào node hiện tại
        self.children.append(child)

    def add_struct(self, s): #hàm này dùng để thêm các sub-problem(bài toán con)
        self.struct.append(s)

X='abcde'
Y='afdbf'
P='abc'

# Print the nodes and edges of the DAG
nodes = []
for i in range (1,len(X)+1,1):#can m (kích thước chuỗi X)
  for j in range(1,len(Y)+1,1):#can n (kích thước chuỗi Y)
    nodes.append(Node([i,j])) #Ở đây chúng ta sẽ thêm toàn bộ các node vào đồ thị
for i in nodes: #Ở vòng lặp này, chúng ta sẽ thêm các node mà node hiện tại đang phụ thuộc
  a=i.name[0]-1 #a và b này là để xác định các node hiện tại đang phụ thuộc
  b=i.name[1]-1
  if(a==0 and b==0): #Ở đây là dành cho node([1,1])
    i.add_child(Node([0,0]))
  for j in nodes: #ở vòng lăp này sẽ thêm các node phụ thuộc tương ứng với a và b
    if(a!=0 and (j.name==[a,i.name[1]])==True):
      i.add_child(j)
    if(b!=0 and (j.name==[i.name[0],b])==True):
      i.add_child(j)
    if(a!=0 and b!=0 and (j.name==[a,b])==True):
      i.add_child(j)
  if(len(i.children)<3): #đây là dành cho các node có node phụ thuộc là [0,0]
    i.add_child(Node([0,0]))
    i.add_child(Node([0,0]))

for i in nodes:
  for j in range(0,len(P),1):#can k
    i.add_struct([i.name[0],i.name[1],j]) #dựa vào kích tập ràng buộc mà chúng ta sẽ thêm các sub-problem tương ứng

for i in nodes:
  print("p:", i.name)
  for j in i.children:
    print("c:", j.name)
  print("-------------")

for i in nodes:
  for s in i.struct:
    print(s)
  break



#print(nodes)
# nodes = [A, B, C, D, E, F, G, H, X, Y, J]
# edges = [(parent.name, child.name) for parent in nodes for child in parent.children]
# print("Nodes:", [node.name for node in nodes])
# print("Edges:", edges)