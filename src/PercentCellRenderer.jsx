import React from 'react';

// cell renderer for the proficiency column. this is a very basic cell renderer,
// it is arguable that we should not of used React and just returned a string of
// html as a normal ag-Grid cellRenderer.
export default class PercentCellRenderer extends React.Component {

    render() {
        let backgroundColor;
        backgroundColor = ['#ffffcc',
                           '#d9f0a3',
                           '#addd8e',
                           '#78c679',
                           '#41ab5d',][Math.max(0, Math.floor(this.props.value / 20 - 0.001))]
        return (
            <div className="div-percent-bar" style={{width: this.props.value + '%', backgroundColor: backgroundColor}}>
                <div className="div-percent-value">{this.props.value}%</div>
            </div>
        );
    }
}
