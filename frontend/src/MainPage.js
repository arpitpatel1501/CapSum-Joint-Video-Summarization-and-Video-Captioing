import React from 'react';
import {Grid} from '@material-ui/core';
import VideoBrowser from './VideoBrowser';
import PrimaryAppBar from './AppBar';

function MainPage(props){
	return(
		<div>
			<Grid container >
				<Grid item xs={12} >
					<PrimaryAppBar user={props.user} />
				</Grid>
				<Grid item xs={12}>
					<VideoBrowser user={props.user} />
				</Grid>
			</Grid>
		</div>
	)

}

export default MainPage;