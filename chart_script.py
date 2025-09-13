import plotly.graph_objects as go
import numpy as np

# Define colors for each layer
colors = {
    'Presentation': '#1FB8CD',  # Strong cyan
    'Business': '#DB4545',      # Bright red  
    'Data': '#2E8B57'          # Sea green
}

# Create figure
fig = go.Figure()

# Define layer positions with better spacing
layers = {
    'Presentation': {
        'y': 5,
        'main': 'SmartTaskMgrGUI',
        'components': ['Input Frame', 'Task List', 'Control Frame', 'Status Frame'],
        'x_positions': [1, 2.5, 4, 5.5]
    },
    'Business': {
        'y': 3,
        'main': 'TaskManager',
        'components': ['Priority Sched', 'Dependency', 'CRUD Ops', 'Persistence'],
        'x_positions': [1, 2.5, 4, 5.5]
    },
    'Data': {
        'y': 1,
        'main': 'Task Model',
        'components': ['Task Props', 'Priority Calc', 'JSON Serial', 'Status Mgmt'],
        'x_positions': [1, 2.5, 4, 5.5]
    }
}

# Add layer background rectangles
for layer_name, details in layers.items():
    fig.add_shape(
        type="rect",
        x0=0.3, y0=details['y']-0.6,
        x1=6.2, y1=details['y']+0.6,
        line=dict(color=colors[layer_name], width=2),
        fillcolor=colors[layer_name],
        opacity=0.1,
        layer="below"
    )

# Add main layer headers
for layer_name, details in layers.items():
    fig.add_trace(go.Scatter(
        x=[0.1],
        y=[details['y']],
        mode='text',
        text=[f"<b>{layer_name}<br>Layer</b>"],
        textposition="middle right",
        textfont=dict(size=12, color=colors[layer_name]),
        showlegend=False,
        hoverinfo='skip'
    ))

# Add component boxes for each layer
for layer_name, details in layers.items():
    for i, component in enumerate(details['components']):
        # Add rectangle shape for component
        fig.add_shape(
            type="rect",
            x0=details['x_positions'][i]-0.4,
            y0=details['y']-0.25,
            x1=details['x_positions'][i]+0.4,
            y1=details['y']+0.25,
            line=dict(color=colors[layer_name], width=2),
            fillcolor=colors[layer_name],
            opacity=0.8
        )
        
        # Add text for component
        fig.add_trace(go.Scatter(
            x=[details['x_positions'][i]],
            y=[details['y']],
            mode='text',
            text=[f"<b>{component}</b>"],
            textposition="middle center",
            textfont=dict(size=10, color='white'),
            showlegend=False,
            hovertemplate=f"<b>{component}</b><br>Layer: {layer_name}<extra></extra>"
        ))

# Add directional arrows between layers
arrow_x = [1.5, 3.25]  # Two main flow paths

for x_pos in arrow_x:
    # From Presentation to Business
    fig.add_annotation(
        x=x_pos, y=4.2,
        ax=x_pos, ay=3.8,
        xref='x', yref='y',
        axref='x', ayref='y',
        arrowhead=2,
        arrowsize=1.5,
        arrowwidth=3,
        arrowcolor='black',
        showarrow=True
    )
    
    # From Business to Data
    fig.add_annotation(
        x=x_pos, y=2.2,
        ax=x_pos, ay=1.8,
        xref='x', yref='y',
        axref='x', ayref='y',
        arrowhead=2,
        arrowsize=1.5,
        arrowwidth=3,
        arrowcolor='black',
        showarrow=True
    )

# Add priority scheduling flow emphasis
fig.add_annotation(
    text="<b>Priority Flow</b>",
    x=4.8, y=4.5,
    showarrow=False,
    font=dict(size=11, color='#DB4545'),
    bgcolor="rgba(255,255,255,0.8)",
    bordercolor="#DB4545",
    borderwidth=1
)

# Highlight priority scheduling connections
fig.add_shape(
    type="line",
    x0=2.5, y0=5.3,
    x1=2.5, y1=0.7,
    line=dict(color='#DB4545', width=3, dash='dash'),
    opacity=0.7
)

# Add legend manually
legend_data = [
    {'name': 'Presentation', 'color': colors['Presentation']},
    {'name': 'Business', 'color': colors['Business']},
    {'name': 'Data', 'color': colors['Data']}
]

for i, item in enumerate(legend_data):
    fig.add_trace(go.Scatter(
        x=[None],
        y=[None],
        mode='markers',
        marker=dict(size=15, color=item['color'], symbol='square'),
        name=item['name'],
        showlegend=True
    ))

# Update layout
fig.update_layout(
    title="Smart Task Manager Architecture",
    xaxis=dict(
        showgrid=False,
        showticklabels=False,
        range=[-0.5, 6.5]
    ),
    yaxis=dict(
        showgrid=False,
        showticklabels=False,
        range=[0, 6]
    ),
    legend=dict(
        orientation='h',
        yanchor='bottom',
        y=1.05,
        xanchor='center',
        x=0.5
    )
)

# Update traces to remove clip on axis
fig.update_traces(cliponaxis=False)

# Save the chart
fig.write_image("architecture_diagram.png")