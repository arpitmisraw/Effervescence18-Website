import React, { Component } from 'react';
import ImagesUploader from 'react-images-uploader';
import 'react-images-uploader/styles.css';
import 'react-images-uploader/font.css';
import axios from 'axios';

export default class MyUploader extends Component {
  constructor(props){
  super(props);

  this.state = {
    selectedFile:null,
    id:this.props.id,


  }
  console.log(this.state);
}
  fileChangedHandler = (event) => {

  this.setState({selectedFile: event.target.files[0]})
}
uploadHandler = () => {
  const token = localStorage.getItem('token');
  console.log(this.state);
  const formData = new FormData()
  formData.append('file', this.state.selectedFile);
  formData.append('id', this.state.id);
  
  console.log(formData);
  var headers = {
           'Content-Type': 'multipart/form-data',
           'Authorization': `Token ${token}`,
           'Access-Control-Allow-Origin': '*',
       }

  axios.post('http://localhost:8000/api/file_upload/', formData,{headers:headers})
  .then((response) => {
            console.log(response);
           })
           .catch((error) => {
              console.log(error);
           })

}
	render() {
		return (
      <div>
      <input type="file" onChange={this.fileChangedHandler} />
<button onClick={this.uploadHandler}>Upload!</button>

</div>
		);
	}
}
