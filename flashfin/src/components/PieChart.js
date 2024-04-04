import React, { useEffect } from 'react';
import Plot from 'react-plotly.js';

function PieChart() {
    useEffect(() => {
        // Ensure Plotly.js is loaded before rendering the chart
        import('plotly.js-dist').then(Plotly => {
            // Data for the pie chart
            const data = [{
                values: [20, 30, 50],
                labels: ['Bills', 'Food', 'Misc.'],
                type: 'pie'
            }];

            // Layout for the pie chart
            const layout = {
                title: 'Monthly Breakdown',
                height: 400,
                width: 350
            };

            // Render the pie chart
            Plotly.newPlot('pie-chart', data, layout);
        });
    }, []); // This effect runs only once after the component mounts

    return (
        <div id="pie-chart">
            {/* This div will be replaced by the pie chart */}
        </div>
    );
}

export default PieChart;