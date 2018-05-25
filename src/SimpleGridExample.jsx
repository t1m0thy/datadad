import React, {Component} from "react";
import {AgGridColumn, AgGridReact} from "ag-grid-react";
import districts from "../districts.json"
import PercentCellRenderer from "./PercentCellRenderer"

export default class extends Component {
    constructor(props) {
        super(props);

        this.state = {
            gridOptions: this.createGridOptions(),
            rowData: this.createRowData()
        }
    }

    onGridReady(params) {
        this.gridApi = params.api;
        this.columnApi = params.columnApi;
        //this.gridApi.sizeColumnsToFit();
    }


    createGridOptions() {
        return {defaultColDef: {width: 50, filter: 'number'},
                columnDefs: [
                   {headerName:'Name', field:'Name', width: 200},
                   {headerName:"Demographics",
                    children: [
                       {headerName:'Total Population', field:'Total', headerTooltip:'TotalPopulation'},
                    
                       {headerName:'AfricanAmerican', field:'AfricanAmerican', headerTooltip:'AfricanAmerican', cellRendererFramework: PercentCellRenderer},
                       {headerName:'Asian', field:'Asian', headerTooltip:'Asian', cellRendererFramework: PercentCellRenderer},
                       {headerName:'White', field:'White', headerTooltip:'White', cellRendererFramework: PercentCellRenderer},
                       {headerName:'Hispanic', field:'Hispanic', headerTooltip:'Hispanic', cellRendererFramework: PercentCellRenderer},
                       {headerName:'MultiRace,NonHispanic', field:'MultiRace,NonHispanic', headerTooltip:'MultiRace,,NonHispanic', cellRendererFramework: PercentCellRenderer},
                    ]},
                   {headerName:"MCAS",
                    children: [
                       {headerName:'Advanced %', field:'APercent', headerTooltip:'APercent', cellRendererFramework: PercentCellRenderer},
                       {headerName:'Proficient %', field:'PPercent', headerTooltip:'PPercent', cellRendererFramework: PercentCellRenderer},
                       {headerName:'Needs Improvment %', field:'NIPercent', headerTooltip:'NIPercent', cellRendererFramework: PercentCellRenderer},
                       {headerName:'Warn/Fail %', field:'WFPercent', headerTooltip:'WFPercent', cellRendererFramework: PercentCellRenderer},
                    ]},
                    {headerName:"AP",
                    children: [
                       {headerName:'1 Scores', field:'Score=1', headerTooltip:'AP Score=1'},
                       {headerName:'2 Scores', field:'Score=2', headerTooltip:'AP Score=2'},
                       {headerName:'3 Scores', field:'Score=3', headerTooltip:'AP Score=3'},
                       {headerName:'4 Scores', field:'Score=4', headerTooltip:'AP Score=4'},
                       {headerName:'5 Scores', field:'Score=5', headerTooltip:'AP Score=5'},
                    ]},

                   {headerName:"HigherEd",
                    children: [
                       {headerName:'AttendingCollUniv %', field:'AttendingCollUnivPercent', headerTooltip:'AttendingCollUnivPercent', cellRendererFramework: PercentCellRenderer},
                       {headerName:'AttendingCollUnivNum', field:'AttendingCollUnivNum', headerTooltip:'AttendingCollUnivNum'},
                    ]},

                   {headerName:'FirstLanguageNotEnglishPercent', field:'FirstLanguageNotEnglishPercent', headerTooltip: 'FirstLanguageNotEnglishPercent', cellRendererFramework: PercentCellRenderer},
                   {headerName:'EnglishLanguageLearnerPercent', field:'EnglishLanguageLearnerPercent', headerTooltip: 'EnglishLanguageLearnerPercent', cellRendererFramework: PercentCellRenderer},
                   {headerName:'StudentsWithDisabilitiesPercent', field:'StudentsWithDisabilitiesPercent', headerTooltip: 'StudentsWithDisabilitiesPercent', cellRendererFramework: PercentCellRenderer},
                   {headerName:'HighNeedsPercent', field:'HighNeedsPercent', headerTooltip: 'HighNeedsPercent', cellRendererFramework: PercentCellRenderer},
                   {headerName:'EconomicallyDisadvantagedPercent', field:'EconomicallyDisadvantagedPercent', headerTooltip: 'EconomicallyDisadvantagedPercent', cellRendererFramework: PercentCellRenderer},
                   {headerName:'AverageSalary', field:'AverageSalary', headerTooltip: 'AverageSalary'},
                    
                ]
            
            };
    }

    createRowData() {
        return districts;
    }

    render() {
        let containerStyle = {
            height: 500,
        };

        console.log(this.state.rowData)

        return (
            <div style={containerStyle} className="ag-fresh">
                <h1>District Data</h1>
                <AgGridReact
                    // properties
                    gridOptions={this.state.gridOptions}
                    rowData={this.state.rowData}
                    // events
                    onGridReady={this.onGridReady}
                    //config
                    enableColResize
                    enableSorting
                    enableFilter
                    floatingFilter
                    multiSelect
                    groupHeaders>


                </AgGridReact>
            </div>
        )
    }
};
