import React, { useState } from 'react';
import {Button,Grid,Typography} from '@material-ui/core/';

function Upload(props){
	//console.log(props)
	const [file,setFile]=useState(null)
	const [name,setName]=useState('')
	const [captions,setCaptions]=useState(null)
	let upload=''
	
	const SendFile=()=>{
	  const formData = new FormData()
	  formData.append('file', file, file.name)
	  //console.log('holla')
	  fetch('http://34.68.228.193:8080/upload', {
		  method: 'POST',
		  headers:{
			  'email':props.user.email,
		  },
		  body: formData,
		})
	  .then((res) => res.json())
	  .then((data) =>  {
		//console.log(data)
		setCaptions(data.captions)
	  })
	  .catch((err)=>console.log(err))
	}
	const onChangeFile=(event)=>{
	  event.stopPropagation();
	  event.preventDefault();
	  var file = event.target.files[0];
	  //console.log(file);
	  setFile(file);
	  if(file!=null){
		  setName(file.name);
		}
		else{
			setName('');
		}
	}
	const uploadClick = e => {
		e.preventDefault();
		upload.click();
		return false;
	  };
	return(
		<div 
		style={{paddingTop:'5px',paddingRight:'15vw'}}
		>
		  	{//direction="column" 
			//alignItems="center" 
			//justify="center" 
			//style={{ minHeight: '40vh',maxWidth:'100%'}}
			}
			  
				<input id="myInput"
					type="file"
					ref={input => {upload = input}}
					style={{display: 'none'}}
					onChange={onChangeFile.bind(this)}
				/>
			  <Grid container style={{width:'25vw'}} >
				<Grid item xs={6} style={{paddingLeft:'20px'}}>
					<Typography variant="h6">
						{name}
					</Typography>
				</Grid>
			  	<Grid item xs={6} >
					<Grid container justify="center" spacing={3} >
						<Grid item xs={6} >
							<Button variant="outlined" color="inherit" onClick={uploadClick}>
								Browse
							</Button>
						</Grid>
						<Grid item xs={6} >
							<Button variant="contained" color="secondary" onClick={()=>{SendFile()}}>
								Upload
							</Button>
						</Grid>
					</Grid>
			  	</Grid>
			  </Grid>
		</div>
	)
	
  }
  export default Upload;
  