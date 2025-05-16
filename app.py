import plotly.express as px
import numpy as np
import pandas as pd
import gradio as gr

csv_path = 'hotel_issues_structured_25rows.csv'

def create_hotel_issues_sunburst(csv_path=csv_path):
    """
    Create a sunburst chart visualization of hotel issues data.
    
    Parameters:
    csv_path (str): Path to the CSV file containing hotel issues data
    
    Returns:
    tuple: (Plotly figure object, DataFrame with the data)
    """
    try:
        # Load the hotel issues data
        df = pd.read_csv(csv_path)
        
        # Create the sunburst chart
        fig = px.sunburst(
            df, 
            path=['Category', 'Sub-Category', 'Issue'], 
            values=df.groupby(['Category', 'Sub-Category', 'Issue']).size().reset_index(name='Count')['Count'],
            color='Priority',
            color_discrete_map={
                'High': 'red',
                'Medium': 'orange',
                'Low': 'green'
            }
        )
        
        # Set dimensions to ensure the chart fits properly
        # Making it more square-shaped to prevent cutoff
        new_height = 500
        new_width = 550  # Slightly wider than height to account for labels
        
        # Update layout with adjusted size and margins
        fig.update_layout(
            margin=dict(t=50, l=50, r=50, b=50),  # Increased margins significantly
            height=new_height,
            width=new_width,
            title="Hotel Issues Breakdown by Category and Priority",
            autosize=False,  # Prevent automatic resizing
            paper_bgcolor='rgba(0,0,0,0)',  # Transparent background
            plot_bgcolor='rgba(0,0,0,0)'    # Transparent plot area
        )
        
        return fig, df
    
    except Exception as e:
        print(f"Error creating sunburst chart: {e}")
        # Return empty figure and dataframe in case of error
        return px.sunburst(pd.DataFrame()), pd.DataFrame()

def create_hotel_issues_app(csv_path=csv_path):
    """
    Create a Gradio app for visualizing hotel issues data.
    
    Parameters:
    csv_path (str): Path to the CSV file containing hotel issues data
    
    Returns:
    gradio.Blocks: Gradio app interface
    """
    # Get the chart and data
    sunburst_chart, hotel_data = create_hotel_issues_sunburst(csv_path)
    
    # Create the Gradio interface with custom theme
    with gr.Blocks() as demo:
        gr.Markdown("# Hotel Issues Visualization Dashboard")
        gr.Markdown("""
        This sunburst chart visualizes hotel issues data, organized by Category, Sub-Category, and specific Issue.
        The color represents Priority level, with red indicating high priority, orange for medium, and green for low.
        """)
        
        # Create tabs for visualization and data
        with gr.Tabs() as tabs:
            with gr.TabItem("Visualization"):
                # Use HTML component for custom styling
                gr.HTML("""
                <div style="display: flex; justify-content: center; padding: 20px;">
                    <!-- Plot will be inserted here -->
                </div>
                """)
                
                # Center the plot and ensure it's fully visible
                plot_output = gr.Plot(value=sunburst_chart)
            
            with gr.TabItem("Data"):
                data_display = gr.DataFrame(value=hotel_data)
        
        gr.Markdown("""
        ### About this Visualization
        
        **Dataset**: Hotel Issues Log
        
        **Chart Structure**:
        - Inner Ring: Issue Categories
        - Middle Ring: Sub-Categories
        - Outer Ring: Specific Issues
        - Segment Size: Number of occurrences
        - Color: Priority Level (red = high, orange = medium, green = low)
        
        **Interaction Tips**:
        - Hover over segments to see detailed information
        - Click on a segment to zoom in on its sub-categories
        - Click in the center to zoom back out
        
        The data tab shows the complete hotel issues log used to create this visualization.
        """)
    
    return demo

# If running this script directly, launch the app
if __name__ == "__main__":
    app = create_hotel_issues_app()
    app.launch(share=True)  # Removed the css parameter