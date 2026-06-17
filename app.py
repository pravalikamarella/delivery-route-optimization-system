import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import heapq

# Set page configuration
st.set_page_config(
    page_title="Delivery Route Optimizer",
    page_icon="🚚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern premium design (dark mode styling, metrics styling)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&display=swap');
    
    /* Global styles */
    html, body, [data-testid="stSidebar"] {
        font-family: 'Outfit', sans-serif;
    }
    
    /* Header Gradient */
    .header-container {
        background: linear-gradient(135deg, #1f4068, #162447, #0f1a1c);
        padding: 2.5rem;
        border-radius: 16px;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.1);
        text-align: center;
    }
    
    .header-title {
        font-size: 2.8rem;
        font-weight: 800;
        letter-spacing: -0.5px;
        margin: 0;
        background: linear-gradient(to right, #00f2fe, #4facfe);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .header-subtitle {
        font-size: 1.1rem;
        opacity: 0.85;
        margin-top: 0.5rem;
        font-weight: 300;
    }
    
    /* Custom metric card */
    .metric-card {
        background-color: #1e2230;
        border-radius: 12px;
        padding: 1.5rem;
        border: 1px solid #2d3250;
        box-shadow: 0 4px 20px rgba(0,0,0,0.15);
        transition: transform 0.2s ease, border-color 0.2s ease;
        margin-bottom: 1rem;
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        border-color: #4facfe;
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: #90a4ae;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-weight: 600;
    }
    
    .metric-value {
        font-size: 2.2rem;
        font-weight: 800;
        color: #ffffff;
        margin-top: 0.3rem;
    }
    
    .metric-desc {
        font-size: 0.8rem;
        color: #607d8b;
        margin-top: 0.2rem;
    }
    
    /* Path display badges */
    .path-step {
        display: inline-block;
        padding: 6px 12px;
        background-color: #2e3b4e;
        border-radius: 20px;
        font-size: 0.9rem;
        font-weight: 600;
        color: #00e5ff;
        margin: 4px;
        border: 1px solid rgba(0, 229, 255, 0.2);
    }
    
    .path-arrow {
        color: #eceff1;
        font-size: 1.2rem;
        font-weight: bold;
        vertical-align: middle;
        margin: 0 4px;
    }
    
</style>
""", unsafe_allow_html=True)

# ----------------------------------------------------
# 1. DEFINE DELIVERY NETWORK GRAPH
# ----------------------------------------------------

# Network Node coordinates (for visualization)
NODE_POSITIONS = {
    'Central Warehouse': (0.0, 0.0),
    'North Hub': (0.0, 4.0),
    'South Hub': (0.0, -4.0),
    'East Hub': (4.0, 0.0),
    'West Hub': (-4.0, 0.0),
    'Downtown (Residential)': (-2.2, 2.2),
    'Suburbs (Residential)': (2.2, -2.2),
    'Industrial Park': (-3.0, -3.0),
    'Airport Cargo': (4.0, 4.0)
}

# The weighted undirected graph dictionary representation
DELIVERY_GRAPH = {
    'Central Warehouse': {'North Hub': 4.0, 'South Hub': 4.0, 'East Hub': 4.0, 'West Hub': 4.0, 'Downtown (Residential)': 3.0, 'Suburbs (Residential)': 3.0},
    'North Hub': {'Central Warehouse': 4.0, 'Downtown (Residential)': 3.0, 'Airport Cargo': 5.0},
    'South Hub': {'Central Warehouse': 4.0, 'Suburbs (Residential)': 3.0, 'Industrial Park': 4.0},
    'East Hub': {'Central Warehouse': 4.0, 'Suburbs (Residential)': 3.0, 'Airport Cargo': 5.0},
    'West Hub': {'Central Warehouse': 4.0, 'Downtown (Residential)': 3.0, 'Industrial Park': 4.0},
    'Downtown (Residential)': {'Central Warehouse': 3.0, 'North Hub': 3.0, 'West Hub': 3.0},
    'Suburbs (Residential)': {'Central Warehouse': 3.0, 'South Hub': 3.0, 'East Hub': 3.0},
    'Industrial Park': {'South Hub': 4.0, 'West Hub': 4.0},
    'Airport Cargo': {'North Hub': 5.0, 'East Hub': 5.0}
}

# ----------------------------------------------------
# 2. DIJKSTRA ALGORITHM IMPLEMENTATION
# ----------------------------------------------------

def run_dijkstra(graph, start_node, end_node):
    """
    Computes shortest path and distance using Dijkstra's Algorithm.
    Tracks iterations for student report visual breakdown.
    """
    # Priority Queue to store tuples of: (cumulative_distance, current_node, path_taken)
    # Min-heap behavior ensures node with lowest cumulative distance is processed next
    min_heap = [(0.0, start_node, [])]
    
    # Store minimum distances to all nodes. Initialize to infinity.
    distances = {node: float('inf') for node in graph}
    distances[start_node] = 0.0
    
    # Record nodes already visited
    visited = set()
    
    # Logging steps for the Educational walkthrough
    execution_steps = []
    
    while min_heap:
        current_dist, node, path = heapq.heappop(min_heap)
        
        # Skip if the node was already processed via a shorter path
        if node in visited:
            continue
            
        visited.add(node)
        new_path = path + [node]
        
        # Log this state for educational display
        execution_steps.append({
            "Step": len(execution_steps) + 1,
            "Current Node": node,
            "Cumulative Distance (km)": current_dist,
            "Path Explored": " → ".join(new_path)
        })
        
        # Destination reached!
        if node == end_node:
            return current_dist, new_path, execution_steps
            
        # Explore neighbors
        for neighbor, weight in graph[node].items():
            if neighbor in visited:
                continue
                
            old_distance = distances[neighbor]
            new_distance = current_dist + weight
            
            # If a shorter path to neighbor is found, update and push to queue
            if new_distance < old_distance:
                distances[neighbor] = new_distance
                heapq.heappush(min_heap, (new_distance, neighbor, new_path))
                
    return float('inf'), [], execution_steps

# ----------------------------------------------------
# 3. VEHICLE PROFILE METRICS & RATES
# ----------------------------------------------------

VEHICLES = {
    "🌱 Electric Cargo Bike": {
        "rate": 10.00,  # Currency units per km
        "speed": 20,    # Speed in km/h
        "co2": 0.0,     # kg per km
        "capacity": "Light (< 50 kg)"
    },
    "🚐 Standard Delivery Van": {
        "rate": 25.00,
        "speed": 50,
        "co2": 0.18,
        "capacity": "Medium (< 500 kg)"
    },
    "🚛 Heavy Freight Truck": {
        "rate": 60.00,
        "speed": 40,
        "co2": 0.45,
        "capacity": "Heavy (< 5000 kg)"
    },
    "🛸 Autonomous Cargo Drone": {
        "rate": 45.00,
        "speed": 80,
        "co2": 0.02,
        "capacity": "Ultra-light (< 5 kg)"
    }
}

# ----------------------------------------------------
# 4. APP LAYOUT & MAIN BODY
# ----------------------------------------------------

# Header section
st.markdown("""
    <div class="header-container">
        <h1 class="header-title">Delivery Route Optimization System</h1>
        <p class="header-subtitle">Intelligent path planning & cost estimation using Dijkstra's Algorithm and Graph Theory</p>
    </div>
""", unsafe_allow_html=True)

# Main columns: Left sidebar for controls, right panel for outcomes
with st.sidebar:
    st.header("⚙️ Configuration")
    
    st.markdown("### 📍 Select Route Locations")
    locations = sorted(list(DELIVERY_GRAPH.keys()))
    
    source = st.selectbox("Source Node", locations, index=0)
    
    # Pre-select different location for destination to avoid trivial route
    dest_index = 8 if len(locations) > 8 else 1
    destination = st.selectbox("Destination Node", locations, index=dest_index)
    
    st.markdown("---")
    st.markdown("### 🚚 Vehicle & Logistics")
    
    vehicle_choice = st.selectbox("Vehicle Type", list(VEHICLES.keys()))
    
    base_fare = st.slider("Base Fare (₹)", min_value=20.0, max_value=200.0, value=50.0, step=10.0)
    
    st.markdown("---")
    st.info("💡 **Dijkstra's Algorithm** guarantees the absolute shortest route in non-negative weighted graphs by greedily checking adjacent paths.")

# Check for identical source & destination
if source == destination:
    st.warning("⚠️ Source and Destination locations are identical! Please select different nodes to compute a route.")
else:
    # ----------------------------------------------------
    # 5. ALGORITHM RUN & COST CALCULATION
    # ----------------------------------------------------
    total_dist, shortest_path, steps_taken = run_dijkstra(DELIVERY_GRAPH, source, destination)
    
    vehicle_info = VEHICLES[vehicle_choice]
    delivery_cost = base_fare + (total_dist * vehicle_info["rate"])
    estimated_time = (total_dist / vehicle_info["speed"]) * 60 # Minutes
    total_co2 = total_dist * vehicle_info["co2"]
    
    # ----------------------------------------------------
    # 6. UI PRESENTATION & METRICS
    # ----------------------------------------------------
    
    # Metric cards layout
    m_col1, m_col2, m_col3, m_col4 = st.columns(4)
    
    with m_col1:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">🗺️ Shortest Distance</div>
                <div class="metric-value">{total_dist:.1f} km</div>
                <div class="metric-desc">Shortest route length</div>
            </div>
        """, unsafe_allow_html=True)
        
    with m_col2:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">💰 Delivery Cost</div>
                <div class="metric-value">₹{delivery_cost:.2f}</div>
                <div class="metric-desc">Base Fare (₹{base_fare:.0f}) + (₹{vehicle_info['rate']:.0f}/km)</div>
            </div>
        """, unsafe_allow_html=True)
        
    with m_col3:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">⏱️ Est. Travel Time</div>
                <div class="metric-value">{estimated_time:.0f} min</div>
                <div class="metric-desc">Avg speed: {vehicle_info['speed']} km/h</div>
            </div>
        """, unsafe_allow_html=True)
        
    with m_col4:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">🌿 Carbon Footprint</div>
                <div class="metric-value">{total_co2:.2f} kg</div>
                <div class="metric-desc">CO2 Emitted ({vehicle_info['co2']} kg/km)</div>
            </div>
        """, unsafe_allow_html=True)

    # ----------------------------------------------------
    # 7. ROUTE PATHWAY & VISUALS
    # ----------------------------------------------------
    
    # Highlighted Path sequence
    st.markdown("### 🗺️ Route Path Breakdown")
    path_html = ""
    for idx, node in enumerate(shortest_path):
        path_html += f'<span class="path-step">{node}</span>'
        if idx < len(shortest_path) - 1:
            path_html += '<span class="path-arrow">➜</span>'
    st.markdown(f'<div style="margin-bottom: 1.5rem;">{path_html}</div>', unsafe_allow_html=True)

    # Two column layout for visualization plot and walkthrough breakdown
    col_left, col_right = st.columns([6, 5])
    
    with col_left:
        st.markdown("### 📊 Delivery Network Map")
        
        # Creating Matplotlib & NetworkX visualization
        fig, ax = plt.subplots(figsize=(10, 7), facecolor='#0e1117')
        ax.set_facecolor('#0e1117')
        
        G = nx.Graph()
        for u, neighbors in DELIVERY_GRAPH.items():
            for v, w in neighbors.items():
                G.add_edge(u, v, weight=w)
                
        # Get path edges to color them differently
        path_edges = []
        for i in range(len(shortest_path) - 1):
            path_edges.append((shortest_path[i], shortest_path[i+1]))
            path_edges.append((shortest_path[i+1], shortest_path[i]))
            
        # Draw node colors
        node_colors = []
        for node in G.nodes():
            if node == source:
                node_colors.append('#00E676')      # Green for start
            elif node == destination:
                node_colors.append('#FF3D00') # Red/coral for destination
            elif node in shortest_path:
                node_colors.append('#00B0FF')   # Blue for path nodes
            else:
                node_colors.append('#37474F')   # Gray for unused nodes
                
        # Draw edge colors & widths
        edge_colors = []
        edge_widths = []
        for u, v in G.edges():
            if (u, v) in path_edges or (v, u) in path_edges:
                edge_colors.append('#00E5FF')   # Cyan highlighted edges
                edge_widths.append(4.0)
            else:
                edge_colors.append('#37474F')   # Dim gray edges
                edge_widths.append(1.5)
                
        # Plotting layout and nodes
        nx.draw_networkx_nodes(
            G, NODE_POSITIONS, 
            node_color=node_colors, 
            node_size=800, 
            ax=ax, 
            alpha=0.95
        )
        
        # Plotting edges
        nx.draw_networkx_edges(
            G, NODE_POSITIONS, 
            edgelist=G.edges(), 
            edge_color=edge_colors, 
            width=edge_widths, 
            ax=ax
        )
        
        # Node Labels
        # Shift labels slightly above actual coordinates for clean display
        label_positions = {k: (v[0], v[1] + 0.35) for k, v in NODE_POSITIONS.items()}
        nx.draw_networkx_labels(
            G, label_positions, 
            font_size=9, 
            font_color='#E0E0E0', 
            font_family='sans-serif',
            font_weight='bold', 
            ax=ax
        )
        
        # Edge Weights (labels)
        edge_labels = nx.get_edge_attributes(G, 'weight')
        formatted_labels = {k: f"{v} km" for k, v in edge_labels.items()}
        nx.draw_networkx_edge_labels(
            G, NODE_POSITIONS, 
            edge_labels=formatted_labels, 
            font_size=8, 
            font_color='#B0BEC5', 
            ax=ax,
            bbox=dict(facecolor='#0e1117', edgecolor='none', alpha=0.8)
        )
        
        ax.axis('off')
        plt.tight_layout()
        st.pyplot(fig)
        
    with col_right:
        st.markdown("### 🎓 Educational Walkthrough")
        
        tab1, tab2 = st.tabs(["🚀 Dijkstra Step-by-Step", "📘 Algorithm Explanation"])
        
        with tab1:
            st.write("Below is the trace of the Dijkstra min-heap execution for your current selection:")
            df_steps = pd.DataFrame(steps_taken)
            st.dataframe(
                df_steps, 
                use_container_width=True, 
                hide_index=True
            )
            
        with tab2:
            st.markdown("""
            #### How Dijkstra's Algorithm Works:
            
            Dijkstra's Algorithm is a **greedy algorithm** used to find the shortest path from a single source node to all other nodes in a weighted graph.
            
            1. **Initialization:**
               - Set the distance to the source node to `0`, and all other nodes to `infinity`.
               - Insert the source node into a Priority Queue (min-heap) as `(distance, node, path)`.
               
            2. **Exploration Loop:**
               - Extract the node with the minimum distance value from the queue. Let's call it current.
               - If current has already been visited with a shorter path, skip it.
               - Otherwise, mark it as visited.
               
            3. **Relaxing Edges:**
               - For each neighbor of current, calculate the tentative distance: 
                 `distance(neighbor) = distance(current) + edge_weight(current, neighbor)`
               - If this calculated distance is less than the neighbor's known distance, update its distance and push it to the queue.
               
            4. **Completion:**
               - Repeat steps 2-3 until the queue is empty or the destination node is extracted.
            
            > 💡 *Note: Dijkstra's algorithm only works correctly when edge weights are positive (no negative distances), which is always true for geographic road networks.*
            """)

# Footer
st.markdown("---")
st.markdown("<p style='text-align: center; color: #78909c; font-size: 0.85rem;'>Delivery Route Optimization System • Built with Streamlit, NetworkX & Matplotlib • AI&DS CRT Mini Project</p>", unsafe_allow_html=True)
