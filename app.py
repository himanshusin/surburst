import plotly.express as px
import numpy as np
import gradio as gr

def create_gapminder_sunburst():
    # Load the Gapminder dataset and filter for 2007
    df = px.data.gapminder().query("year == 2007")
    
    # Create the sunburst chart
    fig = px.sunburst(
        df, 
        path=['continent', 'country'], 
        values='pop',
        color='lifeExp', 
        hover_data=['iso_alpha'],
        color_continuous_scale='RdBu',
        color_continuous_midpoint=np.average(df['lifeExp'], weights=df['pop'])
    )
    
    # Update layout for better display
    fig.update_layout(
        margin=dict(t=30, l=0, r=0, b=0),
        height=700,
        width=900,
        title="Global Population and Life Expectancy (2007)"
    )
    
    return fig, df

# Get the chart and data
sunburst_chart, gapminder_data = create_gapminder_sunburst()

# Create the Gradio interface
with gr.Blocks() as demo:
    gr.Markdown("# Global Population and Life Expectancy Visualization")
    gr.Markdown("""
    This sunburst chart visualizes global population data from 2007, organized by continent and country.
    The color represents life expectancy, with blue indicating higher values and red indicating lower values.
    """)
    
    # Create tabs for visualization and data
    with gr.Tabs() as tabs:
        with gr.TabItem("Visualization"):
            plot_output = gr.Plot(value=sunburst_chart)
        
        with gr.TabItem("Data"):
            # Filter the dataframe to show only the relevant columns
            display_df = gapminder_data[['continent', 'country', 'pop', 'lifeExp', 'iso_alpha']].copy()
            # Format the population column to be more readable
            display_df['pop'] = display_df['pop'].apply(lambda x: f"{int(x):,}")
            data_display = gr.DataFrame(value=display_df)
    
    gr.Markdown("""
    ### About this Visualization
    
    **Dataset**: Gapminder (2007)
    
    **Chart Structure**:
    - **Inner Ring**: Continents
    - **Outer Ring**: Countries
    - **Segment Size**: Population
    - **Color**: Life Expectancy (blue = higher, red = lower)
    
    **Interaction Tips**:
    - Hover over segments to see detailed information
    - Click on a continent to zoom in on its countries
    - Click in the center to zoom back out
    
    The data tab shows the raw data used to create this visualization, including:
    - Continent
    - Country
    - Population
    - Life Expectancy
    - ISO Country Code
    """)

# Launch the app
if __name__ == "__main__":
    demo.launch(share=True)
    