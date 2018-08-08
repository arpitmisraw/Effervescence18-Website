import React, { Component } from "react";
import {
  Grid,
  Row,
  Col,
  FormGroup,
  ControlLabel,
  FormControl
} from "react-bootstrap";

import { Card } from "components/Card/Card.jsx";
import { FormInputs } from "components/FormInputs/FormInputs.jsx";
import { UserCard } from "components/UserCard/UserCard.jsx";
import Button from "components/CustomButton/CustomButton.jsx";

import avatar from "assets/img/faces/face-3.jpg";
const URL = 'http://localhost:8000/api/regular_user/';
const token = localStorage.getItem('token');
class UserProfile extends Component {
  constructor(props){
  super(props);

  this.state = {
    user:'',


  }
}

  componentDidMount(){
  fetch(URL,
  { method:'GET',
  headers:{

           'Authorization': `Token ${token}`,
           'Access-Control-Allow-Origin': '*',
       },

  })

  .then(response =>
    {this.setState({user:response});
    console.log(this.state.user);
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
          <Row>

            <Col md={4}>
              <UserCard
                bgImage="https://ununsplash.imgix.net/photo-1431578500526-4d9613015464?fit=crop&fm=jpg&h=300&q=75&w=400"
                avatar={avatar}
                name="Mike Andrew"
                userName="michael24"
                description={
                  <span>
                    "Lamborghini Mercy
                    <br />
                    Your chick she so thirsty
                    <br />
                    I'm in that two seat Lambo"
                  </span>
                }
                socials={
                  <div>
                    <Button simple>
                      <i className="fa fa-facebook-square" />
                    </Button>
                    <Button simple>
                      <i className="fa fa-twitter" />
                    </Button>
                    <Button simple>
                      <i className="fa fa-google-plus-square" />
                    </Button>
                  </div>
                }
              />
            </Col>
          </Row>
        </Grid>>
      </div>
    );
  }
}

export default UserProfile;
