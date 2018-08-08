import React, { Component } from "react";
import ChartistGraph from "react-chartist";
import { Grid, Row, Col } from "react-bootstrap";

import { Card } from "components/Card/Card.jsx";
import { StatsCard } from "components/StatsCard/StatsCard.jsx";
import { Tasks } from "components/Tasks/Tasks.jsx";
import  EventList from './Events.jsx';
import {
  dataPie,
  legendPie,
  dataSales,
  optionsSales,
  responsiveSales,
  legendSales,
  dataBar,
  optionsBar,
  responsiveBar,
  legendBar
} from "variables/Variables.jsx";

const URL = 'http://localhost:8000/api/events/';
class Dashboard extends Component {
  constructor(props){
  super(props);

  this.state = {
    events:'',


  }
}

  componentDidMount(){
  fetch(URL,
  { method:'GET',
    headers:{"Content-Type": "application/json",
      "Access-Control-Allow-Origin": "*",
      "Access-Control-Allow-Credentials":true,

            }

  })
  .then(response => response.json())
  .then(json =>
    {this.setState({events:json});
    console.log(this.state.events);
    })
.catch(function (error)
  {
    console.log(error);
  });
}
  render() {
    return (
      <div className="content">
        <Grid fluid>


          <EventList event={this.state.events}></EventList>
        </Grid>
      </div>
    );
  }
}

export default Dashboard;
