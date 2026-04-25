import tkinter as tk
import math
import graph5
from tkinter import messagebox
#creating nodes and arrows on the map
def get_edge_points (p1 , p2 , radius) : 
    x1 , y1 = p1
    x2 , y2 = p2 
    dist_x = x2 - x1
    dist_y = y2 - y1 
    dist = math.sqrt(dist_x**2 + dist_y**2)

    if dist == 0 : return p1

    offset_x = (dist_x / dist) * radius
    offset_y = (dist_y / dist) * radius

    return (x1 + offset_x , y1 + offset_y)

def draw_arrow (canvas , p1_center , p2_center , radius = 15) :
    start = get_edge_points(p1_center , p2_center , radius)
    end = get_edge_points(p2_center , p1_center , radius)

    canvas.create_line(
        start[0] , start[1] , end[0] , end[1] ,
        arrow = tk.BOTH , arrowshape = (6,4,4) , fill = "black" , width = 2
    )   


from collections import deque

def animated_bfs (canvas ,node_circles , graph_data , start , goal) : 
    
    visited = set()
    queue = deque([start])
    visited.add(start)
    parent = {start : None}

    def draw_final_path (parent_map , goal_node) :
        curr = goal_node 
        while curr is not None : 
            canvas.itemconfig(node_circles[curr] , fill="yellow")
            curr = parent_map[curr]

    def step () :
        if queue : 
            current_node = queue.popleft()
            canvas.itemconfig(node_circles[current_node] , fill= "skyblue" , outline="red" , width = 3) 
            if current_node != goal : 
                canvas.itemconfig(node_circles[current_node] , fill = "skyblue")
            if current_node == goal : 
                draw_final_path(parent , goal)
                print("you reached " + current_node)
                messagebox.showinfo("Done" , f"{current_node} وصلنا بالسلامة ل")
                return
            
            for neighbor in graph_data[current_node]["neighbors"] :
                if neighbor not in visited and neighbor in graph_data : 
                    queue.append(neighbor)
                    visited.add(neighbor)
                    parent[neighbor] = current_node

            root.after (600 , step)

        else : 
            messagebox.showinfo("Finish point" , "BFS finished !")
    step()


def start_stimulation () : 

    g_name= entry_graph.get() 
    raw_start = entry_start.get()
    raw_end = entry_end.get()

    lookup_map = {k.replace(" " , "").lower() : k for k in graph5.metro_data.keys()}

    clean_start = raw_start.replace(" " , "").lower()
    clean_end = raw_end.replace(" " , "").lower()

     
    start_node = lookup_map.get(clean_start)
    end_node = lookup_map.get(clean_end)

    if start_node in graph5.metro_data and end_node in graph5.metro_data : 
        input_frame.pack_forget() 

        canvas.pack() 
        canvas.create_rectangle(300 , 550 , 480 , 750 , fill = "#753AC9" , outline="black" , width=2)
        canvas.create_text(300 , 540 , text="Labels Definition" , anchor="w" , font=("Arial" , 12 , "bold"))
        canvas.create_text(305 , 670 , text="(*) ---> sidi gaber elshiekh" , anchor="w" , font=("Arial" , 10))
        canvas.create_text(305 , 695 , text="(^) ---> cleopatra elhamamat" , anchor="w" , font=("Arial" , 10))
        canvas.create_oval(310 , 560 , 330 , 580 , fill="skyblue" , outline="black")
        canvas.create_oval(310 , 590 , 330 , 610 , fill="yellow" , outline="black")
        canvas.create_oval(310 , 620 , 330 , 640 , outline="red" , width = 3)
        canvas.create_text(340 , 570 , text=" ---> stations" , anchor="w" , font=("Arial" , 10))
        canvas.create_text(340 , 600 , text=" ---> goal path" , anchor="w" , font=("Arial" , 10))
        canvas.create_text(340 , 630 , text=" ---> BFS path" , anchor="w" , font=("Arial" , 10))
        root.title(f"Project name: {g_name}")

        start_map (start_node , end_node)

    if start_node not in graph5.metro_data and end_node in graph5.metro_data:  
        messagebox.showerror("Error" , " ! اسم محطة البداية غلط يا بشمهدس")
    if end_node not in graph5.metro_data and start_node in graph5.metro_data  : 
        messagebox.showerror("Error" , " ! اسم محطة النهاية غلط يا بشمهدس")
    if start_node not in graph5.metro_data and end_node not in graph5.metro_data : 
        messagebox.showerror("Error" , " ! اسم المحطتين غلط يا بشمهدس")
def start_map (start_node , end_node) :

    drawn_edges = set()
    radius = 10 
    for node , data in graph5.metro_data.items() :
        for neighbor in data["neighbors"] : 
            if neighbor in graph5.metro_data : 
                edge = tuple(sorted((node , neighbor)))
                if edge not in drawn_edges : 
                    draw_arrow(canvas , data["pos"] , graph5.metro_data[neighbor]["pos"] , radius)
                    drawn_edges.add(edge)

    node_circles = {} 
    for node , data in graph5.metro_data.items() : 
        x , y = data["pos"]
        circle_id = canvas.create_oval(x-radius , y-radius , x+radius , y+radius , fill="skyblue" , outline="black")
        node_circles[node] = circle_id
        canvas.create_text(x+15 ,y, text=node , anchor="w" , font=("Arial " , 9)) 

    root.after(500 , lambda : animated_bfs(canvas , node_circles , graph5.metro_data , start_node , end_node ))

root = tk.Tk()


root.title("ALEX Metro")
root.geometry("500x600")

input_frame = tk.Frame(root , pady=50 ,)
input_frame.pack()

tk.Label (input_frame , text="Graph Name" , font=("Arial" , 12)).pack(pady=5)
entry_graph = tk.Entry(input_frame)
entry_graph.pack(pady=5)
entry_graph.insert(0 , "(default) metro_data")

tk.Label (input_frame , text="start point" , font=("Arial" , 12)).pack(pady=5)
entry_start = tk.Entry(input_frame)
entry_start.pack(pady=5)
entry_start.insert(0 , "")

tk.Label (input_frame , text="end point" , font=("Arial" , 12)).pack(pady=5)
entry_end = tk.Entry(input_frame)
entry_end.pack(pady=5)
entry_end.insert(0 , "")

btn_start = tk.Button(input_frame , text="Start Stimulation" , command=start_stimulation , bg = "green" , font=("Arial" , 20 , "bold"))
btn_start.pack(pady=5)

canvas = tk.Canvas(root , width = 500 , height = 1080 , bg = "white")

root.mainloop()
