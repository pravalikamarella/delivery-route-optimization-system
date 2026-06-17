# Delivery Route Optimization System using Graph Algorithms

An interactive, beginner-friendly web application designed for route planning and delivery cost optimization using graph theory and Dijkstra's algorithm. Perfect for college mini projects (AI&DS, CSE, or IT).

---

## 🚀 Project Overview

In logistics and supply chain management, determining the most efficient route is critical to minimize transportation costs, reduce transit time, and curb carbon emissions. This project models a **City Delivery Network** using a weighted undirected graph, where:
- **Nodes** represent logistics locations (Warehouses, Hubs, Residential Areas, Airport Cargo).
- **Edges** represent roads connecting these locations.
- **Edge Weights** represent physical distances in kilometers (km).

The system implements a custom **Dijkstra's Algorithm** to calculate the shortest path, compute delivery costs for different vehicle classes, and display interactive visual maps.

---

## 🛠️ Tech Stack

- **Python**: Core programming language.
- **Streamlit**: Web interface for interactive sliders, dropdowns, and metrics.
- **NetworkX**: Graph modeling and manipulation library.
- **Matplotlib**: Generating high-quality network graph plots.
- **Pandas**: Displaying algorithm trace tables step-by-step.

---

## 📂 Project Structure

```text
├── app.py               # Main application (UI, Graph, Custom Dijkstra implementation)
├── requirements.txt     # List of Python dependencies
└── README.md            # Detailed project documentation (This file)
```

---

## 🧠 Dijkstra's Algorithm Explained

Dijkstra's algorithm solves the **single-source shortest path problem** for graphs with non-negative edge weights.

### Algorithm Steps:
1. **Initialize distances**: Set the distance to the starting node to `0`, and all other nodes to `infinity`.
2. **Priority Queue**: Put the starting node in a priority queue (min-heap) with a distance of `0`.
3. **Loop**:
   - Extract the node with the minimum distance. Let's call it $U$.
   - For each neighbor $V$ of $U$, calculate the tentative distance:  
     $$Distance(V) = Distance(U) + Weight(U, V)$$
   - If this tentative distance is smaller than the current recorded distance for $V$, update it in the priority queue.
4. **Terminate**: Repeat until the destination node is visited or the queue is empty.

---

## 💻 How to Run the Project

### Prerequisites
Make sure you have **Python 3.8 or higher** installed.

### Step 1: Clone or open the project directory
Navigate to the directory where the files are stored:
```bash
cd "d:/Projects/Hackon(hackerRank)"
```

### Step 2: Install dependencies
Install the required Python libraries using `pip`:
```bash
pip install -r requirements.txt
```

### Step 3: Run the Streamlit App
Start the local development server:
```bash
streamlit run app.py
```

### Step 4: Open in Browser
A web browser tab will automatically open at:
```text
http://localhost:8501
```
If it doesn't open, copy the URL from the terminal output and paste it into your browser.

---

## ✨ Features

- **Interactive Settings:** Choose source and destination nodes, base fares, and vehicle types dynamically in the sidebar.
- **Dynamic Cost Calculator:** Calculates fares, estimated travel time, and carbon emissions ($CO_2$) based on vehicle speed and emission profiles:
  - 🌱 *Electric Cargo Bike* (Eco-friendly, rate: ₹10/km)
  - 🚐 *Standard Delivery Van* (Medium, rate: ₹25/km)
  - 🚛 *Heavy Freight Truck* (Bulk, rate: ₹60/km)
  - 🛸 *Autonomous Cargo Drone* (Express, rate: ₹45/km)
- **Visual Map:** Draws the entire graph dynamically, highlighting the chosen path in cyan, the start node in green, and the destination node in red.
- **Trace logs:** Interactive table showing the state of the priority queue at each iteration of Dijkstra's algorithm.

---

## 🔮 Future Enhancements
- **Dynamic Traffic Integration:** Adjust edge weights in real-time based on traffic data.
- **Multiple Delivery Drop-offs:** Solve the Travelling Salesperson Problem (TSP) using genetic algorithms.
- **Time Window constraints:** Implement vehicle routing with scheduling limits.
