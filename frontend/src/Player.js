import React,{useEffect, useState} from 'react';
import {Grid,Paper,Button,Typography} from '@material-ui/core';
import ReactPlayer from 'react-player';


export default function Player(props){

	const [current,setCurrent]=useState(props.vid.urls[0])
	const [caption,setCaption]=useState(props.vid.captions[0])
	
	return(

		<Paper style={{}} elevation={10} 
		alignItems="center" 
		justify="center" 
		style={{
			backgroundColor:'transparent'
		}}>
		
		
		<Grid 
			container 
			spacing={3} 
			className='textToChange' 
			//direction="column" 
			//alignItems="center" 
			//justify="center" 
			style={{ 
				//width:'100vw',
				padding:'30px',
				paddingTop:'0px',
		}} >
			<Grid item xs={7}>
				<Grid container>
					<Grid item xs={1}>
						<Button variant="contained" color="primary" onClick={props.closePlayer} >Back</Button>
					</Grid>
					<Grid item xs={11} style={{paddingLeft:'15px',marginTop:'-5px'}}>
						<Typography variant="h4" component="h2" >
							{props.vid.title}
						</Typography>
					</Grid>
					<Grid item xs={12} style={{paddingTop:'15px'}}>
						<ReactPlayer 
							url={current}
							width={854}
							height={480}
							controls={true}
							playing={true}
						/>
					</Grid>
					<Grid item xs={12} style={{paddingTop:'15px'}}>
						<Typography variant="h5" component="h5" >
						{caption}
						</Typography>
					</Grid>
				</Grid>
			</Grid>
			<Grid item xs={5}>
				<Grid container style={{marginTop:'50px'}}>
					<Grid item xs={12}>
						{props.vid.thumbnail.map((thumbnail,index)=>(
							<div onClick={()=>{setCurrent(props.vid.urls[index]);setCaption(props.vid.captions[index])}}>
								<Grid container spacing={3}>
									<Grid item xs={5}>
										<img src={thumbnail} style={{width:'250px'}} />
									</Grid>
									<Grid item xs={7}>
										<Typography variant="h8" component="h5" >
											{props.vid.captions[index]}
										</Typography>
									</Grid>
								</Grid>
							</div>
						))}
					</Grid>
				</Grid>
			</Grid>
		</Grid>
		</Paper>
	)
	
}
