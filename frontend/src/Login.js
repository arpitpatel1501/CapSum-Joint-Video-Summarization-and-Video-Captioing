import React,{useEffect, useState} from 'react';
import {Button,Grid,Typography} from '@material-ui/core/';

function Login(props){
	let gButton=''
	let auth2=''
	
	useEffect(() => {
		googleSDK()
	});
	
    const googleSDK=()=>{
		window['googleSDKLoaded'] = () => {
			window['gapi'].load('auth2', () => {
				auth2 = window['gapi'].auth2.init({
					client_id: '21903730875-hql4p4h91bni869f4gevmutn5bta7v1t.apps.googleusercontent.com',  //ext
					//client_id: '413833473817-2mvctgjlcfp6015mqh8df3p3bd60757d.apps.googleusercontent.com', //au_internal
					cookiepolicy: 'single_host_origin',
					scope: 'profile email',
					prompt: 'select_account'
              });
              prepareLoginButton();
            });
		}
		(function(d, s, id){
			var js, fjs = d.getElementsByTagName(s)[0];
            if (d.getElementById(id)) {return;}
            js = d.createElement(s); js.id = id;
            js.src = "https://apis.google.com/js/platform.js?onload=googleSDKLoaded";
            fjs.parentNode.insertBefore(js, fjs);
		}(document, 'script', 'google-jssdk'));
    }
	
    const prepareLoginButton = () => {
		auth2.attachClickHandler(gButton, {},
            (googleUser) => {
				let profile = googleUser.getBasicProfile();
				//YOUR CODE HERE
				//console.log(profile);
				props.onLogin(profile.getEmail(),profile.getGivenName(),profile.getFamilyName(),profile.getImageUrl())
            }, (error) => {
			});
		}
	return(
		<div>
			<Grid container alignItems="center" 
			justify="center" 
			style={{marginTop:'70px'}}
			>
				  <Typography variant="h3" noWrap>
						CapSum
					</Typography>
			</Grid>
			<Grid 
			container 
			spacing={3} 
			direction="column" 
			alignItems="center" 
			justify="center" 
			style={{ minHeight: '70vh',maxWidth:'100%'}}
		  >
			  	
				<Grid item xs={12} >
					<Button variant="contained" color="primary" ref={input => {gButton = input}}>
					Login with Google</Button>
				</Grid>
			</Grid>
		</div>
	)
}

export default Login;