import React,{useEffect,useState} from 'react';
import {Grid,Paper,Button} from '@material-ui/core';

import VidCard from './Card'
import Player from './Player'

function VideoBrowser(props){
	//video{name,captions,url}
	const [title,setTitle]=useState(null)
	const [url,setUrl]=useState(null)
	const [captions,setCaptions]=useState(null)
	const [currindex,setCurrindex]=useState(0)

	const [vids,setVids]=useState([{title:null,thumbnail:[null],urls:[null],captions:[null]}])
	const [browser,setBrowser]=useState('')
	const [player,setPlayer]=useState('none')
	function setset(){setVids([
		{
			title:'songs1',
			thumbnail:["https://upload.wikimedia.org/wikipedia/commons/7/7c/Aspect_ratio_16_9_example.jpg","https://upload.wikimedia.org/wikipedia/commons/7/7c/Aspect_ratio_16_9_example.jpg","https://upload.wikimedia.org/wikipedia/commons/7/7c/Aspect_ratio_16_9_example.jpg"],
			urls:['https://www.youtube.com/watch?v=nY1g7hF7CyE','https://www.youtube.com/watch?v=hOC-lSVlF9s','https://www.youtube.com/watch?v=jwPmj0P8-H4'],
			captions:['a song is playing','something happening','just another video']
		},
		{
			title:'vids2',
			thumbnail:["https://upload.wikimedia.org/wikipedia/commons/7/7c/Aspect_ratio_16_9_example.jpg","https://upload.wikimedia.org/wikipedia/commons/7/7c/Aspect_ratio_16_9_example.jpg"],
			urls:['https://www.youtube.com/watch?v=cxvUiE_Rif4','https://www.youtube.com/watch?v=Wh8DT09QCHI'],
			captions:['some anime video','another song maybe']
		},
		{
			title:'another one here asdlknad',
			thumbnail:["https://upload.wikimedia.org/wikipedia/commons/7/7c/Aspect_ratio_16_9_example.jpg","https://upload.wikimedia.org/wikipedia/commons/7/7c/Aspect_ratio_16_9_example.jpg","https://upload.wikimedia.org/wikipedia/commons/7/7c/Aspect_ratio_16_9_example.jpg","https://upload.wikimedia.org/wikipedia/commons/7/7c/Aspect_ratio_16_9_example.jpg"],
			urls:['https://www.youtube.com/watch?v=jaazARZ0ylQ','https://www.youtube.com/watch?v=Pzh98abhAio','https://www.youtube.com/watch?v=t3O6vA0UL3k','https://www.youtube.com/watch?v=B0cggxlWpqw'],
			captions:['ayyymd','something happening again','just asd another video','just asd another asdasczc']
		},
	])}
	useEffect(() => {
		// fetch('http://127.0.0.1:5000/getvid',{
		fetch('http://34.68.228.193:8080/getvid',{
			method:'POST',
			headers:{'Content-Type':'application/json','email':props.user.email,},
			//body:JSON.stringify({user:props.user})
		})
		.then(response=>response.json())
		.then(data=>{
			//console.log(data)
			setVids(data.resp)
		})
		
		//setset()
		
	},[]);

	const openPlayer=(index)=>{
		console.log('opened!')
		//console.log(index)
		setCurrindex(index)
		setBrowser('none')
		setPlayer('')
	}
	const closePlayer=()=>{
		console.log('closed!')
		setBrowser('')
		setPlayer('none')
	}

	return(
		<div>
			{
				//BROWSER....
			}
			<Grid 
			container 
			spacing={3} 
			//direction="column" 
			alignItems="center" 
			justify="center" 
			style={{ width:'100vw',padding:'30px',paddingTop:'50px',display:browser}}
		  	>
      			<Paper style={{}} elevation={10} style={{padding:'0px',backgroundColor:'transparent'}}>
					<Grid container spacing={3}>
						{
							vids.map((vid,index)=>(
								<Grid item xs={3}>
									<VidCard onLog={()=>openPlayer(index)}
										title={vid.title} 
										image={vid.thumbnail[0]}
									/>
								</Grid>
							))
						}
					</Grid>
				</Paper>
			</Grid>

			{
				//PLAYER....
			}

			<Grid 
			container 
			spacing={3} 
			//direction="column" 
			alignItems="center" 
			//justify="center" 
			
			style={{marginLeft:'7vw', width:'100vw',padding:'30px',paddingTop:'50px',display:player}}
		  	>
			{player!=='none' ? <Player closePlayer={closePlayer} vid={vids[currindex]}  /> : null}		  
				
			
			  </Grid>
		</div>
	)

}

export default VideoBrowser;
